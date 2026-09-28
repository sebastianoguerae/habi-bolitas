#!/bin/bash
# Pipeline reproducible: pristine (ago-21) → Plan 2030 → capítulos → cifrado → index.html
set -e; cd "$(dirname "$0")"
cp source/PRISTINE_habi_bolitas_evolucion_2026-08-21.html source/habi_bolitas_evolucion.html
python3 inject_plan2030.py && python3 inject_capitulos.py && python3 build.py profitable2027 >/dev/null && echo "build ok"
