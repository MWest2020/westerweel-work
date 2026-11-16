const decks=[...document.querySelectorAll('.deck')],c=document.getElementById('counter');let d=decks[0],i=0;
const slides=()=>[...d.querySelectorAll('.slide')];
// backgrounds only load when their slide is shown; fetch the next two ahead so they are there on time
const seen=new Set();
function preload(el){if(!el)return;const cs=getComputedStyle(el),b=cs.getPropertyValue('--photo')+cs.getPropertyValue('--tree');
  for(const m of b.matchAll(/url\(['"]?([^'")]+)['"]?\)/g))if(!seen.has(m[1])){seen.add(m[1]);new Image().src=m[1]}}
function go(n){const s=slides();s.forEach(x=>x.classList.remove('active'));i=Math.max(0,Math.min(s.length-1,n));s[i].classList.add('active');s[i].scrollTop=0;
  c.textContent=(i+1)+' / '+s.length;history.replaceState(null,'',location.search+'#'+(i+1));preload(s[i+1]);preload(s[i+2])}
function setLang(l){const t=decks.find(x=>x.lang===l);if(!t)return;d.classList.remove('active');d=t;d.classList.add('active');
  document.documentElement.lang=l;document.title=d.dataset.title;
  document.querySelectorAll('#lang button').forEach(b=>b.classList.toggle('on',b.dataset.lang===l));
  try{localStorage.setItem('lang',l)}catch(e){}go(i)}
document.querySelectorAll('#lang button').forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();setLang(b.dataset.lang)}));
document.addEventListener('keydown',e=>{if(['ArrowRight',' ','PageDown'].includes(e.key))go(i+1);if(['ArrowLeft','PageUp'].includes(e.key))go(i-1);
  if(e.key==='Home')go(0);if(e.key==='End')go(1e9);
  if(e.key==='f'||e.key==='F'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen?.()}
  if(e.key==='l'&&decks.length>1)setLang(decks[(decks.indexOf(d)+1)%decks.length].lang)});
// click or tap: left third goes back, the rest goes forward
document.addEventListener('click',e=>{if(!e.target.closest('a,#lang'))go(e.clientX<innerWidth/3?i-1:i+1)});
let saved=null;try{saved=localStorage.getItem('lang')}catch(e){}
i=Math.max(0,(parseInt(location.hash.slice(1))||1)-1);
setLang(new URLSearchParams(location.search).get('lang')||saved||decks[0].lang);
