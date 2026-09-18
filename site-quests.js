/* Additive quest navigation and map references. Never writes catalog or user saves. */
'use strict';
(()=>{
 if(window.SaqrimQuestIntegration)return;window.SaqrimQuestIntegration=true;
 const node=(t,c,x)=>{const n=document.createElement(t);if(c)n.className=c;if(x!==undefined)n.textContent=x;return n;};
 const nav=document.querySelector('.nav');if(nav&&!nav.querySelector('a[href="quests.html"]')){const a=node('a','','Quests & rewards');a.href='quests.html';nav.append(a);}
 const catalog=document.getElementById('catalog'),mainMap=document.getElementById('map'),worldMap=document.getElementById('world-map');if(!catalog&&!mainMap&&!worldMap)return;
 const style=node('style');style.textContent='.quest-starts{border:1px solid #a4d8ba;border-radius:9px;padding:14px;margin:14px 0}.quest-starts h3{margin:0 0 8px;font-size:17px}.quest-starts a{display:block;margin:8px 0;color:#b0daff}.quest-starts small{display:block;font-size:12px;color:#b2c1cc}.quest-pin{display:block;background:#a4d8ba;border:2px solid #11242d;color:#11242d;border-radius:4px;transform:rotate(45deg);width:25px;height:25px;box-shadow:0 2px 6px #0008}.quest-pin b{display:block;transform:rotate(-45deg);text-align:center;font:bold 18px/21px system-ui}.quest-overlay-control{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:10px 0;font:14px/1.5 system-ui}.quest-overlay-control input{min-height:0;width:20px;height:20px}.quest-catalog-links{margin:8px 0}.quest-catalog-links a{display:inline-block;margin:4px 10px 4px 0;color:#b0daff}';document.head.append(style);
 fetch('quests-data.json?v=3').then(r=>{if(!r.ok)throw Error('Quest links unavailable');return r.json();}).then(pack=>{
  function expand(q,records){const rewards=(q.rewards||[]).map(r=>({...r,...(pack.catalogLinks?.[q.id]?.[r.label]||{})}));if(q.rewardMod)for(const r of records){const raw=r.raw||r.r;if(Number(raw['LO #'])===q.rewardMod.lo)rewards.push({catalog:r.id,kind:(q.rewardMod.boss||[]).includes(r.id)?'boss':q.rewardMod.kind,note:q.rewardMod.note});}return{...q,rewards};}
  function questLinks(parent,items,title){const section=node('section','quest-starts');section.append(node('h3','',title));for(const q of items){const a=node('a','',q.title+' →');a.href='quests.html#'+q.id;section.append(a,node('small','',q.start.place+' · '+q.start.trigger+(q.start.precision==='nearby'?' The pin is a nearby reference, not the exact quest giver.':'')));}parent.append(section);}
  let attempts=0;const timer=setInterval(()=>{
   const api=catalog?window.SaqrimCatalog:(window.SaqrimMap||window.SaqrimWorlds);if(!api){if(++attempts>200)clearInterval(timer);return;}clearInterval(timer);const quests=pack.quests.map(q=>expand(q,api.records));
   if(catalog){const reverse=new Map();for(const q of quests)for(const r of q.rewards){if(!r.catalog)continue;if(!reverse.has(r.catalog))reverse.set(r.catalog,[]);reverse.get(r.catalog).push(q);}
    const add=()=>catalog.querySelectorAll('details[id]').forEach(card=>{if(card.querySelector('.quest-catalog-links')||!reverse.has(card.id))return;const body=card.querySelector('.card-body');if(!body)return;const links=node('div','quest-catalog-links');links.append(node('strong','','Related quests / adventures: '));for(const q of reverse.get(card.id)){const a=node('a','',q.title);a.href='quests.html#'+q.id;links.append(a);}body.prepend(links);});new MutationObserver(add).observe(catalog,{childList:true});add();return;
   }
   connect(api,quests,questLinks);
  },100);
 }).catch(e=>console.warn(e.message));
 function connect(api,quests,questLinks){
  const mainland=!!window.SaqrimMap,element=document.getElementById(mainland?'map':'world-map'),panel=document.getElementById(mainland?'details':'selection');if(!element||!panel)return;
  const control=node('label','quest-overlay-control'),checkbox=node('input');checkbox.type='checkbox';checkbox.id='show-quest-starts';checkbox.checked=true;control.append(checkbox,document.createTextNode('Quest starts · green ! pins'),node('small','','Reference areas; exact starting instructions are in each quest card.'));element.parentElement.before(control);
  const layer=window.L&&api.map?L.layerGroup().addTo(api.map):null,currentWorld=()=>mainland?'skyrim':api.world?.id;let lastWorld=currentWorld();
  const candidates=()=>quests.filter(q=>q.start.world===currentWorld()&&q.start.mapPlace);
  const findPlace=q=>api.places.find(p=>p.name===q.start.mapPlace&&(mainland||p.world===currentWorld()));
  function refreshPanel(){if(panel.querySelector('.quest-starts'))return;const name=panel.querySelector('h2')?.textContent,found=candidates().filter(q=>q.start.mapPlace===name);if(found.length)questLinks(panel,found,'Quests starting here / nearby');}
  new MutationObserver(refreshPanel).observe(panel,{childList:true});
  function matches(q){
   const query=document.getElementById(mainland?'map-search':'world-search')?.value.trim().toLowerCase()||'';
   const itemNames=q.rewards.map(r=>r.label||api.records.find(x=>x.id===r.catalog)?.raw.Target||'').join(' '),text=(JSON.stringify(q)+' '+itemNames).toLowerCase();if(query&&!query.split(/\s+/).every(t=>text.includes(t)))return false;
   const facets=Object.entries(api.selected||{}).filter(([k,v])=>k!=='place'&&v.size),items=q.rewards.filter(r=>r.kind!=='lead');let picks={};try{picks=JSON.parse(localStorage.getItem('skyrimLootChoices_v202_20260917')||'{}')||{};}catch(_){}
   const picking=document.getElementById('picks-only')?.checked;
   if((facets.length||picking)&&!items.some(r=>{const tags={...(api.records.find(x=>x.id===r.catalog)?.meta.tags||{}),...r.tags};return facets.every(([k,v])=>(tags[k]||[]).some(t=>v.has(t)))&&(!picking||['Want','Maybe'].includes(picks[r.catalog]));}))return false;
   if(mainland){const p=findPlace(q);if(api.selected.place?.size&&p&&!api.selected.place.has(p.type))return false;const w=document.getElementById('world')?.value;if(w&&w!=='Skyrim / unspecified')return false;}
   return !document.getElementById('unpinned-only')?.checked;
  }
  function draw(){lastWorld=currentWorld();if(!layer)return;layer.clearLayers();if(!checkbox.checked||(!mainland&&api.world?.kind!=='map'))return;
   const grouped=new Map();for(const q of candidates()){if(!matches(q))continue;const p=findPlace(q);if(!p||(!mainland&&!p.pin))continue;if(!grouped.has(p.name))grouped.set(p.name,{p,qs:[]});grouped.get(p.name).qs.push(q);}
   for(const {p,qs}of grouped.values()){const pos=mainland?p.latlng:[p.y,p.x],title='Quest start reference · '+p.name;const marker=L.marker(pos,{icon:L.divIcon({className:'quest-start-icon',html:'<span class="quest-pin"><b>!</b></span>',iconSize:[25,25],iconAnchor:[12,12]}),title,alt:title,zIndexOffset:400});const popup=node('div');questLinks(popup,qs,'Quests here / nearby');marker.bindPopup(popup,{maxWidth:330,maxHeight:260});marker.bindTooltip(document.createTextNode(title));marker.addTo(layer);}
  }
  const refresh=()=>{draw();refreshPanel();};checkbox.addEventListener('change',draw);document.addEventListener('input',()=>setTimeout(draw,0));document.addEventListener('change',()=>setTimeout(refresh,0));document.addEventListener('click',e=>{if(e.target.closest('#clear-map,#clear-filters'))setTimeout(draw,0);});window.addEventListener('storage',draw);window.addEventListener('hashchange',()=>setTimeout(refresh,0));window.addEventListener('popstate',()=>setTimeout(refresh,0));api.map?.on('moveend',()=>{if(lastWorld!==currentWorld())draw();});refresh();window.SaqrimQuestMap={layer,quests,candidates,refresh:draw};
 }
})();
