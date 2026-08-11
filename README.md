# Habi — Evolución por negocio (gráfica de bolitas)

Visualización 2023–2027 de las líneas de negocio de Habi: crecimiento del GTV
vs. margen de contribución, tamaño de bola = contribución absoluta en US$M.
Incluye vista agregada (Market Maker vs. nuevos negocios vs. total), pies de
reparto del margen de contribución y tablas de detalle 2026 / 2027.

**El contenido está cifrado** (AES-GCM 256, clave derivada con PBKDF2-SHA256,
200k iteraciones). El repo público no contiene cifras en texto claro: se
descifran en el navegador al entrar la clave de acceso.

## Regenerar

    python3 build.py <clave>

Toma `~/Desktop/habi_bolitas_evolucion.html`, lo cifra y escribe `index.html`.
Requiere `cryptography`.

Fuentes de datos: Sheet "Habi — Platform GTV 2022-2026" (GTV, contribución, FX),
BET/IsiBot (MM), y `Modelo habicapital _2026_07_Sent.xlsx` (HabiCapital, unit
economics a NPV).
