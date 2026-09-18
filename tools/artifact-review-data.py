"""Source-qualified artifact additions. No plugin binary or PS5 save was inspected."""
import copy

ART='https://www.nexusmods.com/skyrimspecialedition/mods/99619'
FAKES='https://www.nexusmods.com/skyrimspecialedition/mods/41254'
AXE='https://www.nexusmods.com/skyrimspecialedition/mods/154943'
THANE='https://www.nexusmods.com/skyrimspecialedition/mods/35497'
XEDIT='https://tes5edit.github.io/docs/5-conflict-detection-and-resolution.html'
PATCH='https://www.nexusmods.com/skyrimspecialedition/mods/99684'
VIDEO='https://www.youtube.com/watch?v=4uyqCADqwPo'
BASE='https://skyrim.fandom.com/wiki/'
SCOPE='Author-reference Artificer 1.0.11; recorded PS5 menu v1.00 does not identify its upstream build. This is a documentation-based expectation, not an inspected winning plugin record or an in-game measurement.'

# Names, effect facts and routes are deliberately short summaries, not copied readmes.
# Later ArteFakes conflicts have no asserted final enchantment or borrowed vanilla stats.
ADDITIONS=[
 ('Dawnbreaker','Sword','Undead-only sunlight damage; wounded undead may explode.','The Break of Dawn: complete Meridia\'s quest and take the sword from its pedestal.','Skyrim / Kilkreath / Meridia',BASE+'Dawnbreaker',None),
 ('Ebony Blade','Greatsword','Betrayal strengthens its magic damage and living-target life drain.','The Whispering Door: the locked room in Dragonsreach. Quest access is required.','Skyrim / Whiterun / Dragonsreach',BASE+'Ebony_Blade',None),
 ('Ebony Mail','Heavy armor / cuirass','Additional armor bonus and poison resistance.','Boethiah\'s Calling: loot Boethiah\'s champion at Knifepoint Ridge and follow the quest.','Skyrim / Knifepoint Ridge','https://www.gamebanshee.com/skyrim/walkthrough/boethiahscalling.php',None),
 ('Mace of Molag Bal','Mace','Damage over time and soul trapping; tuning is version-sensitive.','The House of Horrors: Molag Bal\'s altar in Markarth\'s Abandoned House.','Skyrim / Markarth',BASE+'Mace_of_Molag_Bal',None),
 ("Mehrunes' Razor",'Dagger','Bleeding, reduced armor and a chance of instant death.','Pieces of the Past: the restoration outcome at the Shrine of Mehrunes Dagon. Not every quest outcome grants the dagger.','Skyrim / Shrine of Mehrunes Dagon',BASE+'Mehrunes%27_Razor',None),
 ("Savior's Hide",'Light armor / cuirass','Stamina regeneration and disease resistance.','Ill Met by Moonlight: the kill-and-skin-Sinding branch. Alternative to the Ring of Hircine route.','Skyrim / Bloated Man\'s Grotto','https://elderscrolls.fandom.com/wiki/Ill_Met_by_Moonlight',None),
 ("Auriel's Bow",'Bow','Sun damage with extra damage against undead.','Touching the Sky: collect the bow at the end of the Chantry of Auriel route.','Forgotten Vale / Inner Sanctum','https://elderscrolls.fandom.com/wiki/Touching_the_Sky_%28Quest%29',None),
 ('Bloodskal Blade','Greatsword','Power attacks release a magic-damage wave.','The Final Descent: beside Gratian Caerellius in Bloodskal Barrow, reached through Raven Rock Mine.','Solstheim / Raven Rock Mine / Bloodskal Barrow','https://elderscrolls.fandom.com/wiki/Bloodskal_Blade',None),
 ('Gauldur Amulet','Jewelry / amulet','Increases Health, Magicka and Stamina.','Forbidden Legend: reforge and collect the amulet at Reachwater Rock. The separate fragments are not additional final amulets.','Skyrim / Reachwater Rock','https://elderscrolls.fandom.com/wiki/Forbidden_Legend',None),
 ('Staff of Magnus','Staff','Drains Magicka, then Health when the target runs dry.','The Staff of Magnus: loot Morokei in Labyrinthian. Follow the College quest for access.','Skyrim / Labyrinthian',BASE+'Staff_of_Magnus_%28item%29',None),
 ("Arch-Mage's Robes",'Clothing / robes','Cheaper spells, more Magicka and faster Magicka regeneration.','The Eye of Magnus: the College completion reward from Tolfdir.','Skyrim / College of Winterhold','https://elderscrolls.fandom.com/wiki/The_Eye_of_Magnus',None),
 ('Dragonbane','Sword',None,'Sky Haven Temple: the weapon room accessed along the Alduin\'s Wall route.','Skyrim / Sky Haven Temple',BASE+'Sky_Haven_Temple','W629'),
 ('Ghostblade','Sword',None,'Ansilvund: complete the dungeon encounter and collect the ghostly reward.','Skyrim / Ansilvund',BASE+'Ghostblade','W630'),
 ('Soulrender','Sword',None,'Deathbrand: loot Haknir after the final fight in Gyldenhul Barrow.','Solstheim / Gyldenhul Barrow','https://elderscrolls.fandom.com/wiki/Deathbrand_%28Quest%29','W631'),
 ('Bloodscythe','Sword',None,'Deathbrand: pick up the sword in Gyldenhul Barrow\'s final chamber before the boss fight.','Solstheim / Gyldenhul Barrow','https://elderscrolls.fandom.com/wiki/Deathbrand_%28Quest%29','W632'),
 ('Shield of Solitude','Armor / shield',None,'The Wolf Queen Awakened: Falk Firebeard\'s completion reward in Solitude.','Skyrim / Solitude','https://elderscrolls.fandom.com/wiki/The_Wolf_Queen_Awakened','W633'),
]

VANILLA_IDS='W306 W307 W308 W309 W310 W311 W312 W366 W367 W368 W369 W370 W371 W372 W373 W374 W375 W376 W377 W378 W379 W380 W381 W536 W537 W538 W539 W540 W541 W542 W543 W544 W545 W546 W547 W548'.split()
OVERLAPS={'W180':'Steel Battleaxe of Fiery Souls','W539':'Glass Bow of the Stag Prince','W544':'Dawnguard Rune Axe','W545':'Dawnguard Rune Hammer','W629':'Dragonbane','W630':'Ghostblade','W631':'Soulrender','W632':'Bloodscythe','W633':'Shield of Solitude'}
RINGS='W307 W310 W367 W368 W542'.split()

# A link enrichment, not a rewrite of the original 46 quest objects or their progress IDs.
QUEST_LINKS={
 'Q020':{"Auriel's Bow":{'catalog':'W624','note':'Collect at the end of the quest. The linked item separates its expected Artificer effect from PS5 verification.','tags':{}}},
 'Q022':{"Savior's Hide":{'catalog':'W623','note':'Alternative branch reward. Do not assume both outcomes from one normal completion.','tags':{}}},
 'Q042':{'Shield of Solitude':{'catalog':'W633','note':'Completion shield; ArteFakes is a later documented item editor than Artificer. Final effects remain unresolved.','tags':{}}},
 'Q043':{'Gauldur Amulet':{'catalog':'W626','note':'Reforge and collect at Reachwater Rock. See the item for its qualified modded effect.','tags':{}}},
 'Q046':{'Soulrender':{'catalog':'W631','note':'Loot Haknir after the fight; not an automatic inventory grant.','tags':{}},'Bloodscythe':{'catalog':'W632','note':'Pick up in the final chamber before the fight; route loot, not the final payout.','tags':{}}}
}

# Screened roles, not an exhaustive FormID conflict report. Later placement alone is not proof.
ROLES=[
 (1,'USSEP','Earlier fixes. Later copies of records can forward or replace fixes.'),
 (25,'Thaumaturgy','Earlier enchanting dependency; not automatically the final artifact effect.'),
 (26,'Summermyst','New enchantments/distribution. Same enchantment theme does not prove identical artifact records.'),
 (38,'Mysticism','Earlier magic dependency. Linked effects and spells require their own record checks.'),
 (44,'Odin','Later than Mysticism; shared magic effects can matter independently of an item record.'),
 (50,'OWL','Loot and level-list changes; do not equate distribution with an item enchantment.'),
 (51,'OWL randomized special loot','Distribution/variant selection is separate from weapon stats.'),
 (52,'OWL Summermyst patch','Named compatibility scope, not a catch-all artifact patch.'),
 (55,'Simply More Variety AE','Creation loot integration; not proof every vanilla artifact is replaced.'),
 (56,'Praedy staves and patches #57–60','Models and named integrations; artifact pointer/asset coverage requires inspection.'),
 (61,'Artificer','Documented artifact and unique-item changes; PS5 v1.00 is not an upstream version identity.'),
 (62,'Artificer–USSEP patch','Named fix integration. No evidence that it merges later #71, #72 or #91 changes.'),
 (65,'Heavy Armory','New weapon families and distribution; not a global artifact override inferred from its title.'),
 (66,'More Unique weapons #66–68','Hand-placed additions are not automatically replacements for similarly themed vanilla artifacts.'),
 (69,'Artifact of Might','Eight added weapons. Not another name for Artificer.'),
 (70,'Eidolon sword','Standalone port; no Harkon/Daedric artifact identity inferred.'),
 (71,'Fiery Souls Truly Unique','Direct named axe overlap, but #91 loads later.'),
 (72,'Unique Thane Weapons','Later documented thane-reward replacement; quest award and item effects need separate checks.'),
 (73,'Minecraft Weapon Pack','Recorded PS5 description says craftable. Do not import the source PC replacer behavior.'),
 (74,'Volkihar Relic Sword','A standalone relic story; not established as replacing Harkon\'s Sword.'),
 (75,'Infinity Sword / Occiglacies #75–76','Separate pickups; matching dungeon or theme is not a shared FormID.'),
 (78,'Psyche artifacts','Port book and exact item identities remain incomplete; no guessed vanilla collisions.'),
 (79,'Dwarven Power Armor','Halidil offers an Aetherial Shield acquisition route; giving an NPC an item is not proof its ARMO record is overwritten.'),
 (80,'Race Armor / outfits / cloaks #80–86','NPC outfit, appearance and new gear roles are not automatically artifact enchantment edits.'),
 (87,'Deadly Dragons Armory','Additional dragon loot; not assumed to overwrite every existing artifact.'),
 (91,'ArteFakes','Named unique-item edits below Artificer and the dedicated axe. Not safe to treat as textures-only.'),
 (92,'Xavbio #92–93','Later texture assets. Do not infer a final enchantment from texture priority; exact asset paths/bundled plugins are uninspected.'),
 (110,'Wear Multiple Rings','Later equipment/quest-item edits. Per-ring record membership and enchantment forwarding are unknown.'),
 (112,'Animated Armoury / patch #113','Weapon families, animations and list integration; no blanket overwrite of named vanilla artifacts inferred.'),
 (145,'JaySerpa quest bundle / #146–147 patches','Quest choices and award routes can change separately from the artifact object.'),
 (155,'Forbidden Goods','Merchant acquisition is not the same thing as changing the base item.'),
 (159,'Knight of the North','Creation relic hunt and access rules. Keep Creation gear separate from vanilla/DLC uniques.'),
 (162,'Lucien / patches #163–164','Follower and Creation integration; not presumed to repair artifact conflicts.'),
 (168,'Cities / world edits #168 onward','Interior, reference, access and placement conflicts may remain even when an item effect is expected.'),
 (213,'Bedlam','Dungeon encounters are not automatically unique-item records.'),
 (215,'High King location patches #215–216','Specific world integrations, not a generic artifact conflict resolver.'),
 (217,'AFT / addon #218','Follower inventory behavior is separate from a documented base-weapon override.'),
 (219,'Lux','Late interior/reference changes must not be mistaken for a blanket final enchantment provider.'),
]

def build(original):
 rows=copy.deepcopy(original); by={r['Catalog ID']:r for r in rows}; audits={}
 for n,(name,kind,effect,where,region,route,conflict) in enumerate(ADDITIONS,618):
  ident=f'W{n:03}'; assert ident not in by and not any(r['Target'].split(' (')[0].casefold()==name.casefold() for r in rows)
  category='Jewelry' if 'Jewelry' in kind else 'Armor / shields' if any(t in kind for t in ['armor','Armor','Clothing']) else 'Weapons / ammunition'
  r={'Catalog ID':ident,'Target':name,'Type':kind,'Browse category':category,'LO #':'61','Installed mod':'Artificer - An Artifact Overhaul','Effect / interest':effect or 'Final enchantment and stats unresolved: ArteFakes #91 also edits this named item.','Where / unlock':where,'When to look':'Follow the named quest or dungeon route; do not infer a level recommendation.','Acquisition':'Existing unique / quest or dungeon loot','Region / route':region,'Evidence status':'Expected from documentation; PS5 records uninspected','Qualifications':SCOPE,'Source scope':'Mod-author effect documentation; base-game route reference separately identified.','Source URL':ART+'\n'+route,'Found?':'Not checked','My choice':'Undecided','Checked on':'2026-09-18'}
  rows.append(r);by[ident]=r
 def audit(ident,origin='Changed vanilla / DLC unique',status='Expected from documentation'):
  r=by[ident]
  obj={'origin':origin,'status':status,'reviewed':'2026-09-18','basis':'Documentation + recorded 220-entry order; no plugin-record or gameplay verification','expected':'Artificer #61 is the documented effect source. No later item-specific edit has been established by the reviewed descriptions for this entry. This is not proof that the rest of the load order contains no override.','chain':'#61 Artificer; #62 Artificer–USSEP patch is present, but its per-item forwarding has not been inspected.','appearance':'Model and texture resolution is separate. #91 ArteFakes applies only to its documented item scope; #92–93 Xavbio may supply matching textures. Exact asset paths and the port payload are uninspected.','acquisition':'The documented acquisition route is listed separately from effects. Later quest, NPC, inventory and world-reference edits are not certified by this item review.','verification':SCOPE,'sources':[ART,XEDIT],'new':int(ident[1:])>=618}
  audits[ident]=obj;return obj
 for ident in VANILLA_IDS+[f'W{i:03}' for i in range(618,634)]: audit(ident)
 for ident,name in OVERLAPS.items():
  a=audits.get(ident) or audit(ident)
  a.update(status='Documented overlap',expected='Latest documented named-item editor: ArteFakes #91. If the recorded port overrides the same base-item record, that later record has priority. The resulting enchantment, linked effects and stats are NOT established from these descriptions.',chain=('#61 Artificer → #71 Fiery Souls – Truly Unique → #91 ArteFakes' if ident=='W180' else '#61 Artificer → #91 ArteFakes')+'. #62 Artificer–USSEP is earlier than the competing edits; no separately listed matching reconciliation patch is present in the recorded list.',verification='Recorded ArteFakes menu v2.0.1 versus author-reference SE v2.0: matching payload not established. A lower model-oriented plugin can also replace other fields in the same item record. Do not combine all advertised enchantments or assume the final effect is vanilla.',sources=[ART,FAKES,XEDIT,PATCH]+([AXE] if ident=='W180' else []))
  r=by[ident];a['earlierEffect']=r['Effect / interest'] if int(ident[1:])<618 else 'Artificer also documents this item; its effect is not promoted to the final in-game result.'
  r['Effect / interest']='Final effects unresolved · ArteFakes #91 is the latest documented editor of this named item; earlier mod benefits are not assumed to survive.'
  if '(Artificer version)' in r['Target']:r['Previous catalog name']=r['Target'];r['Target']=r['Target'].replace('(Artificer version)','(load-order review)')
 for ident in RINGS:
  a=audits[ident];a.update(status='Possible later edit',expected='Artificer #61 documents this ring, but Wear Multiple Rings #110 is a later equipment editor. The exact ring records it includes and whether it forwards the enchantment are unknown; no winner is certified.',chain='#61 Artificer → #62 Artificer–USSEP scope uninspected → #110 Wear Multiple Rings (possible ring-record overlap, NOT a proven same-record edit).',sources=[ART,VIDEO+'&t=116s',XEDIT])
  a['earlierEffect']=by[ident]['Effect / interest'];by[ident]['Effect / interest']='Final ring effect unresolved · #110 Wear Multiple Rings may affect this item; the Artificer reference is retained below, not certified as the winning effect.'
 for i in range(39,49):
  ident=f'W{i:03}';a=audit(ident,'Replacement thane reward','Documented overlap')
  a.update(expected='Unique Thane Weapons #72 is the later documented thane-reward overhaul. Expect its reward assignment only if its quest/award records win. Do not stack its enchantment with Artificer\'s or assume an already received reward is retroactively replaced.',chain='#61 Artificer → #72 Unique Thane Weapons; reward-selection and item records need separate verification.',sources=[ART,THANE,XEDIT],earlierEffect=by[ident]['Effect / interest'])
  by[ident]['Effect / interest']='Expected #72 thane-reward candidate; final quest assignment and enchantment remain unverified. See the load-order review.'
 for ident in [f'W{i:03}' for i in range(358,365)]:
  a=audit(ident,'Creation relic','Identity / acquisition check');a.update(expected='Knight of the North #159 documents the relic hunt and access conditions. It is the acquisition reference here, not proof of a final artifact-stat winner.',chain='Divine Crusader Creation → #159 Knight of the North acquisition overhaul; intervening equipment and later references remain uninspected.',sources=['https://www.nexusmods.com/skyrimspecialedition/articles/3005',XEDIT],verification='Creation Club relic, not a vanilla Skyrim/DLC unique. Recorded PS5 v1.00 does not establish an exact PC branch.')
 for ident in ['W050','W052','W177','W178','W179','W181','W187']:
  a=audit(ident,'Mod-added / other','Identity / acquisition check')
  a.update(expected='Similar names, shared lore or the same pickup area do not establish a shared FormID. This entry must not be treated as an automatic replacement of another catalog item.',chain='Item identity / acquisition check, not an asserted override chain.',verification='Exact base-item identity remains uninspected; standalone copies, restored cut records and NPC inventory references must be distinguished.',sources=[u for u in by[ident]['Source URL'].splitlines() if u.startswith('http')]+[XEDIT])
  if ident in ['W050','W052']:
   a['expected']='Both Artificer #61 and ArteFakes #91 name this restored or added item. Shared identity has not been established: they may target a shared restored record or introduce separate copies. The name alone does not prove #91 replaces this specific pickup.';a['sources'] += [FAKES]
  if ident=='W177':a['expected']='Volkihar Relic Sword #74 is documented as its own relic story. It is NOT established as a replacement for Harkon\'s Sword (W547).'
  if ident=='W187':a['expected']='Halidil\'s shield is an alternative acquisition lead. An NPC carrying an Aetherial Shield does not prove Dwarven Power Armor #79 overwrites the original shield\'s ARMO record or Artificer effect (W311).'
 for ident,a in audits.items():
  r=by[ident];r['Artifact origin']=a['origin'];r['Artifact review status']=a['status'];r['Load-order review']=a['expected'];r['Override chain']=a['chain'];r['Evidence status']=a['status']+' · PS5 winning records uninspected';r['Qualifications']+=' '+a['expected'];r['Checked on']='2026-09-18'
  if a['status']=='Expected from documentation':r['Effect / interest']='Expected Artificer reference: '+r['Effect / interest']
  r['Source URL']='\n'.join(dict.fromkeys(r['Source URL'].splitlines()+a['sources']))
  if a['new']:r['Artifact batch']='Familiar uniques 1'
 assert len(rows)==633 and len(by)==633
 return rows,audits
