'use strict';
(()=>{
 const nav=document.querySelector('.map-actions');if(!nav||!window.SaqrimWorldData)return;
 const box=document.createElement('div');box.className='realm-picker';
 box.style.cssText='display:flex;align-items:end;flex-wrap:wrap;gap:10px;margin-bottom:14px;padding:14px;border:1px solid #334658;border-radius:10px;background:#1a2632';
 const label=document.createElement('label');label.htmlFor='map-world';label.textContent='Map / world';label.style.cssText='font-size:13px;font-weight:700;flex:1;min-width:190px';
 const select=document.createElement('select');select.id='map-world';select.style.cssText='display:block;width:100%;margin-top:5px;min-height:46px;padding:9px;border-radius:8px;border:1px solid #586c7c;background:#15222d;color:#edf3f7;font:inherit';
 const first=document.createElement('option');first.value='skyrim';first.textContent='Skyrim · mainland';select.append(first);
 for(const world of SaqrimWorldData.worlds){const option=document.createElement('option');option.value=world.id;option.textContent=world.name+(world.kind==='guide'?' · location guide':'');select.append(option);}
 label.append(select);box.append(label);nav.before(box);
 select.addEventListener('change',()=>{if(select.value!=='skyrim')location.href='worlds.html?world='+encodeURIComponent(select.value);});
 const about=document.querySelector('.about p');if(about)about.textContent='Choose Map / world above for the separate-world views. Skyrim and Icemoth use site-hosted map images. Additional native-world reference images depend on an external host; Solstheim also has reference-coordinate pins. Evergloam, Beyond Reach, Atmora and Apocrypha currently have dedicated location guides, not fabricated geographic overlays.';
 // Keep old mainland deep links and its all-world item index functional.
 // Add an explicit realm link beside a selected other-world item instead of forcing a redirect.
 function offerRealm(){
  const api=window.SaqrimMap;if(!api)return;const match=/^#(W\d{3})$/.exec(location.hash);if(!match)return;
  const r=api.records.find(r=>r.id===match[1]);if(!r)return;const raw=r.raw||r.r;if(!raw)return;
  const id=SaqrimWorldData.forRecord(raw).find(id=>id!=='skyrim');if(!id)return;
  const panel=document.getElementById('details');if(!panel||panel.querySelector('[data-realm-item="'+match[1]+'"]'))return;
  panel.querySelectorAll('.open-realm').forEach(a=>a.remove());const world=SaqrimWorldData.worlds.find(w=>w.id===id);
  const link=document.createElement('a');link.className='open-realm';link.dataset.realmItem=match[1];link.textContent='Open '+world.name+(world.kind==='guide'?' location guide →':' map →');link.href='worlds.html?world='+id+'#'+match[1];link.style.cssText='display:inline-block;padding:10px 14px;margin:0 0 12px;border:1px solid #efcc8a;border-radius:8px;color:#efcc8a';panel.prepend(link);
 }
 let attempts=0;const timer=setInterval(()=>{if(window.SaqrimMap){clearInterval(timer);offerRealm();const panel=document.getElementById('details');if(panel)new MutationObserver(offerRealm).observe(panel,{childList:true});}else if(++attempts>200)clearInterval(timer);},50);
 window.addEventListener('hashchange',offerRealm);document.addEventListener('click',()=>setTimeout(offerRealm,0));
})();
