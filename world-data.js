/* World-specific reference data. No invented terrain, coordinates or pickup locations.
   Mainland associations and the 617 source records remain in their original files. */
'use strict';
window.SaqrimWorldData=(()=>{
 const nexus=n=>'https://www.nexusmods.com/skyrimspecialedition/mods/'+n;
 const wiki=n=>'https://en.uesp.net/wiki/'+n;
 const worlds=[
 {id:'solstheim',name:'Solstheim',kind:'map',width:1000,height:888.888889,image:'https://images.uesp.net/9/9e/User-Roger-Solstheim_Map_02.jpg',external:true,source:wiki('File:User-Roger-Solstheim_Map_02.jpg'),credit:'Bethesda terrain, map by UESP contributor Roger; named-position reference: Itemaps.',note:'Dragonborn-era Solstheim. Pins use published game-coordinate references and the UESP map’s stated 27 × 24 cell frame. They mark reference areas, not mod-added chests. The terrain image is externally hosted; a coordinate-only view remains usable when it cannot load.'},
 {id:'evergloam',name:'Evergloam · Aberrations',kind:'guide',source:'https://www.reddit.com/r/SkyrimCreations/comments/1i3wvtw/comment/mvtrgap/',credit:'Original creator Smelly_Dog / Unorthodogg’s reward-location list.',note:'Location guide, not a geographic overlay yet. The named sites and directions are documented; their relative map positions have not been verified. No compass positions or connecting routes are invented.'},
 {id:'beyond-reach',name:'Beyond Reach',kind:'guide',source:nexus(3008),credit:'Original Beyond Reach catalog sources; historical sources remain identified on their records.',note:'Location guide, not a geographic overlay yet. Most spell records are historical leads, not verified placements in the installed PS5 4.8 port. The standalone Tomes of Want’s College and Drunken Huntsman vendors are NOT imported here.'},
 {id:'icemoth',name:'Icemoth · Hjorkvild Isles',kind:'map',width:1000,height:750.243902,image:'assets/map/worlds/icemoth.webp',external:false,source:nexus(109541)+'?tab=images',credit:'Reference map posted by RoastGorilla439; map icons by Klime; game imagery © Bethesda.',note:'Reference map from the Icemoth creator’s gallery. Pins were read from the visible map symbols and are approximate. The Crimson Kiss chest is behind the wreck on the seafloor—not at the wreck marker itself.'},
 {id:'atmora',name:'Atmora · Crucible',kind:'guide',source:'https://creations.bethesda.net/en/skyrim/details/87939b6a-ae0b-4028-8a70-665b48896013/Beyond_the_Edge_of_Atmora',credit:'Recorded PS5 description and original creator reference.',note:'Crucible-island location guide. The six catalog rewards are named, but their exact holders and an accurately calibrated island map have not been established.'},
 {id:'soul-cairn',name:'Soul Cairn',kind:'map',width:1000,height:842.235004,image:'https://images.uesp.net/b/b9/SR-map-Soul_Cairn.jpg',external:true,source:wiki('Skyrim:Soul_Cairn'),credit:'Bethesda game imagery; reference map from UESP.',note:'Zoomable reference image with the catalog’s Soul Cairn rewards alongside it. Exact marker calibration is pending, so the named locations are listed without guessed pins. Terrain depends on the external image host.'},
 {id:'forgotten-vale',name:'Forgotten Vale',kind:'map',width:1000,height:954.900568,image:'https://images.uesp.net/0/0f/SR-map-Forgotten_Vale.jpg',external:true,source:wiki('Skyrim:Forgotten_Vale'),credit:'Bethesda game imagery; reference map from UESP.',note:'Zoomable reference image. Interior sites, the Vale entrance and the separate Vale Forest must not be conflated. Catalog directions remain available; no unverified chest or interior coordinates are plotted.'},
 {id:'blackreach',name:'Blackreach',kind:'map',width:1000,height:1024.80916,image:'https://images.uesp.net/a/ad/SR-map-Blackreach.jpg',external:true,source:wiki('Skyrim:Blackreach'),credit:'Bethesda game imagery; reference map from UESP.',note:'Zoomable reference image. The Tower of Mzark records are access references, not new Blackreach pickup coordinates. This does not move the existing mainland tower-area pins.'},
 {id:'apocrypha',name:'Apocrypha',kind:'guide',source:wiki('Skyrim:Apocrypha'),credit:'Original sources attached to the catalog records.',note:'Location guide only. Apocrypha has multiple Black Book spaces, and random chest distribution is not a unique pickup location. Those records remain unpinned.'}
 ];
 const places=[],links={};
 const addPlace=(world,name,x=null,y=null,note='')=>places.push({world,name,x,y,note});
 function link(world,place,ids,kind='site',note=''){
  if(!places.some(p=>p.world===world&&p.name===place))addPlace(world,place);
  for(const id of ids.split(' '))(links[id]??=[]).push({world,place,kind,note});
 }
 // Game-coordinate facts from the published Solstheim reference index.
 // UESP Roger image frame: 27 columns x 24 rows; cells x=0..26, y=2..25.
 const solstheim=[['Raven Rock',30884,35050],['The Retching Netch',30194,36874],['Severin Manor',25901,37029],['Raven Rock Mine',29653,40352],['Stalhrim Source',29071,78772],['Gyldenhul Barrow',84612,72238],['Benkongerike',48814,80248],['Frostmoon Crag',41569,57139],['Temple of Miraak',56804,62940],['Thirsk Mead Hall',67430,58567],['Tel Mithryn',76863,23034],['Kagrumez',55880,50199],['Fahlbtharz',30921,65460],['Highpoint Tower',49334,38004],['Kolbjorn Barrow',37518,26211],['Ashfallow Citadel',66672,41649],['Fort Frostmoth',52459,23940],['Nchardak',84722,40363],['Bloodskal Barrow',27348,46053],['Hrothmund’s Barrow',43520,75284],['Glacial Cave',46899,92687],['Castle Karstaag Ruins',33312,89920],['Northshore Landing',22751,92430],['Damphall Mine',25738,55271],['Frossel',73271,84589],['Bristleback Cave',18448,83247],['Saering’s Watch',42884,83949],['Earth Stone',22958,30935],['Water Stone',21588,64459],['Sun Stone',72854,34655],['Wind Stone',63355,75109],['Beast Stone',62811,58376],['Old Attius Farm',34666,23259],['Bujold’s Retreat',80276,58550],['Haknir’s Shoal',67552,82272],['Horker Island',88252,70979]];
 for(const [name,x,y]of solstheim)addPlace('solstheim',name,x/110592*1000,(y-8192)/110592*1000,'Published coordinate reference: https://www.itemaps.com/maps/skyrim/solstheim . Approximate map alignment; not a PS5 object-coordinate extraction.');
 link('solstheim','Stalhrim Source','W007');link('solstheim','Gyldenhul Barrow','W008');link('solstheim','Benkongerike','W018');
 link('solstheim','Temple of Miraak','W126');link('solstheim','Thirsk Mead Hall','W129');link('solstheim','Tel Mithryn','W517','vendor','Talvas is the documented vendor; Conjuration 90 and port/stock conditions apply.');
 link('solstheim','Frostmoon Crag','W496 W497','vendor','Majni is the documented vendor. This is the camp reference, not a guaranteed purchase.');
 link('solstheim','Kagrumez','W537');link('solstheim','Fahlbtharz','W538','site','The catalog specifies the Grand Hall. This pin is the ruin-area reference, not a floor plan.');
 link('solstheim','The Retching Netch','W614','quest','A note here marks Syelna’s camp west of Kolbjorn Barrow. The recipe merchant is at that camp, not inside the inn.');
 link('solstheim','Kolbjorn Barrow','W614','nearby','Reference only: Syelna’s camp is west of the barrow. Follow the note from the Retching Netch.');
 link('solstheim','The Retching Netch','W013 W014 W015','quest','Miasma begins with Haj-Xul here. These rewards are obtained later; the quest start is NOT their pickup position.');
 link('solstheim','Gyldenhul Barrow','W207 W208 W209 W210 W211 W212','nearby','An alternative Sonic Magic boss route is described near the barrow. The pin is only a landmark; these are not tomes placed at its door.');
 // Positions read from the creator-posted 1025 x 769 Icemoth map, displayed at 1000 x 750.
 const ice=[['Frostcaller Cave',368,272],["Eyndis’ Folly",488,242],["Saervild’s Trench",368,365],['Lighthouse',444,400],['EEC Warehouse',434,420],['Fort Icemoth',432,449],['Winter-Shroud Sanctum',240,446],['Fjolgen',316,449],["Hjaalskar’s Point",257,478],['Rimewind Grotto',550,505],['Abandoned Fishing Hut',545,551],['Freezewater Plunge',448,624],['Ghoruun Hall',460,641],['Wreck of Northern Grace',478,674]];
 for(const [name,x,y]of ice)addPlace('icemoth',name,x,750.243902-y,'Approximate symbol position read from the creator’s reference map, not a surveyed entrance.');
 link('icemoth','Eyndis’ Folly','W170','nearby','The catalog places Crimson Kiss in a seafloor chest BEHIND Eyndis’ Folly. The wreck pin is the reference point only.');
 // Named discovery locations are useful even before their geographic positions are known.
 const ever=[['Plankside','W552 W573'],['Shrine of the Eye','W553'],['Tonal Architect · NPC location pending','W554'],['Hand of the Forge · NPC location pending','W555'],['Assembly Line','W556'],["Traitor’s Tunnels",'W557'],['The Vault · doors','W558 W559'],['Waterworks','W560 W561'],['Sky Citadel · lobby','W562'],['Forgotten Shrine','W563'],['Heart of the Workshop','W564'],['Underforge Smelter','W565'],['Altar of Lies','W566 W571'],['Edge of Reality','W567'],['Shadow Well','W568'],['Sky Citadel · Engine Room','W569'],['Infinite Spire','W570'],['Sunken Haunts · Far Shore','W572']];
 for(const [name,ids]of ever)link('evergloam',name,ids,'documented','Author-documented location name and directions; geographic position not yet established. PS5 v1.26 placement remains untested.');
 link('atmora','Crucible island · holders pending','W352 W353 W354 W355 W356 W357','region','The recorded description names these rewards. It does not establish their individual holders or exact locations.');
 link('beyond-reach','Nord’s Rest · historical watchtower lead','W581','historical','2017 playthrough lead plus author-confirmed historical spell name. This does not verify the current PS5 4.8 quest or coordinates.');
 link('soul-cairn','Jiub · reward quest','W541','quest','Complete Impatience of a Saint. Jiub’s geographic pin has not been calibrated on this image.');
 link('soul-cairn','Keepers · exact equipment holders unverified','W301 W302 W303 W304','region','Catalog associates this equipment with the Soul Cairn. Individual Keeper positions and the installed port’s drops have not been audited.');
 link('soul-cairn','Reaper · boss reward reference','W305','region','Soul Cairn association retained from the catalog. Exact drop and installed-port behavior remain qualified.');
 link('forgotten-vale','Arch-Curate Vyrthur · encounter','W054 W058','site','The catalog identifies Vyrthur as the holder. No unverified interior position is placed on the exterior image.');
 link('forgotten-vale','Forgotten Vale entrance · nearby lead','W179','nearby','Occiglacies is described near the entrance. No specific doorway or chest position has been inferred.');
 link('blackreach','Tower of Mzark · access reference','W031 W197','site','These items are inside the Tower of Mzark. Existing mainland tower-area references are preserved; no new interior pickup coordinate is inferred.');
 const explicit={W007:'solstheim',W008:'solstheim',W059:'solstheim',W060:'solstheim',W310:'solstheim',W517:'solstheim',W537:'solstheim',W538:'solstheim',W539:'solstheim',W614:'solstheim',W496:'solstheim',W497:'solstheim',W301:'soul-cairn',W302:'soul-cairn',W303:'soul-cairn',W304:'soul-cairn',W305:'soul-cairn',W541:'soul-cairn'};
 function forRecord(r){
  const id=r['Catalog ID'],lo=Number(r['LO #']);
  if(id==='W131')return ['skyrim'];
  if(id==='W031'||id==='W197')return ['skyrim','blackreach'];
  if(explicit[id])return [explicit[id]];
  if(lo===6)return ['evergloam'];if(lo===16)return ['beyond-reach'];if(lo===9)return ['icemoth'];if(lo===13)return ['atmora'];if(lo===12||lo===14)return ['solstheim'];
  if(links[id])return [...new Set(links[id].map(l=>l.world))];
  const old=SaqrimMapLinks.world(r);
  const ids={'Evergloam':'evergloam','Beyond Reach':'beyond-reach','Icemoth':'icemoth','Atmora':'atmora','Soul Cairn':'soul-cairn','Forgotten Vale':'forgotten-vale','Apocrypha':'apocrypha'};
  if(ids[old])return [ids[old]];
  const region=r['Region / route']||'';
  if(/Solstheim|Frostmoon Crag|Tel Mithryn/.test(region)&&!/^Skyrim\s*\//.test(region))return ['solstheim'];
  return ['skyrim'];
 }
 return {worlds,places,links,forRecord};
})();
