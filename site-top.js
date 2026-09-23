'use strict';
// Shared site navigation is independent of the map, reference data and quest loaders.
(() => {
 const entries=[['./','Loot catalog · 633'],['load-order.html','Load order · 214'],['map.html','Map'],['quests.html','Quests & rewards'],['shrines.html','Shrines & Gods'],['standing-stones.html','Standing Stones']];
 function activePath(){
  const file=location.pathname.split('/').pop()||'index.html';
  if(['index.html','loot.html','catalog-source.html','catalog-current.html'].includes(file))return './';
  if(file==='worlds.html')return 'map.html';
  if(file==='blessings.html'){const kind=/^#(deity|shrine|stone)=/.exec(location.hash);return (kind?kind[1]==='stone':new URLSearchParams(location.search).get('tab')==='stones')?'standing-stones.html':'shrines.html';}
  return file;
 }
 function refresh(){
  const nav=document.querySelector('.nav');if(!nav)return;
  const active=activePath(),current=[...nav.children];
  const correct=current.length===entries.length+1&&current[0].classList.contains('brand')&&current[0].tagName==='A'&&entries.every(([href,text],i)=>current[i+1].getAttribute('href')===href&&current[i+1].textContent===text);
  if(!correct){
   const brand=document.createElement('a');brand.className='brand';brand.href='./';brand.textContent='SAQRIM';
   const links=entries.map(([href,text])=>{const a=document.createElement('a');a.href=href;a.textContent=text;return a;});
   nav.replaceChildren(brand,...links);
  }
  nav.setAttribute('aria-label','Saqrim sections');nav.dataset.saqrimNavigation='6';
  for(const a of nav.querySelectorAll('a')){if(!a.classList.contains('brand')&&a.getAttribute('href')===active)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');}
 }
 window.SaqrimNavigation={entries,refresh};refresh();
 window.addEventListener('pageshow',refresh);window.addEventListener('hashchange',refresh);window.addEventListener('popstate',refresh);window.addEventListener('saqrim-reference-view',refresh);
})();
(() => {
 const catalog=document.getElementById('catalog');
 if(catalog){
  const addLinks=()=>catalog.querySelectorAll('details[id]').forEach(card=>{
   if(!/^W\d{3}$/.test(card.id)||card.querySelector('.saqrim-map-link'))return;
   const body=card.querySelector('.card-body');if(!body)return;
   const p=document.createElement('p');p.className='saqrim-map-link';const a=document.createElement('a');a.href='map.html#'+card.id;a.textContent='View location on map / index →';p.append(a);body.prepend(p);
  });
  new MutationObserver(addLinks).observe(catalog,{childList:true});addLinks();
 }
 if(document.getElementById('saqrim-top'))return;
 const style=document.createElement('style');
 style.textContent='.nav{height:auto!important;min-height:66px;flex-wrap:wrap}.nav a:not(.brand){min-height:44px;display:inline-flex;align-items:center}.saqrim-map-link{margin:0 0 12px}.saqrim-map-link a{color:#b0daff}@media(max-width:540px){.nav .brand{flex-basis:100%;margin-bottom:4px}.nav a:not(.brand){font-size:12px!important;padding:8px!important}}#saqrim-top{position:fixed;right:max(16px,env(safe-area-inset-right));bottom:max(18px,env(safe-area-inset-bottom));z-index:9000;border:1px solid #efcc8a;border-radius:999px;background:#efcc8a;color:#111820;padding:12px 18px;min-height:48px;font:750 15px system-ui;box-shadow:0 5px 25px #0007;cursor:pointer}#saqrim-top[hidden]{display:none!important}#saqrim-top:focus-visible{outline:3px solid white;outline-offset:3px}@media print{#saqrim-top{display:none!important}}';
 // One visual treatment as well as one link order, including the reference pages.
 style.textContent+='.nav[data-saqrim-navigation]{box-sizing:border-box;display:flex;align-items:center;justify-content:flex-start;flex-wrap:wrap;gap:6px;width:100%;max-width:none;margin:0;padding:12px max(12px,calc((100% - 1400px)/2));border-bottom:1px solid #334658;background:#111820}.nav[data-saqrim-navigation] .brand{display:block;flex:0 0 auto;margin:0 auto 0 0;padding:0;border:0;background:transparent;color:#efcc8a;font:800 17px/1.4 system-ui;letter-spacing:3px;text-decoration:none}.nav[data-saqrim-navigation] a:not(.brand){box-sizing:border-box;display:inline-flex;align-items:center;justify-content:center;flex:0 0 auto;min-height:44px;max-width:100%;margin:0;padding:10px 12px;border:1px solid #334658;border-radius:7px;background:transparent;color:#b0daff;font:500 14px/1.4 system-ui;letter-spacing:normal;text-decoration:none;white-space:nowrap}.nav[data-saqrim-navigation] a[aria-current="page"]{border-color:#efcc8a;color:#efcc8a;background:transparent}.nav[data-saqrim-navigation] a:hover{border-color:#efcc8a}.nav[data-saqrim-navigation] a:focus-visible{outline:3px solid #efcc8a;outline-offset:3px}@media(max-width:540px){.nav[data-saqrim-navigation] .brand{flex-basis:100%;margin:0 0 6px}.nav[data-saqrim-navigation] a:not(.brand){font-size:12px!important;padding:8px!important}}';
 document.head.append(style);
 const button=document.createElement('button');button.id='saqrim-top';button.type='button';button.textContent='↑ Top';button.setAttribute('aria-label','Jump to top instantly');button.hidden=true;
 button.addEventListener('click',()=>{window.scrollTo({top:0,left:0,behavior:'instant'});const top=document.querySelector('h1');if(top){top.tabIndex=-1;top.focus({preventScroll:true});}});
 document.body.append(button);
 const update=()=>{button.hidden=window.scrollY<300;};window.addEventListener('scroll',update,{passive:true});update();
})();
// Separate optional module; existing Top button and map links remain independent.
(()=>{if(document.querySelector('script[data-saqrim-quests]'))return;const script=document.createElement('script');script.src='site-quests.js?v=3';script.dataset.saqrimQuests='true';script.async=true;document.head.append(script);})();
