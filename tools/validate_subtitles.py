#!/usr/bin/env python3
"""Open standalone validator for KaraokeSync subtitle/karaoke outputs (.lrc, .srt, .ass).

Checks encoding, timestamp syntax, monotonic ordering, overlaps, overly short cues,
and ASS karaoke sections/tags using only the Python standard library.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

__all__ = [
    "ValidationReport",
    "validate_ass",
    "validate_file",
    "validate_lrc",
    "validate_srt",
    "main",
]

_LRC_TIME_RE = re.compile(r"\[(\d{1,3}):(\d{2})(?:[.:](\d{1,3}))?\]")
_SRT_RANGE_RE = re.compile(
    r"^\s*(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*$"
)
_ASS_TIME_RE = re.compile(r"^\s*(\d{1,2}):(\d{2}):(\d{2})\.(\d{2})\s*$")
_ASS_KARAOKE_RE = re.compile(r"\{\\k[fo]?\d+")


@dataclass
class ValidationReport:
    """Result of validating a single subtitle or lyric file."""

    path: str
    kind: str
    cues: int = 0
    karaoke_tagged_cues: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _lrc_to_ms(minutes: str, seconds: str, frac: str | None) -> int:
    ms = int(minutes) * 60_000 + int(seconds) * 1000
    if frac:
        ms += round(int(frac) * 1000 / (10 ** len(frac)))
    return ms


def _hmsms_to_ms(h: str, m: str, s: str, ms: str) -> int:
    return ((int(h) * 60 + int(m)) * 60 + int(s)) * 1000 + int(ms)


def _ass_to_ms(text: str) -> int | None:
    match = _ASS_TIME_RE.match(text)
    if not match:
        return None
    h, m, s, cs = match.groups()
    return ((int(h) * 60 + int(m)) * 60 + int(s)) * 1000 + int(cs) * 10


def validate_lrc(text: str, path: str = "<memory>.lrc") -> ValidationReport:
    """Validate an LRC (or Enhanced LRC) file."""
    report = ValidationReport(path=path, kind="lrc")
    prev_ms = -1
    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        if not stripped:
            continue
        stamps = list(_LRC_TIME_RE.finditer(stripped))
        if not stamps:
            if not stripped.startswith("["):
                report.warnings.append(f"Line {line_no}: plain text without LRC timestamp")
            continue
        for match in stamps:
            ts_ms = _lrc_to_ms(*match.groups())
            if ts_ms < prev_ms:
                report.errors.append(
                    f"Line {line_no}: timestamp moves backward ({ts_ms} ms < {prev_ms} ms)"
                )
            prev_ms = ts_ms
        lyric = _LRC_TIME_RE.sub("", stripped).strip()
        if lyric:
            report.cues += 1
            if re.search(r"<\d{1,3}:\d{2}(?:[.:]\d{1,3})?>", lyric):
                report.karaoke_tagged_cues += 1
    if report.cues == 0 and prev_ms < 0:
        report.errors.append("No timed LRC cues found")
    return report


def validate_srt(text: str, path: str = "<memory>.srt") -> ValidationReport:
    """Validate an SRT subtitle file."""
    report = ValidationReport(path=path, kind="srt")
    normalized = text.replace("\r\n", "\n").strip()
    if not normalized:
        report.errors.append("SRT file is empty")
        return report

    prev_end = 0
    blocks = re.split(r"\n\s*\n", normalized)
    for idx, block in enumerate(blocks, start=1):
        lines = [line for line in block.split("\n") if line.strip() != ""]
        if len(lines) < 2:
            report.errors.append(f"Block {idx}: incomplete SRT cue")
            continue
        ts_idx = 1 if lines[0].strip().isdigit() else 0
        match = _SRT_RANGE_RE.match(lines[ts_idx])
        if not match:
            report.errors.append(f"Block {idx}: invalid SRT timestamp line {lines[ts_idx]!r}")
            continue
        g = match.groups()
        start_ms = _hmsms_to_ms(g[0], g[1], g[2], g[3])
        end_ms = _hmsms_to_ms(g[4], g[5], g[6], g[7])
        if end_ms <= start_ms:
            report.errors.append(
                f"Block {idx}: end time ({end_ms} ms) is not after start ({start_ms} ms)"
            )
        elif end_ms - start_ms < 150:
            report.warnings.append(
                f"Block {idx}: short cue duration ({end_ms - start_ms} ms < 150 ms)"
            )
        if start_ms < prev_end:
            report.warnings.append(
                f"Block {idx}: overlaps previous cue ({start_ms} ms < {prev_end} ms)"
            )
        body = " ".join(lines[ts_idx + 1 :]).strip()
        if not body:
            report.warnings.append(f"Block {idx}: empty subtitle text")
        report.cues += 1
        prev_end = max(prev_end, end_ms)

    if report.cues == 0:
        report.errors.append("No valid SRT cues parsed")
    return report


def validate_ass(text: str, path: str = "<memory>.ass") -> ValidationReport:
    """Validate a SubStation Alpha v4+ (.ass) karaoke file."""
    report = ValidationReport(path=path, kind="ass")
    sections = set(re.findall(r"(?m)^\[([^\]]+)\]\s*$", text))
    for required in ("Script Info", "V4+ Styles", "Events"):
        if required not in sections:
            report.errors.append(f"Missing required section [{required}]")

    in_events = False
    for line_no, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            in_events = stripped.lower() == "[events]"
            continue
        if not in_events or not stripped.startswith("Dialogue:"):
            continue
        parts = stripped.split(",", 9)
        if len(parts) < 10:
            report.errors.append(f"Line {line_no}: malformed ASS Dialogue event")
            continue
        start_ms = _ass_to_ms(parts[1])
        end_ms = _ass_to_ms(parts[2])
        if start_ms is None or end_ms is None:
            report.errors.append(f"Line {line_no}: invalid ASS timestamp(s)")
            continue
        if end_ms <= start_ms:
            report.errors.append(
                f"Line {line_no}: end time ({end_ms} ms) <= start time ({start_ms} ms)"
            )
        payload = parts[9].strip()
        if _ASS_KARAOKE_RE.search(payload):
            report.karaoke_tagged_cues += 1
        report.cues += 1

    if report.cues == 0:
        report.errors.append("No Dialogue events found in [Events]")
    return report


def validate_file(path: str | Path) -> ValidationReport:
    """Read and validate an ``.lrc``, ``.srt``, or ``.ass`` file."""
    file_path = Path(path)
    if not file_path.is_file():
        rep = ValidationReport(path=str(file_path), kind="unknown")
        rep.errors.append(f"File not found: {file_path}")
        return rep

    raw = file_path.read_bytes()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        rep = ValidationReport(path=str(file_path), kind=file_path.suffix.lstrip("."))
        rep.errors.append(f"File is not valid UTF-8: {exc}")
        return rep

    suffix = file_path.suffix.lower()
    if suffix == ".lrc":
        return validate_lrc(text, path=str(file_path))
    if suffix == ".srt":
        return validate_srt(text, path=str(file_path))
    if suffix in {".ass", ".ssa"}:
        return validate_ass(text, path=str(file_path))

    rep = ValidationReport(path=str(file_path), kind=suffix.lstrip(".") or "unknown")
    rep.errors.append(f"Unsupported subtitle extension: {suffix!r}")
    return rep


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate KaraokeSync .lrc, .srt, and .ass subtitle files.",
    )
    parser.add_argument("files", nargs="+", help="Subtitle files to validate")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings (overlaps, short cues) as failures",
    )
    args = parser.parse_args(argv)

    failed = False
    for raw_path in args.files:
        rep = validate_file(raw_path)
        has_issue = not rep.ok or (args.strict and bool(rep.warnings))
        status = "FAIL" if has_issue else "OK"
        print(
            f"[{status}] {rep.path} ({rep.kind}): "
            f"{rep.cues} cue(s), {rep.karaoke_tagged_cues} karaoke-tagged"
        )
        for err in rep.errors:
            print(f"  ERROR: {err}")
        for warn in rep.warnings:
            print(f"  WARN : {warn}")
        if has_issue:
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
