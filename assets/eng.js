/* Domathcalculator - unit converter + engineering tools */
(function(){
var f=function(x){return isFinite(x)?String(parseFloat(x.toPrecision(10))):'undefined'};
var U={Length:{m:1,km:1000,cm:.01,mm:.001,'µm':1e-6,mile:1609.344,yard:.9144,ft:.3048,inch:.0254,'nautical mile':1852},
Mass:{kg:1,g:.001,mg:1e-6,tonne:1000,lb:.45359237,oz:.028349523125},
Area:{'m²':1,'km²':1e6,'cm²':1e-4,'mm²':1e-6,hectare:1e4,acre:4046.8564224,'ft²':.09290304,'in²':6.4516e-4},
Volume:{'m³':1,litre:.001,mL:1e-6,'US gallon':.003785411784,'ft³':.028316846592,'in³':1.6387064e-5},
Time:{s:1,ms:.001,min:60,hour:3600,day:86400,week:604800},
Speed:{'m/s':1,'km/h':1/3.6,mph:.44704,knot:.514444444,'ft/s':.3048},
Pressure:{Pa:1,kPa:1e3,MPa:1e6,bar:1e5,atm:101325,psi:6894.757293168,mmHg:133.322387415},
Energy:{J:1,kJ:1e3,cal:4.184,kcal:4184,Wh:3600,kWh:3.6e6,BTU:1055.05585262,eV:1.602176634e-19,'ft·lbf':1.3558179483314},
Power:{W:1,kW:1e3,MW:1e6,hp:745.69987158227,'BTU/h':.29307107},
Force:{N:1,kN:1e3,lbf:4.4482216152605,kgf:9.80665,dyne:1e-5},
Angle:{degree:1,radian:180/Math.PI,gradian:.9,turn:360},
Data:{bit:1,byte:8,KB:8e3,MB:8e6,GB:8e9,TB:8e12}};
var T={'°C':[function(c){return c},function(c){return c}],'°F':[function(x){return(x-32)*5/9},function(c){return c*9/5+32}],
'K':[function(k){return k-273.15},function(c){return c+273.15}],'°R':[function(r){return(r-491.67)*5/9},function(c){return c*9/5+491.67}]};
var el=document.getElementById('conv');
if(el){
var cats=Object.keys(U).concat('Temperature');
function units(c){return Object.keys(c==='Temperature'?T:U[c])}
function toB(c,u,v){return c==='Temperature'?T[u][0](v):v*U[c][u]}
function fromB(c,u,b){return c==='Temperature'?T[u][1](b):b/U[c][u]}
function opts(a,sel){return a.map(function(x){return'<option'+(x===sel?' selected':'')+'>'+x+'</option>'}).join('')}
el.innerHTML='<div class="g"><label>Category<select id="vc">'+opts(cats,'Length')+'</select></label><label>Value<input id="vv" type="number" value="1" step="any"></label><label>From<select id="vf"></select></label><label>To<select id="vt"></select></label></div><div class="big" id="vr"></div><button class="btn" id="vs" type="button">Swap units</button><div class="sc"><table id="vtb"></table></div>';
var $=function(i){return document.getElementById(i)};
function fill(){var u=units($('vc').value);$('vf').innerHTML=opts(u,u[0]);$('vt').innerHTML=opts(u,u[1]||u[0]);run()}
function run(){var c=$('vc').value,v=parseFloat($('vv').value),a=$('vf').value,b=$('vt').value;
if(isNaN(v)){$('vr').textContent='Enter a number';$('vtb').innerHTML='';return}
var base=toB(c,a,v);$('vr').textContent=f(v)+' '+a+' = '+f(fromB(c,b,base))+' '+b;
$('vtb').innerHTML='<tr><th>Unit</th><th>Value</th></tr>'+units(c).map(function(u){return'<tr><td>'+u+'</td><td>'+f(fromB(c,u,base))+'</td></tr>'}).join('')}
$('vc').onchange=fill;$('vv').oninput=run;$('vf').onchange=run;$('vt').onchange=run;
$('vs').onclick=function(){var a=$('vf').value;$('vf').value=$('vt').value;$('vt').value=a;run()};
fill()}
var E=document.getElementById('eng');
if(E){
function g(v){var ks=[].slice.call(arguments,1);return ks.map(function(k){var x=parseFloat(v[k]);if(isNaN(x))throw'Please fill in all fields';return x})}
var tools=[
{n:'Ohm’s Law & Power',h:'Fill in any two values of V, I and R.',f:[['V','Voltage (V)'],['I','Current (A)'],['R','Resistance (Ω)']],c:function(v){var V=parseFloat(v.V),I=parseFloat(v.I),R=parseFloat(v.R);
if([V,I,R].filter(function(x){return!isNaN(x)}).length<2)throw'Enter at least two values';if(isNaN(V))V=I*R;else if(isNaN(I))I=V/R;else if(isNaN(R))R=V/I;
return['V = '+f(V)+' V','I = '+f(I)+' A','R = '+f(R)+' Ω','P = '+f(V*I)+' W']}},
{n:'Resistors: Series & Parallel',h:'Enter resistor values separated by commas.',f:[['list','Values in Ω (e.g. 100, 220, 470)']],c:function(v){var a=(v.list||'').split(/[,\s]+/).map(Number).filter(function(x){return x>0});
if(!a.length)throw'Enter at least one positive value';return['Series: '+f(a.reduce(function(s,x){return s+x},0))+' Ω','Parallel: '+f(1/a.reduce(function(s,x){return s+1/x},0))+' Ω']}},
{n:'RC Time Constant & Cut-off',h:'First-order RC filter.',f:[['R','Resistance (Ω)'],['C','Capacitance (µF)']],c:function(v){var a=g(v,'R','C'),t=a[0]*a[1]*1e-6;
return['τ = RC = '+f(t)+' s','Cut-off frequency = '+f(1/(2*Math.PI*t))+' Hz','Reaches 99.3% in 5τ = '+f(5*t)+' s']}},
{n:'Beam Deflection (simply supported, central load)',h:'δ = PL³ / 48EI and M = PL / 4.',f:[['P','Load P (N)'],['L','Span L (m)'],['E','Young’s modulus E (GPa)'],['I','Second moment I (cm⁴)']],c:function(v){var a=g(v,'P','L','E','I');
return['Max deflection = '+f(a[0]*Math.pow(a[1],3)/(48*a[2]*1e9*a[3]*1e-8)*1000)+' mm','Max bending moment = '+f(a[0]*a[1]/4)+' N·m']}},
{n:'Stress, Strain & Young’s Modulus',h:'Axial loading of a bar.',f:[['F','Force (N)'],['A','Area (mm²)'],['L','Original length (mm)'],['d','Extension (mm)']],c:function(v){var a=g(v,'F','A','L','d'),s=a[0]/a[1],e=a[3]/a[2];
return['Stress σ = '+f(s)+' MPa','Strain ε = '+f(e),'Young’s modulus E = '+f(s/e/1000)+' GPa']}},
{n:'Pipe Flow Rate',h:'Q = A × v for a full circular pipe.',f:[['D','Inside diameter (mm)'],['v','Velocity (m/s)']],c:function(v){var a=g(v,'D','v'),A=Math.PI*Math.pow(a[0]/1000,2)/4;
return['Area = '+f(A)+' m²','Q = '+f(A*a[1])+' m³/s','Q = '+f(A*a[1]*1000)+' L/s']}},
{n:'Kinetic & Potential Energy',h:'KE = ½mv², PE = mgh with g = 9.80665 m/s².',f:[['m','Mass (kg)'],['v','Speed (m/s)'],['h','Height (m)']],c:function(v){var a=g(v,'m','v','h');
return['Kinetic energy = '+f(.5*a[0]*a[1]*a[1])+' J','Potential energy = '+f(a[0]*9.80665*a[2])+' J']}},
{n:'Ideal Gas Law',h:'P = nRT / V',f:[['n','Amount n (mol)'],['T','Temperature (K)'],['V','Volume (L)']],c:function(v){var a=g(v,'n','T','V'),p=a[0]*8.314462618*a[1]/a[2];
return['Pressure = '+f(p)+' kPa','Pressure = '+f(p/101.325)+' atm']}},
{n:'Quadratic Equation Solver',h:'Solves ax² + bx + c = 0.',f:[['a','a'],['b','b'],['c','c']],c:function(v){var a=g(v,'a','b','c'),D=a[1]*a[1]-4*a[0]*a[2];if(a[0]===0)throw'a must not be 0';
if(D>=0)return['Discriminant = '+f(D),'x₁ = '+f((-a[1]+Math.sqrt(D))/(2*a[0])),'x₂ = '+f((-a[1]-Math.sqrt(D))/(2*a[0]))];
var re=-a[1]/(2*a[0]),im=Math.sqrt(-D)/(2*a[0]);return['Discriminant = '+f(D)+' (complex roots)','x₁ = '+f(re)+' + '+f(Math.abs(im))+'i','x₂ = '+f(re)+' − '+f(Math.abs(im))+'i']}},
{n:'Number Base Converter',h:'Binary, octal, decimal and hexadecimal.',f:[['val','Number'],['base','Input base (2–36)','10']],c:function(v){var b=parseInt(v.base||'10',10),n=parseInt(v.val,b);
if(isNaN(n)||b<2||b>36)throw'Invalid number or base';return['Binary: '+n.toString(2),'Octal: '+n.toString(8),'Decimal: '+n.toString(10),'Hex: '+n.toString(16).toUpperCase()]}}];
tools.forEach(function(t){var d=document.createElement('section');d.className='card';
d.innerHTML='<h2>'+t.n+'</h2><p class="m">'+t.h+'</p><div class="g">'+t.f.map(function(x){return'<label>'+x[1]+'<input data-k="'+x[0]+'" '+(x[2]?'value="'+x[2]+'"':'')+'></label>'}).join('')+'</div><button type="button" class="btn">Calculate</button><div class="out"></div>';
d.querySelector('button').onclick=function(){var v={};[].forEach.call(d.querySelectorAll('input'),function(i){v[i.dataset.k]=i.value});var o=d.querySelector('.out');
try{o.innerHTML=t.c(v).map(function(l){return'<div>'+l+'</div>'}).join('')}catch(e){o.textContent=typeof e==='string'?e:'Please check your inputs'}};
E.appendChild(d)})}
})();
