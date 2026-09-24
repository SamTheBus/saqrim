'use strict';
(async () => {
 const $=id=>document.getElementById(id), KEY='skyrimLootChoices_v202_20260917', RKEY='saqrimObservedStats_v1';
 const valid=['Undecided','Want','Maybe','Skip'];
 let data=[], records=[], choices={}, ratings={}, single=null, canSave=true, transferName='Saqrim_Backup.json', saveJSON=true;
 const selected={},inputs=[];
 function node(tag,cls,text){const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n;}
 function say(s){$('feedback').textContent=s;$('feedback').hidden=false;}
 function read(key){try{return JSON.parse(localStorage.getItem(key)||'{}');}catch(_){canSave=false;return {};}}
 function write(){try{localStorage.setItem(KEY,JSON.stringify(choices));localStorage.setItem(RKEY,JSON.stringify(ratings));canSave=true;}catch(_){canSave=false;}storageNote();}
 function storageNote(){$('save-status').textContent=canSave?'Your choices and entered ratings are saved in this browser only. Old choice backups still work.':'Browser storage is unavailable. Changes work for this visit only; use Back up before leaving.';}
 function validNumber(n){return typeof n==='number'&&Number.isFinite(n)&&n>=0&&n<=1000000;}
 function sanitizeChoices(obj){const out={};if(!obj||typeof obj!=='object'||Array.isArray(obj))return out;for(const r of data){const id=r['Catalog ID'];if(valid.includes(obj[id]))out[id]=obj[id];}return out;}
 function sanitizeRatings(obj){const out={};if(!obj||typeof obj!=='object'||Array.isArray(obj))return out;for(const r of data){const id=r['Catalog ID'];if(!obj[id]||typeof obj[id]!=='object')continue;const v={};for(const k of ['armor','damage'])if(validNumber(obj[id][k]))v[k]=obj[id][k];if(Object.keys(v).length)out[id]=v;}return out;}
 function pick(r){return choices[r['Catalog ID']]||(valid.includes(r['My choice'])?r['My choice']:'Undecided');}
 function statType(){return /^(armor|damage)-/.exec($('sort').value)?.[1]||null;}
 function value(item,key){return $('stat-source').value==='mine'?(ratings[item.id]?.[key]??null):item.meta.stats[key];}
 function matches(item,except=null){
  const r=item.r,q=$('search').value.toLowerCase().trim();
  if(q&&!q.split(/\s+/).every(t=>item.search.includes(t)))return false;
  if($('mod').value&&String(r['LO #'])!==$('mod').value)return false;
  if($('only-new').checked&&(Number(item.id.slice(1))<=551||Number(item.id.slice(1))>617))return false;
  if($('only-artifact-batch').checked&&r['Artifact batch']!=='Familiar uniques 1')return false;
  for(const [group,set] of Object.entries(selected)){
   if(group===except||!set.size)continue;
   const values=group==='choice'?[pick(r)]:item.meta.tags[group];
   if(!values.some(x=>set.has(x)))return false;
  }
  const key=statType();
  if(key&&$('known-only').checked&&!validNumber(value(item,key)))return false;
  return true;
 }
 function updateChoice(item){const p=pick(item.r);item.card.dataset.choice=p;item.card.querySelector('.pick-select').value=p;item.card.querySelector('.saved-choice').textContent=p==='Undecided'?'':p;}
 function sorted(items){
  const sort=$('sort').value,key=statType();
  return [...items].sort((a,b)=>{
   if(key){const av=value(a,key),bv=value(b,key),ak=validNumber(av),bk=validNumber(bv);if(ak!==bk)return ak?-1:1;if(ak&&av!==bv)return (sort.endsWith('desc')?-1:1)*(av-bv);}
   if(sort==='name')return a.r.Target.localeCompare(b.r.Target)||a.index-b.index;
   if(sort==='id')return Number(a.id.slice(1))-Number(b.id.slice(1));
   if(sort==='mod'){const av=String(a.r['LO #']??'').trim(),bv=String(b.r['LO #']??'').trim();if(Boolean(av)!==Boolean(bv))return av?-1:1;return (Number(av)||0)-(Number(bv)||0)||a.index-b.index;}
   return a.index-b.index;
  });
 }
 function render(){
  const filtered=records.filter(i=>matches(i)),visible=single?filtered.filter(i=>i.id===single):filtered;
  const wanted=data.filter(r=>pick(r)==='Want').length;
  $('count').textContent=`${visible.length} / 633 shown · ${wanted} wanted`;
  const ids=new Set(visible.map(i=>i.id));
  const frag=document.createDocumentFragment();sorted(records).forEach(i=>{i.card.hidden=!ids.has(i.id);frag.append(i.card);});$('catalog').append(frag);
  $('empty').hidden=visible.length!==0;
  const counts={};for(const [group] of SaqrimTags.groups){counts[group]={};for(const i of records){if(!matches(i,group))continue;for(const v of group==='choice'?[pick(i.r)]:i.meta.tags[group])counts[group][v]=(counts[group][v]||0)+1;}}
  for(const {group,val,label} of inputs)label.textContent=counts[group][val]||0;
  const active=$('active-filters');active.replaceChildren();let n=0;
  for(const [group,set] of Object.entries(selected))for(const val of set){n++;const b=node('button','chip',SaqrimTags.groups.find(g=>g[0]===group)[1]+': '+val+' ×');b.type='button';b.setAttribute('aria-label','Remove '+val+' filter');b.addEventListener('click',()=>{set.delete(val);inputs.find(i=>i.group===group&&i.val===val).input.checked=false;single=null;render();});active.append(b);}
  if(single){const b=node('button','chip','Show other matches ×');b.addEventListener('click',()=>{single=null;render();});active.append(b);}
  $('filter-total').textContent=n+' active';
  const key=statType();$('stat-tools').hidden=!key;
  if(key){const known=filtered.filter(i=>validNumber(value(i,key))).length;const totalKnown=records.filter(i=>validNumber(value(i,key))).length;
   $('stat-note').textContent=`${known} displayed matches have a recorded ${key==='armor'?'armor rating':'base damage'} value (${totalKnown} in this catalog view's source). Unknown values go last in either direction. `+($('stat-source').value==='author'?(totalKnown?'Author values are not verified PS5 inventory stats.':'No author base values for this stat have been indexed yet; a numerical ranking is not available from that source.'):'These are your manually entered in-game values, not automatically measured or author base stats.');
  }
  return visible;
 }
 function reset(){for(const set of Object.values(selected))set.clear();for(const x of inputs)x.input.checked=false;$('search').value='';$('mod').value='';$('only-new').checked=false;$('only-artifact-batch').checked=false;$('known-only').checked=false;$('sort').value='catalog';single=null;render();}
 function scrollResults(){$('catalog').scrollIntoView({behavior:'instant',block:'start'});}
 function openHash(){let hash;try{hash=decodeURIComponent(location.hash.slice(1));}catch(_){return;}const i=records.find(i=>i.id===hash);if(i){reset();i.card.open=true;requestAnimationFrame(()=>i.card.scrollIntoView({block:'start',behavior:'instant'}));}else if(/^category-[1-6]$/.test(hash)){reset();const cat=SaqrimTags.groups[0][2][Number(hash.slice(-1))-1];selected.category.add(cat);inputs.find(i=>i.group==='category'&&i.val===cat).input.checked=true;render();scrollResults();}}
 function panel(title,text,name,importing=false){$('transfer-title').textContent=title;$('transfer-text').value=text;$('transfer-text').readOnly=!importing;$('transfer').hidden=false;$('apply-import').hidden=!importing;$('file-label').hidden=!importing;$('save-backup').hidden=importing;$('copy').hidden=importing;transferName=name;saveJSON=name.endsWith('.json');$('transfer').scrollIntoView({block:'start',behavior:'instant'});}
 function backup(){return JSON.stringify({format:'skyrim-loot-choices',version:2,catalogTargets:data.length,exportedAt:new Date().toISOString(),choices:Object.fromEntries(data.map(r=>[r['Catalog ID'],pick(r)])),ratings},null,2);}
 function importBackup(raw){if(raw.length>2*1024*1024)throw Error('Backup is too large.');const parsed=JSON.parse(raw);if(!parsed||typeof parsed!=='object'||Array.isArray(parsed))throw Error('Expected a JSON backup object.');const incoming=sanitizeChoices(parsed.choices||parsed),stats=sanitizeRatings(parsed.ratings||{});if(!Object.keys(incoming).length&&!Object.keys(stats).length)throw Error('No recognized W-numbers and values found.');Object.assign(choices,incoming);for(const [id,v]of Object.entries(stats))ratings[id]={...ratings[id],...v};write();records.forEach(i=>{updateChoice(i);updateStat(i);});single=null;render();say(`Imported ${Object.keys(incoming).length} choices and ${Object.keys(stats).length} personal rating records.`);}
 function updateStat(item){if(!item.statline)return;const {key,input,line}=item.statline;input.value=ratings[item.id]?.[key]??'';const author=item.meta.stats[key];line.textContent=`Author base ${key==='armor'?'armor':'damage'}: ${validNumber(author)?author:'Unknown'} · Your in-game value: ${ratings[item.id]?.[key]??'Not entered'}`;}
 function enrichCard(item){
  const {card,meta,r,id}=item;card.open=false;
  card.querySelectorAll('.js-only').forEach(n=>n.hidden=false);card.querySelectorAll('[disabled]').forEach(n=>n.disabled=false);
  const badges=node('div','tags');const seen=new Set();for(const k of ['school','hand','weapon','armor','slot'])for(const v of meta.tags[k]){const label=v==='Unknown'?(k==='school'?'School':k==='armor'?'Armor class':k==='slot'?'Slot':'Weapon type')+' unknown':v;if(!seen.has(label)){badges.append(node('span','tag',label));seen.add(label);}}
  card.querySelector('summary').insertBefore(badges,card.querySelector('.expand-label'));
  const detail=card.querySelector('.card-body');
  const note=node('div','classification');note.append(node('h4','', 'Browse tags & numeric values'));
  meta.notes.forEach(n=>note.append(node('p','hint',n)));
  for(const u of meta.urls){const a=node('a','', 'Classification / base-value source');a.href=u;a.target='_blank';a.rel='noopener noreferrer';const p=node('p','hint');p.append(a);note.append(p);}detail.append(note);
  if(meta.tags.category[0]==='Armor / clothing'||meta.tags.category[0]==='Weapons / ammunition'){
   const key=meta.tags.category[0]==='Armor / clothing'?'armor':'damage';
   const line=node('p','statline');card.querySelector('summary').insertBefore(line,badges);
   const form=node('form','personal-stat');const label=node('label','',key==='armor'?'Your displayed armor rating (optional)':'Your displayed weapon damage (optional)');const input=node('input');input.type='number';input.id='stat_'+id;input.min='0';input.max='1000000';input.step='any';input.inputMode='decimal';input.placeholder='Unknown — enter only a number you have observed';label.htmlFor=input.id;const b=node('button','', 'Save my value');b.type='submit';form.append(label,input,b,node('p','hint','For your own comparison. Record the same variant and character conditions. Set/family entries can cover more than one item; do not mix set totals with single-piece ratings. Blank clears the value.'));
   form.addEventListener('submit',e=>{e.preventDefault();const raw=input.value.trim();if(raw){const v=Number(raw);if(!validNumber(v)){say('Enter a nonnegative rating, or leave it blank to clear it.');return;}ratings[id]={...ratings[id],[key]:v};}else if(ratings[id]){delete ratings[id][key];if(!Object.keys(ratings[id]).length)delete ratings[id];}write();updateStat(item);render();say(id+' personal value saved. Choose My in-game values when sorting to use it.');});
   detail.append(form);item.statline={key,input,line};updateStat(item);
  }
  card.querySelector('.pick-select').addEventListener('change',e=>{choices[id]=e.target.value;updateChoice(item);write();render();say(id+' → '+pick(r)+(canSave?' · saved.':' · session only.'));});updateChoice(item);
 }
 try{
  const res=await fetch('catalog-current.html?v=2');if(!res.ok)throw Error('Catalog data request failed.');
  const text=await res.text();const parsed=new DOMParser().parseFromString(text,'text/html');data=JSON.parse(parsed.getElementById('dataset').textContent);
  if(data.length!==633||new Set(data.map(r=>r['Catalog ID'])).size!==633)throw Error('Catalog integrity check failed.');
  choices=sanitizeChoices(read(KEY));ratings=sanitizeRatings(read(RKEY));
  records=data.map((r,index)=>{const id=r['Catalog ID'];const original=parsed.getElementById(id);if(!original)throw Error('Missing card '+id);const meta=SaqrimTags.classify(r);return {id,r,index,meta,card:document.importNode(original,true),search:(Object.values(r).join(' ')+' '+Object.values(meta.tags).flat().join(' ')).toLowerCase()};});
  for(const [group,title,values]of SaqrimTags.groups){selected[group]=new Set();const block=node('details','facet');block.open=['category','school','armor','slot'].includes(group);block.append(node('summary','',title));const field=node('fieldset');field.append(node('legend','',title));for(const val of values){const label=node('label','tick');const input=node('input');input.type='checkbox';input.dataset.group=group;input.value=val;const count=node('span','', '0');count.setAttribute('aria-hidden','true');label.append(input,node('span','',val),count);field.append(label);inputs.push({group,val,input,label:count});input.addEventListener('change',()=>{if(input.checked)selected[group].add(val);else selected[group].delete(val);single=null;render();});}block.append(field);$('facets').append(block);}
  const mods=new Map();for(const r of data){const id=String(r['LO #']??'').trim();if(id)mods.set(id,r['Installed mod']);}[...mods].sort((a,b)=>Number(a[0])-Number(b[0])).forEach(([id,name])=>{const o=node('option','', '#'+id+' '+name);o.value=id;$('mod').append(o);});
  records.forEach(enrichCard);
  document.querySelectorAll('[disabled]').forEach(n=>n.disabled=false);
  for(const id of ['search','mod','sort','only-new','only-artifact-batch','stat-source','known-only'])$(id).addEventListener(id==='search'?'input':'change',()=>{single=null;render();});
  $('clear').addEventListener('click',reset);$('view-results').addEventListener('click',()=>{if(matchMedia('(max-width:720px)').matches)$('filter-panel').open=false;scrollResults();});
  $('expand').addEventListener('click',()=>records.forEach(i=>{if(!i.card.hidden)i.card.open=true;}));$('collapse').addEventListener('click',()=>records.forEach(i=>{if(!i.card.hidden)i.card.open=false;}));
  $('random').addEventListener('click',()=>{const pool=records.filter(i=>matches(i)&&pick(i.r)!=='Skip');if(!pool.length){say('No unskipped matches. Clear or change a filter.');return;}const item=pool[Math.floor(Math.random()*pool.length)];single=item.id;render();item.card.open=true;scrollResults();});
  $('backup').addEventListener('click',()=>panel('Back up choices and personal ratings',backup(),'Saqrim_Backup.json'));
  $('picks').addEventListener('click',()=>{const rows=data.filter(r=>pick(r)!=='Undecided');panel('Your selected items',rows.map(r=>`${r['Catalog ID']} | ${pick(r)} | ${r.Target}\n${r['Installed mod']}\n${r['Where / unlock']}\n${r['Source URL']}\n`).join('\n')||'No choices yet. Open a card and choose Want, Maybe or Skip.','Saqrim_Picks.txt');});
  $('import').addEventListener('click',()=>panel('Import old or new choices backup','','Saqrim_Backup.json',true));$('close-transfer').addEventListener('click',()=>$('transfer').hidden=true);
  $('copy').addEventListener('click',async()=>{try{await navigator.clipboard.writeText($('transfer-text').value);say('Copied.');}catch(_){$('transfer-text').focus();$('transfer-text').select();say('Text selected. Use your device’s Copy command.');}});
  $('save-backup').addEventListener('click',()=>{const u=URL.createObjectURL(new Blob([$ ('transfer-text').value],{type:saveJSON?'application/json':'text/plain;charset=utf-8'}));const a=node('a');a.href=u;a.download=transferName;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),10000);});
  $('apply-import').addEventListener('click',()=>{try{importBackup($('transfer-text').value);}catch(e){say('Import failed: '+e.message);}});
  $('import-file').addEventListener('change',async e=>{try{const f=e.target.files[0];if(!f)return;if(f.size>2*1024*1024)throw Error('Backup is too large.');importBackup(await f.text());}catch(err){say('Import failed: '+err.message);}e.target.value='';});
  window.addEventListener('hashchange',openHash);
  if(matchMedia('(max-width:720px)').matches)$('filter-panel').open=false;
  // Do not overwrite storage on startup. Existing records remain intact.
  storageNote();
  const query=new URLSearchParams(location.search);for(const [group,,vals]of SaqrimTags.groups)for(const value of query.getAll(group))if(vals.includes(value)){selected[group].add(value);inputs.find(i=>i.group===group&&i.val===value).input.checked=true;}if(query.get('batch')==='Familiar uniques 1')$('only-artifact-batch').checked=true;
  render();openHash();
  window.SaqrimCatalog={records,render,reset,selected,sorted,value,statType};
 }catch(e){$('error').hidden=false;$('count').textContent='Interactive catalog unavailable';console.error(e);}
})();
