/* Domathcalculator - calculator engine + keypad UI (no eval, safe parser) */
var DMC=(function(){
var deg=true,ans=0;
var toR=function(x){return deg?x*Math.PI/180:x},fromR=function(x){return deg?x*180/Math.PI:x};
var clean=function(x){return Math.abs(x)<1e-14?0:x};
function fact(n){if(n<0||n!==Math.floor(n)||n>170)return NaN;var r=1;for(var i=2;i<=n;i++)r*=i;return r}
var F={sin:function(x){return clean(Math.sin(toR(x)))},cos:function(x){return clean(Math.cos(toR(x)))},tan:function(x){return clean(Math.tan(toR(x)))},
asin:function(x){return fromR(Math.asin(x))},acos:function(x){return fromR(Math.acos(x))},atan:function(x){return fromR(Math.atan(x))},
sinh:Math.sinh,cosh:Math.cosh,tanh:Math.tanh,log:Math.log10,ln:Math.log,sqrt:Math.sqrt,cbrt:Math.cbrt,abs:Math.abs,exp:Math.exp,
floor:Math.floor,ceil:Math.ceil,round:Math.round,fact:fact};
var C={pi:Math.PI,e:Math.E,ans:function(){return ans}};
function evaluate(src){
var s=src.replace(/π/g,'pi').replace(/×/g,'*').replace(/÷/g,'/').replace(/−/g,'-').replace(/√/g,'sqrt').replace(/\s+/g,'').toLowerCase(),i=0;
function pk(){return s[i]}
function expr(){var v=term();while(pk()==='+'||pk()==='-'){var o=s[i++],r=term();v=o==='+'?v+r:v-r}return v}
function term(){var v=unary();for(;;){var c=pk();if(c==='*'||c==='/'){i++;var r=unary();v=c==='*'?v*r:v/r}else if(c&&/[a-z(0-9.]/.test(c)){v*=unary()}else break}return v}
function unary(){if(pk()==='-'){i++;return -unary()}if(pk()==='+'){i++;return unary()}return pow()}
function pow(){var b=post();if(pk()==='^'){i++;return Math.pow(b,unary())}return b}
function post(){var v=atom();while(pk()==='!'||pk()==='%'){v=s[i++]==='!'?fact(v):v/100}return v}
function close(){if(pk()!==')')throw 1;i++}
function atom(){var c=pk();
if(c==='('){i++;var v=expr();close();return v}
var rest=s.slice(i),m=/^(\d*\.?\d+(?:e[+-]?\d+)?)/.exec(rest);
if(m&&/[\d.]/.test(c)){i+=m[0].length;return parseFloat(m[0])}
var w=/^[a-z]+/.exec(rest);
if(w){var n=w[0];
if(n in C){i+=n.length;var k=C[n];return typeof k==='function'?k():k}
if(n in F){i+=n.length;if(pk()==='('){i++;var a=expr();close();return F[n](a)}return F[n](unary())}}
throw 1}
var r=expr();if(i<s.length)throw 1;return r}
function fmt(v){if(isNaN(v))return'Error';if(!isFinite(v))return v>0?'∞':'-∞';return String(parseFloat(v.toPrecision(12)))}
function ui(){
var root=document.getElementById('calc'),hist=[];
try{hist=JSON.parse(localStorage.getItem('dmc_h')||'[]')}catch(e){}
var rows=[['sin(','cos(','tan(','DEG','AC'],['asin(','acos(','atan(','(',')'],['log(','ln(','sqrt(','^','DEL'],['sinh(','cosh(','tanh(','!','%'],
['7','8','9','÷','π'],['4','5','6','×','e'],['1','2','3','−','Ans'],['0','.','EXP','+','=']];
var html='<div class="disp"><input id="ci" autocomplete="off" spellcheck="false" inputmode="none" aria-label="Expression" placeholder="0"></div><div class="res" id="co" aria-live="polite"></div><div class="keys">';
rows.forEach(function(r){r.forEach(function(k){var cl='ƒ';if('÷×−+^!%'.indexOf(k)>-1)cl='op';if(k==='=')cl='eq';
html+='<button type="button" class="'+cl+'" data-k="'+k+'">'+(k==='DEG'?'DEG':k.replace('(',''))+'</button>'})});
html+='</div><details><summary>History</summary><div class="hist" id="ch"></div><button type="button" class="keys-clear" id="cc" style="margin-top:8px">Clear history</button></details>';
root.innerHTML=html;
var inp=document.getElementById('ci'),out=document.getElementById('co'),hd=document.getElementById('ch');
function ins(t){var s=inp.selectionStart,e=inp.selectionEnd;inp.value=inp.value.slice(0,s)+t+inp.value.slice(e);var p=s+t.length;inp.setSelectionRange(p,p);inp.focus();prev()}
function prev(){if(!inp.value.trim()){out.textContent='';return}try{var v=evaluate(inp.value);out.textContent=isNaN(v)?'':'= '+fmt(v)}catch(e){out.textContent=''}}
function draw(){hd.innerHTML='';hist.forEach(function(h){var d=document.createElement('div');d.textContent=h[0]+' = '+h[1];d.onclick=function(){inp.value=h[0];prev();inp.focus()};hd.appendChild(d)})}
function save(){try{localStorage.setItem('dmc_h',JSON.stringify(hist))}catch(e){}}
function eq(){if(!inp.value.trim())return;try{var v=evaluate(inp.value);if(isNaN(v))throw 0;ans=v;var r=fmt(v);hist.unshift([inp.value,r]);hist=hist.slice(0,25);save();draw();inp.value=r;out.textContent=''}catch(e){out.textContent='Error – check the expression'}}
root.addEventListener('click',function(ev){var b=ev.target.closest('button[data-k]');if(!b)return;var k=b.dataset.k;
if(k==='AC'){inp.value='';out.textContent=''}
else if(k==='DEL'){var s=inp.selectionStart,e=inp.selectionEnd;if(s===e&&s>0)s--;inp.value=inp.value.slice(0,s)+inp.value.slice(e);inp.setSelectionRange(s,s);prev()}
else if(k==='='){eq()}
else if(k==='DEG'){deg=!deg;b.textContent=deg?'DEG':'RAD';prev()}
else if(k==='Ans'){ins('ans')}else if(k==='EXP'){ins('×10^')}else ins(k)});
inp.addEventListener('input',prev);
inp.addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();eq()}else if(e.key==='Escape'){inp.value='';out.textContent=''}});
document.getElementById('cc').onclick=function(){hist=[];save();draw()};
draw()}
if(typeof document!=='undefined'&&document.getElementById('calc'))ui();
return{evaluate:evaluate,setDeg:function(d){deg=d}}})();
if(typeof module!=='undefined')module.exports=DMC;
