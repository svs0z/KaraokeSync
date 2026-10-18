# KaraokeSync — Guía de uso completa

**Para cualquier persona, sin conocimientos técnicos.** Todo lo que hay que hacer
está aquí, paso a paso, con los textos exactos que hay que escribir.

KaraokeSync escucha una canción y te dice:

1. **Cuándo se canta** y cuándo no (voz, instrumental, silencio, ruido), con
   marcas de tiempo del tipo `00:01:23.450` (al milisegundo).
2. **Qué se canta**, si le das la letra: te genera un `.lrc` (karaoke), un `.srt`
   (subtítulos) y un `.json`.
3. **Un reporte `.txt`** que se abre perfecto en el Bloc de notas.

---

## Índice

1. [Antes de empezar: qué necesitas](#1-antes-de-empezar-qué-necesitas)
2. [Instalación en Windows](#2-instalación-en-windows)
3. [Comprobar que funciona](#3-comprobar-que-funciona)
4. [Usar la ventana (lo más fácil)](#4-usar-la-ventana-lo-más-fácil)
5. [Subir las canciones](#5-subir-las-canciones)
6. [La letra: la parte que importa](#6-la-letra-la-parte-que-importa)
7. [Dónde conseguir un `.lrc` ya sincronizado](#7-dónde-conseguir-un-lrc-ya-sincronizado)
8. [Errores típicos al preparar la letra](#8-errores-típicos-al-preparar-la-letra)
9. [¿Está bien sincronizado? Cómo comprobarlo](#9-está-bien-sincronizado-cómo-comprobarlo)
10. [Leer el reporte](#10-leer-el-reporte)
11. [Qué hacer con los archivos que genera](#11-qué-hacer-con-los-archivos-que-genera)
12. [Problemas y soluciones](#12-problemas-y-soluciones)
13. [Referencia rápida de comandos](#13-referencia-rápida-de-comandos)

---

## 1. Antes de empezar: qué necesitas

| | |
|---|---|
| **Sistema** | Windows 10 u 11 (también funciona en Linux y macOS, ver el `README.md`) |
| **Espacio en disco** | Unos 4 GB con todo instalado (PyTorch y Demucs ocupan bastante) |
| **Internet** | Solo la primera vez, para descargar los modelos. Después funciona sin conexión |
| **Tarjeta gráfica** | No hace falta. Con CPU funciona; con GPU NVIDIA va mucho más rápido |
| **Conocimientos** | Ninguno. Los comandos se copian y se pegan |

**Un aviso importante sobre el antivirus.** Windows puede bloquear las librerías
de cálculo (numpy, torch) si el **Control de aplicaciones inteligentes** está
activado, y entonces verás errores de tipo *"No module named 'numpy'"* o
*"acceso denegado"* aunque la instalación haya ido bien. Si te pasa:

> Inicio → **Seguridad de Windows** → *Control de aplicaciones y navegador* →
> *Control de aplicaciones inteligentes* → **Desactivado**. Reinicia el equipo y
> vuelve a probar.

---

## 2. Instalación en Windows

1. Descarga **`KaraokeSync-1.0.0-win64.zip`** desde la página de *Releases*.
2. Clic derecho sobre el archivo → **Extraer todo…** y elige una carpeta
   (por ejemplo `C:\Users\<tu usuario>\KaraokeSync`).
3. Entra en la carpeta y haz **doble clic en `KaraokeSync.exe`**.

No hay que instalar Python, ni ffmpeg, ni nada más: todo va dentro.

> La primera vez, Windows puede avisar de que el archivo no tiene firma digital.
> Es normal: pulsa **Más información → Ejecutar de todas formas**.

## 3. Comprobar que funciona

Si algo va mal, esto te dice qué. En la ventana gráfica pulsa el botón
**Diagnóstico**; o en la consola:

```powershell
KaraokeSync.exe --diagnostico
```

Tiene que aparecer algo así (esta es la salida real de este equipo):

```
  Python       : 3.12.10
  ffmpeg       : C:\...\ffmpeg.exe
  Interfaz GUI : disponible
  GPU CUDA     : no

  [ OK ] numpy       [ OK ] torch        [ OK ] silero_vad
  [ OK ] demucs      [ OK ] librosa      [ OK ] faster_whisper

  RESULTADO: el equipo PUEDE ejecutar KaraokeSync.
```

Si la última línea dice **PUEDE ejecutar KaraokeSync**, todo está listo. Si dice
que **no**, copia el texto y mira la sección [Problemas y
soluciones](#11-problemas-y-soluciones).

---

## 4. Usar la ventana (lo más fácil)

La ventana tiene tres apartados. Se rellena de arriba abajo y se pulsa **Generar
reporte**.

### Archivos

| Campo | Qué poner |
|---|---|
| **Audio** | Pulsa *Seleccionar…* y elige la canción (MP3, FLAC, WAV, M4A, OGG…) |
| **Letra (opcional)** | Pulsa *Seleccionar…* y elige tu `.txt`, `.lrc` o `.srt`. **Si lo dejas vacío, el programa funciona igual**, pero solo te dirá *cuándo* se canta, no *qué* se canta |
| **Carpeta de salida** | Dónde quieres los resultados. Si la dejas vacía, se guardan junto a la canción |

### Precisión

| Opción | Qué hace | Cuándo elegirla |
|---|---|---|
| **Rápida** | Ventanas de 32 ms. La más veloz | Para probar si la letra cuadra, o para muchas canciones |
| **Equilibrada** ← *por defecto* | Ventanas de 10 ms | **Es la que debes usar.** Buen equilibrio |
| **Alta precisión** | 10 ms, Demucs reforzado y un modelo de reconocimiento enorme (`large-v3`), con marcas por palabra | Solo si tienes una GPU NVIDIA o mucha paciencia: en un ordenador normal puede tardar **más de una hora por canción** y descarga unos 3 GB |

Casillas:

- **Separar voz e instrumental con Demucs** — *activada por defecto*. Es lo que
  hace que la detección sea precisa: separa la voz del acompañamiento antes de
  analizar. Si la desactivas, va mucho más rápido pero detecta peor.
- **Abrir la carpeta de salida al terminar** — cómodo para ver los resultados.
- **Guardar también `vocals.wav` y `no_vocals.wav`** — solo si quieres quedarte
  con la voz aislada y el acompañamiento (útil para cantar encima).

### Botones

- **Generar reporte** — empieza. Verás una barra de progreso y, debajo, un
  registro con lo que está pasando.
- **Cancelar** — lo detiene sin dejar archivos a medias.
- **Abrir editor de tiempos** — se activa cuando el análisis termina y abre en el
  navegador el editor de la canción, para corregir a mano cualquier línea que
  haya quedado desfasada. Es el botón que hace falta cuando algo no cuadra: no
  tienes que buscar archivos por las carpetas.
- **Diagnóstico** — comprueba el equipo.
- **Limpiar log** — vacía el registro de la pantalla.

> **No cierres la ventana mientras trabaja.** Una canción de 4 minutos tarda
> unos 4 o 5 minutos la primera vez. Si vuelves a analizar **la misma canción con
> los mismos ajustes**, tarda unos segundos: el programa guarda la separación de
> voz ya hecha.

---

## 5. Subir las canciones

**No hay que "subir" nada a ningún sitio.** Todo se queda en tu ordenador.

1. Guarda la canción en cualquier carpeta (Escritorio, Música, un USB…).
2. En la ventana, pulsa *Seleccionar…* en **Audio** y búscala.

Formatos que acepta: **MP3, FLAC, WAV, M4A, OGG, OGA, OPUS, AAC, WMA, AIFF, MP4,
WEBM**.

Cosas prácticas:

- **La calidad importa más de lo que parece.** Un MP3 de 128 kbps con mucho
  ruido de fondo da peores resultados que un FLAC o un MP3 de 320 kbps. Los
  formatos sin pérdida (FLAC, WAV) son los mejores.
- **Una canción por vez.** Para varias, repite el proceso.
- **Los vídeos también valen** (`.mp4`, `.webm`): se les extrae el audio.
- **La primera canción de todas tarda más** y necesita internet: el programa
  descarga el modelo que separa la voz del acompañamiento (80 MB) y, si vas a
  sincronizar letra, el modelo de reconocimiento (unos 140 MB). Después ya están
  guardados y puedes trabajar sin conexión. Si quieres descargarlos de antemano
  (por ejemplo antes de un viaje), ejecuta `KaraokeSync.exe --descargar-modelos`.
- **Se genera una copia de trabajo temporal** (en `%TEMP%\karaokesync_stems_cache`).
  Cada canción ocupa unos 100 MB y se guardan las últimas 20. Si el disco se
  llena, borra esa carpeta sin miedo: solo se pierde la rapidez al repetir.

---

## 6. La letra: la parte que importa

### ¿Es obligatoria? No, pero cambia todo

| | Sin letra | Con letra |
|---|---|---|
| **Cuándo** se canta | Sí, con precisión | Sí, con precisión |
| **Qué** se canta | No | Sí |
| Archivos | Reporte `.txt` y `.json` | Además `.lrc` y `.srt` |

Sin letra es imposible saber qué se canta, y el programa **nunca se lo inventa**:
si no puede alinear la letra, lo dice claramente en el reporte.

### Formato 1: un archivo `.txt` (el más fácil)

Es lo que debes usar si no tienes nada. **Una línea de letra por renglón.**

**Paso a paso, desde una web de letras:**

1. Abre la canción en musixmatch, letras.com, Genius… lo que uses.
2. Selecciona **todo** el texto de la página (Ctrl+A) y cópialo (Ctrl+C).
3. Abre el **Bloc de notas** y pega (Ctrl+V).
4. Guarda con **Archivo → Guardar como**:
   - **Tipo:** *Todos los archivos* (¡importante!)
   - **Nombre:** `letra.txt` (con el `.txt` incluido, entre comillas si hace falta)
   - **Codificación:** `UTF-8`
5. En KaraokeSync, elige ese archivo en **Letra (opcional)**.

> **El error más común:** si en *Tipo* dejas *Documentos de texto* y escribes
> `letra.txt`, Windows guarda `letra.txt.txt` y luego no lo encuentras. Elige
> **Todos los archivos** o escribe el nombre **entre comillas**: `"letra.txt"`.

**Pega sin miedo el encabezado de la web.** KaraokeSync está preparado para eso y
sabe distinguir la letra de lo que no lo es:

| Lo que aparece al pegar | Qué hace con ello |
|---|---|
| `Luna (feat. Lo Blondo)`, `Zoé`, `Letra de Luna`, `Ver más`, `© 2024 …`, enlaces | Lo reconoce como título, créditos o interfaz y **no** lo cuenta como letra |
| `Título:`, `Artista:`, `Composición:`, `Escritores:`, `Álbum:`… | Lo guarda como dato de la canción y lo usa para la cabecera del `.lrc` |
| `[Verso 1]`, `[Estribillo]`, `[Coro]` | Etiquetas de sección |
| `(oh yeah)`, `(no, no, no)` | **Letra cantada.** Los paréntesis nunca son una sección |
| `Ana: mi parte` | Intérprete, en canciónes a dúo |
| `Dime: ¿por qué no vuelves?` | Letra cantada completa (no pierde el `Dime:`) |

**Y siempre te avisa.** Si descarta alguna línea por creer que es encabezado, lo
dice en el reporte con el texto exacto:

```
[AVISO] LET-004: Se ignoraron 1 linea(s) de encabezado/creditos al principio
del archivo: 'Zoé'. Si alguna era letra, borrala del .txt o quita el
encabezado para que se conserve.
```

**Plantilla recomendada.** Copia esto, cambia el texto y guarda como `.txt`:

```
Título: Nombre de la canción
Artista: Quien la canta

[Verso 1]
Primera línea que se canta de un tirón
Segunda línea que se canta de un tirón

[Estribillo]
El estribillo entero, línea a línea

[Verso 2]
Y sigue la canción
```

**Tres consejos que mejoran el resultado:**

1. **Una línea = una frase cantada.** No pegues un párrafo entero: si una línea
   es larguísima, se reparte mal. Y al contrario, no partas una frase cantada en
   dos líneas.
2. **El `Título:` sirve para algo.** Si lo pones, aparece en la cabecera del
   `.lrc`. Si no, se usa el nombre del archivo de audio.
3. **Marca las secciones con corchetes** (`[Estribillo]`). Se usan para etiquetar
   los tramos y se ven en el reporte.

### Formato 2: un archivo `.lrc` (el mejor resultado)

Si ya tienes un `.lrc` (letra ya sincronizada, con marcas `[00:12.34]`), úsalo:
**es el mejor punto de partida posible**. El programa aprovecha esas marcas como
anclas y ajusta el resto a *tu* audio, así que el resultado es más fiable y más
rápido.

También admite `.lrc` enriquecido (con marcas por palabra, `<00:12.34>`).

### Formato 3: un `.srt` (subtítulos)

Si tienes los subtítulos de un vídeo karaoke en `.srt`, también vale. Se
aprovechan sus tiempos igual que los del `.lrc`.

### Qué formato elegir

| Situación | Usa |
|---|---|
| No tengo nada | **`.txt`** pegando de la web (con la plantilla de arriba) |
| Encontré un `.lrc` de la canción | **`.lrc`**, es lo mejor |
| Tengo los subtítulos de un karaoke | **`.srt`** |

### La letra: cómo debe estar para el mejor resultado

Esto es lo que más diferencia hace, y es gratis. La regla de oro es **una línea
= una frase cantada**: el programa encaja *líneas* contra el audio, así que si
partes un verso en trozos de subtítulo, tiene que adivinar dos veces.

| Haz esto | Evita esto |
|---|---|
| Una frase cantada por línea | Cortar a mitad de frase |
| El **orden** en que se canta, con los estribillos **repetidos** cada vez | Escribir «(x2)» o poner el estribillo una sola vez |
| La letra de **esa grabación** (estudio ≠ directo ≠ remezcla) | Mezclar versiones o traducciones |
| Todo en **un** idioma | Pegar la letra y la traducción alternadas |
| Un `.txt` en UTF-8 (Bloc de notas) | Fotos, PDF, texto con formato |
| Copiar y pegar de letras.com, Musixmatch o Genius | Escribirla de memoria |

**Pegar de letras.com funciona tal cual.** Lo que llega de más se limpia solo:
las etiquetas `[Verso 1: …]`, `[Pre-Coro: …]`, `[Letra de "…"]` y el bloque
«You might also like» de Genius con sus tres pares de canciones. Un ejemplo de
letra pegada de la web, tal cual:

```
[Letra de "Luna (Unplugged)" ft. Denise Gutiérrez]

[Verso 1: Denise Gutiérrez]
Entiendo que no puedo suplicarle una vez más
Pero nada se detiene, solo vivo para ti

[Pre-Coro: Denise Gutiérrez, Denise Gutiérrez & León Larregui]
Y cuando te me acercas, se acelera mi motor
```

Eso se convierte en **3 versos limpios**: las dos etiquetas y el encabezado se
descartan y la sección (`Verso 1`) se conserva como dato, no como letra.

Y si el resultado no queda perfecto, no hace falta volver a analizar: el editor
de tiempos (en el apartado «¿Está bien sincronizado? Cómo comprobarlo») lo
arregla en un par de minutos.


> **Aviso importante sobre la versión.** La causa número uno de que la letra no
> cuadre es que la letra sea de **otra versión**: la de estudio, la del directo,
> la del disco recopilatorio, o una traducción. Si el programa avisa de que *"la
> letra no coincide con lo que se canta"*, casi siempre es esto. Busca la letra
> de la versión exacta que tienes (mismo álbum, mismo directo).

---

## 7. Dónde conseguir un `.lrc` ya sincronizado

Un `.lrc` es un archivo de texto con marcas de tiempo delante de cada línea:

```
[ti:Luna]
[ar:Zoé]
[00:15.20]Yo te espero en la esquina
[00:18.90]con la luna en la mirada
```

Esos archivos son los que usan los reproductores para mostrar la letra
sincronizada, así que se consiguen por las mismas vías:

1. **LRCLIB** — [lrclib.net](https://lrclib.net) es una base de datos **gratuita
   y abierta** de letras sincronizadas, sin necesidad de cuenta. Busca la canción,
   y si tiene versión sincronizada te muestra las marcas `[mm:ss.xx]`: selecciona,
   copia y guarda como `.txt`/`.lrc` con el Bloc de notas. Es la fuente más limpia
   y la que usan muchas herramientas libres, por ejemplo
   [lrcdl](https://github.com/viown/lrcdl) o
   [lyric_extract](https://github.com/nestormata/lyric_extract).

2. **MusicBee** (reproductor gratuito para Windows) con el complemento
   [mb_AutoLyrics](https://getmusicbee.com/addons/plugins/584/mb-autolyrics-multi-source-amp-synced-lyrics-plugin/)
   — busca y descarga la letra sincronizada **automáticamente**, y la guarda como
   `.lrc` en la misma carpeta que la canción. Es la opción más cómoda si tienes
   toda tu música en el ordenador: seleccionas las canciones, le das a descargar
   letras y ya tienes los `.lrc` listos para pasar por KaraokeSync.

3. **Reproductores con letra sincronizada** (AIMP, foobar2000 con complemento,
   algunos reproductores de Android) suelen guardar la letra que descargan como
   `.lrc` en la carpeta de la canción. Búscala ahí: mismo nombre que el audio y
   extensión `.lrc`.

4. **musixmatch, letras.com, Genius** — **no** dan `.lrc` descargable, solo
   texto. Para esos, usa el camino del `.txt` de la sección anterior: se pega tal
   cual y el programa lo limpia.

> **Las letras de las webs tienen derechos de autor.** Úsalas para tu uso
> personal. Si vas a publicar o compartir el resultado, usa letras libres o
> pide permiso.

> **Y recuerda:** KaraokeSync **genera** el `.lrc` por ti. Si no encuentras
> ninguno, no pasa nada: pega la letra en un `.txt` y el programa te hará el
> `.lrc` con los tiempos de *tu* archivo de audio, que es justo lo que quieres.

---

## 8. Errores típicos al preparar la letra

| Síntoma | Causa | Solución |
|---|---|---|
| *"No se ha podido extraer ninguna línea de letra"* | El archivo está vacío o solo tiene el encabezado | Comprueba que dentro está la letra |
| La letra es un solo párrafo enorme | Se pegó sin saltos de línea | Corta cada frase en su propia línea |
| *"La letra no coincide con lo que se canta"* (similitud baja) | La letra es de otra versión, otro idioma o no es de esa canción | Busca la letra de la versión exacta. Si estás seguro de que es correcta, baja el listón: `--set alignment.min_similarity=0.30` |
| Falta una línea que sí era letra | Se descartó por parecer encabezado | El reporte dice cuál (`LET-004`). Quita esa línea del `.txt` o borra el encabezado y vuelve a ejecutarlo |
| Una línea sale con `Ana:` delante | El nombre aparecía una sola vez y no se tomó por intérprete | Es deliberado: perder texto es peor. Escribe `Ana:` en sus líneas o quítalo |
| Los acentos salen mal | El `.txt` no estaba en UTF-8 | Vuelve a guardarlo eligiendo codificación **UTF-8** |
| El programa no encuentra el archivo | Se guardó como `letra.txt.txt` | Activa *Ver → Extensiones de nombre de archivo* en el Explorador y renómbralo |

---

## 9. ¿Está bien sincronizado? Cómo comprobarlo

Esta es la pregunta importante, y tiene tres respuestas, de la más rápida a la
más fiable.

### Paso 1: mira lo que el propio programa dice (5 segundos)

Abre el reporte y busca estas dos líneas:

```
  Alineación real       : SÍ
  Letra verificada      : SÍ (similitud 0.63)
```

- **`Alineación real: SÍ`** → las marcas salen de encajar la letra contra el
  audio. Es lo que quieres.
- **`Alineación real: NO`** → la letra **se repartió** sobre los tramos de voz.
  Sirve para saber *cuándo* se canta, pero **no** para karaoke palabra a palabra.
  El reporte lo explica en las incidencias (`ALU-003`). No hace falta seguir
  comprobando: el programa ya te está diciendo que no te fíes de esas marcas.
- **`similitud`** es cuánto se parece tu letra a lo que se reconoce en el audio.
  Por debajo del 45 % la alineación se rechaza. Si está entre el 45 % y el 60 %,
  conviene comprobar a oído.

### Paso 2: pide la auditoría del resultado

```powershell
KaraokeSync.exe --verificar "C:\Salida\cancion.json"
```

Esto hace la parte que **sí** se puede comprobar sin oír, y escribe un
`cancion_auditoria.txt` que puedes abrir en el Bloc de notas. Comprueba diez
cosas: si hubo alineación real, si los tiempos van en orden, si las líneas se
pisan, si alguna dura 20 ms o 30 s, si cada línea tiene voz debajo, si cada
palabra cae dentro de su línea, si algo se sale de la duración del audio y si
quedaron incidencias. Al final da un **veredicto** en lenguaje llano.

Ejemplo real de un resultado correcto (8 comprobaciones bien, 2 avisos, 0 fallos):

```
  VEREDICTO
  La sincronización es coherente, con 2 aviso(s) menor(es).
  Confírmalo escuchando los momentos del final.

  [OK]    Alineación real
          Alineación real con el audio (motor: faster_whisper). Similitud: 100%.
  [OK]    Tiempos en orden
  [AVISO] Duraciones razonables
          1 línea dura más de 25 s.
  [AVISO] Cada línea tiene voz debajo
          4 líneas no tienen ningún tramo de voz debajo (revisa el detalle).
```

Los avisos no significan que esté mal: significan «aquí hay algo que conviene
mirar». En ese caso, el detector de voz no marcó voz en 4 sitios donde el
reconocimiento sí encontró palabras; puede ser que el VAD se quedara corto.

### Paso 3: escúchalo (la prueba definitiva)

**El programa no oye**, así que no puede certificar por sí solo que una marca sea
correcta. La comprobación final es tu oído, y cuesta dos minutos:

1. La auditoría te propone **cinco momentos** repartidos por la canción (la
   primera línea, la mitad, la última y el arranque de algunos tramos de voz),
   con su minuto exacto. Son los sitios donde un desfase se nota enseguida.
2. Abre el audio en un reproductor que muestre la letra:
   - **VLC** con el `.srt` (Arrastrar y soltar → *Subtítulo → Añadir archivo de
     subtítulos*).
   - **AIMP, MusicBee, foobar2000 o Poweramp** (móvil) con el `.lrc` junto a la
     canción, con el mismo nombre.
3. Salta a esos minutos y compara: si lo que suena coincide con lo que dice el
   texto, está sincronizado. **Si el texto va adelantado o atrasado más de medio
   segundo, se nota al instante.**

### Paso 4: si algo baila, corrígelo en el editor

Ningún programa acierta siempre. Lo honesto no es prometerlo, sino darte la
herramienta para arreglarlo en dos minutos.

```powershell
KaraokeSync.exe -i cancion.flac -l letra.txt --language es --editor
```

Eso genera, junto a la canción, un archivo **`cancion_editor.html`**. Se abre con
**doble clic** en el navegador (no hace falta internet ni instalar nada) y
aparece la canción con todas sus líneas y sus horas:

| Quiero… | Cómo |
|---|---|
| Oír dónde cae una línea | Clic en la línea: salta a ese instante y la marca |
| Oír **solo** una línea | Botón 🔊 de esa línea: la reproduce desde medio segundo antes |
| Mover una línea | Botones `−250` `−50` `+50` `+250` de esa línea |
| Marcar el inicio «aquí» | Reproduce y pulsa `T` (o «Inicio aquí») |
| Mover **toda** la letra | Botones «Desplazar TODA la letra» de la barra |
| Corregir el texto | Clic en el texto y escribe |
| Añadir una línea | Botón **＋** de la línea anterior (o «＋ Añadir línea» arriba) |
| Borrar una línea | Botón **✕** de esa línea |
| Ver la letra como en un karaoke | El recuadro grande de arriba, mientras suena |
| Deshacer | `Ctrl+Z` (también deshace añadir y borrar) |
| Guardar | «💾 Guardar cambios» o «📁 Guardar en carpeta» |

**Guardar sin pasar por Descargas.** El botón **📁 Guardar en carpeta** te pide la
carpeta **una sola vez** y escribe ahí los dos archivos (`cancion.lrc` y
`cancion_editor.json`), sobrescribiendo los que ya hubiera: así el `.lrc` que
generó el análisis queda actualizado, sin `cancion (1).lrc` sueltos. Los botones
`⬇ .lrc` y `⬇ .json` hacen lo mismo de uno en uno, y el navegador **recuerda** la
carpeta que elegiste la última vez. En el editor, debajo de la barra, tienes la
ruta de la carpeta del reporte y un botón **Copiar ruta** para pegarla la primera
vez.

La barra de tiempo de arriba muestra **dónde está cada línea**: así se ven de un
vistazo los huecos y los montones, que son los dos fallos típicos. Y si dejas
tres líneas seguidas a menos de 1,2 s o dos que se pisan, sale un aviso en
amarillo.

Cuando termines, descarga el `.lrc` corregido y úsalo con el reproductor. Si
vuelves a analizar la canción con ese `.lrc`, el programa respetará sus marcas
como anclas (`anclas_archivo`), que es el método más exacto de todos.

### Lo que no se puede certificar solo

El reporte promete ±50 ms por línea cuando la alineación es real, pero eso es el
objetivo del método, no una medición hecha contra una verdad escrita a mano: para
medir la precisión absoluta haría falta marcar a mano una canción entera. Lo que
sí se puede comprobar, y es lo que hacen los tres pasos de arriba, es que las
marcas sean coherentes, que salgan de una alineación real y que suenen bien. Si
algo no cuadra, el paso 4 lo arregla.

---

## 10. Leer el reporte
El reporte es el archivo `<nombre de la canción>_karaokesync.txt`. Se abre con
doble clic en el Bloc de notas y se lee de arriba abajo.

**Las 6 primeras líneas** son la cabecera, siempre igual:

```
# REPORTE KARAOKESYNC
Archivo: cancion1.flac
Duración: 00:04:40.400
Sample rate: 44100 Hz
Método: Demucs (htdemucs) + Silero VAD + faster-whisper + encaje de la letra
Fecha: 2026-10-14 15:04:04
---
```

**El bloque de la línea de tiempo** es lo más útil. Una línea por tramo, con
formato `[inicio - fin] TIPO | conf=…`:

```
[00:00:00.000 - 00:00:31.500] INSTRUMENTAL | conf=0.99
[00:00:31.500 - 00:00:36.120] VOZ+INSTRUMENTAL | conf=0.81 texto="Yo te espero..."
```

Los tipos son:

| Tipo | Significa |
|---|---|
| `VOZ` | Se canta solo, sin acompañamiento |
| `VOZ+INSTRUMENTAL` | Se canta con música de fondo |
| `INSTRUMENTAL` | Suena música, nadie canta |
| `SILENCIO` | No hay nada audible |
| `RUIDO` | Ruido de banda ancha (aplausos, siseo, estática) |

Las marcas de tiempo **nunca** se redondean a segundos: siempre van al
milisegundo (`HH:MM:SS.mmm`).

Después vienen el resumen por tipos, el glosario, la letra sincronizada, los
parámetros usados, la precisión y, al final, **las incidencias**, que es lo que
hay que leer si algo no ha salido bien:

```
  Incidencias      : 2 advertencia(s), 0 error(es)
    [AVISO] LET-004 (letra): Se ignoraron 1 linea(s) de encabezado...
    [AVISO] ALU-003 (alineacion): La letra no coincide con lo que se canta...
```

---

## 11. Qué hacer con los archivos que genera

| Archivo | Para qué sirve |
|---|---|
| `<nombre>_karaokesync.txt` | **El reporte.** Se lee en el Bloc de notas |
| `<nombre>.lrc` | **Karaoke.** Cópialo junto a la canción con el mismo nombre y el reproductor te mostrará la letra sincronizada (AIMP, foobar2000, MusicBee, Poweramp en Android, VLC…) |
| `<nombre>.srt` | **Subtítulos.** Ábrelo con el vídeo en VLC (Arrastrar y soltar → *Subtítulo → Añadir archivo de subtítulos*). También se puede subir a YouTube |
| `<nombre>.json` | Los mismos datos en formato de datos, por si los quieres procesar |
| `vocals.wav`, `no_vocals.wav` | Solo si marcaste la casilla. La voz aislada y el acompañamiento, para cantar encima |

**Para usarlo como karaoke en el móvil:** copia el `.lrc` junto al MP3 con el
**mismo nombre** (`cancion.mp3` + `cancion.lrc`) y el reproductor lo detecta solo.

---

## 12. Problemas y soluciones

### `No module named 'numpy'` (o 'torch', o 'soundfile')

Estás ejecutando el Python del sistema en vez del del programa. Usa siempre los
lanzadores: **doble clic en `KaraokeSync.exe`**, o `KaraokeSync.exe` en la
consola. Si insistes en llamar a Python directamente, tiene que ser
`KaraokeSync.exe`.

Si aun así falla, puede ser el **Control de aplicaciones inteligentes** de
Windows (ver el punto 1).

### `No se ha encontrado ffmpeg`

```powershell
winget install Gyan.FFmpeg
```

Después **cierra y vuelve a abrir la consola**. Si sigue sin encontrarlo, dile
dónde está:

```powershell
$env:KARAOKESYNC_FFMPEG = "C:\ruta\a\ffmpeg.exe"
```

### Tarda muchísimo

Es normal: el programa hace un trabajo pesado (separar la voz del
acompañamiento). Referencia medida en un ordenador normal **sin** tarjeta
gráfica: una canción de 4:40 tardó **4 minutos y 24 segundos**.

Para ir más rápido:

- Elige precisión **Rápida**.
- Desmarca **Separar voz e instrumental** (mucho más rápido, menos preciso).
- Repite la misma canción: la segunda vez tarda **segundos**.
- Si tienes GPU NVIDIA, el programa la usa sola (no hay que instalar nada).

### Repetir el análisis de una canción ya hecha

**La segunda vez tarda segundos, no minutos.** El programa guarda en el temporal
tres cosas que cuestan mucho de calcular:

- la separación de voz e instrumental,
- el reconocimiento de la voz,
- **el resultado completo** (segmentos y letra ya alineada).

Medido en una canción de 4:40: la primera vez 385 s, la segunda **2,4 s**. Es
perfecto para el caso de *"no cuadraba → he corregido una línea de la letra →
vuelvo a ejecutar"*: el reconocimiento no depende de la letra, así que se
reutiliza. Cuando ocurre, el reporte lo dice: `CAC-001` si se reutilizó y
`ALU-007` para el reconocimiento.

Si borras esas carpetas no se rompe nada: solo vuelve a tardar como la primera
vez. Puedes ver qué ocupan y liberarlas así:

```powershell
KaraokeSync.exe --cache-info      # qué ocupa cada cosa
KaraokeSync.exe --clean-temp      # borra restos de ejecuciones interrumpidas
KaraokeSync.exe --purge-cache     # borra toda la caché
```

### Varias canciones de una vez (lote)

```powershell
# Todas las canciones de una carpeta, buscando su letra por el nombre
KaraokeSync.exe --batch "C:\Musica" --lyrics-dir "C:\Letras" -d "C:\Salida"
```

Los modelos se cargan **una sola vez** para todo el lote (medido: 3 canciones,
20,3 s sueltas frente a 8,5 s en lote) y **una canción que falle no detiene las
demás**. Al final sale un resumen con el tiempo de cada una.

Si solo quieres repetir con más calidad las que salgan mal:

```powershell
KaraokeSync.exe --batch "C:\Musica" --escalate-if-similarity 0.5
```

### Saber si el programa avanza

Cada etapa informa con porcentaje, tiempo transcurrido y lo que queda, **también
con `-q`**. Si pasan 25 segundos sin novedades, imprime un aviso de que sigue
trabajando, así que **nunca hay más de 30 s sin señal de vida**:

```
  10%  Separando voz e instrumental (Demucs)   0:00  queda ~--:--
  11%  Separando voz e instrumental (Demucs)   0:30  queda ~9:24 sigue trabajando: ...
  16%  Separando voz e instrumental (Demucs)   0:41  queda ~2:46 Separación completada.
```

### El programa dice que no coincide aunque la letra es correcta

Mira la incidencia `ALU-003` y la línea `Letra verificada: NO (similitud X)`. El
programa compara tu letra con lo que reconoce en el audio y exige un **45 %** de
parecido. Si está por debajo, no inventa marcas: te dice que no puede y reparte la
letra sobre los tramos de voz (que sirven para saber *cuándo* se canta, no *qué*).

Causas, por orden de frecuencia:

1. **La letra es de otra versión** (directo, remasterización, traducción) o no es
   de esa canción. Es lo más habitual. Busca la letra de la versión exacta.
2. **La letra está incompleta** o tiene una parte inventada o repetida. El
   verificador lo detecta y por eso rechaza.
3. **Estás muy cerca del umbral.** Medido: dos transcripciones independientes de
   la misma canción se parecen un 47 %, así que una letra correcta pero de otra
   fuente puede quedarse al borde. Si estás seguro de que tu letra es la correcta:

```powershell
KaraokeSync.exe -i cancion.flac -l letra.txt --language es --set alignment.min_similarity=0.40
```

### Repetir el análisis de una canción ya hecha

**La segunda vez tarda segundos, no minutos.** El programa guarda en el temporal
dos cosas que cuestan mucho de calcular:

- la separación de voz e instrumental (`%TEMP%\karaokesync_stems_cache`),
- el reconocimiento de la voz (`%TEMP%\karaokesync_asr_cache`).

Medido en una canción de 4:40: la primera vez 385 s, la segunda **9,7 s**. Es
perfecto para el caso de *"no cuadraba → he corregido una línea de la letra →
vuelvo a ejecutar"*: el reconocimiento no depende de la letra, así que se
reutiliza. Cuando ocurre, el reporte lo dice con la incidencia `ALU-007`.

Si borras esas carpetas no se rompe nada: solo vuelve a tardar como la primera vez.

### El programa dice que no puede alinear la letra

Mira las incidencias del reporte. Los dos avisos habituales son:

- **`ALU-003` / "La letra no coincide con lo que se canta"** → la letra no es de
  esa versión o de ese idioma. Si estás seguro de que es correcta, baja el
  listón: `KaraokeSync.exe -i cancion.flac -l letra.txt --set alignment.min_similarity=0.30`
- **`LET-004`** → se descartó una línea creyendo que era encabezado. El aviso
  dice el texto exacto: quítalo del `.txt` y repite.

En cualquier caso, el programa **no inventa marcas**: si no puede alinear, lo
dice y te da los tramos de voz, que son fiables.

### La ventana se cierra sola al abrirla

Abre una consola y ejecuta `KaraokeSync.exe --gui`: así ves el mensaje de error
en la consola en vez de perderlo.

