'use strict';
(async()=>{
 const $=id=>document.getElementById(id),KEY='skyrimLootChoices_v202_20260917';
 const node=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n;};
 const norm=s=>String(s||'').toLowerCase().replace(/[’‘]/g,"'");
 const kinds={site:'Named site · reference only',vendor:'Vendor / camp · stock not guaranteed',quest:'Quest or clue · NOT the reward position',nearby:'Nearby landmark · NOT the pickup spot',region:'Regional reference · exact location pending',documented:'Documented name · geographic position pending',historical:'Historical lead · current port unverified'};
 let records=[],places=[],filtered=[],shownPlaces=[],world=null,map=null,image=null,markers=null,selectedRecord=null,selectedPlace=null,limit=35,mode='places',choices={},generation=0,imageFailed=false;
 const selected={},checks=[],views=new Map(),worlds=SaqrimWorldData.worlds;
 const byWorld=id=>worlds.find(w=>w.id===id);
 const pkey=p=>p.world+'::'+p.name;
 function readChoices(){try{const v=JSON.parse(localStorage.getItem(KEY)||'{}');choices=v&&typeof v==='object'&&!Array.isArray(v)?v:{};}catch(_){choices={};}}
 function pick(r){const v=choices[r.id];return ['Want','Maybe','Skip','Undecided'].includes(v)?v:(r.raw['My choice']||'Undecided');}
 function say(t){$('feedback').textContent=t;$('feedback').hidden=false;clearTimeout(say.timer);say.timer=setTimeout(()=>$('feedback').hidden=true,6000);}
 function sourceLink(url,text){const a=node('a','',text);if(/^https?:\/\//i.test(url)){a.href=url;a.target='_blank';a.rel='noopener noreferrer';}return a;}
 function terms(){return norm($('world-search').value).trim().split(/\s+/).filter(Boolean);}
 function matches(r,omit=''){
  if(!r.worlds.includes(world.id))return false;
  if($('picks-only').checked&&!['Want','Maybe'].includes(pick(r)))return false;
  if($('unpinned-only').checked&&r.links.some(l=>l.world===world.id&&l.pin))return false;
  for(const [group,set]of Object.entries(selected))if(group!==omit&&set.size&&![...set].some(v=>r.meta.tags[group]?.includes(v)))return false;
  return terms().every(t=>r.search.includes(t)||r.links.some(l=>norm(l.place).includes(t)));
 }
 function itemFilters(){return $('picks-only').checked||$('unpinned-only').checked||Object.values(selected).some(s=>s.size);}
 function hashForPlace(p){return '#place='+encodeURIComponent(p.name);}
 function updateURL(hash='',push=false){const u=new URL(location.href);u.searchParams.set('world',world.id);u.hash=hash;(push?history.pushState:history.replaceState).call(history,null,'',u.pathname+u.search+u.hash);}
 function heading(){const p=$('selection');p.replaceChildren(node('h2','','Select a place or item.'),node('p','','The original directions and source qualifications appear here. A nearby landmark or quest start is not an exact pickup position.'));}
 function itemCard(r){
  const a=node('article','loot-item');a.dataset.item=r.id;
  a.append(node('div','meta',r.id+' · #'+r.raw['LO #']+' '+r.raw['Installed mod']+' · '+pick(r)),node('h3','',r.raw.Target));
  const tags=node('div','tag-row');for(const t of new Set(Object.values(r.meta.tags).flat()))tags.append(node('span','tag',t));a.append(tags);
  for(const [label,key]of [['Where / unlock','Where / unlock'],['Effect / interest','Effect / interest'],['Evidence','Evidence status'],['Qualifications','Qualifications']]){if(!r.raw[key])continue;const p=node('p');p.append(node('strong','',label+': '),document.createTextNode(r.raw[key]));a.append(p);}
  const audit=SaqrimTags.auditNode(r.raw);if(audit)a.append(audit);const refs=node('div','source-links');const full=node('a','','Open full catalog entry →');full.href='./#'+r.id;refs.append(full);
  const urls=(r.raw['Source URL']||'').split(/\s*[|\n]\s*/).filter(u=>/^https?:\/\//i.test(u));urls.forEach((u,i)=>refs.append(sourceLink(u,urls.length>1?'Original source '+(i+1):'Original source')));a.append(refs);
  const local=r.links.filter(l=>l.world===world.id);
  if(!local.length)a.append(node('p','hint','No geographic pin has been established for this record. Its directions above remain available.'));
  for(const l of local){const box=node('div','association');const b=node('button','',(l.pin?'Show reference pin · ':'Read location notes · ')+l.place);b.type='button';b.addEventListener('click',()=>selectPlace(l.place));box.append(b,node('p','',kinds[l.kind]||l.kind));if(l.note)box.append(node('p','',l.note));a.append(box);}
  return a;
 }
 function focusDetails(){requestAnimationFrame(()=>{$('selection').scrollIntoView({block:'nearest',behavior:'instant'});$('selection').focus({preventScroll:true});});}
 function selectItem(id,{focus=true,hash=true}={}){
  const r=records.find(r=>r.id===id);if(!r)return;
  if(!r.worlds.includes(world.id)){
   const target=r.worlds.find(id=>byWorld(id));
   if(!target){location.href='map.html#'+id;return;}
   switchWorld(target,{push:false,clearSearch:true});
  }
  selectedRecord=r;selectedPlace=null;
  const panel=$('selection');panel.replaceChildren(node('h2','',r.raw.Target),itemCard(r));
  const p=r.links.find(l=>l.world===world.id&&l.pin)?.location;
  if(p&&world.kind==='map'){map.setView([p.y,p.x],Math.max(map.getZoom(),1.5),{animate:false});}
  if(hash)updateURL('#'+id);drawMarkers();if(focus)focusDetails();
 }
 function selectPlace(name,{focus=true,hash=true}={}){
  const p=places.find(p=>p.world===world.id&&p.name===name);if(!p)return;
  selectedPlace=p;selectedRecord=null;
  const panel=$('selection');panel.replaceChildren(node('h2','',p.name));
  panel.append(node('p','notice',p.pin?'Approximate reference point—not an exact chest, shelf, room or NPC coordinate. Read the individual directions below.':'This location name is documented, but its geographic position has not been established. No pin has been invented.'));
  if(p.note)panel.append(node('p','hint',p.note));
  const matchesHere=p.items.filter(r=>matches(r));
  if(!matchesHere.length)panel.append(node('p','hint',p.items.length?'No linked records match your current filters. Clear filters to see the linked notes.':'No catalog item is linked here yet. That does not mean this place has no loot.'));
  for(const r of matchesHere)panel.append(itemCard(r));
  if(p.pin&&world.kind==='map')map.setView([p.y,p.x],Math.max(map.getZoom(),1.5),{animate:false});
  if(hash)updateURL(hashForPlace(p));drawMarkers();if(focus)focusDetails();
 }
 function drawMarkers(){
  if(!markers)return;markers.clearLayers();if(!world||world.kind!=='map')return;
  for(const p of shownPlaces){if(!p.pin)continue;const chosen=selectedPlace===p||selectedRecord?.links.some(l=>l.location===p);const has=p.matches.length>0;
   const marker=L.circleMarker([p.y,p.x],{radius:chosen?10:7,color:chosen?'#ffffff':has?'#efcc8a':'#a9d7ef',weight:chosen?3:2,fillColor:has?'#dbad60':'#427e9b',fillOpacity:.9,bubblingMouseEvents:false});
   marker.bindTooltip(node('span','',p.name+(has?' · '+p.matches.length+' item lead'+(p.matches.length===1?'':'s'):'')),{direction:'top'}).on('click',()=>selectPlace(p.name)).addTo(markers);
  }
 }
 function row(text,sub,callback){const b=node('button','list-row');b.type='button';b.append(node('b','',text),node('small','',sub));b.addEventListener('click',callback);return b;}
 function renderGuide(){
  const g=$('guide-places');g.replaceChildren();
  for(const p of shownPlaces){const b=node('button','guide-place');b.type='button';b.append(node('strong','',p.name),node('span','',p.matches.length+' linked record'+(p.matches.length===1?'':'s')+(p.pin?' · reference pin':' · unpinned')));b.addEventListener('click',()=>selectPlace(p.name));g.append(b);}
  const noSite=filtered.filter(r=>!r.links.some(l=>l.world===world.id));
  if(noSite.length){const b=node('button','guide-place');b.type='button';b.append(node('strong','','Other item-location notes'),node('span','',noSite.length+' records without a mapped site'));b.addEventListener('click',()=>{mode='items';limit=35;renderList();$('world-list').scrollIntoView({block:'start',behavior:'instant'});});g.append(b);}
  if(!g.children.length)g.append(node('p','hint','No current matches. Clear a filter or switch to the item list.'));
 }
 function renderList(){
  $('place-tab').setAttribute('aria-pressed',String(mode==='places'));$('item-tab').setAttribute('aria-pressed',String(mode==='items'));
  const list=$('world-list');list.replaceChildren();const pool=mode==='places'?shownPlaces:filtered;
  for(const r of pool.slice(0,limit)){
   if(mode==='places')list.append(row(r.name,r.matches.length+' linked item'+(r.matches.length===1?'':'s')+' · '+(r.pin?'reference pin':'geographic position pending'),()=>selectPlace(r.name)));
   else list.append(row(r.id+' · '+r.raw.Target,(r.links.some(l=>l.world===world.id&&l.pin)?'Reference pin available':'Unpinned location note')+' · '+pick(r),()=>selectItem(r.id)));
  }
  if(!pool.length)list.append(node('p','notice',mode==='places'?'No locations match. Try Items for unpinned notes, or clear a filter.':'No items match. Clear a filter or try another world.'));
  $('more').hidden=pool.length<=limit;$('count').textContent=pool.length+' '+(mode==='places'?'locations':'items')+' · '+filtered.length+' catalog matches in this world';
 }
 function render(){
  if(!world)return;filtered=records.filter(r=>matches(r));const allowed=new Set(filtered.map(r=>r.id));const query=terms();
  shownPlaces=places.filter(p=>p.world===world.id).filter(p=>{p.matches=p.items.filter(r=>allowed.has(r.id));return p.matches.length||(!itemFilters()&&query.every(t=>norm(p.name).includes(t)));});
  shownPlaces.sort((a,b)=>b.matches.length-a.matches.length||a.name.localeCompare(b.name));
  for(const c of checks)c.count.textContent=String(records.filter(r=>matches(r,c.group)&&r.meta.tags[c.group]?.includes(c.value)).length);
  $('filter-count').textContent=Object.values(selected).reduce((n,s)=>n+s.size,0)+' active';
  const realm=records.filter(r=>r.worlds.includes(world.id)),pinned=realm.filter(r=>r.links.some(l=>l.world===world.id&&l.pin));
  $('world-coverage').textContent=realm.length+' catalog records · '+places.filter(p=>p.world===world.id).length+' named reference places · '+pinned.length+' records linked to geographic reference pins';
  renderList();renderGuide();drawMarkers();$('fit-pins').disabled=!shownPlaces.some(p=>p.pin);
 }
 function reset(){for(const s of Object.values(selected))s.clear();checks.forEach(c=>c.input.checked=false);$('world-search').value='';$('picks-only').checked=false;$('unpinned-only').checked=false;selectedRecord=selectedPlace=null;limit=35;heading();render();}
 function switchWorld(id,{push=true,clearSearch=true}={}){
  if(id==='skyrim'){location.href='map.html';return;}
  const next=byWorld(id);if(!next)return;
  if(world?.kind==='map'&&map&&map._loaded)views.set(world.id,{center:map.getCenter(),zoom:map.getZoom()});
  world=next;generation++;const token=generation;imageFailed=false;selectedRecord=selectedPlace=null;limit=35;
  if(clearSearch)$('world-search').value='';$('map-world').value=id;$('world-title').textContent=next.name;document.title='Saqrim · '+next.name;
  $('world-note').textContent=next.note;$('world-mode').textContent=next.kind==='guide'?'Location guide · map pending':next.external?'Reference map · external terrain':'Geographic reference map';$('world-mode').classList.toggle('is-guide',next.kind==='guide');
  $('map-tools').hidden=$('map-shell').hidden=next.kind!=='map';$('guide').hidden=next.kind==='map';$('image-status').hidden=true;
  $('credits').replaceChildren(document.createTextNode(next.credit+' '),sourceLink(next.source,'Map / location source'));
  if(image){image.remove();image=null;}markers?.clearLayers();
  document.body.classList.remove('map-expanded');$('large-map').setAttribute('aria-pressed','false');$('large-map').textContent='Larger map';
  if(next.kind==='map'){
   const bounds=L.latLngBounds([0,0],[next.height,next.width]);map.setMaxBounds(bounds.pad(.25));map.invalidateSize();
   image=L.imageOverlay(next.image,bounds,{interactive:false,alt:next.name+' reference terrain'}).addTo(map);
   $('map-caption').textContent='Loading reference terrain…';
   image.on('load',()=>{if(token!==generation)return;$('map-caption').textContent=next.name+' · approximate reference points';});
   image.on('error',()=>{if(token!==generation)return;imageFailed=true;$('image-status').hidden=false;$('image-status').replaceChildren(document.createTextNode('The terrain host did not serve this image. '+(places.some(p=>p.world===id&&p.pin)?'The reference-coordinate pins still work; the grid is not terrain. ':'The original item and location notes remain available below. ')),sourceLink(next.source,'Open the source map page'));
    $('map-caption').textContent='Coordinate-only view · terrain unavailable';
    if(!places.some(p=>p.world===id&&p.pin)){$('map-shell').hidden=$('map-tools').hidden=true;$('guide').hidden=false;$('guide .eyebrow');const label=$('guide').querySelector('.eyebrow');label.textContent='LOCATION NOTES · TERRAIN IMAGE UNAVAILABLE';}
   });
   requestAnimationFrame(()=>{if(token!==generation)return;map.invalidateSize();const v=views.get(id);if(v)map.setView(v.center,v.zoom,{animate:false});else map.fitBounds(bounds,{padding:[12,12],animate:false});});
  }else{$('guide').querySelector('.eyebrow').textContent='LOCATION GUIDE · GEOGRAPHIC OVERLAY PENDING';}
  heading();render();updateURL('',push);
 }
 function followURL(){
  let hash='';try{hash=decodeURIComponent(location.hash.slice(1));}catch(_){return;}
  const requested=new URLSearchParams(location.search).get('world');
  if(/^W\d{3}$/.test(hash)){
   const r=records.find(r=>r.id===hash);if(!r)return;
   const id=r.worlds.includes(requested)?requested:r.worlds.find(id=>byWorld(id));
   if(!id){location.replace('map.html#'+hash);return;}
   if(world?.id!==id)switchWorld(id,{push:false});selectItem(hash,{focus:false});
  }else{
   const id=byWorld(requested)?requested:'solstheim';if(world?.id!==id)switchWorld(id,{push:false});
   if(hash.startsWith('place='))selectPlace(hash.slice(6),{focus:false});
  }
 }
 try{
  const res=await fetch('catalog-current.html?v=1');if(!res.ok)throw Error('Catalog request failed.');const doc=new DOMParser().parseFromString(await res.text(),'text/html');const data=JSON.parse(doc.getElementById('dataset').textContent);
  if(data.length!==633||new Set(data.map(r=>r['Catalog ID'])).size!==633)throw Error('Catalog integrity check failed.');
  places=SaqrimWorldData.places.map(p=>({...p,pin:Number.isFinite(p.x)&&Number.isFinite(p.y),items:[],matches:[]}));const lookup=new Map(places.map(p=>[pkey(p),p]));
  records=data.map(raw=>{const id=raw['Catalog ID'],meta=SaqrimTags.classify(raw);const links=(SaqrimWorldData.links[id]||[]).map(l=>{const location=lookup.get(l.world+'::'+l.place);if(!location)throw Error('Missing reference location: '+l.place);return {...l,location,pin:location.pin};});return {id,raw,meta,links,worlds:SaqrimWorldData.forRecord(raw),search:norm(Object.values(raw).join(' ')+' '+Object.values(meta.tags).flat().join(' '))};});
  for(const r of records)for(const l of r.links)if(!l.location.items.includes(r))l.location.items.push(r);
  for(const w of worlds){const o=node('option','',w.name+(w.kind==='guide'?' · guide':''));o.value=w.id;$('map-world').append(o);}
  for(const [group,title,values]of SaqrimTags.groups.filter(g=>g[0]!=='choice')){
   selected[group]=new Set();const details=node('details','facet');details.append(node('summary','',title));const field=node('fieldset');field.append(node('legend','',title));
   for(const value of values){const label=node('label','tick'),input=node('input');input.type='checkbox';input.dataset.group=group;input.value=value;const count=node('span','','0');count.setAttribute('aria-hidden','true');label.append(input,node('span','',value),count);field.append(label);checks.push({group,value,input,count});input.addEventListener('change',()=>{if(input.checked)selected[group].add(value);else selected[group].delete(value);limit=35;render();});}
   details.append(field);$('facets').append(details);
  }
  map=L.map('world-map',{crs:L.CRS.Simple,minZoom:-3,maxZoom:4,zoomSnap:.25,zoomDelta:.5,scrollWheelZoom:true,attributionControl:true}).setView([0,0],0);map.attributionControl.addAttribution('Reference imagery © its creators / Bethesda');markers=L.layerGroup().addTo(map);
  readChoices();followURL();$('map-world').disabled=$('world-search').disabled=false;
  $('map-world').addEventListener('change',()=>switchWorld($('map-world').value));
  $('world-search').addEventListener('input',()=>{limit=35;render();});for(const id of ['picks-only','unpinned-only'])$(id).addEventListener('change',()=>{limit=35;render();});$('clear-filters').addEventListener('click',reset);
  $('place-tab').addEventListener('click',()=>{mode='places';limit=35;renderList();});$('item-tab').addEventListener('click',()=>{mode='items';limit=35;renderList();});$('more').addEventListener('click',()=>{limit+=35;renderList();});
  $('reset-view').addEventListener('click',()=>map.fitBounds([[0,0],[world.height,world.width]],{padding:[12,12],animate:false}));
  $('fit-pins').addEventListener('click',()=>{const points=shownPlaces.filter(p=>p.pin).map(p=>[p.y,p.x]);if(points.length)map.fitBounds(points,{padding:[35,35],maxZoom:2,animate:false});});
  const large=on=>{document.body.classList.toggle('map-expanded',on);$('large-map').setAttribute('aria-pressed',String(on));$('large-map').textContent=on?'Close larger map':'Larger map';requestAnimationFrame(()=>map.invalidateSize());};
  $('large-map').addEventListener('click',()=>large(!document.body.classList.contains('map-expanded')));window.addEventListener('keydown',e=>{if(e.key==='Escape')large(false);});
  $('share-world').addEventListener('click',async()=>{try{await navigator.clipboard.writeText(location.href);say('World / selected-item link copied.');}catch(_){say('Use your browser’s address bar to copy this world’s link.');}});
  window.addEventListener('hashchange',followURL);window.addEventListener('popstate',followURL);window.addEventListener('storage',e=>{if(e.key===KEY){readChoices();render();}});
  window.SaqrimWorlds={records,places,worlds,map,selected,render,reset,switchWorld,selectItem,selectPlace,get world(){return world;},get filtered(){return filtered;},get shownPlaces(){return shownPlaces;},get imageFailed(){return imageFailed;}};
 }catch(e){$('world-note').textContent='This world view could not load. Your original catalog and mainland map are unchanged.';$('selection').replaceChildren(node('h2','','World view unavailable'),sourceLink(location.origin+location.pathname.replace(/worlds\.html$/,'catalog-source.html'),'Read all original location notes'));console.error(e);}
})();
