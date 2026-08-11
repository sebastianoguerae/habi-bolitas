#!/usr/bin/env python3
"""Cifra el HTML de la gráfica de bolitas y lo empaqueta en index.html (GitHub Pages).

Uso:  python3 build.py [clave]
Fuente: ~/Desktop/habi_bolitas_evolucion.html   Salida: ./index.html

El payload va cifrado con AES-GCM 256 (clave derivada con PBKDF2-SHA256, 200k
iteraciones), así que el repo público no contiene las cifras en texto claro.
"""
import base64, hashlib, json, os, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

SRC = os.path.expanduser("~/Desktop/habi_bolitas_evolucion.html")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
CLAVE = sys.argv[1] if len(sys.argv) > 1 else "bolitas2027"
ITERS = 200_000

payload = open(SRC, encoding="utf-8").read()
salt = os.urandom(16)
iv = os.urandom(12)
key = hashlib.pbkdf2_hmac("sha256", CLAVE.encode(), salt, ITERS, dklen=32)
ct = AESGCM(key).encrypt(iv, payload.encode("utf-8"), None)

blob = json.dumps({
    "salt": base64.b64encode(salt).decode(),
    "iv": base64.b64encode(iv).decode(),
    "ct": base64.b64encode(ct).decode(),
    "iters": ITERS,
})

GATE = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Habi — Evolucion por negocio</title>
<meta name="robots" content="noindex, nofollow">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Montserrat,-apple-system,"Segoe UI",Roboto,sans-serif;background:#F5F2FC;color:#191919;
     min-height:100vh;display:grid;place-items:center;padding:24px}
.card{background:#fff;border-radius:18px;padding:34px 30px;max-width:400px;width:100%;
      box-shadow:0 14px 40px rgba(75,26,139,.18);text-align:center}
.mark{width:46px;height:46px;border-radius:14px;margin:0 auto 16px;
      background:linear-gradient(135deg,#4B1A8B,#830EFF)}
h1{font-size:17px;font-weight:900;color:#4B1A8B;line-height:1.3}
p.sub{font-size:12px;color:#4C4C4D;margin-top:8px;line-height:1.5}
form{display:flex;flex-direction:column;gap:10px;margin-top:22px}
input{font-family:inherit;font-size:15px;padding:12px 14px;border:1.5px solid #DED4F2;border-radius:11px;
      text-align:center;letter-spacing:.5px;background:#FBFAFE}
input:focus{outline:none;border-color:#830EFF;box-shadow:0 0 0 3px rgba(131,14,255,.15)}
button{font-family:inherit;font-size:15px;font-weight:800;padding:12px;border:none;border-radius:11px;
       background:#830EFF;color:#fff;cursor:pointer}
button:hover:not(:disabled){background:#4B1A8B}
button:disabled{opacity:.6;cursor:progress}
.err{color:#E4545D;font-size:12px;font-weight:700;min-height:16px;margin-top:4px}
.foot{font-size:10px;color:#8A8496;margin-top:18px;font-style:italic}
</style>
</head>
<body>
<div class="card">
  <div class="mark"></div>
  <h1>Habi &mdash; Evolucion por negocio</h1>
  <p class="sub">Crecimiento del GTV vs. margen de contribucion por linea de negocio, 2023&ndash;2027. Documento interno.</p>
  <form id="f">
    <input id="pw" type="password" placeholder="Clave de acceso" autocomplete="off" autofocus>
    <button id="b" type="submit">Entrar</button>
    <div class="err" id="e"></div>
  </form>
  <p class="foot">Informacion confidencial de Habi. No redistribuir.</p>
</div>
<script>
const BLOB = __BLOB__;
const b64 = s => Uint8Array.from(atob(s), c => c.charCodeAt(0));
document.getElementById('f').addEventListener('submit', async ev => {
  ev.preventDefault();
  const btn = document.getElementById('b'), err = document.getElementById('e');
  err.textContent = ''; btn.disabled = true; btn.textContent = 'Abriendo...';
  try {
    const km = await crypto.subtle.importKey('raw', new TextEncoder().encode(document.getElementById('pw').value), 'PBKDF2', false, ['deriveKey']);
    const key = await crypto.subtle.deriveKey(
      { name:'PBKDF2', salt: b64(BLOB.salt), iterations: BLOB.iters, hash:'SHA-256' },
      km, { name:'AES-GCM', length:256 }, false, ['decrypt']);
    const pt = await crypto.subtle.decrypt({ name:'AES-GCM', iv: b64(BLOB.iv) }, key, b64(BLOB.ct));
    const html = new TextDecoder().decode(pt);
    document.open(); document.write(html); document.close();
  } catch (_) {
    err.textContent = 'Clave incorrecta.';
    btn.disabled = false; btn.textContent = 'Entrar';
    document.getElementById('pw').select();
  }
});
</script>
</body>
</html>
"""

open(OUT, "w", encoding="utf-8").write(GATE.replace("__BLOB__", blob))
print(f"OK  {OUT}  ({os.path.getsize(OUT)/1024:.0f} KB)  clave: {CLAVE}")
