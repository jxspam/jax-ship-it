const slides=[...document.querySelectorAll('.slide')];
let cur=Math.min(Math.max(parseInt(location.hash.slice(2))||0,0),slides.length-1);
const params=new URLSearchParams(location.search);
const KEY=params.get('key');
if(KEY)document.body.classList.add('presenter');
const ORIGIN=location.protocol.startsWith('http')?location.origin:'https://jax-build-club-brisbane.vercel.app';
const ASK=ORIGIN+'/ask';

function show(n){
  const prevCp=slides[cur]&&slides[cur].dataset.cp;
  cur=Math.min(Math.max(n,0),slides.length-1);
  const s=slides[cur];
  slides.forEach((x,i)=>x.classList.toggle('active',i===cur));
  document.getElementById('count').textContent=(cur+1)+' / '+slides.length;
  document.getElementById('bar').style.width=((cur+1)/slides.length*100)+'%';
  document.body.classList.toggle('dark',s.classList.contains('check'));
  history.replaceState(null,'',location.search+'#/'+cur);
  const here=ORIGIN+'/#/'+cur;document.getElementById('slideqr').src=QR(here);document.getElementById('slideurl').textContent=ORIGIN.replace(/^https?:\/\//,'');
  document.querySelectorAll('.fill,.stack>div').forEach(f=>f.style.width='0');
  setTimeout(()=>s.querySelectorAll('.fill,.stack>div').forEach(f=>f.style.width=f.dataset.w+'%'),120);
  if(KEY&&s.dataset.cp)admin({action:'state',cp:+s.dataset.cp});
  document.querySelectorAll('video').forEach(v=>{if(!s.contains(v))v.pause();else if(v.autoplay)v.play().catch(()=>{})});
}
addEventListener('keydown',e=>{
  if(e.target.closest('input,textarea'))return;
  if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'){e.preventDefault();show(cur+1)}
  else if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();show(cur-1)}
  else if(e.key==='Home')show(0);
  else if(e.key==='End')show(slides.length-1);
  else if(e.key==='f')document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();
});
/* Tap and swipe. iOS Safari only fires click on elements it treats as clickable, so the
   listener lives on #deck (which carries an onclick attribute) instead of window. */
const deckEl=document.getElementById('deck');
const skip=e=>e.target.closest('a,button,.toast,video,iframe,.cmd,.qb,input,textarea');
let tx=null,ty=null,swiped=false;
deckEl.addEventListener('touchstart',e=>{const t=e.touches[0];tx=t.clientX;ty=t.clientY;swiped=false},{passive:true});
deckEl.addEventListener('touchend',e=>{if(tx===null)return;const t=e.changedTouches[0],dx=t.clientX-tx,dy=t.clientY-ty;tx=null;
  if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy)*1.5){swiped=true;show(dx<0?cur+1:cur-1)}},{passive:true});
deckEl.addEventListener('click',e=>{if(swiped){swiped=false;return}if(skip(e))return;show(e.clientX>innerWidth/3?cur+1:cur-1)});
addEventListener('hashchange',()=>{const n=parseInt(location.hash.slice(2))||0;if(n!==cur)show(n)});

/* ============ LIVE Q&A ============ */
const QR=u=>'https://api.qrserver.com/v1/create-qr-code/?size=600x600&margin=0&data='+encodeURIComponent(u);
document.querySelectorAll('[data-qr]').forEach(i=>i.src=QR(i.dataset.qr||ASK));

if(KEY)fetch('/api/jev',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key:KEY})}).then(r=>r.json()).then(j=>{if(!j.key)return;document.querySelectorAll('[data-jevqr]').forEach(i=>i.src=QR(j.key));document.querySelectorAll('[data-jevkey]').forEach(e=>{e.textContent=j.key;e.style.wordBreak='break-all'})}).catch(()=>{});
document.querySelectorAll('[data-jevqr]').forEach(i=>{if(!KEY)i.closest('.qr').style.display='none'});
/* showcase timer */
let tLeft=180,tRun=null;
function tDraw(){const el=document.getElementById('timer');if(!el)return;const m=Math.floor(Math.abs(tLeft)/60),s=Math.abs(tLeft)%60;el.textContent=(tLeft<0?'+':'')+m+':'+String(s).padStart(2,'0');el.classList.toggle('over',tLeft<0)}
addEventListener('keydown',e=>{if(!slides[cur].hasAttribute('data-timer'))return;
  if(e.key==='t'){if(tRun){clearInterval(tRun);tRun=null}else tRun=setInterval(()=>{tLeft--;tDraw()},1000)}
  if(e.key==='r'){clearInterval(tRun);tRun=null;tLeft=180;tDraw()}});
document.querySelectorAll('[data-url]').forEach(e=>e.textContent=ASK.replace(/^https?:\/\//,''));
document.querySelectorAll('[data-link]').forEach(e=>e.href=ASK);
const esc=t=>String(t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function admin(b){fetch('/api/admin',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({...b,key:KEY})}).catch(()=>{})}
let seen=null;
function toast(q){
  if(!KEY)return;
  const t=document.createElement('div');t.className='toast';
  t.innerHTML=`<div class="label">New question · Checkpoint ${q.cp} · ${q.name?esc(q.name):'Anonymous'}</div><p>${esc(q.text)}</p>`;
  const box=document.getElementById('toasts');box.prepend(t);
  while(box.children.length>4)box.lastChild.remove();
  setTimeout(()=>{t.classList.add('out');setTimeout(()=>t.remove(),300)},9000);
}
function renderLists(qs){
  document.querySelectorAll('[data-list]').forEach(el=>{
    const cp=+el.dataset.list;
    const mine=qs.filter(q=>q.cp===cp).sort((a,b)=>b.votes-a.votes||a.ts-b.ts);
    el.innerHTML=mine.length?mine.slice(0,6).map(q=>`<div class="item"><div><p>${esc(q.text)}</p><div class="who">${q.name?esc(q.name):'Anonymous'}</div></div><div><span class="v">▲ ${q.votes}</span><button class="x" data-hide="${q.id}" title="Hide">✕</button></div></div>`).join(''):'<div class="none">Scan to ask, anonymous by default</div>';
  });
  document.querySelectorAll('[data-hide]').forEach(b=>b.onclick=()=>{admin({action:'hide',id:b.dataset.hide});b.closest('.item').remove()});
}
async function poll(){
  if(!location.protocol.startsWith('http'))return;
  try{
    const r=await fetch('/api/questions',{cache:'no-store'});if(!r.ok)return;
    const j=await r.json();const qs=j.questions||[];
    if(seen){const fresh=qs.filter(q=>!seen.has(q.id));fresh.forEach(toast);fresh.forEach(q=>qbFresh.add(q.id));if(fresh.length)qbNotify(fresh)}
    seen=new Set(qs.map(q=>q.id));
    renderLists(qs);
    qbRender(qs);
  }catch{}
}
/* ============ QUESTIONS BUBBLE (presenter) ============ */
const qb=document.createElement('div');qb.className='qb';
qb.innerHTML=`<div class="qb-panel"><div class="qb-head"><button data-f="0" aria-pressed="true">All</button><button data-f="1">CP 1</button><button data-f="2">CP 2</button><button data-f="3">CP 3</button></div><div class="qb-list"></div></div><button class="qb-btn" aria-label="Questions">?<span class="badge"></span></button>`;
let qbF=0,qbAll=[],qbFresh=new Set();
const qbList=()=>[qb.querySelector('.qb-list')];
function qbHTML(){
  const qs=qbAll.filter(q=>!qbF||q.cp===qbF).sort((a,b)=>b.ts-a.ts);
  return qs.length?qs.map(q=>`<div class="qb-item ${qbFresh.has(q.id)?'new':''}"><div><p>${esc(q.text)}</p><div class="who">CP ${q.cp} · ${q.name?esc(q.name):'Anonymous'}</div></div><div><span class="v">▲ ${q.votes}</span><button class="x" data-hide="${q.id}" title="Hide">✕</button></div></div>`).join(''):'<div class="qb-empty">No questions yet</div>';
}
function qbRender(qs){
  if(qs)qbAll=qs;
  qbList().forEach(el=>{el.innerHTML=qbHTML();el.querySelectorAll('[data-hide]').forEach(b=>b.onclick=()=>{admin({action:'hide',id:b.dataset.hide});qbAll=qbAll.filter(q=>q.id!==b.dataset.hide);qbRender()})});
  const b=qb.querySelector('.badge');const n=qbFresh.size;b.textContent=n;b.classList.toggle('on',n>0);
}
qb.querySelector('.qb-btn').onclick=()=>{qb.classList.toggle('open');if(qb.classList.contains('open')){qbFresh.clear();qbRender()}};
qb.querySelectorAll('[data-f]').forEach(b=>b.onclick=()=>{qbF=+b.dataset.f;qb.querySelectorAll('[data-f]').forEach(x=>x.setAttribute('aria-pressed',x===b));qbRender()});
function qbNotify(){qbRender()}
show(cur);
/* ============ AGENDA PANEL ============ */
(function(){
  const A=window.AGENDA||[],ag=document.getElementById('ag');if(!ag)return;
  const mins=t=>{const [h,m]=t.split(':').map(Number);return h*60+m};
  const fmt=t=>{let [h,m]=t.split(':').map(Number);const ap=h>=12?'PM':'AM';h=h%12||12;return h+':'+String(m).padStart(2,'0')+' '+ap};
  document.getElementById('agList').innerHTML=A.map(a=>`<li data-k="${a[0]}"><span class="t">${fmt(a[1])}</span><span>${a[3]}</span></li>`).join('');
  const first=k=>{if(k==='d')return slides.length-1;const i=slides.findIndex(s=>s.dataset.ag===k);return i<0?0:i};
  document.querySelectorAll('#agList li').forEach(li=>li.onclick=e=>{e.stopPropagation();show(first(li.dataset.k))});
  try{if(localStorage.getItem('agOpen')==='1')ag.classList.add('open')}catch(e){}
  const toggle=()=>{ag.classList.toggle('open');try{localStorage.setItem('agOpen',ag.classList.contains('open')?'1':'0')}catch(e){}};
  document.getElementById('agPill').onclick=e=>{e.stopPropagation();toggle()};
  ag.addEventListener('click',e=>e.stopPropagation());
  addEventListener('keydown',e=>{if(e.key==='a'&&!e.target.closest('input,textarea'))toggle()});
  function tick(){
    const parts=new Intl.DateTimeFormat('en-GB',{timeZone:'America/Los_Angeles',hour:'2-digit',minute:'2-digit',hour12:false}).formatToParts(new Date());
    const hh=+parts.find(p=>p.type==='hour').value%24,mm=+parts.find(p=>p.type==='minute').value,now=hh*60+mm;
    document.getElementById('agClock').textContent=fmt(hh+':'+mm);
    const s=document.querySelector('.slide.active');const k=s&&s.dataset.ag;
    const cur=A.find(a=>a[0]===k)||A[0];
    document.getElementById('agNow').textContent=fmt(cur[1])+' · '+cur[3];
    const left=mins(cur[2])-now,el=document.getElementById('agLeft');
    const inDay=now>=mins(A[0][1])-120&&now<=mins(A[A.length-1][2])+60;
    el.textContent=!inDay?'':left<0?(-left)+' min over':(now<mins(cur[1])?'starts in '+(mins(cur[1])-now)+' min':left+' min left');
    el.classList.toggle('over',inDay&&left<0);
    const ci=A.indexOf(cur);
    document.querySelectorAll('#agList li').forEach((li,i)=>{li.classList.toggle('cur',i===ci);li.classList.toggle('done',i<ci);
      li.classList.toggle('clock',inDay&&now>=mins(A[i][1])&&now<mins(A[i][2])&&i!==ci)});
  }
  new MutationObserver(tick).observe(document.getElementById('deck'),{subtree:true,attributes:true,attributeFilter:['class']});
  tick();setInterval(tick,15000);addEventListener('hashchange',tick);addEventListener('keydown',()=>setTimeout(tick,50));
  document.getElementById('deck').addEventListener('click',()=>setTimeout(tick,50));
})();
