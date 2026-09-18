/* Reviewed associations to the original catalog, not newly verified item coordinates.
   Each entry links a W-number to a named site, vendor hub, quest lead or reference area.
   Source text, original URLs and all port qualifications are displayed from the catalog. */
'use strict';
window.SaqrimMapLinks=(()=>{
 const links={};
 function add(place,ids,kind='site',note=''){
  ids.split(' ').forEach(id=>{(links[id]??=[]).push({place,kind,note});});
 }
 add('Whiterun','W004 W048 W039','hub','City-level reference. Follow the catalog directions or thaneship conditions; this is not a street-level item pin.');
 add('Whiterun','W049','quest','The catalog identifies a key in Kodlak’s room, not the final weapon lying at this pin.');
 add('Riften','W005 W193 W543','hub','City-level reference for Riftweald Manor or the Thieves Guild. Read the individual directions.');
 add("Dead Men's Respite",'W006 W056');
 add('Lost Valkygg','W009');add('Forelhost','W010');add('Korvanjund','W011');
 add('Ironbind Barrow','W012 W180');
 add('Lost Prospect Mine','W021');add('Castle Volkihar','W022 W177 W547');
 add('Lost Tongue Overlook','W023');add('Fort Kastav','W024');add('Fort Sungard','W025');
 add('Bthardamz','W026');add("Tolvald's Cave",'W027');add('Broken Fang Cave','W028');
 add('Bloodlet Throne','W029');add('Lost Valley Redoubt','W030 W052');
 add('Tower of Mzark','W031 W197','site','Exterior tower-area reference. The item is inside; Blackreach access and the tower’s entrance state matter.');
 add('Lost Echo Cave','W032');add("Robber's Gorge",'W033');add("Bruca's Leap Redoubt",'W034');
 add('Redwater Den','W035');add('Yngvild','W036');add('Fort Dunstad','W037');add('Fort Hraggstad','W038');
 for(const [place,id]of [['Solitude','W040'],['Riften','W041'],['Markarth','W042'],['Windhelm','W043'],['Morthal','W044'],['Dawnstar','W045'],['Falkreath','W046'],['Winterhold','W047']])add(place,id,'quest','Thane reward hub, not an item lying at the map marker.');
 add('Southfringe Sanctum','W053');add('Angarvunde','W055');add('Shroud Hearth Barrow','W057');
 add('Riverwood','W131','hub','Town-level source location; exact container has not been established.');
 add('Mzulft','W185 W186 W187');
 add('Darkfall Cave','W195');add('Dark Brotherhood Sanctuary','W196');
 add('The Tower Stone','W358 W359 W365','nearby','Reference landmark only. The catalog points to the nearby Iceberg Explorer site, not the standing stone itself.');
 add('Eldergleam Sanctuary','W360');add("Stendarr's Beacon",'W361');
 add('Markarth','W362 W542','hub','City reference. Follow the Temple of Dibella or Cidhna Mine quest instructions in the catalog.');
 add('Solitude','W363','hub','Hall of the Dead / Wolf Queen quest reference, not an outdoor pickup.');
 add('College of Winterhold','W536','quest','Arniel’s Endeavor reward scene; pin shows the College area, not the final weapon position.');
 add('College of Winterhold','W540','hub','Arch-Mage’s Quarters reference; not a courtyard pickup.');
 add("Ysgramor's Tomb",'W548');
 add('Dawnstar','W616','nearby','Reference town only. The merchant is southwest of Dawnstar; use the original author map linked in the record.');
 // Named, documented Triumvirate vendors. Stock remains skill/port dependent.
 const vendors=[['Whiterun','W076 W077 W078 W080 W229 W230 W486 W487'],['Markarth','W079 W227 W228 W488'],['Winterhold','W081 W231 W232 W233 W234 W235'],['Morthal','W082 W083 W084 W489 W490 W491 W492'],['Riften','W085 W236 W237 W238 W239 W495'],['Falkreath','W086 W240 W493 W494'],['Windhelm','W087 W498 W499']];
 for(const [place,ids]of vendors)add(place,ids,'vendor','Named vendor’s town, not a guaranteed purchase or exact shop pin. Skill requirements and port behavior still apply.');
 function world(r){
  const t=[r['Region / route'],r['Installed mod'],r['Where / unlock']].join(' ');
  if(/Evergloam|Aberrations of the Dwemer/i.test(t))return 'Evergloam';
  if(/Beyond Reach/i.test(t))return 'Beyond Reach';
  if(/Icemoth|Hjorkvild/i.test(t))return 'Icemoth';
  if(/Atmora|Crucible island/i.test(t))return 'Atmora';
  if(/Soul Cairn/i.test(t))return 'Soul Cairn';
  if(/Forgotten Vale|Vyrthur|Gelebor/i.test(t))return 'Forgotten Vale';
  if(/Apocrypha/i.test(t))return 'Apocrypha';
  if(/Solstheim|Bloodmoon|Kagrumez|Fahlbtharz|Frostmoon Crag/i.test(t)&&!links[r['Catalog ID']])return 'Solstheim / mixed';
  return 'Skyrim / unspecified';
 }
 function reason(r){
  if(links[r['Catalog ID']])return 'Linked to a reference pin';
  const w=world(r);if(!['Skyrim / unspecified'].includes(w))return 'Other world / no map layer';
  const t=(r.Acquisition+' '+r['Where / unlock']).toLowerCase();
  if(/random|dragon.loot|dragon weapon loot|leveled loot/.test(t))return 'Random / distributed loot';
  if(/craft|forge|tanning|manufacture/.test(t))return 'Crafting / no unique pin';
  if(/vendor|merchant/.test(t))return 'Vendors / no unique pin';
  return 'Location / coordinates pending';
 }
 const cities=new Set(['Dawnstar','Winterhold','Windhelm','Riften','Falkreath','Markarth','Solitude','Morthal','Whiterun']);
 const towns=new Set(['Dragon Bridge','Karthwasten','Rorikstead','Helgen','Ivarstead',"Shor's Stone",'Riverwood','Kynesgrove','Stonehills','Darkwater Crossing']);
 function placeType(name){
  if(cities.has(name))return 'Cities';if(towns.has(name))return 'Towns';
  if(/\bStone(s)?$/.test(name)&&!['Weynon Stones'].includes(name))return 'Standing stones';
  if(/Mine$/.test(name))return 'Mines';
  if(/Cave|Cavern|Grotto|Burrow|Depths|Pass$/.test(name))return 'Caves / passes';
  if(/Barrow|Tomb|Crypt|Cairn|Ruins|Labyrinthian|Bthardamz|Mzulft|Alftand|Arkngthamz|Avanchnzel|Lost Valkygg|Korvanjund|Yngvild/.test(name))return 'Ruins / tombs';
  if(/Fort |Castle |Tower|Redoubt/.test(name))return 'Forts / towers';
  return 'Other landmarks';
 }
 return {links,world,reason,placeType,cities,towns};
})();
