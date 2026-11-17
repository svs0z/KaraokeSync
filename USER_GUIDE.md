# KaraokeSync — Complete User Guide

🌐 [English](README.md) | [Español](README.es.md) | **User Guide (EN)** | [Guía de uso (ES)](GUIA_DE_USO.md)

**For anyone, no technical knowledge required.** Everything you need to do is
here, step by step, with the exact text to type or click.

KaraokeSync listens to a song and tells you:

1. **When** someone sings and when they do not (vocals, instrumental, silence,
   noise), with timestamps such as `00:01:23.450`, accurate to the millisecond.
2. **What** is being sung, if you provide the lyrics: it generates an `.lrc`
   (karaoke), an `.srt` (subtitles) and a `.json`.
3. It also writes a **`.txt` report** that opens perfectly in Notepad.

---

## Contents

1. [Before you start: what you need](#1-before-you-start-what-you-need)
2. [Installing on Windows](#2-installing-on-windows)
3. [Checking that it works](#3-checking-that-it-works)
4. [Using KaraokeSync Studio](#4-using-karaokesync-studio)
5. [Adding songs](#5-adding-songs)
6. [Lyrics: the part that matters](#6-lyrics-the-part-that-matters)
7. [Where to find an already synced `.lrc`](#7-where-to-find-an-already-synced-lrc)
8. [Typical lyric mistakes](#8-typical-lyric-mistakes)
9. [Is it well synchronized? How to check](#9-is-it-well-synchronized-how-to-check)
10. [Word-by-word subtitles for CapCut, DaVinci and Premiere](#10-word-by-word-subtitles-for-capcut-davinci-and-premiere)
11. [Lyrics for music players](#11-lyrics-for-music-players)
12. [The visual editor and keyboard shortcuts](#12-the-visual-editor-and-keyboard-shortcuts)
13. [Understanding report warnings](#13-understanding-report-warnings)
14. [What to do with the generated files](#14-what-to-do-with-the-generated-files)
15. [Problems and solutions](#15-problems-and-solutions)
16. [Frequently asked questions](#16-frequently-asked-questions)
17. [Quick command reference](#17-quick-command-reference)

---

## 1. Before you start: what you need

| | |
|---|---|
| **System** | Windows 10 or 11 (also works on Linux and macOS, see `README.md`) |
| **Disk space** | About 4 GB with everything installed (PyTorch and Demucs are large) |
| **Internet** | Only the first time, to download models. Afterwards it works offline |
| **Graphics card** | Not required. CPU works; an NVIDIA GPU is much faster |
| **Knowledge** | None. Commands are copied and pasted |

**An important note about antivirus software.** Windows may block the
calculation libraries (numpy, torch) when **Smart App Control** is enabled, and
then you will see errors such as *“No module named 'numpy'”* or *“access
denied”* even though installation went well. If that happens:

> Start → **Windows Security** → *App & browser control* → *Smart App Control* →
> **Off**. Restart the computer and try again.

---

## 2. Installing on Windows

1. Download **`KaraokeSync-1.3.0-win64.zip`** from the *Releases* page.
2. Right-click the file → **Extract All…** and choose a folder
   (for example `C:\Users\<your user>\KaraokeSync`).
3. Open the folder and **double-click `KaraokeSync.exe`**.

No Python, ffmpeg or anything else is required: everything is inside the
package.

> The first time, Windows may warn that the file has no digital signature. This
> is normal: click **More info → Run anyway**.

### KaraokeSync Studio: the application window

Double-click `KaraokeSync.exe` and **KaraokeSync Studio** opens in its own
application window, with no address bar or browser tabs:

- choose the audio and lyrics, or search **LRCLIB** from the same window;
- process with Demucs, hybrid Silero VAD and lyric alignment;
- use the live karaoke stage with word-by-word highlighting;
- see the cyan VAD vocal band under the green lyric blocks in the timeline;
- choose **Word-by-word SRT (CapCut / Reels / TikTok)** and **Enhanced LRC**;
- drag audio or lyric files directly onto the window;
- fix timings, press **📋 Copy LRC** and save `.lrc`, `.srt` and `.json`.

Closing the window stops the application: no server or background process
remains.

## 3. Checking that it works

If something goes wrong, diagnostics tells you what. In the GUI, press the
**Diagnostics** button; from the console:

```powershell
KaraokeSync.exe --diagnostico
```

A healthy environment looks like this:

```text
  Python       : 3.12.10
  ffmpeg       : C:\...\ffmpeg.exe
  GUI          : available
  CUDA GPU     : no

  [ OK ] numpy       [ OK ] torch        [ OK ] silero_vad
  [ OK ] demucs      [ OK ] librosa      [ OK ] faster_whisper

  RESULT: this computer CAN run KaraokeSync.
```

If the last line says **CAN run KaraokeSync**, everything is ready.

---

## 4. Using KaraokeSync Studio

KaraokeSync Studio is the main interface. Double-click `KaraokeSync.exe`, or
`KaraokeSync.exe` when running from source. Everything happens on one
screen:

### 4.1 Song

Press the file button or simply **drag the audio file onto the window**. Studio
tries to recover the real Windows path from known folders (output folder,
previous audio folder, current folder, Downloads, Music, Desktop and one level
inside Downloads/Music). If it cannot find the file, it tells you and opens the
Windows picker.

Accepted audio: **MP3, FLAC, WAV, M4A, OGG, OGA, OPUS, AAC, WMA, AIFF, MP4,
WEBM**.

### 4.2 Lyrics

You can:

- press **📄 .lrc / .txt / .srt file** and choose a lyrics file;
- drag an `.lrc`, `.txt` or `.srt` onto the window or directly onto the lyrics
  text box — it loads immediately;
- search **LRCLIB** by metadata or by typing an artist/title;
- or paste the lyrics directly into the text box.

Lyrics are optional. Without them KaraokeSync still detects **when** someone
sings, but it cannot know **what** is being sung.

### 4.3 Synchronization

Choose:

- **Precision preset**: Fast, Balanced (recommended) or High.
- **Separate sources with Demucs**: recommended; separates vocals from the
  instrumental before analysis.
- **Save stems**: writes `vocals.wav` and `no_vocals.wav`.
- **Word-by-word SRT (CapCut / Reels / TikTok)**: one subtitle cue per word.
- **Enhanced LRC**: adds `<mm:ss.xx>` word tags to the `.lrc`.
- Which files to generate: report, LRC, SRT, JSON and HTML editor.

Press **⚡ Sync karaoke** and wait. You will see a progress bar, live logs and a
cancel button.

### 4.4 Live karaoke stage

The large stage shows the current line, the next line and an internal progress
bar. When word timings exist:

- the **current word is highlighted**;
- words already sung are marked;
- words still to come stay dimmed.

This makes timing errors obvious without reading numbers.

### 4.5 Interactive timeline

The timeline shows:

- **green blocks**: your lyric lines, from `start_ms` to `end_ms`;
- a **soft cyan band below the green blocks**: VAD-detected vocal segments;
- a position needle for the current playback time.

Use it to see where real singing happens. Click to seek, drag a green block to
move that line, and use the global ±50/±250 ms buttons for a uniform offset.

### 4.6 Timing editor

The editor lets you:

- edit the text of each line;
- edit `start_ms` and `end_ms` directly;
- move a line 100 ms earlier or later;
- mark the current playback instant;
- jump to a line;
- insert or delete lines;
- undo with `Ctrl+Z`;
- press **📋 Copy LRC** to copy the current LRC to the clipboard;
- save `.lrc`, `.srt` and `.json` directly to the output folder.

---

## 5. Adding songs

**Nothing is uploaded anywhere.** Everything stays on your computer.

1. Save the song in any folder (Desktop, Music, USB drive…).
2. In Studio, choose the audio or drag it onto the window.

Practical notes:

- **Quality matters.** A 128 kbps MP3 with background noise gives worse results
  than FLAC or a 320 kbps MP3. Lossless formats (FLAC, WAV) are best.
- **One song at a time** in Studio. For many songs, use batch mode from the CLI.
- **Videos also work** (`.mp4`, `.webm`): the audio is extracted.
- The **first song takes longer** and needs internet, because models are
  downloaded. Afterwards they are cached.
- To preload models before a trip:

```powershell
KaraokeSync.exe --descargar-modelos
```

---

## 6. Lyrics: the part that matters

### Is it mandatory? No, but it changes everything

| | Without lyrics | With lyrics |
|---|---|---|
| **When** someone sings | Yes, precisely | Yes, precisely |
| **What** is being sung | No | Yes |
| Files | `.txt` and `.json` report | Plus `.lrc` and `.srt` |

Without lyrics it is impossible to know what is being sung, and the program
**never invents it**: if it cannot align the lyrics, it says so clearly in the
report.

### Format 1: a `.txt` file (easiest)

This is what to use if you have nothing else. **One lyric line per row.**

**Step by step from a lyrics website:**

1. Open the song on musixmatch, letras.com, Genius… whatever you use.
2. Select **all** page text (`Ctrl+A`) and copy it (`Ctrl+C`).
3. Open **Notepad** and paste (`Ctrl+V`).
4. Save with **File → Save As**:
   - **Type:** *All files* (important!)
   - **Name:** `lyrics.txt`
   - **Encoding:** `UTF-8`
5. In KaraokeSync, choose that file under **Lyrics**.

> **The most common mistake:** if you leave *Type* as *Text Documents* and type
> `lyrics.txt`, Windows saves `lyrics.txt.txt` and you will not find it. Choose
> **All files** or type the name **in quotes**: `"lyrics.txt"`.

**Paste the website header without fear.** KaraokeSync is prepared for it:

| What appears after pasting | What it does |
|---|---|
| `Luna (feat. Lo Blondo)`, `Zoé`, `Letra de Luna`, `Ver más`, `© 2024 …`, links | Recognizes it as title, credits or interface and does **not** count it as lyrics |
| `Título:`, `Artista:`, `Composición:`, `Escritores:`, `Álbum:`… | Stores it as song data and uses it in the `.lrc` header |
| `[Verso 1]`, `[Chorus]`, `[Coro]` | Section tags |
| `(oh yeah)`, `(no, no, no)` | **Sung lyrics.** Parentheses are never a section |
| `Ana: my part` | Singer, in duets |
| `Dime: ¿por qué no vuelves?` | Full sung line (does not lose `Dime:`) |

**It always warns you.** If it discards a line because it thinks it is a header,
the report says so with the exact text:

```text
[WARNING] LET-004: Ignored 1 header/credit line(s) at the beginning of the
file: 'Zoé'. If one of them was lyrics, remove it from the .txt or remove the
header so it is preserved.
```

**Recommended template** (English lyrics in the same structure):

```text
Title: Song name
Artist: Who sings it

[Verse 1]
First line that is sung in one breath
Second line that is sung in one breath

[Chorus]
The whole chorus, line by line

[Verse 2]
And the song continues
```

**Three tips that improve the result:**

1. **One line = one sung phrase.** Do not paste a whole paragraph: if a line is
   very long, it is distributed badly. Do not split one sung phrase into two
   lines either.
2. **`Title:` is useful.** It appears in the `.lrc` header. Otherwise the audio
   filename is used.
3. **Mark sections with square brackets** (`[Chorus]`). They label segments and
   appear in the report.

### Format 2: an `.lrc` file (best result)

If you already have an `.lrc` (synced lyrics with `[00:12.34]` marks), use it:
**it is the best possible starting point.** The program uses those marks as
anchors and adjusts the rest to *your* audio, so the result is more reliable and
faster.

Enhanced LRC with word marks (`<00:12.34>`) is also supported.

### Format 3: an `.srt` (subtitles)

If you have karaoke video subtitles in `.srt`, they work too. Their timings are
used just like `.lrc` marks.

### Which format to choose

| Situation | Use |
|---|---|
| I have nothing | **`.txt`** pasted from a website (with the template above) |
| I found an `.lrc` for the song | **`.lrc`** — the best option |
| I have karaoke subtitles | **`.srt`** |

### How lyrics should look for the best result

This makes the biggest difference, and it is free. The golden rule is **one line
= one sung phrase**: the program fits *lines* against the audio, so if you split
a verse into subtitle fragments, it has to guess twice.

| Do this | Avoid this |
|---|---|
| One sung phrase per line | Cutting in the middle of a phrase |
| The **order** in which it is sung, with choruses **repeated** every time | Writing “(x2)” or listing the chorus only once |
| The lyrics of **that recording** (studio ≠ live ≠ remix) | Mixing versions or translations |
| Everything in **one** language | Alternating original lyrics and translation |
| A UTF-8 `.txt` (Notepad) | Photos, PDFs, formatted text |
| Copy and paste from letras.com, Musixmatch or Genius | Writing from memory |

**Pasting from lyrics websites works as-is.** Extra content is cleaned up: tags
such as `[Verse 1: …]`, `[Pre-Chorus: …]`, `[Letra de "…"]` and Genius's “You
might also like” block with three song pairs.

> **Important warning about versions.** The number-one reason lyrics do not fit
> is that they come from **another version**: studio, live, compilation or a
> translation. If the program warns that *“the lyrics do not match what is being
> sung”*, it is almost always this. Find the lyrics for the exact version you
> have.

---

## 7. Where to find an already synced `.lrc`

An `.lrc` is a text file with time marks before each line:

```text
[ti:Luna]
[ar:Zoé]
[00:15.20]I wait for you on the corner
[00:18.90]with the moon in my eyes
```

Players use these files to show synchronized lyrics, so they are available from
the same places:

1. **LRCLIB** — [lrclib.net](https://lrclib.net) is a **free and open** database
   of synced lyrics, no account required. Search for the song; if a synced
   version exists it shows `[mm:ss.xx]` marks. Copy it and save as `.txt` or
   `.lrc` with Notepad.
2. **MusicBee** (free Windows player) with the
   [mb_AutoLyrics](https://getmusicbee.com/addons/plugins/584/mb-autolyrics-multi-source-amp-synced-lyrics-plugin/)
   plugin — automatically finds and downloads synced lyrics and saves `.lrc`
   next to the song.
3. **Players with synchronized lyrics** (AIMP, foobar2000 with plugins, some
   Android players) often save downloaded lyrics as `.lrc` in the song folder.
4. **musixmatch, letras.com, Genius** — **do not** offer downloadable `.lrc`,
   only text. Use the `.txt` path from the previous section.

> **Website lyrics are copyrighted.** Use them for personal use. If you publish
> or share the result, use public-domain/free lyrics or ask for permission.

> **Remember:** KaraokeSync **generates** the `.lrc` for you. If you cannot find
> one, paste the lyrics into a `.txt` and the program will create the `.lrc`
> with the timings of *your* audio file, which is exactly what you want.

---

## 8. Typical lyric mistakes

| Symptom | Cause | Solution |
|---|---|---|
| *“No lyric line could be extracted”* | The file is empty or only has a header | Check that the lyrics are inside |
| The lyrics are one huge paragraph | It was pasted without line breaks | Put each phrase on its own line |
| *“The lyrics do not match what is being sung”* (low similarity) | Lyrics from another version, another language, or not this song | Find the exact version. If you are sure, lower the threshold: `--set alignment.min_similarity=0.30` |
| A line that was lyrics is missing | It was discarded as a header | The report names it (`LET-004`). Remove that line from the `.txt` or remove the header and rerun |
| A line keeps `Ana:` in front | The name appeared only once and was not treated as a singer | This is deliberate: losing text is worse. Write `Ana:` on all their lines or remove it |
| Accents look wrong | The `.txt` was not UTF-8 | Save it again with **UTF-8** encoding |
| The program cannot find the file | It was saved as `lyrics.txt.txt` | Enable *View → File name extensions* in Explorer and rename it |

---

## 9. Is it well synchronized? How to check

This is the important question, and it has three answers, from fastest to most
reliable.

### Step 1: read what the program says (5 seconds)

Open the report and look for these two lines:

```text
  Real alignment       : YES
  Lyrics verified      : YES (similarity 0.63)
```

- **`Real alignment: YES`** → timings come from fitting the lyrics against the
  audio. This is what you want.
- **`Real alignment: NO`** → lyrics were **spread** over vocal segments. It tells
  you *when* someone sings, but it is **not** word-by-word karaoke. The report
  explains it in the issues (`ALU-003`).
- **`similarity`** is how much your lyrics resemble what is recognized in the
  audio. Below 45 % alignment is rejected. Between 45 % and 60 %, check by ear.

### Step 2: ask for an audit

```powershell
KaraokeSync.exe --verificar "C:\Output\song.json"
```

This does the part that **can** be checked without listening, and writes
`song_auditoria.txt` for Notepad. It checks ten things: whether alignment was
real, times are ordered, lines overlap, any line lasts 20 ms or 30 s, every line
has voice underneath, every word falls inside its line, nothing exceeds the
audio duration, and whether there were issues. At the end it gives a
plain-language **verdict** and suggests five moments to listen to.

### Step 3: listen (the definitive test)

**The program does not hear**, so it cannot certify by itself that a mark is
correct. The final check is your ears, and it takes two minutes:

1. The audit suggests **five moments** spread across the song (first line, the
   middle, the last line and the start of some vocal segments), with exact
   minutes.
2. Open the audio in a player that shows lyrics:
   - **VLC** with the `.srt` (drag and drop → *Subtitle → Add subtitle file*).
   - **AIMP, MusicBee, foobar2000 or Poweramp** (mobile) with the `.lrc` next to
     the song, same filename.
3. Jump to those minutes and compare: if what sounds matches the text, it is
   synced. **If the text is more than half a second ahead or behind, you notice
   immediately.**

### Step 4: if something is off, fix it in the editor

No program is always right. The honest thing is not to promise perfection but to
give you the tool to fix it in two minutes.

Use **KaraokeSync Studio** or:

```powershell
KaraokeSync.exe -i song.flac -l lyrics.txt --language en --editor
```

This generates `song_editor.html` next to the song. Double-click it (no internet
or installation required). See [section 12](#12-the-visual-editor-and-keyboard-shortcuts).

---

## 10. Word-by-word subtitles for CapCut, DaVinci and Premiere

This is the workflow for social video and professional editors.

### CapCut / Reels / TikTok

1. In Studio's **Synchronization** card, enable
   **Word-by-word SRT (CapCut / Reels / TikTok)**.
2. Make sure **SRT** is among the files to generate.
3. Sync the song.
4. Import the generated `<name>.srt` into CapCut:
   **Text → Import subtitles** (or drag the `.srt` onto the timeline).
5. Choose a word-by-word caption style and adjust colours/fonts in CapCut.

Because each cue contains one word, the result behaves like a karaoke caption
track rather than a paragraph subtitle.

### DaVinci Resolve

1. Use the same **Word-by-word SRT** option.
2. In Resolve: **File → Import → Subtitle…** and choose the `.srt`.
3. Drag the subtitle track under the video and style it with the Text+ tools.

### Premiere Pro

1. Use the same **Word-by-word SRT** option.
2. In Premiere: **File → Import** and select the `.srt`, or use the Captions
   workspace to import it.
3. Apply a caption style; each word is an independent cue.

### Enhanced LRC for karaoke players

Enable **Enhanced LRC** if you want word tags:

```text
[00:12.34]<00:12.34>Hello <00:12.70>world
```

This is the format used by karaoke-capable LRC players. If you only need
line-by-line lyrics, leave it off and keep the standard `.lrc`.

> **Tip:** use the **📋 Copy LRC** button in the editor to paste the current LRC
> into another tool without saving a file first.

---

## 11. Lyrics for music players

KaraokeSync can prepare lyrics for software players and servers:

- **Spotify-style local lyrics / MusicBee / AIMP / foobar2000** — use the
  standard `.lrc`.
- **Navidrome / Plex / Jellyfin** — use the `.lrc` next to the audio file, with
  the same basename (`song.flac` + `song.lrc`).
- **Enhanced LRC** — use it only if your player supports `<mm:ss.xx>` word tags.
- **Mobile players** — copy `song.mp3` and `song.lrc` to the phone with the same
  filename; the player detects them automatically.

For video platforms that only accept subtitles, use the `.srt` instead.

---

## 12. The visual editor and keyboard shortcuts

The Studio editor is designed for quick fixes. It is also available as a
standalone HTML file generated with `--editor`.

| I want to… | How |
|---|---|
| Hear where a line falls | Click the line: it seeks there and highlights it |
| Move one line | `−0.1 s` / `+0.1 s` buttons, or drag its green block on the timeline |
| Mark the start “here” | Play and press `⏱` (or `T` in the standalone editor) |
| Move **all** lyrics | ±50 / ±250 ms buttons |
| Edit the text | Click the text field and type |
| Add a line | **＋** on the previous line |
| Delete a line | **×** on that line |
| See the lyrics like karaoke | The large stage at the top |
| Copy the LRC | **📋 Copy LRC** |
| Undo | `Ctrl+Z` |
| Play / pause | `Space` |
| Save | Save buttons for `.lrc`, `.srt`, `.json`, or the folder button |

**Keyboard shortcuts in Studio:**

| Shortcut | Action |
|---|---|
| `Space` | Play / pause |
| `Ctrl+Z` | Undo the last timing or text change (50 states) |
| `T` | Mark the current instant in the standalone editor |
| `Enter` | Confirm a numeric timing field |

**Timeline colours:**

- **Green blocks** = lyric lines.
- **Cyan band below** = VAD-detected vocal segments.
- **Needle** = current playback position.

If a green block sits outside the cyan band, that line is probably misplaced.

---

## 13. Understanding report warnings

The report ends with an **Issues** section. Codes are stable and grouped by
stage.

| Prefix | Stage | What it usually means |
|---|---|---|
| `LET-` | Lyrics | `LET-001` lyrics read, `LET-002` could not read the file, `LET-003` no lyrics supplied, `LET-004` a header/credit line was discarded (the exact text is shown) |
| `VAD-` | Voice detection | `VAD-001` fallback to energy, `VAD-002` detected voice ends much earlier than the music (possible lost singing at the end), `VAD-003` the aligned lyrics confirmed extra vocal segments and the timeline was extended with them |
| `ALU-` | Alignment | `ALU-003` supplied lyrics do not match what is recognized, `ALU-007` recognition cache reused, `ALU-009` three or more lines squeezed together (times are estimates), `ALU-011` final timing coherence warning. Others describe anchors, proportional distribution or verification |
| `SEP-` | Source separation | `SEP-001`/`SEP-004`/`SEP-005` Demucs warning or fallback, `SEP-002` separation reused from cache, `SEP-007` CPU optimization details |
| `PIP-001` | Pipeline | Long file analyzed in blocks |
| `OUT-001` | Export | Output file bytes do not match the expected Notepad-compatible encoding/newlines |
| `CAC-001` | Cache | Full result reused from cache |

Warnings are not failures. They tell you **where to look**. If a warning says
timings are estimates, check them by ear or fix them in the editor.

---

## 14. What to do with the generated files

| File | Purpose |
|---|---|
| `<name>_karaokesync.txt` | **The report.** Read it in Notepad |
| `<name>.lrc` | **Karaoke.** Copy it next to the song with the same name; the player shows synchronized lyrics (AIMP, foobar2000, MusicBee, Poweramp on Android, VLC…) |
| `<name>.srt` | **Subtitles.** Open it with the video in VLC (drag and drop → *Subtitle → Add subtitle file*). Upload it to YouTube or import it into CapCut/DaVinci/Premiere |
| Enhanced `.lrc` | Word-level `<mm:ss.xx>` tags for compatible karaoke players |
| `<name>.json` | The same data in machine-readable form |
| `<name>_editor.html` | Standalone timing editor |
| `vocals.wav`, `no_vocals.wav` | Only with **Save stems**. Isolated vocals and accompaniment, for singing over |

**For karaoke on your phone:** copy the `.lrc` next to the MP3 with the **same
name** (`song.mp3` + `song.lrc`) and the player detects it automatically.

---

## 15. Problems and solutions

### `No module named 'numpy'` (or `torch` / `soundfile`)

You are running the system Python instead of the program's environment. Always
use the launchers: double-click `KaraokeSync.exe` or `KaraokeSync.exe`, or
run `KaraokeSync.exe` in the console. If you call Python directly, it must be
`KaraokeSync.exe`.

If it still fails, it may be Windows **Smart App Control** (see section 1).

### `ffmpeg not found`

```powershell
winget install Gyan.FFmpeg
```

Then close and reopen the console. If it still cannot find it:

```powershell
$env:KARAOKESYNC_FFMPEG = "C:\path\to\ffmpeg.exe"
```

### It takes a very long time

This is normal: the program does heavy work (separating vocals from the
accompaniment). Measured on a normal computer **without** a graphics card: a
4:40 song took **4 minutes 24 seconds**.

To go faster:

- Choose **Fast** precision.
- Uncheck **Separate vocals and instrumental** (much faster, less precise).
- Repeat the same song: the second time takes **seconds**.
- With an NVIDIA GPU, install the GPU build from source (see `README.md`).

### Re-analyzing a song you already processed

**The second time takes seconds, not minutes.** The program stores three
expensive results in the temporary folder: source separation, speech recognition
and the **complete result**. Measured on a 4:40 song: first time 385 s, second
time **2.4 s**. This is perfect for *“it did not fit → I fixed one lyric line →
run again”*.

If you delete those folders nothing breaks: it just takes as long as the first
time. You can inspect and free space with:

```powershell
KaraokeSync.exe --cache-info      # what each cache occupies
KaraokeSync.exe --clean-temp      # remove orphaned work folders
KaraokeSync.exe --purge-cache     # delete the whole cache
```

### Several songs at once (batch)

```powershell
# Every song in a folder, lyrics found by filename
KaraokeSync.exe --batch "C:\Music" --lyrics-dir "C:\Lyrics" -d "C:\Output"
```

Models are loaded **once** for the whole batch and **one failed song does not
stop the others**. At the end you get a summary with each song's time.

### Knowing whether the program is advancing

Every stage reports percentage, elapsed time and what remains, **also with
`-q`**. If 25 seconds pass without news, it prints a heartbeat, so there is
never more than 30 s without a sign of life.

### The program says the lyrics do not match, but they are correct

Check issue `ALU-003` and the line `Lyrics verified: NO (similarity X)`. The
program compares your lyrics with what it recognizes and requires **45 %**
similarity. Below that it does not invent timings: it says so and distributes
the lyrics over vocal segments (useful for *when*, not *what*).

Usual causes:

1. **The lyrics are from another version** (live, remaster, translation) or not
   this song.
2. **The lyrics are incomplete** or contain an invented/repeated part.
3. **You are very close to the threshold.** Two independent transcriptions of
   the same song were measured at 47 % similarity, so a correct lyric from a
   different source can sit near the limit.

If you are sure:

```powershell
KaraokeSync.exe -i song.flac -l lyrics.txt --language en --set alignment.min_similarity=0.40
```

### The window closes immediately when opened

Open a console and run `KaraokeSync.exe --gui`: the error message stays in the
console instead of disappearing.

### The Drag & Drop does not find my audio

The browser never reveals the real path of a dropped file, only its name. Studio
searches that name and size in the output folder, previous audio folder, current
folder, Downloads, Music, Desktop and one level inside Downloads/Music.

If the file is on another drive or in a deep folder, you will see the
`toast.browserNoPath` message and the Windows picker opens. This is not an
error: use the picker once. Lyrics (`.lrc`, `.txt`, `.srt`) do not have this
problem because they are read directly in the browser.

## 16. Frequently asked questions

**Does KaraokeSync upload my song anywhere?**
No. It runs locally. Only model downloads need internet, and only the first
time.

**Can I use it without lyrics?**
Yes. It detects vocals, instrumental, silence and noise. You just will not get
`.lrc` or `.srt` text.

**Does it work on songs in any language?**
Yes, but tell the aligner the language with `--language` when possible. Without
lyrics, the VAD is language-independent.

**Does it separate vocals from the music?**
Yes, with Demucs `htdemucs`. On CPU the optimized pipeline is substantially
faster; with `--keep-stems` you can keep the isolated vocals and accompaniment.

**Why does the first song take so long?**
It downloads models and runs Demucs. Re-running the same song uses the cache and
takes seconds.

**Does it invent lyrics?**
No. If it cannot align your lyrics reliably, it says so and marks timings as
estimates.

**Can I edit the result?**
Yes. Use the Studio timing editor or the standalone `--editor` HTML file.

**Can I export word-by-word subtitles for CapCut?**
Yes. Enable **Word-by-word SRT (CapCut / Reels / TikTok)** before processing and
import the `.srt` into CapCut, DaVinci Resolve or Premiere Pro.

**Can I get Enhanced LRC?**
Yes. Enable **Enhanced LRC** to add `<mm:ss.xx>` word tags.

**Does it work offline?**
Yes, after models are downloaded. Use `--descargar-modelos` before going offline.

**Can I process many songs at once?**
Yes, with `--batch`. Models load once and a failure does not stop the batch.

**Is it open source?**
No. It is proprietary software with a license that allows personal, educational
and evaluation use but not commercial use or redistribution. See `LICENSE`.

---

## 17. Quick command reference

Everything here is optional: **the GUI needs none of it**. Commands are typed
inside the program folder.

```powershell
# The basics: song + lyrics
KaraokeSync.exe -i song.flac -l lyrics.txt

# Without lyrics (only detect when singing happens)
KaraokeSync.exe -i song.mp3

# Choose output folder and precision
KaraokeSync.exe -i song.flac -l lyrics.txt -d C:\Output -p equilibrada

# Faster (less precise)
KaraokeSync.exe -i song.flac -l lyrics.txt --no-separation

# Open KaraokeSync Studio
KaraokeSync.exe --studio

# Open the classic GUI
KaraokeSync.exe --gui

# Check the computer
KaraokeSync.exe --diagnostico

# Preload models for offline use
KaraokeSync.exe --descargar-modelos

# Word-by-word SRT through the CLI
KaraokeSync.exe -i song.flac -l lyrics.txt --srt words.srt --set output.srt_unit=palabra

# Enhanced LRC through the CLI
KaraokeSync.exe -i song.flac -l lyrics.txt --lrc words.lrc --set output.lrc_word_tags=true

# Audit a result
KaraokeSync.exe --verificar "C:\Output\song.json"

# Generate the standalone editor
KaraokeSync.exe -i song.flac -l lyrics.txt --language en --editor
```

| Option | Purpose |
|---|---|
| `-i`, `--input` | The song (MP3, FLAC, WAV, M4A, OGG…) |
| `-l`, `--lyrics` | The lyrics (`.txt`, `.lrc` or `.srt`) |
| `-o`, `--output` | Path of the `.txt` report |
| `-d`, `--outdir` | Output folder |
| `-p`, `--precision` | `rapida`, `equilibrada` (default) or `alta` |
| `--language` | Lyrics language: `es`, `en`, `fr`… |
| `--no-separation` | Do not use Demucs (faster) |
| `--keep-stems` | Also save `vocals.wav` and `no_vocals.wav` |
| `--lrc`, `--srt`, `--json` | Specific path for each file |
| `--set key=value` | Change one parameter, e.g. `--set alignment.min_similarity=0.30` |

---

**What if something does not work?** Run `KaraokeSync.exe --diagnostico` and
read the report issues: they explain the problem and usually say what to do. The
program is designed to **never invent data**: when it cannot do something
precisely, it says so in the report instead of giving you false data.
