/* Static, read-only map/index. No console access, geolocation, or storage writes. */
'use strict';
(async()=>{
 const $=id=>document.getElementById(id), KEY='skyrimLootChoices_v202_20260917';
 const el=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n;};
 const norm=s=>String(s||'').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 const slug=s=>norm(s).replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
 const kinds={site:'Named site · approximate area',hub:'City / town reference',vendor:'Vendor town · stock not guaranteed',quest:'Quest / clue hub',nearby:'Nearby landmark · NOT the pickup spot'};
 let records=[],places=[],map=null,pins=null,area=null,visiblePlaces=[],filteredItems=[],selectedPlace=null,selectedItem=null,mode='places',limit=40,choices={};
 const selected={},controls=[],bounds=[[0,0],[768,1024]];
 function readChoices(){try{const v=JSON.parse(localStorage.getItem(KEY)||'{}');choices=v&&typeof v==='object'&&!Array.isArray(v)?v:{};}catch(_){choices={};}}
 function pick(r){const v=choices[r.id]||r.raw['My choice'];return ['Want','Maybe','Skip'].includes(v)?v:'Undecided';}
 function external(url,text){const a=el('a','',text);try{const u=new URL(url);if(!['https:','http:'].includes(u.protocol))return null;a.href=u.href;}catch(_){return null;}a.target='_blank';a.rel='noopener noreferrer';return a;}
 function termsMatch(text,terms){return terms.every(t=>text.includes(t));}
 function itemMatches(r,terms){
  if($('picks-only').checked&&!['Want','Maybe'].includes(pick(r)))return false;
  if($('world').value&&r.world!==$('world').value)return false;
  if($('unpinned-only').checked&&r.links.length)return false;
  for(const [group,values]of Object.entries(selected)){if(group==='place')continue;if(values.size&&!r.meta.tags[group].some(v=>values.has(v)))return false;}
  return termsMatch(r.search,terms);
 }
 function itemCard(r,link){
  const a=el('article','item-card');a.dataset.item=r.id;
  a.append(el('h3','',r.id+' · '+r.raw.Target));
  a.append(el('p','type-line',r.raw.Type+' · #'+r.raw['LO #']+' '+r.raw['Installed mod']));
  if(link)a.append(el('p','location-hint',kinds[link.kind]+(link.note?' — '+link.note:'')));
  if(!r.links.length)a.append(el('p','location-hint',r.reason+' · '+r.world));
  a.append(el('p','',r.raw['Effect / interest']));const audit=SaqrimTags.auditNode(r.raw);if(audit)a.append(audit);
  const where=el('p');where.append(el('strong','','Where / unlock: '),document.createTextNode(r.raw['Where / unlock']||'Not established'));a.append(where);
  const details=el('details');details.append(el('summary','','Evidence, requirements & sources'));
  for(const field of ['When to look','Acquisition','Evidence status','Qualifications','Source scope'])if(r.raw[field])details.append(el('p','',field+': '+r.raw[field]));
  const sourceLinks=el('p','links');String(r.raw['Source URL']||'').split(/\s*[|\n]\s*/).forEach((url,i)=>{const a=external(url,'Original source '+(i+1));if(a)sourceLinks.append(a);});details.append(sourceLinks);a.append(details);
  const actions=el('div','links');const catalog=el('a','','Open full catalog entry →');catalog.href='./#'+r.id;actions.append(catalog);
  if(!link)for(const assoc of r.links){const b=el('button','text-button','Show '+assoc.place+' on map');b.type='button';b.addEventListener('click',()=>selectPlace(assoc.place));actions.append(b);}
  a.append(actions);return a;
 }
 function detailFocus(){if(matchMedia('(max-width:850px)').matches){if(document.body.classList.contains('map-expanded'))setExpanded(false);$('details').scrollIntoView({behavior:'instant',block:'start'});}$('details').focus({preventScroll:true});}
 function setHash(value){history.replaceState(null,'',location.pathname+location.search+'#'+value);}
 function selectPlace(name,{hash=true,focus=true,pan=true}={}){
  const p=places.find(x=>x.name===name);if(!p)return;
  selectedPlace=p.name;selectedItem=null;if(hash)setHash('place='+encodeURIComponent(p.name));
  if(map){if(pan)map.setView(p.latlng,Math.max(map.getZoom(),0.6),{animate:false});if(area)map.removeLayer(area);const radius=SaqrimMapLinks.cities.has(p.name)?12:6;area=L.rectangle([[p.latlng[0]-radius,p.latlng[1]-radius],[p.latlng[0]+radius,p.latlng[1]+radius]],{color:'#efcc8a',weight:2,dashArray:'5 5',fillOpacity:0.12,interactive:false}).addTo(map);}
  const detail=$('details');detail.replaceChildren(el('h2','',p.name),el('p','location-hint',p.type+' · Approximate exterior reference area'));
  detail.append(el('p','hint','The highlighted area is a navigation reference, not an exact interior entrance, chest or NPC coordinate. Follow each original location note.'));
  const shown=p.items.filter(r=>filteredItems.includes(r));
  if(!p.items.length)detail.append(el('p','','No catalog items have been linked here yet. This does not mean this place has no loot.'));
  else if(!shown.length)detail.append(el('p','',p.items.length+' catalog records are linked here, but your filters exclude them. Clear filters to see them.'));
  else {detail.append(el('p','',shown.length+' matching catalog '+(shown.length===1?'record':'records')+' linked to this area.'));for(const r of shown)detail.append(itemCard(r,r.links.find(a=>a.place===p.name)));}
  const link=el('a','', 'Link to this place');link.href='#place='+encodeURIComponent(p.name);detail.append(link);
  updateList();if(focus)detailFocus();
 }
 function selectItem(id,{hash=true,focus=true}={}){
  const r=records.find(x=>x.id===id);if(!r)return;
  selectedItem=r.id;selectedPlace=null;if(hash)setHash(id);
  const detail=$('details');detail.replaceChildren(el('h2','','Item location'),itemCard(r));
  if(!r.links.length)detail.prepend(el('p','location-hint','No positioned pin for this record. The location notes below are still available.'));
  if(map&&area){map.removeLayer(area);area=null;}
  if(map&&r.links.length){const p=places.find(p=>p.name===r.links[0].place);map.setView(p.latlng,Math.max(map.getZoom(),0.6),{animate:false});}
  updateList();if(focus)detailFocus();
 }
 function markerPopup(group){
  const box=el('div');box.append(el('strong','',group.length===1?group[0].name:group.length+' nearby places'));
  if(group.length===1){const p=group[0];box.append(el('p','',p.matched.length?p.matched.length+' matching catalog records · area reference':'Known place · no matching catalog leads'));const b=el('button','','View place & items');b.type='button';b.addEventListener('click',()=>selectPlace(p.name));box.append(b);}
  else {box.append(el('p','','Choose a place:'));for(const p of group){const b=el('button','',p.name);b.type='button';b.addEventListener('click',()=>selectPlace(p.name));box.append(b);}}
  return box;
 }
 function drawPins(){
  if(!map||!pins)return;pins.clearLayers();const clusters=new Map();
  for(const p of visiblePlaces){const px=map.project(p.latlng,map.getZoom());const key=Math.floor(px.x/38)+','+Math.floor(px.y/38);if(!clusters.has(key))clusters.set(key,[]);clusters.get(key).push(p);}
  for(const group of clusters.values()){
   const hasLoot=group.some(p=>p.matched.length),isCluster=group.length>1;
   const pos=[group.reduce((s,p)=>s+p.latlng[0],0)/group.length,group.reduce((s,p)=>s+p.latlng[1],0)/group.length];
   const count=isCluster?group.length:(hasLoot?group[0].matched.length:'');
   const icon=L.divIcon({className:'map-icon',html:'<span class="map-pin '+(isCluster?'cluster':hasLoot?'':'known')+'">'+count+'</span>',iconSize:[30,30],iconAnchor:[15,15]});
   const title=isCluster?group.length+' grouped places':group[0].name;
   const marker=L.marker(pos,{icon,title,alt:title,keyboard:true}).addTo(pins);
   marker.bindTooltip(document.createTextNode(title));
   marker.on('click',()=>{
    if(isCluster&&map.getZoom()<2.5){map.fitBounds(L.latLngBounds(group.map(p=>p.latlng)),{padding:[45,45],maxZoom:Math.min(3,map.getZoom()+1.25),animate:false});}
    else {marker.bindPopup(markerPopup(group),{maxHeight:260,autoPan:true}).openPopup();if(!isCluster)selectPlace(group[0].name,{focus:false,pan:false});}
   });
  }
 }
 function updateList(){
  const list=$('location-index');list.replaceChildren();const entries=mode==='places'?visiblePlaces:filteredItems;
  $('places-tab').setAttribute('aria-pressed',String(mode==='places'));$('items-tab').setAttribute('aria-pressed',String(mode==='items'));$('item-options').hidden=mode!=='items';
  $('result-count').textContent=mode==='places'?entries.length+' matching places · '+visiblePlaces.reduce((s,p)=>s+p.matched.length,0)+' linked item associations':entries.length+' matching item records · '+entries.filter(r=>!r.links.length).length+' without a positioned pin';
  for(const entry of entries.slice(0,limit)){
   const b=el('button','list-row');b.type='button';
   if(mode==='places'){b.classList.toggle('is-selected',selectedPlace===entry.name);b.append(el('strong','',entry.name),el('small','',entry.type+' · '+(entry.matched.length?entry.matched.length+' catalog leads':'known place')));b.addEventListener('click',()=>selectPlace(entry.name));}
   else {b.classList.toggle('is-selected',selectedItem===entry.id);b.append(el('strong','',entry.raw.Target),el('small','id',entry.id+' · '+entry.world),el('small','',entry.links.length?'Reference pin: '+entry.links.map(a=>a.place).join(', '):entry.reason));b.addEventListener('click',()=>selectItem(entry.id));}
   list.append(b);
  }
  if(!entries.length)list.append(el('p','hint','No matches. Clear filters, switch to All item locations, or try a different search.'));
  $('more').hidden=entries.length<=limit;$('more').textContent='Show more ('+Math.max(0,entries.length-limit)+' remaining)';
 }
 function render(){
  const terms=norm($('map-search').value).trim().split(/\s+/).filter(Boolean);
  filteredItems=records.filter(r=>itemMatches(r,terms));
  const itemFilters=Object.entries(selected).some(([k,s])=>k!=='place'&&s.size)||$('picks-only').checked||$('world').value||$('unpinned-only').checked;
  visiblePlaces=[];
  for(const p of places){p.matched=p.items.filter(r=>filteredItems.includes(r));if(selected.place.size&&!selected.place.has(p.type))continue;
   if(p.matched.length){if($('show-linked').checked)visiblePlaces.push(p);}
   else if($('show-known').checked&&!itemFilters&&termsMatch(norm(p.name+' '+p.type),terms))visiblePlaces.push(p);
  }
  const count=Object.values(selected).reduce((s,v)=>s+v.size,0)+Number($('picks-only').checked)+Number(!!$('world').value)+Number($('unpinned-only').checked);
  $('filter-count').textContent=count?'· '+count+' active':'';limit=40;drawPins();updateList();
  // Keep the selected panel consistent with updated item filters, without panning.
  if(selectedPlace)selectPlace(selectedPlace,{hash:false,focus:false,pan:false});
 }
 function reset(){for(const s of Object.values(selected))s.clear();controls.forEach(c=>c.checked=false);$('map-search').value='';$('show-linked').checked=true;$('show-known').checked=true;$('picks-only').checked=false;$('world').value='';$('unpinned-only').checked=false;render();}
 function setExpanded(value){document.body.classList.toggle('map-expanded',value);$('large-map').setAttribute('aria-pressed',String(value));$('large-map').textContent=value?'Close larger map':'Larger map';requestAnimationFrame(()=>map?.invalidateSize());}
 function followHash(){let hash;try{hash=decodeURIComponent(location.hash.slice(1));}catch(_){return;}if(/^W\d{3}$/.test(hash))selectItem(hash,{hash:false});else if(hash.startsWith('place='))selectPlace(hash.slice(6),{hash:false});}
 try{
  const responses=await Promise.all([fetch('catalog-current.html?v=1'),fetch('map-locations.json')]);if(responses.some(r=>!r.ok))throw Error('Map data request failed');
  const [html,geo]=await Promise.all([responses[0].text(),responses[1].json()]);const parsed=new DOMParser().parseFromString(html,'text/html');const raw=JSON.parse(parsed.getElementById('dataset').textContent);
  if(raw.length!==633||new Set(raw.map(r=>r['Catalog ID'])).size!==633||geo.locations.length!==364||geo.coordinateOrigin!=='bottom-left')throw Error('Map/catalog integrity check failed');
  places=geo.locations.map(([name,x,y])=>{if(!name||!Number.isFinite(x)||!Number.isFinite(y)||x<0||y<0||x>8192||y>6144)throw Error('Invalid map point');return {name,x,y,latlng:[y/8,x/8],type:SaqrimMapLinks.placeType(name),items:[],matched:[]};});
  const byName=new Map(places.map(p=>[p.name,p]));if(byName.size!==364)throw Error('Duplicate reference place');
  records=raw.map(r=>{const id=r['Catalog ID'],meta=SaqrimTags.classify(r),links=SaqrimMapLinks.links[id]||[];for(const a of links)if(!byName.has(a.place))throw Error('Unmatched reference place '+a.place);return {id,raw:r,meta,links,world:SaqrimMapLinks.world(r),reason:SaqrimMapLinks.reason(r),search:norm(Object.values(r).join(' ')+' '+Object.values(meta.tags).flat().join(' ')+' '+links.map(a=>a.place).join(' '))};});
  for(const r of records)for(const a of r.links)byName.get(a.place).items.push(r);
  readChoices();const groups=[['place','Known-place type',[...new Set(places.map(p=>p.type))].sort()],...SaqrimTags.groups.filter(g=>g[0]!=='choice')];
  for(const [group,label,values]of groups){selected[group]=new Set();const section=el('details','facet');section.append(el('summary','',label));const field=el('fieldset');field.append(el('legend','',label));for(const value of values){const label=el('label');const input=el('input');input.type='checkbox';input.dataset.group=group;input.value=value;label.append(input,document.createTextNode(value));field.append(label);controls.push(input);input.addEventListener('change',()=>{if(input.checked)selected[group].add(value);else selected[group].delete(value);render();});}section.append(field);$('map-facets').append(section);}
  [...new Set(records.map(r=>r.world))].sort().forEach(w=>{const o=el('option','',w);o.value=w;$('world').append(o);});
  const linked=records.filter(r=>r.links.length).length;const linkedPlaces=places.filter(p=>p.items.length).length;
  $('coverage').textContent=places.length+' known places · '+linked+' catalog records linked to '+linkedPlaces+' reference areas · All 633 item-location notes searchable';
  if(window.L){
   map=L.map('map',{crs:L.CRS.Simple,minZoom:-2,maxZoom:3,zoomSnap:0.25,zoomDelta:0.5,maxBounds:[[-180,-180],[948,1204]],maxBoundsViscosity:0.7});
   const image=L.imageOverlay('assets/map/skyrim.webp',bounds,{attribution:'Skyrim artwork © Bethesda · <a href="assets/map/SOURCES.txt" target="_blank" rel="noopener">Sources / approximate coordinates</a>'}).addTo(map);
   image.on('error',()=>{$('map-error').textContent='Map artwork could not load. The item and location index still works.';$('map-error').hidden=false;});
   pins=L.layerGroup().addTo(map);map.fitBounds(bounds,{padding:[8,8],animate:false});map.on('zoomend',drawPins);
  }else{$('map-error').textContent='The interactive map library could not load. You can still search the location index.';$('map-error').hidden=false;}
  $('map-search').disabled=false;$('map-search').addEventListener('input',render);
  for(const id of ['show-linked','show-known','picks-only','world','unpinned-only'])$(id).addEventListener('change',render);
  $('clear-map').addEventListener('click',reset);$('more').addEventListener('click',()=>{limit+=40;updateList();});
  $('places-tab').addEventListener('click',()=>{mode='places';limit=40;updateList();});$('items-tab').addEventListener('click',()=>{mode='items';limit=40;updateList();});
  $('reset-view').addEventListener('click',()=>map?.fitBounds(bounds,{padding:[8,8],animate:false}));
  $('fit-results').addEventListener('click',()=>{if(map&&visiblePlaces.length)map.fitBounds(L.latLngBounds(visiblePlaces.map(p=>p.latlng)),{padding:[35,35],maxZoom:1.5,animate:false});});
  $('large-map').addEventListener('click',()=>setExpanded(!document.body.classList.contains('map-expanded')));
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&document.body.classList.contains('map-expanded')){setExpanded(false);$('large-map').focus();}});
  document.addEventListener('click',e=>{const b=e.target.closest('[data-place]');if(b)selectPlace(b.dataset.place);});
  window.addEventListener('storage',e=>{if(e.key===KEY||e.key===null){readChoices();render();}});
  window.addEventListener('hashchange',followHash);if(window.ResizeObserver&&map)new ResizeObserver(()=>map.invalidateSize()).observe($('map'));
  render();window.SaqrimMap={records,places,map,render,reset,selectPlace,selectItem,selected,get visiblePlaces(){return visiblePlaces;},get filteredItems(){return filteredItems;},linkedCount:linked,linkedPlaceCount:linkedPlaces};followHash();
 }catch(e){$('coverage').textContent='Map data could not load.';$('map-error').textContent='Reload to try again. The original location notes remain in the Loot catalog.';$('map-error').hidden=false;console.error(e);}
})();
