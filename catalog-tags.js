/* Browsing metadata only. Original 617 records remain in catalog-source.html.
   Classifications are taken from explicit catalog wording and the cited sources.
   A name-derived tag is a browsing aid, not a claim of PS5 record verification. */
'use strict';
window.SaqrimTags = (() => {
 const schools=['Alteration','Conjuration','Destruction','Illusion','Restoration'];
 const source=n=>'https://www.nexusmods.com/skyrimspecialedition/mods/'+n;
 const schoolOverrides={};
 function school(ids,value,url){ids.split(' ').forEach(id=>schoolOverrides[id]={value,url});}
 school('W061 W062 W063 W064 W065','Destruction',source(51199));
 school('W066 W067 W068 W069 W070','Conjuration',source(51199));
 school('W071 W072 W073 W074 W075','Alteration',source(51199));
 school('W076 W077 W078 W081','Alteration',source(39170));
 school('W079 W082 W083 W084','Conjuration',source(39170));
 school('W080 W087','Destruction',source(39170));
 school('W085','Illusion',source(39170));
 school('W086','Restoration',source(39170));
 const damage={W004:22,W005:8,W006:6,W007:20,W008:13,W009:12,W010:18,W011:13};
 const equipmentOverrides={
  W012:{armor:['Heavy armor','Clothing'],slot:['Full set'],note:'The recorded Skull Commander port description lists heavy armor and clothing variants. The legendary record does not establish every variant.'},
  W055:{slot:['Body / robes']},W056:{slot:['Hands / gauntlets']},W057:{slot:['Feet / boots']},
  W058:{slot:['Body / robes']},W060:{armor:['Clothing'],slot:['Body / robes']},
  W169:{slot:['Ring']},W307:{slot:['Ring']},
  W178:{hand:['One-handed','Two-handed'],weapon:['Sword','Greatsword']},
  W190:{armor:['Light armor'],slot:['Shield']},
  W269:{slot:['Body / robes']},W270:{slot:['Body / robes']},W271:{slot:['Body / robes']},W272:{slot:['Body / robes']},
  W308:{slot:['Helmet / headwear']},W309:{slot:['Helmet / headwear']},
  W374:{slot:['Helmet / headwear']},W375:{slot:['Helmet / headwear']},W376:{slot:['Helmet / headwear']},
  W377:{slot:['Helmet / headwear']},W378:{slot:['Helmet / headwear']},W379:{slot:['Helmet / headwear']},
  W451:{armor:['Light armor','Clothing'],slot:['Full set'],url:source(137420),note:'The author lists light armor and clothing versions; this catalog row covers the set rather than each variant.'},
  W452:{armor:['Light armor'],slot:['Full set'],url:source(137420),note:'Legendary version from the author\'s light-armor integration. Exact values have not been established.'},
  W461:{hand:['One-handed'],weapon:['Sword']},W462:{hand:['Two-handed'],weapon:['Polearm']},
  W463:{hand:['Two-handed'],weapon:['Polearm']},W464:{hand:['Two-handed'],weapon:['Quarterstaff']},
  W465:{hand:['One-handed'],weapon:['Claws']},W466:{hand:['One-handed'],weapon:['Whip']},
  W467:{hand:['One-handed'],weapon:['Sword']},W478:{hand:['Two-handed'],weapon:['Polearm']},
  W479:{hand:['One-handed'],weapon:['Polearm']},W481:{hand:['One-handed'],weapon:['Mace']},
  W482:{hand:['One-handed'],weapon:['War axe']},W483:{hand:['Two-handed'],weapon:['Warhammer']},
  W484:{hand:['Two-handed'],weapon:['Polearm']},W485:{hand:['Two-handed'],weapon:['Polearm']}
 };
 const categoryMap={'Weapons / ammunition':'Weapons / ammunition','Armor / shields':'Armor / clothing','Jewelry':'Jewelry','Spells / summons':'Spells / summons','Enchantments':'Enchantments','Books / powers / other':'Books / powers / other'};
 function classify(r){
  const id=r['Catalog ID'],category=categoryMap[r['Browse category']],type=r.Type||'',name=r.Target||'',effect=r['Effect / interest']||'';
  const text=(type+' '+name+' '+effect).toLowerCase();
  const tags={category:[category],school:[],hand:[],weapon:[],armor:[],slot:[]};
  const notes=['Type and slot tags use catalog labels and explicit descriptions. Names can suggest a browsing type without proving the installed plugin record. Unknown classifications remain searchable.'];
  const urls=new Set();
  if(category==='Spells / summons'){
   const declared=type+' '+r['When to look'];
   tags.school=schools.filter(s=>new RegExp('\\b'+s+'\\b','i').test(declared));
   if(schoolOverrides[id]){tags.school=[schoolOverrides[id].value];urls.add(schoolOverrides[id].url);}
   if(!tags.school.length && /\bDestruction spell\b/i.test(effect))tags.school=['Destruction'];
   if(!tags.school.length)tags.school=['Unknown'];
  }
  if(category==='Weapons / ammunition'){
   const tests=[['Greatsword',/\b(greatswords?|claymore)\b/],['Battleaxe',/\bbattle[ -]?axes?\b/],['Warhammer',/\b(war[ -]?hammers?|battlehammer|sledgehammer)\b/],['Dagger',/\b(daggers?|dirk)\b/],['War axe',/\bwar[ -]?axes?\b/],['Mace',/\bmaces?\b/],['Sword',/\b(swords?|shortsword|saber|sabre|rapier|katana)\b/],['Bow',/\bbows?\b/],['Crossbow',/\bcrossbows?\b/],['Staff',/\b(staff|staves)\b/],['Firearm',/\b(pistol|musket|rifle|firearm|cannon|guns?)\b/]];
   if(/ammunition/i.test(type))tags.weapon=['Ammunition'];
   else {const hit=tests.find(([,rx])=>rx.test(text));tags.weapon=[hit?hit[0]:'Unknown'];}
   const w=tags.weapon[0];
   if(['Sword','Dagger','Mace','War axe'].includes(w))tags.hand=['One-handed'];
   else if(['Greatsword','Battleaxe','Warhammer'].includes(w))tags.hand=['Two-handed'];
   else if(['Bow','Crossbow','Firearm','Ammunition'].includes(w))tags.hand=['Ranged'];
   else if(w==='Staff')tags.hand=['Staff']; else tags.hand=['Unknown'];
  }
  if(category==='Armor / clothing'||category==='Jewelry'){
   const identity=(name+' '+type).toLowerCase();
   if(category==='Armor / clothing'){
    if(/\bheavy (armor|armour|equipment|chestpiece|mechanized|outfit|set)\b/.test(text))tags.armor.push('Heavy armor');
    if(/\blight (armor|armour|equipment|orcish|chestpiece|shield|outfit|set)\b/.test(text))tags.armor.push('Light armor');
    if(/\b(clothing|robes?|cloak|cape)\b/.test(identity))tags.armor.push('Clothing');
    if(!tags.armor.length)tags.armor=['Unknown'];
   }
   if(/\b(shield|targe)\b/.test(identity))tags.slot=['Shield'];
   else if(/\b(rings?|band)\b/.test(identity))tags.slot=['Ring'];
   else if(/\b(amulet|necklace|pendant|locket)\b/.test(identity))tags.slot=['Amulet / necklace'];
   else if(/\b(crown|circlet)\b/.test(identity))tags.slot=['Circlet / crown'];
   else if(/\b(cloak|cape)\b/.test(identity))tags.slot=['Cloak / cape'];
   else if(/\b(helm|helmet|hood|hat|mask|masque|visage)\b/.test(identity))tags.slot=['Helmet / headwear'];
   else if(/\b(gauntlets?|gloves?|bracers?|hands)\b/.test(identity))tags.slot=['Hands / gauntlets'];
   else if(/\b(boots?|shoes?|greaves|walkers)\b/.test(identity))tags.slot=['Feet / boots'];
   else if(/\b(cuirass|robe|robes|apron|chestpiece|torso)\b/.test(identity))tags.slot=['Body / robes'];
   else if(/\b(set|outfit)\b/.test(identity))tags.slot=['Full set']; else tags.slot=['Unknown'];
  }
  const override=equipmentOverrides[id];
  if(override){for(const k of ['hand','weapon','armor','slot'])if(override[k])tags[k]=override[k];if(override.note)notes.push(override.note);if(override.url)urls.add(override.url);}
  // A mask's weight class is not assumed from its vanilla counterpart.
  // No enchantment magnitude or health bonus is parsed as a base rating.
  const stats={damage:null,armor:null};
  if(Object.hasOwn(damage,id)){stats.damage=damage[id];urls.add(source(104381));notes.push('Base damage is the original author\'s value (Artifact of Might 1.0.3), not an observed PS5 inventory value. The port, skills and upgrades can change your displayed number.');}
  tags.origin=[r['Artifact origin']||'Unreviewed / other'];tags.review=r['Artifact review status']?[r['Artifact review status']]:[];
  return {tags,stats,notes,urls:[...urls]};
 }
 const groups=[
  ['category','Item category',Object.values(categoryMap)],
  ['school','Spell school',[...schools,'Unknown']],
  ['hand','Weapon handling',['One-handed','Two-handed','Ranged','Staff','Unknown']],
  ['weapon','Weapon type',['Sword','Dagger','War axe','Mace','Greatsword','Battleaxe','Warhammer','Bow','Crossbow','Staff','Firearm','Ammunition','Polearm','Quarterstaff','Claws','Whip','Unknown']],
  ['armor','Armor class',['Heavy armor','Light armor','Clothing','Unknown']],
  ['slot','Equipment slot',['Full set','Helmet / headwear','Body / robes','Hands / gauntlets','Feet / boots','Shield','Ring','Amulet / necklace','Circlet / crown','Cloak / cape','Unknown']],
  ['origin','Item origin',['Changed vanilla / DLC unique','Replacement thane reward','Creation relic','Mod-added / other','Unreviewed / other']],
  ['review','Artifact review',['Expected from documentation','Documented overlap','Possible later edit','Identity / acquisition check']],
  ['choice','My choices',['Want','Maybe','Skip','Undecided']]
 ];
 function auditNode(raw){
 const a=raw['Artifact audit'];if(!a)return null;const box=document.createElement('details');box.className='artifact-audit';box.style.cssText='border:1px solid #c5ab76;border-radius:8px;padding:12px;margin:14px 0;font-size:14px;overflow-wrap:anywhere';
 const summary=document.createElement('summary');summary.textContent='Load-order review · '+a.status;box.append(summary);
 for(const [key,label]of [["basis", "Evidence level"], ["expected", "Expected version / unresolved winner"], ["chain", "Recorded order / scope"], ["earlierEffect", "Other documented version / caveat"], ["appearance", "Appearance / assets"], ["acquisition", "Acquisition / distribution"], ["verification", "What is not verified"]]){if(!a[key])continue;const h=document.createElement('h4'),p=document.createElement('p');h.textContent=label;p.textContent=a[key];box.append(h,p);}
 for(const [i,url]of a.sources.entries()){if(!url.startsWith('https://'))continue;const p=document.createElement('p'),link=document.createElement('a');link.textContent='Review source '+(i+1);link.href=url;link.target='_blank';link.rel='noopener noreferrer';p.append(link);box.append(p);}return box;
 }
 return {classify,groups,auditNode};
})();
