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
      <div><b>Home Equity arranca despacio y acelera en 2028.</b> Piloto de ~450 créditos (US$10M) en 2027 para medir pérdida y conversión; 10 mil créditos en 2028, 24 mil en 2029, 34 mil en 2030.</div>
      <div><b>Una sola ronda de US$40M en 2027.</b> Al vender Home Equity la segunda ronda (160 en 2028) deja de ser necesaria: el freno de capital queda en 100% todos los años.</div>
      <div><b>HabiCapital = el plan que ya vio BBVA</b> (599 de originación en 2030), sin adelanto de seguros/servicing, rotando la cartera en 1,5 meses.</div>
      <div><b>Vivienda Nueva no crece.</b> El negocio no interesa: run-off −15%/año (39 → 20 de GTV).</div>
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
    <div class="note">HabiCredit CO = canal abierto (+15%/año) + attach sobre MM e Inmo CO, margen 0,74% + 15 pbs de precio al banco. Broker MX desde 2027: 600 → 6.000 créditos. HabiCapital: plan deck, margen contable 1,9% → 5,6% del monto (NPV 4,89% solo para valoración). Home Equity: base = casas vendidas + clientes HabiCredit + 5% de leads (134 mil hogares en 2030), penetración madura 25%, LTV 30% sobre casa de US$72K (ticket US$21,6K).</div>
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
      <tr><td class="l">CM 2030 con la misma base</td><td>44,5 (freno 81%)</td><td><b>90,1</b></td><td>7,9</td></tr>
    </tbody></table></div>
    <div class="note">El premio es el supuesto crítico: cada punto son ~7 US$M de margen en 2030. Con comprador al 17% (premio 6,6%) el margen de Home Equity 2030 baja a 68; al 18% (3,3%) a 44, lo mismo que retener pero sin capital.</div>
  </div>

  <div class="tblcard">
    <h2>6 · Qué tiene que ser verdad, y qué no está medido</h2>
    <div class="p30dec" style="margin-top:10px">
      <div class="p30warn"><b>Comprador de cartera de Home Equity al 16%</b> con forward flow y servicing retenido, sobre US$730M/año en 2030. Hoy no existe uno probado en Colombia. Sostiene 90 de los 201 de margen.</div>
      <div class="p30warn"><b>Base y penetración de Home Equity:</b> 134 mil hogares y 25% anual = 34 mil créditos en 2030, cinco veces HabiCredit hoy. Nadie ha medido el mercado de libre inversión con garantía.</div>
      <div class="p30warn"><b>Inmo México ×16 en cuatro años</b> (467 → 7.500 cierres) y broker México de 100 a 6 mil créditos: cero años de evidencia de esa pendiente.</div>
      <div class="p30warn"><b>HabiCapital coloca el 93% del mercado colombiano de titularización en 2030:</b> vehículos propios (universalidades, patrimonios con emisión) desde 2028 o el número no existe.</div>
      <div class="p30warn"><b>Ticket de HabiCredit:</b> US$62K en el modelo; el memo de julio dice 259M COP (US$83K). Cambia el GTV de crédito en 30%.</div>
      <div class="p30warn"><b>2027 sigue en −8 de EBTDA y 2028 es el año apretado de caja</b> (32 con la ronda de 40 adentro). El OPEX de crédito (US$100 por crédito + 0,3% del libro administrado) ya está contado: 14 en 2030.</div>
    </div>
  </div>

  <div class="tblcard">
    <h2>7 · Conciliación 2030 <span>este caso plan contra las versiones anteriores · US$M</span></h2>
    <div class="tblscroll"><table class="p30tbl"><thead><tr><th class="l">Versión</th><th>GTV bruto</th><th>CM after fin.</th><th>EBTDA</th><th>Ronda</th><th>Nota</th></tr></thead><tbody>
      <tr><td class="l"><b>Caso plan v2 (27-sep)</b></td><td><b>4.809</b></td><td><b>202</b></td><td><b>141</b></td><td>40 (2027)</td><td class="l">HE vendido a 4 meses, VN run-off, OPEX de crédito, impuestos en caja</td></tr>
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
  const W=960,H=470,L=80,R=30,T=30,B=50,pw=W-L-R,ph=H-T-B; const GX0=-10,GX1=110,MY0=0,MY1=14;
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
    s+=`<circle cx="${gx(gr)}" cy="${gy(m)}" r="${r}" fill="${b.color}" opacity=".82" ${b.cap?'stroke="#8A6608" stroke-width="3" stroke-dasharray="6 4"':'stroke="#fff" stroke-width="1.5"'}><title>${b.name} ${y}: GTV ${p30f0(b.gtv)} · CM ${p30f1(b.cm)} · ${m.toFixed(1)}% · crec ${gr.toFixed(0)}%</title></circle><text x="${gx(gr)}" y="${gy(m)-r-5}" text-anchor="middle" font-size="10" font-weight="800" fill="#191919">${b.name} · $${p30f1(b.cm)}M</text>`;});
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
# 4) header: aviso
s = s.replace('<h1>Habi — Evolución por negocio · tamaño = margen de contribución</h1>',
              '<h1>Habi — Evolución por negocio · tamaño = margen de contribución</h1>\n  <p style="margin-top:4px;font-size:12px;color:#FFD166;font-weight:700">Nuevo (27-sep-2026): pestaña «Plan 2030» con el caso plan del Modelo 2030 v2 y las decisiones tomadas. Las proyecciones 2027-2030 de las demás pestañas son las de agosto.</p>')
assert 'id="pane-p30"' in s and "p30:'pane-p30'" in s and "drawP30" in s
open(SRC, "w", encoding="utf-8").write(s); shutil.copy(SRC, DESK)
print("ok", len(s), "bytes")
