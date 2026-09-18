'use strict';
(async()=>{
 const $=id=>document.getElementById(id),U=window.SaqrimBlessingsUI,F=window.SaqrimFaithData,S=window.SaqrimStonesData;
 if(!$('faith-cards')||!U||!F||!S)return;
 const section=document.body.dataset.faithSection||'all';
 const allowed=section==='stones'?['stones']:section==='shrines'?['deities','shrines']:['deities','shrines','stones'];
 let tab=allowed[0],selectedRace='Breton',mainPlaces=[],realmPlaces=window.SaqrimWorldData?.places||[],single=null;
 const pantheons=new Set(),checks=[],worlds=[...new Set(F.shrines.map(s=>s.world))];
 const resolve=entry=>U.resolve(entry,mainPlaces,realmPlaces),terms=()=>U.norm($('faith-page-search').value).trim().split(/\s+/).filter(Boolean);
 const matchText=(value,q)=>q.every(t=>U.norm(value).includes(t));
 const realmOK=s=>!$('faith-page-world').value||s.world===$('faith-page-world').value;
 const pinOK=s=>!$('faith-pinned-only').checked||resolve(s);
 function shrineOK(s){return realmOK(s)&&pinOK(s)&&(!pantheons.size||s.deities.some(id=>pantheons.has(F.deities.find(d=>d.id===id)?.pantheon)));}
 function updateURL(hash=''){const u=new URL(location.href);u.search='';u.searchParams.set('tab',tab);u.searchParams.set('race',selectedRace);if($('faith-page-search').value)u.searchParams.set('q',$('faith-page-search').value);if($('faith-page-world').value)u.searchParams.set('world',$('faith-page-world').value);if($('faith-pinned-only').checked)u.searchParams.set('pinned','1');for(const p of pantheons)u.searchParams.append('pantheon',p);u.hash=hash;history.replaceState(null,'',u.pathname+u.search+u.hash);window.dispatchEvent(new Event('saqrim-reference-view'));}
 function say(text){$('faith-page-message').textContent=text;$('faith-page-message').hidden=false;}
 const raceControl=U.raceSelect('faith-page-race-select','Breton',r=>{selectedRace=r;single=null;render();updateURL();});$('faith-page-race').append(raceControl.label);
 for(const world of worlds){const o=U.node('option','',U.worldName(world));o.value=world;$('faith-page-world').append(o);}
 const field=U.node('fieldset');field.append(U.node('legend','','Pantheon'));
 for(const group of new Set(F.deities.map(d=>d.pantheon))){const label=U.node('label','faith-check'),input=U.node('input');input.type='checkbox';input.value=group;input.dataset.pantheon=group;label.append(input,document.createTextNode(group));field.append(label);checks.push(input);input.addEventListener('change',()=>{input.checked?pantheons.add(group):pantheons.delete(group);single=null;render();updateURL();});}$('faith-pantheons').append(field);
 const notes=section==='stones'?S.notes:section==='shrines'?F.notes:[...F.notes,...S.notes];
 for(const text of notes)$('faith-page-notes').append(U.node('p','',text));
 const options=()=>({resolve,race:selectedRace,onShrine:id=>{single=id;tab='shrines';updateURL('shrine='+id);render();$('faith-single').scrollIntoView({block:'start',behavior:'instant'});}});
 function render(){const q=terms(),oldOpen=new Set([...$('faith-cards').querySelectorAll('.faith-card[open]')].map(n=>n.id));let pool=[];$('faith-cards').replaceChildren();$('faith-single').replaceChildren();$('faith-single').hidden=!single;$('faith-pantheons').hidden=tab==='stones';$('faith-page-race').hidden=tab!=='stones';
  document.querySelectorAll('[data-faith-tab]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.faithTab===tab)));
  if(single){const s=F.shrines.find(s=>s.id===single);if(s){const back=U.node('button','','Show all matching shrine locations');back.addEventListener('click',()=>{single=null;updateURL();render();});$('faith-single').append(back,U.shrineCard(s,options()));$('faith-page-count').textContent=s.name+' · '+s.deities.length+' deity profile'+(s.deities.length===1?'':'s');}return;}
  if(tab==='deities'){pool=F.deities.filter(d=>(!pantheons.size||pantheons.has(d.pantheon))&&d.shrines.some(id=>{const s=F.shrines.find(s=>s.id===id);return realmOK(s)&&pinOK(s);})&&matchText([d.name,d.pantheon,d.eligibility,d.blessing,d.follower,d.devotee,d.worship,...d.shrines.map(id=>{const s=F.shrines.find(s=>s.id===id);return s.name+' '+s.directions+' '+s.mapPlace;})].join(' '),q));for(const d of pool)$('faith-cards').append(U.deityCard(d,{...options(),open:oldOpen.has('deity-'+d.id)}));$('faith-page-count').textContent=pool.length+' / '+F.deities.length+' deity profiles';$('faith-page-note').textContent='Open a god for the shrine blessing, follower benefit and 100%-favor Devotee ability. Location and pantheon filters combine; multiple pantheons use OR.';}
  else if(tab==='shrines'){pool=F.shrines.filter(s=>shrineOK(s)&&matchText(s.name+' '+s.directions+' '+s.mapPlace+' '+s.deities.map(id=>F.deities.find(d=>d.id===id)?.name).join(' '),q));for(const s of pool){const row=U.locationRow(s,options());row.id='shrine-'+s.id;$('faith-cards').append(row);}$('faith-page-count').textContent=pool.length+' / '+F.shrines.length+' shrine-location records · '+pool.filter(s=>resolve(s)).length+' with map references';$('faith-page-note').textContent='One temple can contain several shrines. Markers use existing named areas; nearby clues do not place the shrine directly on that landmark.';}
  else{pool=S.stones.filter(s=>realmOK(s)&&pinOK(s)&&matchText(s.name+' '+s.directions+' '+JSON.stringify(S.effects[selectedRace][s.key]),q));for(const s of pool)$('faith-cards').append(U.stoneCard(s,selectedRace,{resolve,open:oldOpen.has('stone-'+s.id)}));$('faith-page-count').textContent=pool.length+' / 13 stones · '+selectedRace+' preview'+(selectedRace==='Breton'?' · both effects shown':'');$('faith-page-note').textContent='13 Skyrim standing stones × 10 races. '+(selectedRace==='Breton'?'Bretons have a Freyr effect plus a Stones of Galen effect for each stone. ':'Open a stone to compare all races. ')+'Solstheim All-Maker Stones are separate and not included in this Freyr table.';}
  if(!pool.length)$('faith-cards').append(U.node('p','faith-empty','No matches. Clear a filter or try another view; the thirteen Freyr stones are on mainland Skyrim.'));
 }
 function reset(){pantheons.clear();checks.forEach(n=>n.checked=false);$('faith-page-search').value='';$('faith-page-world').value='';$('faith-pinned-only').checked=false;single=null;render();updateURL();}
 function followURL(){
  const p=new URLSearchParams(location.search);tab=['deities','shrines','stones'].includes(p.get('tab'))?p.get('tab'):allowed[0];
  let hash='';try{hash=decodeURIComponent(location.hash.slice(1));}catch(_){}
  const parts=/^(deity|stone|shrine)=(.+)$/.exec(hash);if(parts)tab=parts[1]==='stone'?'stones':parts[1]==='shrine'?'shrines':'deities';
  if(!allowed.includes(tab)){
   const target=new URL(tab==='stones'?'standing-stones.html':'shrines.html',location.href);target.search=location.search;target.searchParams.set('tab',tab);target.hash=location.hash;location.replace(target.href);return;
  }
  selectedRace=U.race(p.get('race'));raceControl.select.value=selectedRace;$('faith-page-search').value=p.get('q')||'';$('faith-page-world').value=worlds.includes(p.get('world'))?p.get('world'):'';$('faith-pinned-only').checked=p.get('pinned')==='1';pantheons.clear();for(const v of p.getAll('pantheon'))if(F.deities.some(d=>d.pantheon===v))pantheons.add(v);checks.forEach(c=>c.checked=pantheons.has(c.value));single=null;
  if(parts?.[1]==='shrine'&&F.shrines.some(s=>s.id===parts[2]))single=parts[2];
  render();window.dispatchEvent(new Event('saqrim-reference-view'));
  if(parts&&parts[1]!=='shrine'){const card=document.getElementById(parts[1]+'-'+parts[2]);if(card){card.open=true;requestAnimationFrame(()=>card.scrollIntoView({block:'start',behavior:'instant'}));}}
 }
 document.querySelectorAll('[data-faith-tab]').forEach(b=>b.addEventListener('click',()=>{if(!allowed.includes(b.dataset.faithTab))return;tab=b.dataset.faithTab;single=null;render();updateURL();}));
 $('faith-page-search').addEventListener('input',()=>{single=null;render();updateURL();});for(const id of ['faith-page-world','faith-pinned-only'])$(id).addEventListener('change',()=>{single=null;render();updateURL();});$('faith-clear').addEventListener('click',reset);
 $('faith-share').addEventListener('click',async()=>{try{await navigator.clipboard.writeText(location.href);say('Reference-view link copied. No private notes or progress are included.');}catch(_){say('Copy this page’s address from your browser to share these filters and race preview.');}});window.addEventListener('hashchange',followURL);window.addEventListener('popstate',followURL);
 try{const response=await fetch('map-locations.json');if(response.ok){const geo=await response.json();mainPlaces=geo.locations.map(([name,x,y])=>({name,x,y}));}}catch(_){say('Map coordinates are unavailable in this visit. The deity and stone reference remains readable.');}
 followURL();window.SaqrimBlessingsPage={render,reset,resolve,section,get tab(){return tab;},get race(){return selectedRace;},get mainPlaces(){return mainPlaces;},get realmPlaces(){return realmPlaces;}};
})();
