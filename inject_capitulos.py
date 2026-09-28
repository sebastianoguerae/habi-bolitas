#!/usr/bin/env python3
"""Actualiza TODOS los capítulos del aplicativo con el caso plan del Modelo 2030 v2.
Capa 1: la base 2027 de cada línea (LINES) pasa a ser el 2027 del caso plan (antes 2027e de agosto) y se agregan Home Equity y Broker MX.
Capa 2: cada capítulo recibe un bloque «Caso plan 2030» con sus cifras 2026-2030 y la nota de qué sigue siendo motor de agosto.
Corre DESPUÉS de inject_plan2030.py. Fuente de cifras: app_payload_plan2030.json (Modelo_2030_v2, FX 3.100/17)."""
import json, os, re, shutil
SRC = os.path.expanduser("~/leon/habi-bolitas/source/habi_bolitas_evolucion.html")
PAY = os.path.expanduser("~/leon/habi-plan-2030/08_modelo_2030_v2/app_payload_plan2030.json")
DESK = os.path.expanduser("~/Desktop/habi_bolitas_evolucion.html")
s = open(SRC, encoding="utf-8").read()
assert 'id="pane-p30"' in s, "corre primero inject_plan2030.py"
P = json.load(open(PAY))["plan"]
Y = ["2026", "2027", "2028", "2029", "2030"]
g = lambda y, k: P[y][k]
toApp = lambda v, pais: (v * 3100 / 3900) if pais == "CO" else (v * 17 / 18.5)   # USD@3100/17 → USD@3900/18.5 (base de LINES)

# ============================ CAPA 1: base 2027 = caso plan ============================
MAP = {"mmco": ("MM.co_gtv", "MM.co_cm_pre", "MM.co_cm", "CO"), "mmmx": ("MM.mx_gtv", "MM.mx_cm_pre", "MM.mx_cm", "MX"),
       "inmoco": ("Red.co_gtv", "Red.co_cm", "Red.co_cm", "CO"), "inmomx": ("Red.mx_gtv", "Red.mx_cm", "Red.mx_cm", "MX"),
       "habicredit": ("Credito.hcr_orig", "Credito.hcr_cm", "Credito.hcr_cm", "CO"), "pulppo": ("Red.pu_gtv", "Red.pu_cm", "Red.pu_cm", "MX"),
       "habicapital": ("Credito.hcap_orig", "Credito.hcap_cm", "Credito.hcap_cm", "CO"), "vivnueva": ("Red.vn_gtv", "Red.vn_cm", "Red.vn_cm", "MX")}
def set_last(arr_src, val):
    vals = arr_src.split(","); vals[-1] = f"{val:.2f}"; return ",".join(vals)
for lid, (kg, kb, ka, pais) in MAP.items():
    i = s.index(f"{{id:'{lid}'"); j = s.index("},", i)
    ent = s[i:j]
    def rep(field, val, ent=ent):
        m = re.search(field + r":\[([^\]]*)\]", ent); return ent.replace(m.group(0), f"{field}:[{set_last(m.group(1), val)}]")
    ent2 = rep("gtv", toApp(g("2027", kg), pais)); ent2 = rep("cb", toApp(g("2027", kb), pais), ent2); ent2 = rep("ca", toApp(g("2027", ka), pais), ent2)
    s = s[:i] + ent2 + s[j:]
# líneas nuevas (solo 2027 en LINES; el resto vive en Plan 2030 / Crecimiento)
he27 = toApp(g("2027", "Credito.he_orig"), "CO"); hec27 = toApp(g("2027", "Credito.he_cm"), "CO")
bm27 = toApp(g("2027", "Credito.mx_orig"), "MX"); bmc27 = toApp(g("2027", "Credito.mx_cm"), "MX")
NEW = (f" {{id:'homeeq',name:'Home Equity',pais:'CO',cap:'light',role:'prioridad',color:'#D95926',dashed:true,\n"
       f"  // CASO PLAN v2 (27-sep-2026): originar y vender a 4 meses; 2027 = piloto. 2028-2030 en la pestaña Plan 2030.\n"
       f"  gtv:[null,null,null,null,{he27:.2f}], cb:[null,null,null,null,{hec27:.2f}], ca:[null,null,null,null,{hec27:.2f}]}},\n"
       f" {{id:'brokermx',name:'Broker MX (HabiCredit)',pais:'MX',cap:'light',role:'margen',color:'#0B7285',dashed:true,\n"
       f"  // CASO PLAN v2: crédito bancario gestionado por HabiCredit en México desde 2027 (600 créditos → 6.000 en 2030).\n"
       f"  gtv:[null,null,null,null,{bm27:.2f}], cb:[null,null,null,null,{bmc27:.2f}], ca:[null,null,null,null,{bmc27:.2f}]}},\n")
i = s.index("{id:'vivnueva'"); j = s.index("},", i) + 2
s = s[:j] + "\n" + NEW.rstrip("\n") + s[j:]
s = s.replace("members:['habicredit','habicapital']", "members:['habicredit','habicapital','homeeq','brokermx']")
# la pestaña Crecimiento ya trae sus propias líneas extra: evitar duplicado
s = s.replace("const cnActive=()=>AGRUP()==='bloque'?BLOCKS:LINES.concat(CN_EXTRA);", "const cnActive=()=>AGRUP()==='bloque'?BLOCKS:LINES;")
s = s.replace("const cnG=(e,k)=>CN_YY[k]>=2027?cnPlan(e,k,'g'):(e.extra?null:G(e,CN_I[k]));", "const cnG=(e,k)=>CN_YY[k]>=2027?cnPlan(e,k,'g'):G(e,CN_I[k]);")
s = s.replace("const cnC=(e,k)=>CN_YY[k]>=2027?cnPlan(e,k,'c'):(e.extra?null:contrib(e,CN_I[k]));", "const cnC=(e,k)=>CN_YY[k]>=2027?cnPlan(e,k,'c'):contrib(e,CN_I[k]);")

# ============================ CAPA 2: bloques por capítulo ============================
f0 = lambda v: f"{v:,.0f}"; f1 = lambda v: f"{v:,.1f}"; pc = lambda a, b: f"{100*a/b:.1f}%" if b else "—"
def tbl(headers, rows):
    L = ' class="l"'
    h = "".join(f"<th{L if i == 0 else ''}>{x}</th>" for i, x in enumerate(headers))
    b = "".join("<tr" + (' class="tot"' if r[0].startswith("**") else "") + ">" + "".join(f"<td{L if i == 0 else ''}>{str(c).strip('*')}</td>" for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="tblscroll"><table class="p30tbl"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'
def card(title, sub, inner, note):
    return (f'<div class="tblcard" style="border:2px solid var(--bright)"><h2>Caso plan 2030 · {title} <span>{sub}</span></h2>{inner}'
            f'<div class="note"><b>Fuente:</b> Modelo 2030 v2, caso plan decidido el 27-sep-2026 (FX constante 3.100 / 17,0; MM después de intereses). {note}</div></div>')
def series(k): return [g(y, k) for y in Y]
def row(label, k, f=f1, tot=False): return [("**" if tot else "") + label] + [f(v) for v in series(k)]
def rowv(label, vals, f=f1, tot=False): return [("**" if tot else "") + label] + [f(v) for v in vals]
H = ["US$M"] + Y

blocks = {}
# --- Detalle por línea (sin jhead: aviso al inicio del pane)
blocks["det"] = ('<div class="note" style="background:#FFF6E5;border-left:4px solid var(--amber);padding:8px 12px;margin:12px 2px"><b>2027 = caso plan del Modelo 2030 v2 (27-sep-2026)</b>, ya no el 2027e de agosto: cada línea toma su GTV y contribución 2027 del modelo por drivers, convertidos a la tasa de esta pestaña. Aparecen dos líneas nuevas desde 2027: <b>Home Equity</b> (piloto, se vende a 4 meses) y <b>Broker MX</b>. 2028-2030 viven en las pestañas «Plan 2030» y «Crecimiento por negocio».</div>')
# --- Red Habi
red_rows = [row("GTV Inmo CO", "Red.co_gtv"), row("GTV Inmo MX", "Red.mx_gtv"), row("GTV Pulppo", "Red.pu_gtv"), row("GTV Vivienda Nueva (run-off)", "Red.vn_gtv"), row("GTV Red Habi", "Red.gtv", tot=True),
            rowv("Cierres Inmo CO", series("Red.co_cierres"), f0), rowv("Cierres Inmo MX", series("Red.mx_cierres"), f0), rowv("Cierres Pulppo", series("Red.pu_cierres"), f0),
            row("CM Inmo CO (sin attach)", "Red.co_cm"), row("CM Inmo MX", "Red.mx_cm"), row("CM Pulppo", "Red.pu_cm"), row("CM Vivienda Nueva", "Red.vn_cm"), row("CM Red sin attach", "Red.cm", tot=True),
            rowv("CM Red con el crédito que refiere (comparable con este capítulo)", series("Red.memo_cm_con_attach"), f1, True),
            rowv("Margen con attach / GTV", [100 * g(y, "Red.memo_cm_con_attach") / g(y, "Red.gtv") for y in Y], lambda v: f"{v:.2f}%")]
blocks["red"] = card("Red Habi", "cierres × ticket × take por canal · attach en Crédito", tbl(H, red_rows),
    "Drivers del caso plan: Inmo CO cierres +165% en 2027, +100%, +60%, +40% con franquicia 25→68% (take propio 2,13%, franquicia 0,92%); Inmo MX +220% en 2027 y +110%/año después (×30) con franquicia 30→65% y attach nuevo 100→200 pbs (no medido); Pulppo +10%/año y take 0,56→1,56%; <b>Vivienda Nueva en run-off −15%/año por decisión</b>. Los sliders de abajo son el motor de agosto (Colombia ×2/×2/60/40 y peso de Inmo MX 67%): siguen sirviendo para sensibilidades, pero las cifras oficiales son estas.")
# --- Crédito
cr_rows = [row("Originación HabiCredit CO (broker)", "Credito.hcr_orig", f0), row("Originación HabiCapital (×1,35 del plan deck)", "Credito.hcap_orig", f0), row("Originación Broker MX", "Credito.mx_orig", f0), row("Originación Home Equity (vendido a 4 meses)", "Credito.he_orig", f0),
           row("GTV crédito", "Credito.gtv", f0, True), rowv("Créditos originados", series("Credito.loans"), f0),
           row("CM HabiCredit CO", "Credito.hcr_cm"), row("CM HabiCapital (escalera: premio 5,5% + seguros 0,75% + servicing 0,3% − orig. 1,17%)", "Credito.hcap_cm"), row("CM Broker MX", "Credito.mx_cm"), row("CM Home Equity (premio 9,9% + seguros 1% + servicing 0,5% − costo 0,75%)", "Credito.he_cm"),
           row("CM crédito", "Credito.cm", tot=True), rowv("Take blended", [100 * g(y, "Credito.cm") / g(y, "Credito.gtv") for y in Y], lambda v: f"{v:.2f}%"),
           rowv("Libro administrado (HE vendido + HabiCapital titularizado)", [g(y, "Credito.he_libro_vendido") + g(y, "Credito.hcap_libro_admin") for y in Y], f0),
           rowv("% del mercado colombiano de titularización", [100 * g(y, "Capital.titul_pct") for y in Y], lambda v: f"{v:.0f}%"), rowv("Freno de capital", [100 * g(y, "Capital.freno") for y in Y], lambda v: f"{v:.0f}%")]
blocks["cred"] = card("Crédito", "HabiCredit, HabiCapital, Broker MX y Home Equity · originar, tener pocos meses, vender, administrar", tbl(H, cr_rows),
    "<b>Decisiones del 27-sep que cambian este capítulo:</b> Home Equity <u>no se retiene</u> (se vende a ~4 meses a un comprador que exige ~16%; piloto de ~300 créditos en 2027, penetración madura 15%, LTV 30%, base CRM); HabiCapital crece ×1,35 del plan deck con rotación de 1,5 meses y la misma escalera explícita; broker México desde 2027 (4.500 créditos en 2030); HabiCredit canal abierto +10%; una sola ronda de US$40M en 2027. El motor de sliders de abajo (Home Equity retenido, 12,21% nominal, adelantos) es el de agosto y queda como referencia; el techo de titularización pasa de 93% a 125% del mercado: vehículos propios obligatorios desde 2028.")
# --- Modelo 2030
m_rows = [row("GTV bruto", "Consolidado.gtv_bruto", f0, True), row("  Market Maker", "MM.gtv", f0), row("  Red Habi", "Red.gtv", f0), row("  Crédito", "Credito.gtv", f0), row("GTV neto (solape 30% sobre crédito de compra)", "Consolidado.gtv_neto", f0),
          row("CM after financing", "Consolidado.cm_after_fin", tot=True), row("  MM post intereses", "MM.cm"), rowv("  Red con attach", series("Red.memo_cm_con_attach")), rowv("  Crédito neto del attach", [g(y, "Credito.cm") - g(y, "Credito.co_attach_cm") for y in Y]), rowv("  Financieros corporativos", [-g(y, "Consolidado.fin_corp") for y in Y]),
          rowv("CM % del GTV bruto", [100 * g(y, "Consolidado.cm_after_fin") / g(y, "Consolidado.gtv_bruto") for y in Y], lambda v: f"{v:.2f}%"),
          row("OPEX de estructura", "OPEX.estructura"), row("OPEX de crédito (US$100/crédito + 0,3% del libro administrado)", "OPEX.cred_total"), row("OPEX total", "OPEX.total"),
          rowv("OPEX % del GTV bruto", [100 * g(y, "OPEX.total") / g(y, "Consolidado.gtv_bruto") for y in Y], lambda v: f"{v:.2f}%"),
          row("EBTDA", "Consolidado.ebtda", tot=True), row("Memo · EBITDA", "Consolidado.ebitda"), rowv("Impuestos (33% sobre EBTDA positivo)", series("Caja.impuestos"))]
blocks["m30"] = card("Modelo 2030 consolidado", "por drivers · reemplaza al modelo de agosto (3.341 / 111 / 66)", tbl(H, m_rows),
    "El modelo de agosto (abajo) sumaba las líneas a FX 3.175 con OPEX 35,7 y llegaba a GTV 3.341, CM 110,7 y EBTDA 65,7 en 2030; el caso plan llega a ~5.170 / ~201 / ~143 con OPEX 2027 de 41,2 (BLT vivo) más un OPEX de crédito que escala con el volumen. La tijera sigue siendo la tesis: el margen sube de 2,1% a 3,9% del GTV y el OPEX baja de 4,6% a 1,2%.")
# --- Caja
c_rows = [row("EBTDA", "Consolidado.ebtda"), rowv("Ronda", series("Capital.ronda")), rowv("Equity operativo requerido (stock)", series("Capital.eq_req")), rowv("Impuestos", series("Caja.impuestos")), row("Caja fin de año (simplificada)", "Caja.fin", tot=True),
          rowv("Freno de capital", [100 * g(y, "Capital.freno") for y in Y], lambda v: f"{v:.0f}%")]
blocks["caja"] = card("Caja", "anual, simplificada · ronda única de US$40M en 2027", tbl(H, c_rows),
    "En agosto este capítulo concluía que 2027 necesitaba US$32,7M de financiamiento nuevo; en el caso plan, con Home Equity y HabiCapital vendiendo cartera a los pocos meses, basta una ronda de 40 en 2027: 2027 cierra en −1,7 de EBTDA y la caja mínima es 44. La caja mensual de decisión sigue siendo la del Habi_Model_IB (CFO agent); esta es anual y no incluye capital de trabajo de MM más allá del equity en inventario.")
# --- Vista Junta
j_rows = [rowv("GTV Market Maker", series("MM.gtv"), f0), rowv("GTV Red Habi", series("Red.gtv"), f0), rowv("GTV Crédito y Capital", series("Credito.gtv"), f0),
          rowv("CM Market Maker (post int.)", series("MM.cm")), rowv("CM Red Habi (con attach)", series("Red.memo_cm_con_attach")), rowv("CM Crédito y Capital (neto attach)", [g(y, "Credito.cm") - g(y, "Credito.co_attach_cm") for y in Y]),
          rowv("Margen MM", [100 * g(y, "MM.cm") / g(y, "MM.gtv") for y in Y], lambda v: f"{v:.1f}%"), rowv("Margen Red", [100 * g(y, "Red.memo_cm_con_attach") / g(y, "Red.gtv") for y in Y], lambda v: f"{v:.2f}%"), rowv("Margen Crédito", [100 * (g(y, "Credito.cm") - g(y, "Credito.co_attach_cm")) / g(y, "Credito.gtv") for y in Y], lambda v: f"{v:.2f}%"),
          rowv("Peso de crédito en el CM", [100 * (g(y, "Credito.cm") - g(y, "Credito.co_attach_cm")) / g(y, "Consolidado.cm_after_fin") for y in Y], lambda v: f"{v:.0f}%")]
blocks["jun"] = card("bloques de junta hasta 2030", "Market Maker · Red Habi · Crédito y Capital", tbl(H, j_rows),
    "Las burbujas y el camino a rentabilidad de abajo llegan hasta 2027, que ahora es el 2027 del caso plan. En 2030 el crédito hace el 62% del margen; en 2026 Market Maker hacía el 86%. Ese cambio de naturaleza es el mensaje de junta.")
# --- Market Maker
mm_rows = [rowv("Casas vendidas CO", series("MM.co_casas"), f0), rowv("Casas vendidas MX", series("MM.mx_casas"), f0), row("GTV MM CO", "MM.co_gtv", f0), row("GTV MM MX", "MM.mx_gtv", f0),
           row("CM pre intereses CO", "MM.co_cm_pre"), row("CM pre intereses MX", "MM.mx_cm_pre"), rowv("Interés del warehouse (serie BLT)", [g(y, "MM.co_int") + g(y, "MM.mx_int") for y in Y]), row("CM post intereses MM", "MM.cm", tot=True),
           rowv("Margen post intereses / GTV", [100 * g(y, "MM.cm") / g(y, "MM.gtv") for y in Y], lambda v: f"{v:.1f}%")]
blocks["mm"] = card("Market Maker", "casas × ticket × margen · plano en 2027, +10%/año desde 2028", tbl(H, mm_rows),
    "Coincide con la tesis de este capítulo (cash cow, +10% desde 2028 se autofinancia). Cambios: interés del warehouse con la serie del BLT (CO 1,2% del GTV, MX 4,7→4,5%) en vez del tracker; margen pre intereses CO 12,6→14,0% y MX 10,6→12,0%; volumen 2027 plano a run-rate real (2.229 casas CO, 1.140 MX), no el del presupuesto.")
# --- Sensibilidad
blocks["sen"] = ('<div class="note" style="background:#F5F2FC;border-left:4px solid var(--bright);padding:8px 12px;margin:12px 2px"><b>Caso plan 2030:</b> las tablas de abajo usan como base el año activo del primer tab; el 2027 ya es el del caso plan. Para las sensibilidades del plan a 2030 (premio de venta, penetración de Home Equity, plan de HabiCapital, ronda) el modelo vivo es <b>Modelo_2030_v2.xlsx</b> (hoja Inputs) y sus escenarios en RESULTADOS.md.</div>')
# --- Volúmenes
v_rows = [rowv("Casas vendidas MM CO", series("MM.co_casas"), f0), rowv("Casas vendidas MM MX", series("MM.mx_casas"), f0), rowv("Cierres Inmo CO", series("Red.co_cierres"), f0), rowv("Cierres Inmo MX", series("Red.mx_cierres"), f0), rowv("Cierres Pulppo", series("Red.pu_cierres"), f0),
          rowv("Créditos HabiCredit CO", series("Credito.hcr_loans"), f0), rowv("Hipotecas HabiCapital", series("Credito.hcap_loans"), f0), rowv("Créditos Broker MX", series("Credito.mx_loans"), f0), rowv("Créditos Home Equity", series("Credito.he_loans"), f0), rowv("Créditos totales", series("Credito.loans"), f0, True)]
blocks["vol"] = card("volúmenes del caso plan", "transacciones por línea 2026-2030", tbl(["#"] + Y, v_rows),
    "Tickets del caso plan: MM CO US$61,6K, MM MX US$77,5K, Inmo CO US$70K, Inmo MX US$70,6K (1,2M MXN), Pulppo US$109K, HabiCredit US$62K (por confirmar: el memo de julio dice 259M COP), HabiCapital US$52-58K, Broker MX US$141K, Home Equity US$21,6K (30% de una casa de US$72K).")

# insertar cada bloque después del jhead de su pane
for pid, html in blocks.items():
    tag = f'<div id="pane-{pid}"'
    i = s.index(tag)
    if pid == "det":
        j = s.index(">", i) + 1
    else:
        jh = s.index('<div class="jhead">', i); j = s.index("</div>", jh) + len("</div>")
    s = s[:j] + "\n" + html + "\n" + s[j:]
# encabezado
s = s.replace("Nuevo (27-sep-2026): pestaña «Plan 2030» con el caso plan del Modelo 2030 v2 y las decisiones tomadas. Las proyecciones 2027-2030 de las demás pestañas son las de agosto.",
              "Actualizado 27-sep-2026 con el caso plan del Modelo 2030 v2: 2027 de todas las líneas = caso plan; cada capítulo trae su bloque «Caso plan 2030» con las cifras nuevas; los motores de sliders de Red Habi, Crédito, Modelo 2030 y Caja son los de agosto y quedan como referencia.")
open(SRC, "w", encoding="utf-8").write(s); shutil.copy(SRC, DESK)
print("capítulos ok", len(s), "bytes")
