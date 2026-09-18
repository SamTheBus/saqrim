'use strict';
(() => {
 if(document.getElementById('saqrim-top'))return;
 const style=document.createElement('style');
 style.textContent='#saqrim-top{position:fixed;right:max(16px,env(safe-area-inset-right));bottom:max(18px,env(safe-area-inset-bottom));z-index:9000;border:1px solid #efcc8a;border-radius:999px;background:#efcc8a;color:#111820;padding:12px 18px;min-height:48px;font:750 15px system-ui;box-shadow:0 5px 25px #0007;cursor:pointer}#saqrim-top[hidden]{display:none!important}#saqrim-top:focus-visible{outline:3px solid white;outline-offset:3px}@media print{#saqrim-top{display:none!important}}';
 document.head.append(style);
 const button=document.createElement('button');button.id='saqrim-top';button.type='button';button.textContent='↑ Top';button.setAttribute('aria-label','Jump to top instantly');button.hidden=true;
 button.addEventListener('click',()=>{window.scrollTo({top:0,left:0,behavior:'instant'});const top=document.querySelector('h1');if(top){top.tabIndex=-1;top.focus({preventScroll:true});}});
 document.body.append(button);
 const update=()=>{button.hidden=window.scrollY<300;};window.addEventListener('scroll',update,{passive:true});update();
})();
