# KaraokeSync

<p align="center"><img src="src/karaokesync/assets/logo.png" alt="KaraokeSync" width="110"></p>

<p align="center">
  <a href="https://github.com/svs0z/KaraokeSync/releases/download/v1.0.0/KaraokeSync-1.0.0-win64.zip">
    <img src="https://img.shields.io/badge/Descargar_para_Windows-559_MB-2f6f4f?style=for-the-badge" alt="Descargar KaraokeSync para Windows">
  </a>
</p>

> [!WARNING]
> **Este repositorio no contiene el código fuente de Python.** Incluye la
> documentación y la **aplicación web** (`index.html`), lista para desplegar en
> Cloudflare Pages. El programa de escritorio —doble clic y listo, sin instalar
> nada— está **en el botón de arriba**, o en
> [**Releases**](https://github.com/svs0z/KaraokeSync/releases/latest).


**KaraokeSync escucha una canción y dice, con precisión de milisegundos, cuándo
se canta y cuándo no**, y sincroniza la letra para karaoke.

## Qué hace

- **Línea de tiempo** de la canción en cinco tipos de tramo: **VOZ**,
  **VOZ+INSTRUMENTAL**, **INSTRUMENTAL**, **SILENCIO** y **RUIDO**, con las marcas
  de tiempo al milisegundo.
- **Sincronización de letra** a partir de un `.txt`, `.lrc` o `.srt`: palabra por
  palabra o línea por línea, con avisos honestos cuando los tiempos no son de
  fiar.
- **Editor de tiempos** en el navegador, incluido: arrastra los bloques sobre la
  barra, mira la letra grande como en un karaoke, oye una sola línea para
  comprobarla, y añade o quita líneas con un clic.
- **Exporta** `.lrc`, `.srt` y `.json`, y un **reporte `.txt`** que se abre
  perfectamente en el Bloc de notas.
- **KaraokeSync Studio en el navegador**: escenario karaoke en vivo, línea de tiempo interactiva, editor de tiempos, buscador LRCLIB, 4 idiomas (EN/ES/PT/FR) y modo híbrido con o sin servidor local.
- **Funciona sin conexión** después del primer uso, y sin tarjeta gráfica.

## KaraokeSync Studio en el navegador

Además de la ventana de escritorio, KaraokeSync incluye **KaraokeSync Studio**,
una interfaz web completa con dos modos:

- **Modo local**: al abrirla desde el programa, usa el motor Python de tu PC
  (Demucs, VAD, alineación) y genera reporte, `.lrc`, `.srt`, `.json` y stems.
- **Modo web**: al abrirla desde Cloudflare Pages, detecta que no hay servidor
  local y activa los respaldos del navegador: carga audio y letra desde tu
  equipo, busca la letra en [LRCLIB](https://lrclib.net), sincroniza y descarga
  `.lrc`, `.srt` y `.json`. Para separar `.wav` con IA (Demucs) hay que usar el
  programa de escritorio.

Incluye escenario karaoke en vivo, línea de tiempo interactiva, editor de
tiempos con deshacer, buscador integrado de LRCLIB y **cuatro idiomas**
(English, Español, Português, Français; inglés por defecto). Demucs en CPU usa
menos ventanas y varias en paralelo: *Dreams* (4:18) pasó de 5 min 41 s a
~1 min 25 s.

### Desplegar la versión web en Cloudflare Pages

Este repositorio ya trae en la raíz `index.html` (la aplicación completa) y
`favicon.ico`. No hay que compilar ni subir el código Python:

1. Cloudflare Pages → **Create a project** → **Connect to Git**.
2. Elige `svs0z/KaraokeSync`.
3. Framework preset: **None**. Build command: vacío. Output directory: `/`.
4. **Save and Deploy**.

La app arranca en inglés y detecta si hay servidor local. En Pages no lo hay,
así que usa el modo web; para el motor completo, abre `KaraokeSync.exe` en tu PC.

## Cómo se usa

1. **Descarga** el paquete del botón de arriba
   (`KaraokeSync-1.0.0-win64.zip`, unos 559 MB).
2. **Descomprímelo** donde quieras (clic derecho → *Extraer todo…*).
3. **Doble clic en `KaraokeSync.exe`**.
4. Elige la canción, y la letra si la tienes, y pulsa **Generar reporte**.

La carpeta queda así:

```
KaraokeSync\
├── KaraokeSync.exe        <- doble clic aquí
└── _internal\             <- todo lo que necesita (no tocar)
```

La **primera canción tarda 4-5 minutos**: descarga los modelos (unos 220 MB) y
separa la voz. Las siguientes tardan segundos.

> **Aviso del antivirus.** El `.exe` no está firmado digitalmente (firmar cuesta
> dinero) y Windows puede pedir confirmación la primera vez: *Más información →
> Ejecutar de todas formas*, o añade la carpeta a las exclusiones.

## Qué necesitas

| | |
|---|---|
| **Sistema** | Windows 10 u 11, de 64 bits |
| **Memoria** | Unos 4 GB libres |
| **Disco** | 2 GB para el programa y los modelos |
| **Sonido** | Cualquier formato habitual (`.flac`, `.mp3`, `.m4a`, `.wav`, `.ogg`) |
| **GPU** | No hace falta; con tarjeta NVIDIA va más rápido |
| **Conocimientos** | Ninguno |

## La guía

Todo el detalle —cómo preparar la letra, qué significa cada aviso del reporte,
qué hacer con los archivos, errores típicos— está en
[**GUIA_DE_USO.md**](GUIA_DE_USO.md).

## Licencia

Software **propietario** de **Sara Valentina Sepúlveda Ortiz (svs0z)**. Se
permite el uso personal, educativo o de evaluación. **No** se permite venderlo,
redistribuirlo ni usarlo comercialmente. El texto completo está en
[**LICENSE**](LICENSE).

Las letras y las grabaciones no se incluyen ni se distribuyen: cada obra tiene
su autor y sus derechos.

## Contacto

- GitHub: [@svs0z](https://github.com/svs0z)
- Incidencias y sugerencias: [Issues](https://github.com/svs0z/KaraokeSync/issues)
