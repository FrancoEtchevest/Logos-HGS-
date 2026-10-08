# Video Tablero de Dirección® — ABRE Integradores (HyperFrames)

Video de 60 s (1920×1080) con música propia a 120 BPM. Cada aparición cae en un golpe de la música
(un compás = 2 s). Los textos se escriben en pantalla; no hay recortes del brochure.

| Tiempo | Escena |
|---|---|
| 0–4 s | Gancho: "¿Sabés dónde está parada tu empresa hoy?" |
| 4–8 s | Título: Tablero de Dirección® |
| 8–16 s | ¿Qué es? + tablero ilustrativo animado + Medí / Planificá / Decidí |
| 16–30 s | 6 preguntas que te ayuda a responder (una cada 2 s) |
| 30–44 s | Cómo trabajamos en 6 pasos (uno cada 2 s) |
| 44–52 s | Beneficios |
| 52–56 s | "¿Listo para tomar decisiones con información clara y confiable?" |
| 56–60 s | Cierre con logo y contacto |

```bash
cd abre-tablero
npm run dev      # preview en el navegador
npm run render   # exporta MP4 a renders/
python3 tools/generar_musica.py musica.wav   # regenera la música (requiere numpy y scipy)
```

- `index.html`: composición y timeline.
- `assets/audio/musica.mp3`: música generada por `tools/generar_musica.py` (libre de derechos).
- `renders/tablero-de-direccion.mp4`: render ya generado.
