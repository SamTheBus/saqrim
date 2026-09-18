'use strict';
(() => {
 const nav=document.querySelector('.nav');
 if(nav&&!nav.querySelector('a[href="map.html"]')){const link=document.createElement('a');link.href='map.html';link.textContent='Map';nav.append(link);}
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
 style.textContent='.nav{height:auto!important;min-height:66px;flex-wrap:wrap}.saqrim-map-link{margin:0 0 12px}.saqrim-map-link a{color:#b0daff}@media(max-width:540px){.nav .brand{flex-basis:100%;margin-bottom:4px}.nav a:not(.brand){font-size:12px!important;padding:8px!important}}#saqrim-top{position:fixed;right:max(16px,env(safe-area-inset-right));bottom:max(18px,env(safe-area-inset-bottom));z-index:9000;border:1px solid #efcc8a;border-radius:999px;background:#efcc8a;color:#111820;padding:12px 18px;min-height:48px;font:750 15px system-ui;box-shadow:0 5px 25px #0007;cursor:pointer}#saqrim-top[hidden]{display:none!important}#saqrim-top:focus-visible{outline:3px solid white;outline-offset:3px}@media print{#saqrim-top{display:none!important}}';
 document.head.append(style);
 const button=document.createElement('button');button.id='saqrim-top';button.type='button';button.textContent='↑ Top';button.setAttribute('aria-label','Jump to top instantly');button.hidden=true;
 button.addEventListener('click',()=>{window.scrollTo({top:0,left:0,behavior:'instant'});const top=document.querySelector('h1');if(top){top.tabIndex=-1;top.focus({preventScroll:true});}});
 document.body.append(button);
 const update=()=>{button.hidden=window.scrollY<300;};window.addEventListener('scroll',update,{passive:true});update();
})();
// Separate optional module; existing Top button and map links remain independent.
(()=>{if(document.querySelector('script[data-saqrim-quests]'))return;const script=document.createElement('script');script.src='site-quests.js?v=1';script.dataset.saqrimQuests='true';script.async=true;document.head.append(script);})();
