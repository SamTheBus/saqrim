"""Source-qualified artifact additions. No plugin binary or PS5 save was inspected."""
import copy

ART='https://www.nexusmods.com/skyrimspecialedition/mods/99619'
FAKES='https://www.nexusmods.com/skyrimspecialedition/mods/41254'
AXE='https://www.nexusmods.com/skyrimspecialedition/mods/154943'
THANE='https://www.nexusmods.com/skyrimspecialedition/mods/35497'
XEDIT='https://tes5edit.github.io/docs/5-conflict-detection-and-resolution.html'
PATCH='https://www.nexusmods.com/skyrimspecialedition/mods/99684'
PRAEDY='https://www.nexusmods.com/skyrimspecialedition/mods/65481'
PRAEDY_PATCH='https://www.nexusmods.com/skyrimspecialedition/mods/65660'
JAY_ART='https://www.nexusmods.com/skyrimspecialedition/mods/151173'
VIDEO='https://www.youtube.com/watch?v=4uyqCADqwPo'
BASE='https://skyrim.fandom.com/wiki/'
SCOPE='Author-reference Artificer 1.0.11; recorded PS5 menu v1.00 does not identify its upstream build. Current 21 September load-order priority is applied, but this is still a documentation-based expectation, not an inspected winning plugin record or an in-game measurement.'

def current_lo(n):
 if n<=32:m=n
 elif 33<=n<=37:m=n+183
 else:
  fixed={38:33,39:35,40:34,41:39,42:40,43:41,44:36,45:38,46:37,47:42,48:43,91:56}
  if n in fixed:m=fixed[n]
  elif 49<=n<=60:m=n-5
  elif 61<=n<=90:m=n-4
  elif 92<=n<=220:m=n-5
  else:m=n
 if m==100:return None
 return m-1 if m>100 else m

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
 ('Dragonbane','Sword','30 Shock damage to Health and Magicka; dragons take double damage.','Sky Haven Temple: the weapon room accessed along the Alduin\'s Wall route.','Skyrim / Sky Haven Temple',BASE+'Sky_Haven_Temple','W629'),
 ('Ghostblade','Sword','Deals 10 irresistible damage.','Ansilvund: complete the dungeon encounter and collect the ghostly reward.','Skyrim / Ansilvund',BASE+'Ghostblade','W630'),
 ('Soulrender','Sword','Deals 10 Magicka damage per second for 10 seconds.','Deathbrand: loot Haknir after the final fight in Gyldenhul Barrow.','Solstheim / Gyldenhul Barrow','https://elderscrolls.fandom.com/wiki/Deathbrand_%28Quest%29','W631'),
 ('Bloodscythe','Sword','Absorbs 30 Health from living targets.','Deathbrand: pick up the sword in Gyldenhul Barrow\'s final chamber before the boss fight.','Solstheim / Gyldenhul Barrow','https://elderscrolls.fandom.com/wiki/Deathbrand_%28Quest%29','W632'),
 ('Shield of Solitude','Armor / shield','Magic Resistance is increased by 25%.','The Wolf Queen Awakened: Falk Firebeard\'s completion reward in Solitude.','Skyrim / Solitude','https://elderscrolls.fandom.com/wiki/The_Wolf_Queen_Awakened','W633'),
]

VANILLA_IDS='W306 W307 W308 W309 W310 W311 W312 W366 W367 W368 W369 W370 W371 W372 W373 W374 W375 W376 W377 W378 W379 W380 W381 W536 W537 W538 W539 W540 W541 W542 W543 W544 W545 W546 W547 W548'.split()
OVERLAPS={'W180':'Steel Battleaxe of Fiery Souls','W539':'Glass Bow of the Stag Prince','W544':'Dawnguard Rune Axe','W545':'Dawnguard Rune Hammer','W629':'Dragonbane','W630':'Ghostblade','W631':'Soulrender','W632':'Bloodscythe','W633':'Shield of Solitude'}
RINGS='W307 W310 W367 W368 W542'.split()

# A link enrichment, not a rewrite of the original 46 quest objects or their progress IDs.
QUEST_LINKS={
 'Q020':{"Auriel's Bow":{'catalog':'W624','note':'Collect at the end of the quest. The linked item separates its expected Artificer effect from PS5 verification.','tags':{}}},
 'Q022':{"Savior's Hide":{'catalog':'W623','note':'Alternative branch reward. Do not assume both outcomes from one normal completion.','tags':{}}},
 'Q042':{'Shield of Solitude':{'catalog':'W633','note':'Completion shield; Artificer is now below ArteFakes in the current order, so its mechanics are the expected item-record outcome. ArteFakes appearance is not guaranteed without a compatibility patch.','tags':{}}},
 'Q043':{'Gauldur Amulet':{'catalog':'W626','note':'Reforge and collect at Reachwater Rock. See the item for its qualified modded effect.','tags':{}}},
 'Q046':{'Soulrender':{'catalog':'W631','note':'Loot Haknir after the fight; not an automatic inventory grant.','tags':{}},'Bloodscythe':{'catalog':'W632','note':'Pick up in the final chamber before the fight; route loot, not the final payout.','tags':{}}}
}

# Screened roles, not an exhaustive FormID conflict report. Later placement alone is not proof.
ROLES=[
 (1,'USSEP','Earlier fixes. Later copies of records can forward or replace fixes.'),
 (25,'Thaumaturgy','Artificer dependency; Summermyst remains a separate installed enchanting overhaul whose broader compatibility is not resolved here.'),
 (26,'Summermyst','New enchantments/distribution. Same enchantment theme does not prove identical artifact records.'),
 (33,'Mysticism','Artificer dependency. Linked effects and spells require their own record checks.'),
 (36,'Odin','Magic overhaul; shared magic effects can matter independently of an item record.'),
 (45,'OWL','Loot and level-list changes; do not equate distribution with an item enchantment.'),
 (46,'OWL randomized special loot','Distribution/variant selection is separate from weapon stats.'),
 (47,'OWL Summermyst patch','Named compatibility scope, not a catch-all artifact patch.'),
 (50,'Simply More Variety AE','Creation loot integration; not proof every vanilla artifact is replaced.'),
 (51,'Praedy staves and patches #52–55','Visual staff records and named magic integrations. Artificer loads later at #57; no Artificer–Praedy patch is in this load order.'),
 (56,'ArteFakes','Unique-item model/record edits now intentionally placed above Artificer. If both edit the same item record, #57 Artificer is the later candidate; ArteFakes models are not assumed to survive without a patch.'),
 (57,'Artificer','Documented artifact and unique-item changes; current priority is below ArteFakes and above the dedicated Fiery Souls / thane replacers.'),
 (58,'Artificer–USSEP patch','Named fix integration. No evidence that it merges later #67 or #68 changes.'),
 (61,'Heavy Armory','New weapon families and distribution; not a global artifact override inferred from its title.'),
 (62,'More Unique weapons #62–64','Hand-placed additions are not automatically replacements for similarly themed vanilla artifacts.'),
 (65,'Artifact of Might','Eight added weapons. Not another name for Artificer.'),
 (66,'Eidolon sword','Standalone port; no Harkon/Daedric artifact identity inferred.'),
 (67,'Fiery Souls Truly Unique','Direct named axe overlap and now the latest of ArteFakes #56, Artificer #57 and the dedicated axe.'),
 (68,'Unique Thane Weapons','Later than Artificer; documented thane-reward replacement remains the expected reward candidate.'),
 (69,'Minecraft Weapon Pack','Recorded PS5 description says craftable. Do not import the source PC replacer behavior.'),
 (70,'Volkihar Relic Sword','A standalone relic story; not established as replacing Harkon\'s Sword.'),
 (71,'Infinity Sword / Occiglacies #71–72','Separate pickups; matching dungeon or theme is not a shared FormID.'),
 (74,'Psyche artifacts','Port book and exact item identities remain incomplete; no guessed vanilla collisions.'),
 (75,'Dwarven Power Armor','Halidil offers an Aetherial Shield acquisition route; giving an NPC an item is not proof its ARMO record is overwritten.'),
 (76,'Race Armor / outfits / cloaks #76–82','NPC outfit, appearance and new gear roles are not automatically artifact enchantment edits.'),
 (83,'Deadly Dragons Armory','Additional dragon loot; not assumed to overwrite every existing artifact.'),
 (87,'Xavbio #87–88','Later texture assets. Do not infer a final enchantment from texture priority; exact asset paths/bundled plugins are uninspected.'),
 (104,'Wear Multiple Rings','Later equipment editor. Unique-ring coverage in this exact PS5 port remains unverified, so ring-record conflicts stay possible rather than certified.'),
 (106,'Animated Armoury / patch #107','Weapon families, animations and list integration; no blanket overwrite of named vanilla artifacts inferred.'),
 (139,'JaySerpa quest bundle / #140–141 patches','Later quest edits. Destroy the Dark Brotherhood has a documented Artificer incompatibility affecting Windshear and Firiniel\'s End unless specifically patched.'),
 (149,'Forbidden Goods','Merchant acquisition is not the same thing as changing the base item.'),
 (153,'Knight of the North','Creation relic hunt and access rules. Keep Creation gear separate from vanilla/DLC uniques.'),
 (156,'Lucien / patches #157–158','Follower and Creation integration; not presumed to repair artifact conflicts.'),
 (162,'Cities / world edits #162 onward','Interior, reference, access and placement conflicts may remain even when an item effect is expected.'),
 (207,'Bedlam','Dungeon encounters are not automatically unique-item records.'),
 (209,'High King location patches #209–210','Specific world integrations, not a generic artifact conflict resolver.'),
 (211,'AFT / addon #212','Follower inventory behavior is separate from a documented base-weapon override.'),
 (213,'Lux','Late interior/reference changes must not be mistaken for a blanket final enchantment provider.'),
]
def build(original):
 rows=copy.deepcopy(original)
 for r in rows:
  try:
   mapped=current_lo(int(r['LO #']))
   if mapped is not None:r['LO #']=str(mapped)
  except (ValueError,TypeError,KeyError):pass
 by={r['Catalog ID']:r for r in rows}; audits={}
 for n,(name,kind,effect,where,region,route,conflict) in enumerate(ADDITIONS,618):
  ident=f'W{n:03}'; assert ident not in by and not any(r['Target'].split(' (')[0].casefold()==name.casefold() for r in rows)
  category='Jewelry' if 'Jewelry' in kind else 'Armor / shields' if any(t in kind for t in ['armor','Armor','Clothing']) else 'Weapons / ammunition'
  r={'Catalog ID':ident,'Target':name,'Type':kind,'Browse category':category,'LO #':'57','Installed mod':'Artificer - An Artifact Overhaul','Effect / interest':effect or 'Final enchantment and stats unresolved: ArteFakes #91 also edits this named item.','Where / unlock':where,'When to look':'Follow the named quest or dungeon route; do not infer a level recommendation.','Acquisition':'Existing unique / quest or dungeon loot','Region / route':region,'Evidence status':'Expected from documentation; PS5 records uninspected','Qualifications':SCOPE,'Source scope':'Mod-author effect documentation; base-game route reference separately identified.','Source URL':ART+'\n'+route,'Found?':'Not checked','My choice':'Undecided','Checked on':'2026-09-18'}
  rows.append(r);by[ident]=r
 def audit(ident,origin='Changed vanilla / DLC unique',status='Expected from documentation'):
  r=by[ident]
  obj={'origin':origin,'status':status,'reviewed':'2026-09-18','basis':'Documentation + recorded 220-entry order; no plugin-record or gameplay verification','expected':'Artificer #57 is the documented effect source. No later item-specific edit has been established by the reviewed descriptions for this entry. This is not proof that the rest of the load order contains no override.','chain':'#57 Artificer; #58 Artificer–USSEP patch is present, but its per-item forwarding has not been inspected.','appearance':'Model and texture resolution is separate. #56 ArteFakes is earlier than Artificer; #87–88 Xavbio may supply matching textures. Exact asset paths and the PS5 port payload are uninspected.','acquisition':'The documented acquisition route is listed separately from effects. Later quest, NPC, inventory and world-reference edits are not certified by this item review.','verification':SCOPE,'sources':[ART,XEDIT],'new':int(ident[1:])>=618}
  audits[ident]=obj;return obj
 for ident in VANILLA_IDS+[f'W{i:03}' for i in range(618,634)]: audit(ident)
 for ident,name in OVERLAPS.items():
  a=audits.get(ident) or audit(ident)
  r=by[ident]
  if ident=='W180':
   a.update(status='Documented overlap',expected='Steel Battleaxe of Fiery Souls – Truly Unique #67 is the latest documented item-specific editor after ArteFakes #56 and Artificer #57. Its Emberwisp / Flameclaim version is therefore the expected candidate, but the exact PS5 winning records remain uninspected.',chain='#56 ArteFakes → #57 Artificer → #58 Artificer–USSEP scope uninspected → #67 Fiery Souls – Truly Unique.',appearance='The dedicated #67 overhaul is also later than ArteFakes. Do not assume ArteFakes supplies the final model or that Artificer\'s Soulbrand fields are merged into #67.',verification='Recorded PS5 menu versions establish order, not record contents. The dedicated axe is the latest documented same-item editor, so its mechanics are the expectation rather than a certified plugin scan.',sources=[ART,FAKES,AXE,XEDIT])
   a['earlierEffect']='Artificer #57 separately renames and reworks this weapon as Soulbrand; those earlier fields are not assumed to survive #67.'
  else:
   a.update(status='Documented overlap',expected='Artificer #57 loads after ArteFakes #56. If both PS5 ports override the same base-item record, Artificer is the later documented record candidate, so its mechanics are the expected version. ArteFakes\' model assignment is not guaranteed to survive without a compatibility patch.',chain='#56 ArteFakes → #57 Artificer → #58 Artificer–USSEP scope uninspected. No separately listed Artificer–ArteFakes reconciliation patch is present in the current load order.',appearance='A public Artificer–ArteFakes compatibility patch exists specifically to carry ArteFakes models into Artificer. It is not installed here, so the site does not promise ArteFakes visuals on these overlapping items.',verification='This is load-order precedence from documented overlap, not an inspected PS5 plugin record. The exact port payload and any asset-only wins remain unverified.',sources=[ART,FAKES,PATCH,XEDIT])
   a['earlierEffect']='ArteFakes #56 is earlier and model-focused. Without the compatibility patch, its appearance is not assumed to survive the later Artificer item record.'
   r['Effect / interest']='Expected Artificer reference: '+r['Effect / interest']
 for ident in RINGS:
  a=audits[ident];a.update(status='Possible later edit',expected='Artificer #57 documents this ring, but Wear Multiple Rings #104 is a later equipment editor. The exact ring records it includes and whether it forwards the enchantment are unknown; no winner is certified.',chain='#57 Artificer → #58 Artificer–USSEP scope uninspected → #104 Wear Multiple Rings (possible ring-record overlap, NOT a proven same-record edit).',sources=[ART,VIDEO+'&t=116s',XEDIT])
  a['earlierEffect']=by[ident]['Effect / interest'];by[ident]['Effect / interest']='Final ring effect unresolved · #104 Wear Multiple Rings may affect this item; the Artificer reference is retained below, not certified as the winning effect.'
 for i in range(39,49):
  ident=f'W{i:03}';a=audit(ident,'Replacement thane reward','Documented overlap')
  a.update(expected='Unique Thane Weapons #68 is the later documented thane-reward overhaul. Expect its reward assignment only if its quest/award records win. Do not stack its enchantment with Artificer\'s or assume an already received reward is retroactively replaced.',chain='#57 Artificer → #68 Unique Thane Weapons; reward-selection and item records need separate verification.',sources=[ART,THANE,XEDIT],earlierEffect=by[ident]['Effect / interest'])
  by[ident]['Effect / interest']='Expected #68 thane-reward candidate; final quest assignment and enchantment remain unverified. See the load-order review.'
 for ident in [f'W{i:03}' for i in range(358,365)]:
  a=audit(ident,'Creation relic','Identity / acquisition check');a.update(expected='Knight of the North #153 documents the relic hunt and access conditions. It is the acquisition reference here, not proof of a final artifact-stat winner.',chain='Divine Crusader Creation → #153 Knight of the North acquisition overhaul; intervening equipment and later references remain uninspected.',sources=['https://www.nexusmods.com/skyrimspecialedition/articles/3005',XEDIT],verification='Creation Club relic, not a vanilla Skyrim/DLC unique. Recorded PS5 v1.00 does not establish an exact PC branch.')
 for ident in ['W050','W052','W177','W178','W179','W181','W187']:
  a=audit(ident,'Mod-added / other','Identity / acquisition check')
  a.update(expected='Similar names, shared lore or the same pickup area do not establish a shared FormID. This entry must not be treated as an automatic replacement of another catalog item.',chain='Item identity / acquisition check, not an asserted override chain.',verification='Exact base-item identity remains uninspected; standalone copies, restored cut records and NPC inventory references must be distinguished.',sources=[u for u in by[ident]['Source URL'].splitlines() if u.startswith('http')]+[XEDIT])
  if ident in ['W050','W052']:
   a['expected']='Both Artificer #57 and ArteFakes #56 name this restored or added item. Shared identity has not been established: they may target a shared restored record or introduce separate copies. The name alone does not prove the two ports use the same record; if they do, #57 Artificer is later.';a['sources'] += [FAKES]
  if ident=='W177':a['expected']='Volkihar Relic Sword #70 is documented as its own relic story. It is NOT established as a replacement for Harkon\'s Sword (W547).'
  if ident=='W187':a['expected']='Halidil\'s shield is an alternative acquisition lead. An NPC carrying an Aetherial Shield does not prove Dwarven Power Armor #75 overwrites the original shield\'s ARMO record or Artificer effect (W311).'
 # Additional current-order conflicts found after the first artifact pass.
 a=audits['W627']
 a.update(status='Documented overlap',expected='Artificer #57 is later than Praedy\'s Staves #51–55. Artificer\'s Staff of Magnus mechanics are the expected record outcome, but Praedy\'s model is not guaranteed because published Praedy/Artificer compatibility patches exist and none is present in this load order.',chain='#51 Praedy\'s Staves → #52 Apocalypse patch → #53 Mysticism patch → #54 Odin patch → #55 USSEP patch → #57 Artificer. No Artificer–Praedy patch appears in the current order.',appearance='Praedy documents that staves edited by other mods can need compatibility patches, and its patch hub includes Artificer. Treat the Staff of Magnus appearance as unresolved while retaining Artificer\'s documented mechanics.',sources=[ART,PRAEDY,PRAEDY_PATCH,XEDIT],earlierEffect='Praedy\'s Staff of Magnus model is installed earlier; without the missing Artificer compatibility patch it is not promised to survive the later item edit.')
 by['W627']['Effect / interest']='Expected Artificer reference: '+by['W627']['Effect / interest']
 for target in ['Windshear',"Firiniel's End"]:
  r=next((x for x in rows if x['Target'].split(' (')[0].casefold()==target.casefold()),None)
  if not r:continue
  ident=r['Catalog ID'];a=audit(ident,'Changed vanilla / DLC unique','Documented overlap')
  a.update(expected='JaySerpa\'s Quest Expansion Bundle #140 loads after Artificer #57. A published compatibility patch states that Destroy the Dark Brotherhood – Quest Expansion can prevent this Artificer artifact from being obtainable. The specific Artificer compatibility patch is not present in the current 220-mod order.',chain='#57 Artificer → #139 JaySerpa Quest Expansion Bundle. #140 Wintersun and #141 USSEP are bundle patches, not the separate Artificer compatibility patch.',acquisition='Acquisition is the conflict here: the later quest expansion can remove the NPC/item handoff used by Artificer. Do not promise this pickup until the PS5 bundle is checked or a matching compatibility patch is added.',verification='The incompatibility is documented for the upstream mods. The exact PS5 bundle/port contents have not been inspected, so the site labels the pickup at risk rather than certifying it absent.',sources=[ART,JAY_ART,XEDIT],earlierEffect=r['Effect / interest'])
  r['Effect / interest']='Artificer effect documented; acquisition is at risk because the later Destroy the Dark Brotherhood quest expansion has a documented incompatibility without its specific Artificer patch.'
 for ident,a in audits.items():
  r=by[ident];r['Artifact origin']=a['origin'];r['Artifact review status']=a['status'];r['Load-order review']=a['expected'];r['Override chain']=a['chain'];r['Evidence status']=a['status']+' · PS5 winning records uninspected';r['Qualifications']+=' '+a['expected'];r['Checked on']='2026-09-18'
  if a['status']=='Expected from documentation':r['Effect / interest']='Expected Artificer reference: '+r['Effect / interest']
  r['Source URL']='\n'.join(dict.fromkeys(r['Source URL'].splitlines()+a['sources']))
  if a['new']:r['Artifact batch']='Familiar uniques 1'
 assert len(rows)==633 and len(by)==633
 return rows,audits
