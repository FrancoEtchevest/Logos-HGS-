# Video institucional ABRE Integradores (HyperFrames)

Video de 45 s (1920×1080) hecho con [HyperFrames](https://hyperframes.heygen.com) a partir del brochure institucional.
La identidad de marca (logo, colores, tipografía, textos y tono) está en [`MARCA.md`](MARCA.md).

Escenas: portada → quiénes somos → nuestros servicios → los 4 servicios → beneficios → metodología → diferencial → contacto.

Requisitos: Node.js ≥ 22 y FFmpeg.

```bash
cd abre-integradores
npm run dev      # preview en el navegador (Studio)
npm run check    # lint + validación
npm run render   # exporta MP4 a renders/
```

- `index.html`: la composición (escenas + timeline GSAP).
- `assets/brand/`: logo, isotipo e íconos con fondo transparente (versión color y `-blanco`).
- `assets/photos/`: fotos del brochure.
- `assets/fonts/` y `assets/vendor/`: Fira Sans y GSAP locales (renderiza sin internet).
- `renders/abre-integradores.mp4`: render ya generado.
