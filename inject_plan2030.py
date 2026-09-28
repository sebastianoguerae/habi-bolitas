#!/usr/bin/env python3
"""Inyecta la pestaña «Plan 2030» al aplicativo de bolitas con el caso plan del Modelo 2030 v2.
Fuente: source/habi_bolitas_evolucion.html → escribe source/habi_bolitas_evolucion.html (backup .bak) y ~/Desktop/… para build.py"""
import json, os, re, shutil
SRC = os.path.expanduser("~/leon/habi-bolitas/source/habi_bolitas_evolucion.html")
PAY = os.path.expanduser("~/leon/habi-plan-2030/08_modelo_2030_v2/app_payload_plan2030.json")
DESK = os.path.expanduser("~/Desktop/habi_bolitas_evolucion.html")
s = open(SRC, encoding="utf-8").read()
if 'id="pane-p30"' in s:
    s = re.sub(r'<!-- P30 START -->.*?<!-- P30 END -->', '', s, flags=re.S)
    s = s.replace('<button class="tab" id="tab-p30" aria-selected="false">Plan 2030</button>\n', '')
    s = s.replace("p30:'pane-p30',", "").replace("p30:'tab-p30',", "").replace("  if(which==='p30')drawP30();\n", "")
shutil.copy(SRC, SRC + ".bak")
pay = json.load(open(PAY))

PANE = r'''<!-- P30 START -->
<style>
.p30kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-top:14px}
.p30k{background:#fff;border-radius:12px;padding:12px 14px;box-shadow:0 4px 18px rgba(75,26,139,.08)}
.p30k b{display:block;font-size:22px;font-weight:900;color:var(--pur)}.p30k small{color:var(--gray);font-size:10.5px;display:block;margin-top:2px}.p30k i{color:#8A8496;font-size:10px;font-style:normal}
.p30dec{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px}
.p30dec div{background:#fff;border-left:4px solid var(--bright);border-radius:0 10px 10px 0;padding:10px 12px;font-size:12px;line-height:1.5;box-shadow:0 4px 18px rgba(75,26,139,.06)}
.p30dec div b{color:var(--pur)}
.p30warn{background:#FFF6E5;border-left:4px solid var(--amber)}
.p30tbl td.neg{color:var(--red)}
</style>
<div id="pane-p30" style="display:none">
  <div class="jhead">
    <h2>Plan 2030 · caso plan del Modelo 2030 v2 <span style="font-size:11px;font-weight:600;color:#E4D7FA">· 27-sep-2026</span></h2>
    <p>Reemplaza a las proyecciones 2027-2030 de las otras pestañas. Construido por drivers (casas × ticket × margen, cierres × take por canal, originación × economía por fuente) con FX constante 3.100 / 17,0, MM después de intereses, GTV bruto y neto, y un módulo de capital que frena el crédito cuando falta equity. Las decisiones tomadas hoy están abajo; los supuestos que todavía no tienen dato, también. Modelo: <b>leon/habi-plan-2030/08_modelo_2030_v2/Modelo_2030_v2.xlsx</b>.</p>
  </div>
  <div class="p30kpis" id="p30kpis"></div>

  <div class="tblcard">
    <h2>1 · Decisiones tomadas por Sebastián Noguera <span>27-sep-2026</span></h2>
    <div class="p30dec" style="margin-top:10px">
      <div><b>Home Equity se origina para vender a ~4 meses.</b> El comprador de cartera exige ~16%: premio de venta 9,9% del principal. Producto eficiente en capital, no de balance. Habi retiene servicing (0,5%/año) y seguros (1% upfront).</div>
      <div><b>Home Equity arranca despacio, acelera en 2028 y se mantiene acotado.</b> Piloto de ~300 créditos en 2027; penetración madura 15% (no 25%): 6 mil créditos en 2028, 14 mil en 2029, 20 mil en 2030 (US$440M).</div>
      <div><b>Una sola ronda de US$40M en 2027.</b> Al vender la cartera de los dos productos a los pocos meses, la segunda ronda (160 en 2028) deja de ser necesaria: el freno de capital queda en 100% todos los años. Broker México llega a 4.500 créditos.</div>
      <div><b>HabiCapital crece ×1,35 del plan que vio BBVA</b> (808 de originación, ~14 mil hipotecas en 2030), con la misma escalera explícita que Home Equity: premio 5,5%, seguros 0,75%, servicing 0,3%/año, rotación 1,5 meses. Se bajó de ×2 en dos pasos para darle más peso a Red Habi.</div>
      <div><b>Vivienda Nueva no crece.</b> El negocio no interesa: run-off −15%/año (39 → 20 de GTV).</div>
      <div><b>Red Habi crece antes que el crédito.</b> En 2027 Inmo CO acelera a +165% y Inmo MX a +220% (luego +110%/año); Pulppo +10%. Red pasa de US$388M a US$2.170M de GTV y de 4,8 a ~79 de margen con attach en 2030.</div>
      <div><b>Meta 2030:</b> GTV consolidado ~5.000 bruto y margen de contribución después de financieros &gt; 200; crédito ~3.000 de GTV y &gt; 100 de margen.</div>
    </div>
  </div>

  <div class="tblcard">
    <h2>2 · Evolución por negocio <span>X = crecimiento del GTV · Y = margen de contribución % · tamaño = contribución US$M · anillo = año anterior</span></h2>
    <div class="controls" style="box-shadow:none;padding:10px 0 0;margin:0">
      <div class="yearrow"><span class="yearbig" id="p30yl">2027</span><button class="btn" id="p30play">▶ Play</button><input type="range" id="p30sl" min="2027" max="2030" step="1" value="2027"></div>
      <div class="filters" style="margin-top:8px;padding-top:8px"><div class="fgroup"><b>Escenario</b>
        <label><input type="radio" name="p30sc" value="plan" checked> Caso plan</label>
        <label><input type="radio" name="p30sc" value="base"> Base (defaults, sin ronda)</label></div></div>
    </div>
    <div class="tblscroll"><svg viewBox="0 0 960 470" id="p30svg"></svg></div>
    <div class="note" id="p30note"></div>
  </div>

  <div class="tblcard">
    <h2>3 · GTV y margen de contribución 2026-2030 <span>US$M · caso plan</span></h2>
    <div class="tblscroll"><table id="p30t1" class="p30tbl"></table></div>
  </div>

  <div class="tblcard">
    <h2>4 · Crédito por fuente <span>originación US$M · margen US$M · # créditos</span></h2>
    <div class="tblscroll"><table id="p30t2" class="p30tbl"></table></div>
    <div class="note">HabiCredit CO = canal abierto (+10%/año) + attach sobre MM e Inmo CO, margen 0,74% + 15 pbs de precio al banco. Broker MX desde 2027: 500 → 4.500 créditos. HabiCapital: ×1,35 del plan deck, escalera explícita (spread en tránsito + premio 5,5% + seguros 0,75% − costo de originación 1,17% + servicing 0,3% del libro administrado); el NPV 4,89% queda solo para valoración. Home Equity: base = casas vendidas + clientes HabiCredit + 5% de leads (134 mil hogares en 2030), penetración madura 15%, LTV 30% sobre casa de US$72K (ticket US$21,6K).</div>
  </div>

  <div class="tblcard">
    <h2>5 · Home Equity · economía por cada US$100 originados <span>tres modos; el plan usa "vender a 4 meses"</span></h2>
    <div class="tblscroll"><table class="p30tbl"><thead><tr><th class="l">Peldaño</th><th>Retenido 8 años</th><th>Vender a 4 meses (plan)</th><th>Broker puro</th></tr></thead><tbody>
      <tr><td class="l">Margen de interés / spread</td><td>4,3% anual sobre saldo (5,5% − 1,2% pérdida)</td><td>+1,4 (4 meses, neto de pérdida)</td><td>—</td></tr>
      <tr><td class="l">Premio de venta</td><td>—</td><td><b>+9,9</b> (cliente 19% vs comprador 16% × duración 3,3)</td><td>+2,0 (take)</td></tr>
      <tr><td class="l">Seguros upfront</td><td>no modelado</td><td>+1,0</td><td>—</td></tr>
      <tr><td class="l">Servicing retenido</td><td>incluido en el spread</td><td>+2,2 nominal (0,5%/año × vida 4,5)</td><td>—</td></tr>
      <tr><td class="l">Costo comercial</td><td>−0,75</td><td>−0,75</td><td>−0,75</td></tr>
      <tr class="tot"><td class="l">Total</td><td>~19 nominal · ~14 en VP</td><td><b>~13,8 · el 85% en el año 1</b></td><td>1,25</td></tr>
      <tr><td class="l">Capital por unidad</td><td>20 durante años</td><td>5 durante 4 meses</td><td>0</td></tr>
      <tr><td class="l">CM 2030 (penetración 15%)</td><td>~27 (con freno)</td><td><b>54,1</b></td><td>~5</td></tr>
    </tbody></table></div>
    <div class="note">El premio es el supuesto crítico en los dos productos: en Home Equity cada punto son ~4,4 US$M de margen en 2030; en HabiCapital, ~12. HabiCapital y Home Equity corren con la misma mecánica (originar, tener pocos meses, vender, administrar); difieren en producto, comprador (titularización vs venta bilateral) y premio.</div>
  </div>

  <div class="tblcard">
    <h2>6 · Qué tiene que ser verdad, y qué no está medido</h2>
    <div class="p30dec" style="margin-top:10px">
      <div class="p30warn"><b>Comprador de cartera de Home Equity al 16%</b> con forward flow y servicing retenido, sobre US$440M/año en 2030. Hoy no existe uno probado en Colombia. Sostiene ~53 de los 201 de margen.</div>
      <div class="p30warn"><b>HabiCapital ×1,35 = ~14 mil hipotecas en 2030, ~15% de la vivienda usada financiada en Colombia, y 125% del mercado anual de titularización.</b> Sin vehículos propios y ventas bilaterales de cartera el número no existe.</div>
      <div class="p30warn"><b>Inmo México ×30 en cuatro años</b> (467 → 13.800 cierres, +220% en 2027 y +110% después), Inmo CO +165% en 2027, y broker México de 100 a 4.500 créditos: es el supuesto de ejecución más exigente del caso.</div>
      <div class="p30warn"><b>Home Equity acotado:</b> 134 mil hogares × 15% = 20 mil créditos en 2030, tres veces HabiCredit hoy. Nadie ha medido el mercado de libre inversión con garantía; la primera cosecha de 2027 calibra conversión y pérdida.</div>
      <div class="p30warn"><b>Ticket de HabiCredit:</b> US$62K en el modelo; el memo de julio dice 259M COP (US$83K). Cambia el GTV de crédito en 30%.</div>
      <div class="p30warn"><b>2027 queda en −1,6 de EBTDA y la caja mínima es 45 en 2027-28</b> con la ronda de 40 adentro. El OPEX de crédito (US$100 por crédito + 0,3% del libro administrado) ya está contado.</div>
    </div>
  </div>

  <div class="tblcard">
    <h2>7 · Conciliación 2030 <span>este caso plan contra las versiones anteriores · US$M</span></h2>
    <div class="tblscroll"><table class="p30tbl"><thead><tr><th class="l">Versión</th><th>GTV bruto</th><th>CM after fin.</th><th>EBTDA</th><th>Ronda</th><th>Nota</th></tr></thead><tbody>
      <tr><td class="l"><b>Caso plan balanceado v2 (27-sep)</b></td><td><b>5.168</b></td><td><b>201</b></td><td><b>143</b></td><td>40 (2027)</td><td class="l">HabiCapital ×1,35 con escalera, Red acelerada desde 2027, broker MX 4,5k, HabiCredit +10%, HE 15% vendido a 4 meses, MX 4,5k, VN run-off, OPEX de crédito, impuestos en caja</td></tr>
      <tr><td class="l">Caso plan anterior (HE 25%, HabiCapital ×1)</td><td>4.809</td><td>202</td><td>141</td><td>40 (2027)</td><td class="l">Home Equity 34 mil créditos: volumen juzgado exagerado</td></tr>
      <tr><td class="l">Base v2 (defaults, sin ronda)</td><td>3.563</td><td>92</td><td>42</td><td>0</td><td class="l">HE retenido, freno de capital al 15%</td></tr>
      <tr><td class="l">Paquete v11 base (24-ago, BBVA)</td><td>3.758</td><td>150</td><td>96</td><td>0</td><td class="l">serie v7 = reparto del total, no drivers; financieros dentro de MM</td></tr>
      <tr><td class="l">Paquete v11 con ronda</td><td>4.607</td><td>188</td><td>133</td><td>20-40</td><td class="l">unlock +30% MM / +40% crédito</td></tr>
      <tr><td class="l">Este aplicativo, Modelo 2030 (16-ago)</td><td>3.341</td><td>111</td><td>66</td><td>0</td><td class="l">FX 3.175, OPEX 35,7, sumado desde las líneas</td></tr>
    </tbody></table></div>
  </div>
</div>
<script>
const P30=__PAYLOAD__;
const P30Y=[2026,2027,2028,2029,2030];
const p30g=(sc,y,k)=>P30[sc][String(y)][k];
const p30f0=v=>v.toLocaleString('en-US',{maximumFractionDigits:0});
const p30f1=v=>v.toLocaleString('en-US',{minimumFractionDigits:1,maximumFractionDigits:1});
const p30pct=(a,b)=>b?(100*a/b).toFixed(1)+'%':'—';
function p30biz(sc,y){
  const d=P30[sc][String(y)];
  const credOrigCompra=d['Credito.hcr_orig']+d['Credito.hcap_orig']+d['Credito.mx_orig'];
  const credCmCompra=d['Credito.hcr_cm']+d['Credito.hcap_cm']+d['Credito.mx_cm'];
  return [
   {id:'mm',name:'Market Maker',color:'#6B21C8',gtv:d['MM.gtv'],cm:d['MM.cm'],cap:1},
   {id:'red',name:'Red Habi',color:'#146B3A',gtv:d['Red.gtv'],cm:d['Red.memo_cm_con_attach'],cap:0},
   {id:'cred',name:'Crédito de compra',color:'#0E9DA8',gtv:credOrigCompra,cm:credCmCompra-d['Credito.co_attach_cm'],cap:1},
   {id:'he',name:'Home Equity',color:'#C43E7A',gtv:d['Credito.he_orig'],cm:d['Credito.he_cm'],cap:0}];
}
function p30kpis(){
  const sc=document.querySelector('input[name=p30sc]:checked').value; const d=P30[sc]['2030'], d6=P30[sc]['2026'];
  const items=[[p30f0(d['Consolidado.gtv_bruto']),'GTV bruto 2030','neto '+p30f0(d['Consolidado.gtv_neto'])],[p30f1(d['Consolidado.cm_after_fin']),'CM after financing 2030',p30pct(d['Consolidado.cm_after_fin'],d['Consolidado.gtv_bruto'])+' del bruto'],
    [p30f1(d['Consolidado.ebtda']),'EBTDA 2030','2027: '+p30f1(P30[sc]['2027']['Consolidado.ebtda'])],[p30f0(d['Credito.gtv']),'GTV crédito 2030','CM '+p30f1(d['Credito.cm'])],
    [p30f0(d['Credito.he_orig']),'Home Equity originación 2030','CM '+p30f1(d['Credito.he_cm'])+' · '+p30f0(d['Credito.he_loans'])+' créditos'],[p30f1(d['Caja.fin']),'Caja fin 2030','mín. '+p30f1(Math.min(...P30Y.slice(1).map(y=>p30g(sc,y,'Caja.fin'))))],
    [(100*d['Capital.freno']).toFixed(0)+'%','Freno de capital 2030','titularización '+(100*d['Capital.titul_pct']).toFixed(0)+'% del mercado CO'],[p30f1(d['OPEX.total']),'OPEX 2030','de los cuales crédito '+p30f1(d['OPEX.cred_total'])]];
  document.getElementById('p30kpis').innerHTML=items.map(([v,l,s])=>`<div class="p30k"><b>${v}</b><small>${l}</small><i>${s}</i></div>`).join('');
}
function p30draw(){
  const sc=document.querySelector('input[name=p30sc]:checked').value; const y=+document.getElementById('p30sl').value;
  document.getElementById('p30yl').textContent=y;
  const W=960,H=470,L=80,R=30,T=30,B=50,pw=W-L-R,ph=H-T-B; const GX0=-10,GX1=110,MY0=0,MY1=16;
  const gx=g=>L+(Math.max(GX0,Math.min(GX1,g))-GX0)/(GX1-GX0)*pw, gy=m=>T+ph-(Math.max(MY0,Math.min(MY1,m))-MY0)/(MY1-MY0)*ph;
  let s='';
  for(let v=0;v<=MY1;v+=2){s+=`<line x1="${L}" x2="${W-R}" y1="${gy(v)}" y2="${gy(v)}" stroke="#EDE9F5"/><text x="${L-8}" y="${gy(v)+4}" text-anchor="end" font-size="10" fill="#8A8496">${v}%</text>`;}
  for(let g=0;g<=GX1;g+=20){s+=`<line y1="${T}" y2="${T+ph}" x1="${gx(g)}" x2="${gx(g)}" stroke="#EDE9F5"/><text y="${T+ph+16}" x="${gx(g)}" text-anchor="middle" font-size="10" fill="#8A8496">+${g}%</text>`;}
  s+=`<line x1="${gx(0)}" x2="${gx(0)}" y1="${T}" y2="${T+ph}" stroke="#B8B2CC"/><text x="${(L+W-R)/2}" y="${H-8}" text-anchor="middle" font-size="11" font-weight="800" fill="#4B1A8B">CRECIMIENTO DEL GTV (YoY) →</text><text transform="rotate(-90 18 ${T+ph/2})" x="18" y="${T+ph/2}" text-anchor="middle" font-size="11" font-weight="800" fill="#4B1A8B">MARGEN DE CONTRIBUCIÓN % GTV →</text>`;
  const cur=p30biz(sc,y), prev=p30biz(sc,y-1);
  cur.forEach((b,i)=>{const p=prev[i]; const gr=p.gtv?100*(b.gtv/p.gtv-1):0, m=b.gtv?100*b.cm/b.gtv:0, pm=p.gtv?100*p.cm/p.gtv:0, pgr=0;
    const r=Math.max(6,Math.sqrt(Math.max(b.cm,0.2))*7.5);
    const pgrv=(y-1>2026)?(()=>{const pp=p30biz(sc,y-2)[i];return pp.gtv?100*(p.gtv/pp.gtv-1):0;})():null;
    if(pgrv!==null){s+=`<circle cx="${gx(pgrv)}" cy="${gy(pm)}" r="5" fill="none" stroke="${b.color}" stroke-dasharray="2 2" opacity=".6"/><line x1="${gx(pgrv)}" y1="${gy(pm)}" x2="${gx(gr)}" y2="${gy(m)}" stroke="${b.color}" stroke-width="1.5" opacity=".6"/>`;}
    s+=`<circle cx="${gx(gr)}" cy="${gy(m)}" r="${r}" fill="${b.color}" opacity=".82" ${b.cap?'stroke="#8A6608" stroke-width="3" stroke-dasharray="6 4"':'stroke="#fff" stroke-width="1.5"'}><title>${b.name} ${y}: GTV ${p30f0(b.gtv)} · CM ${p30f1(b.cm)} · ${m.toFixed(1)}% · crec ${gr.toFixed(0)}%</title></circle><text x="${gx(gr)}" y="${Math.max(T+12,gy(m)-r-5)}" text-anchor="middle" font-size="10" font-weight="800" fill="#191919">${b.name} · $${p30f1(b.cm)}M</text>`;});
  document.getElementById('p30svg').innerHTML=s;
  const d=P30[sc][String(y)];
  document.getElementById('p30note').innerHTML=`<b>${y} · ${sc==='plan'?'caso plan':'base'}:</b> GTV bruto ${p30f0(d['Consolidado.gtv_bruto'])} (neto ${p30f0(d['Consolidado.gtv_neto'])}) · CM after financing ${p30f1(d['Consolidado.cm_after_fin'])} (${p30pct(d['Consolidado.cm_after_fin'],d['Consolidado.gtv_bruto'])}) · EBTDA ${p30f1(d['Consolidado.ebtda'])} · caja ${p30f1(d['Caja.fin'])} · freno ${(100*d['Capital.freno']).toFixed(0)}%. Anillo dorado = capital-intensivo (MM y crédito de compra). Crédito de compra = HabiCredit CO + HabiCapital + broker MX, neto del attach que ya cuenta Red Habi.`;
}
function p30tables(){
  const sc='plan'; const th=`<thead><tr><th class="l">US$M</th>${P30Y.map(y=>`<th>${y}</th>`).join('')}</tr></thead>`;
  const rows=[['GTV bruto','Consolidado.gtv_bruto',0,1],['  Market Maker','MM.gtv',0],['  Red Habi (Inmo CO + Inmo MX + Pulppo + VN)','Red.gtv',0],['  Crédito','Credito.gtv',0],['GTV neto (solape 30% sobre crédito de compra)','Consolidado.gtv_neto',0],
    ['CM after financing','Consolidado.cm_after_fin',1,1],['  Market Maker (post intereses)','MM.cm',1],['  Red Habi (con attach de crédito)','Red.memo_cm_con_attach',1],['  Crédito (neto del attach)',null,1],['  Financieros corporativos','Consolidado.fin_corp',1,0,-1],
    ['CM % del GTV bruto',null,'pct'],['OPEX estructura','OPEX.estructura',1],['OPEX de crédito (escala con volumen)','OPEX.cred_total',1],['EBTDA','Consolidado.ebtda',1,1],['Caja fin de año','Caja.fin',1],['Freno de capital',null,'freno'],['% mercado titularización CO',null,'titul']];
  let b='';
  rows.forEach(([lab,k,dec,tot,sign])=>{const cells=P30Y.map(y=>{const d=P30[sc][String(y)];let v;
    if(lab.startsWith('  Crédito (neto'))v=d['Credito.cm']-d['Credito.co_attach_cm'];else if(dec==='pct')v=100*d['Consolidado.cm_after_fin']/d['Consolidado.gtv_bruto'];else if(dec==='freno')v=100*d['Capital.freno'];else if(dec==='titul')v=100*d['Capital.titul_pct'];else v=d[k]*(sign||1);
    const txt=(dec==='pct'||dec==='freno'||dec==='titul')?v.toFixed(dec==='pct'?2:0)+'%':(dec===1?p30f1(v):p30f0(v));return `<td class="${v<0?'neg':''}">${txt}</td>`;}).join('');
    b+=`<tr class="${tot?'tot':''}"><td class="l">${lab}</td>${cells}</tr>`;});
  document.getElementById('p30t1').innerHTML=th+'<tbody>'+b+'</tbody>';
  const r2=[['HabiCredit CO · originación','Credito.hcr_orig',0],['HabiCredit CO · margen','Credito.hcr_cm',1],['HabiCredit CO · créditos','Credito.hcr_loans',0],['HabiCapital · originación','Credito.hcap_orig',0],['HabiCapital · margen contable','Credito.hcap_cm',1],['HabiCapital · créditos','Credito.hcap_loans',0],['Broker MX · originación','Credito.mx_orig',0],['Broker MX · margen','Credito.mx_cm',1],['Broker MX · créditos','Credito.mx_loans',0],['Home Equity · originación','Credito.he_orig',0],['Home Equity · margen','Credito.he_cm',1],['Home Equity · créditos','Credito.he_loans',0],['Home Equity · libro vendido que Habi administra','Credito.he_libro_vendido',0],['TOTAL crédito · originación','Credito.gtv',0,1],['TOTAL crédito · margen','Credito.cm',1,1],['TOTAL crédito · take',null,'pct'],['TOTAL créditos','Credito.loans',0,1]];
  let c='';
  r2.forEach(([lab,k,dec,tot])=>{const cells=P30Y.map(y=>{const d=P30[sc][String(y)];const v=dec==='pct'?100*d['Credito.cm']/d['Credito.gtv']:d[k];return `<td>${dec==='pct'?v.toFixed(2)+'%':(dec===1?p30f1(v):p30f0(v))}</td>`;}).join('');c+=`<tr class="${tot?'tot':''}"><td class="l">${lab}</td>${cells}</tr>`;});
  document.getElementById('p30t2').innerHTML=th+'<tbody>'+c+'</tbody>';
}
let p30playing=false,p30timer=null;
function drawP30(){p30kpis();p30draw();p30tables();}
document.getElementById('tab-p30').addEventListener('click',()=>setTab3('p30'));
document.getElementById('p30sl').addEventListener('input',p30draw);
document.querySelectorAll('input[name=p30sc]').forEach(el=>el.addEventListener('change',()=>{p30kpis();p30draw();}));
document.getElementById('p30play').addEventListener('click',function(){const sl=document.getElementById('p30sl');if(p30playing){clearInterval(p30timer);p30playing=false;this.textContent='▶ Play';return;}p30playing=true;this.textContent='⏸ Pausa';sl.value=2027;p30draw();p30timer=setInterval(()=>{if(+sl.value>=2030){clearInterval(p30timer);p30playing=false;document.getElementById('p30play').textContent='▶ Play';return;}sl.value=+sl.value+1;p30draw();},1100);});
</script>
<!-- P30 END -->
'''.replace("__PAYLOAD__", json.dumps({"plan": pay["plan"], "base": pay["base"]}, ensure_ascii=False))

# 1) botón de pestaña (primera posición, para que se vea)
s = s.replace('<button class="tab" id="tab-det" aria-selected="true">Detalle por línea</button>',
              '<button class="tab" id="tab-p30" aria-selected="false">Plan 2030</button>\n  <button class="tab" id="tab-det" aria-selected="true">Detalle por línea</button>')
# 2) pane antes del tooltip
s = s.replace('<div id="pane-vol" style="display:none">', PANE + '\n<div id="pane-vol" style="display:none">', 1)
# 3) setTab3
s = s.replace("const P={det:'pane-det',", "const P={p30:'pane-p30',det:'pane-det',")
s = s.replace("const T={det:'tab-det',", "const T={p30:'tab-p30',det:'tab-det',")
s = s.replace("  if(which==='jun')renderJunta();", "  if(which==='p30')drawP30();\n  if(which==='jun')renderJunta();")

# ===================== PESTAÑA «CRECIMIENTO POR NEGOCIO» HASTA 2030 =====================
i0 = s.index("// ================= PESTAÑA: CRECIMIENTO POR NEGOCIO"); i1 = s.index("function cnChks(){"); i1 = s.index("}\n", s.index("box.querySelectorAll('.cnfe')", i1)) + 2
blk = s[i0:i1]
blk = blk.replace("const CN_YY=[2024,2025,2026,2027];", """const CN_YY=[2024,2025,2026,2027,2028,2029,2030]; const CN_N=CN_YY.length, CN_LAST=CN_N-1;
// 2027-2030 salen del Modelo 2030 v2 (caso plan balanceado, payload P30). Las líneas nuevas solo existen aquí.
const CN_EXTRA=[{id:'homeeq',name:'Home Equity',pais:'CO',cap:'light',role:'prioridad',color:'#D95926',extra:true},{id:'brokermx',name:'Broker MX (HabiCredit)',pais:'MX',cap:'light',role:'margen',color:'#0B7285',extra:true}];
const CN_MAP={mmco:['MM.co_gtv','MM.co_cm','MM.co_cm_pre','CO'],mmmx:['MM.mx_gtv','MM.mx_cm','MM.mx_cm_pre','MX'],inmoco:['Red.co_gtv','Red.co_cm',null,'CO'],inmomx:['Red.mx_gtv','Red.mx_cm',null,'MX'],
  habicredit:['Credito.hcr_orig','Credito.hcr_cm',null,'CO'],pulppo:['Red.pu_gtv','Red.pu_cm',null,'MX'],habicapital:['Credito.hcap_orig','Credito.hcap_cm',null,'CO'],vivnueva:['Red.vn_gtv','Red.vn_cm',null,'MX'],
  homeeq:['Credito.he_orig','Credito.he_cm',null,'CO'],brokermx:['Credito.mx_orig','Credito.mx_cm',null,'MX']};
const CN_BLOCK_MEMBERS={bmm:['mmco','mmmx'],bcred:['habicredit','habicapital','homeeq','brokermx'],binmo:['inmoco','inmomx','pulppo'],bvn:['vivnueva']};
function cnFxDisp(p,y){ if(!fxVar()) return FXCONST[p]; const r=FX[p]&&FX[p][y]; return r||(p==='CO'?3175:17.30); }
function cnPlanLine(id,y,key){ const m=CN_MAP[id]; if(!m) return null; const d=P30.plan[String(y)]; if(!d) return null;
  const k=key==='g'?m[0]:((document.getElementById('postfin').checked||!m[2])?m[1]:m[2]); const v=d[k]; if(v==null) return null;
  const loc=m[3]==='CO'?v*3100:v*17; return loc/cnFxDisp(m[3],y); }
function cnPlan(e,k,key){ const y=CN_YY[k];
  if(e.members||CN_BLOCK_MEMBERS[e.id]){ const ids=CN_BLOCK_MEMBERS[e.id]||e.members; let t=null;
    ids.forEach(id=>{ const m=byId[id]||CN_EXTRA.find(x=>x.id===id); if(!m||!memberOk(m)) return; const v=cnPlanLine(id,y,key); if(v!=null) t=(t||0)+v; }); return t; }
  return cnPlanLine(e.id,y,key); }""")
blk = blk.replace("function cnReset(){ CN_SEL={}; ACTIVE().forEach(e=>CN_SEL[e.id]=true); }\nfunction cnAct(){ return ACTIVE().filter(e=>cnOk(e)&&CN_SEL[e.id]); }",
 "const cnActive=()=>AGRUP()==='bloque'?BLOCKS:LINES.concat(CN_EXTRA);\nfunction cnReset(){ CN_SEL={}; cnActive().forEach(e=>CN_SEL[e.id]=true); }\nfunction cnAct(){ return cnActive().filter(e=>cnOk(e)&&CN_SEL[e.id]); }")
blk = blk.replace("const cnG=(e,k)=>G(e,CN_I[k]);\nconst cnC=(e,k)=>contrib(e,CN_I[k]);",
 "const cnG=(e,k)=>CN_YY[k]>=2027?cnPlan(e,k,'g'):(e.extra?null:G(e,CN_I[k]));\nconst cnC=(e,k)=>CN_YY[k]>=2027?cnPlan(e,k,'c'):(e.extra?null:contrib(e,CN_I[k]));")
blk = blk.replace("const W=262,GH=68,LH=54,PAD=30,GAP=20;", "const W=300,GH=68,LH=54,PAD=30,GAP=20;")
blk = blk.replace("const bw=26, slot=(W-PAD-6)/4, bx=k=>PAD+slot*k+slot/2;", "const slot=(W-PAD-6)/CN_N, bw=Math.min(24,slot*0.62), bx=k=>PAD+slot*k+slot/2;")
blk = blk.replace("${y===2027?'27e':String(y).slice(2)}", "${String(y).slice(2)}${y>=2027?'p':''}")
blk = blk.replace("const cg=cnCagr(g[0],g[3],3), dp=(p[0]!=null&&p[3]!=null)?p[3]-p[0]:null;", "const cg=cnCagr(g[0],g[CN_LAST],CN_LAST), dp=(p[0]!=null&&p[CN_LAST]!=null)?p[CN_LAST]-p[0]:null;")
blk = blk.replace("$${cnF(g[3])}M de GTV en 2027e", "$${cnF(g[CN_LAST])}M de GTV en 2030p")
blk = blk.replace("CAGR GTV 24-27", "CAGR GTV 24-30").replace("Margen 2027e</div><div class=\"v\" style=\"color:${e.color}\">${p[3]==null?'n/d':p[3].toFixed(2)+'%'}", "Margen 2030p</div><div class=\"v\" style=\"color:${e.color}\">${p[CN_LAST]==null?'n/d':p[CN_LAST].toFixed(2)+'%'}")
blk = blk.replace("const slot=(X1-X0)/4, bw=Math.min(120,slot*0.5);", "const slot=(X1-X0)/CN_N, bw=Math.min(120,slot*0.5);")
blk = blk.replace("const slot=(X1-X0)/4, sx=k=>X0+slot*k+slot/2;", "const slot=(X1-X0)/CN_N, sx=k=>X0+slot*k+slot/2;")
blk = blk.replace("${y}${y===2027?'e':''}", "${y}${y>=2027?'p':''}")
blk = blk.replace("+`<th>YoY 25</th><th>YoY 26</th><th>YoY 27e</th><th>CAGR 24-27</th></tr></thead><tbody>`;", "+CN_YY.slice(1).map(y=>`<th>YoY ${String(y).slice(2)}${y>=2027?'p':''}</th>`).join('')+`<th>CAGR 24-30</th></tr></thead><tbody>`;")
blk = blk.replace("const row=(name,color,v,cls)=>{const c=cnCagr(v[0],v[3],3);", "const row=(name,color,v,cls)=>{const c=cnCagr(v[0],v[CN_LAST],CN_LAST);")
blk = blk.replace("+cnPc(cnYoY(v[0],v[1]))+cnPc(cnYoY(v[1],v[2]))+cnPc(cnYoY(v[2],v[3]))", "+v.slice(1).map((x,i)=>cnPc(cnYoY(v[i],x))).join('')")
blk = blk.replace("<th>Δ 2024 → 2027e</th>", "<th>Δ 2024 → 2030p</th>")
blk = blk.replace("const row=(n,color,p,cls)=>{const d=(p[0]!=null&&p[3]!=null)?p[3]-p[0]:null;", "const row=(n,color,p,cls)=>{const d=(p[0]!=null&&p[CN_LAST]!=null)?p[CN_LAST]-p[0]:null;")
blk = blk.replace("const g0=E.map(e=>cnG(e,0)||0), g3=E.map(e=>cnG(e,3)||0);", "const g0=E.map(e=>cnG(e,0)||0), g3=E.map(e=>cnG(e,CN_LAST)||0);")
blk = blk.replace("const m3=E.map((e,i)=>g3[i]?(cnC(e,3)||0)/g3[i]*100:0);", "const m3=E.map((e,i)=>g3[i]?(cnC(e,CN_LAST)||0)/g3[i]*100:0);")
blk = blk.replace("'Sin base de 2024 o de 2027e en la selección", "'Sin base de 2024 o de 2030p en la selección").replace("['Margen 2027e',p3.toFixed(2)+'%','llegada']", "['Margen 2030p',p3.toFixed(2)+'%','llegada']")
blk = blk.replace("<th>% del GTV 2027e</th><th>% del margen 2027e</th>", "<th>% del GTV 2030p</th><th>% del margen 2030p</th>").replace("`En 2027e ${E[bi].name} hace", "`En 2030p ${E[bi].name} hace")
blk = blk.replace("box.innerHTML=ACTIVE().map(e=>", "box.innerHTML=cnActive().map(e=>")
blk = blk.replace("document.getElementById('cnnote').innerHTML=\n    `<b>Fuente y método.</b>", "document.getElementById('cnnote').innerHTML=\n    `<b>2027p-2030p = caso plan balanceado del Modelo 2030 v2 (27-sep-2026)</b>, por línea de negocio y convertido a la tasa de esta pestaña; reemplaza al 2027e de agosto. Home Equity y Broker MX son líneas nuevas que solo existen desde 2027. Los bloques suman sus líneas incluyendo las nuevas. `\n   +`<b>Fuente y método (2024-2026).</b>")
assert "CN_EXTRA" in blk and "cnPlanLine" in blk and "CN_LAST" in blk
s = s[:i0] + blk + s[i1:]
s = s.replace("<h2>Crecimiento por negocio · GTV y margen de contribución 2024-2027e</h2>", "<h2>Crecimiento por negocio · GTV y margen de contribución 2024-2030 <span style=\"font-size:11px;font-weight:600;color:#E4D7FA\">· 2027-2030 = caso plan v2</span></h2>")
s = s.replace(".cngrid{", ".cngrid{grid-template-columns:repeat(auto-fill,minmax(300px,1fr));", 1) if ".cngrid{" in s else s

# 4) header: aviso
s = s.replace('<h1>Habi — Evolución por negocio · tamaño = margen de contribución</h1>',
              '<h1>Habi — Evolución por negocio · tamaño = margen de contribución</h1>\n  <p style="margin-top:4px;font-size:12px;color:#FFD166;font-weight:700">Nuevo (27-sep-2026): pestaña «Plan 2030» con el caso plan del Modelo 2030 v2 y las decisiones tomadas. Las proyecciones 2027-2030 de las demás pestañas son las de agosto.</p>')
assert 'id="pane-p30"' in s and "p30:'pane-p30'" in s and "drawP30" in s
open(SRC, "w", encoding="utf-8").write(s); shutil.copy(SRC, DESK)
print("ok", len(s), "bytes")
