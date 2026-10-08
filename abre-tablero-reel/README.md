# Reel Tablero de Dirección® — ABRE Integradores (HyperFrames)

Versión vertical (1080×1920) del video del Tablero de Dirección, más pausada para leer cómodo en el celular.
Dura 100 s; cada pregunta y cada paso queda 4 s en pantalla y cada beneficio 3 s.
Los textos quedan dentro de la zona segura de Reels (no los tapan los botones de Instagram).

| Tiempo | Escena |
|---|---|
| 0–6 s | Gancho |
| 6–10 s | Título |
| 10–20 s | ¿Qué es? + tablero ilustrativo |
| 20–48 s | 6 preguntas (4 s c/u) |
| 48–76 s | Cómo trabajamos en 6 pasos (4 s c/u) |
| 76–88 s | Beneficios (3 s c/u) |
| 88–94 s | Pregunta final |
| 94–100 s | Cierre y contacto |

Música: `assets/audio/musica-reel.mp3`, generada con `python3 ../abre-tablero/tools/generar_musica.py musica-reel.wav reel`.

```bash
cd abre-tablero-reel
npm run dev      # preview
npm run render   # exporta MP4 a renders/
```
