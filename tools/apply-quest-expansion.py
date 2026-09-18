"""Deterministic, branch-scoped expansion builder. Build from a pinned reviewed base."""
from pathlib import Path
import hashlib,json,re,runpy,subprocess
P=Path(__file__).resolve().parents[1]
BASE_SHA='fa3967e753b2e923c4ec0aae59fc07ea08a9cd19'
names=['quests-data.json','quests.js','site-quests.js','site-top.js','index.html','load-order.html','map.html','worlds.html','quests.html','shrines.html','standing-stones.html','blessings.html','tests/quest-browser.py','tests/navigation-browser.py','tests/blessings-browser.py','QUESTS.md']
BASE={n:subprocess.check_output(['git','show',BASE_SHA+':'+n],cwd=P).decode('utf-8') for n in names}
# Refuse an unreviewed newer baseline rather than quietly overwriting somebody else's work.
for n in names:
 if (P/n).read_text()!=BASE[n]:raise RuntimeError('Expected reviewed pre-expansion file: '+n)
base=json.loads(BASE['quests-data.json']);assert len(base['quests'])==22
extra=runpy.run_path(str(P/'tools/quest-expansion-data.py'))['qs'];assert len(extra)==24
scope='46 curated quest/adventure cards, not a complete census. Original Q001–Q022 retained; expansion Q023–Q046.'
all_quests=base['quests']+extra
(P/'quests-data.json').write_text('{"version":2,"updated":"2026-09-18","scope":'+json.dumps(scope)+',"quests":[\n'+',\n'.join(json.dumps(q,ensure_ascii=False,separators=(',',':')) for q in all_quests)+'\n]}\n')
def edit(file,pairs):
 text=BASE[file]
 for old,new in pairs:
  assert old in text,(file,old)
  text=text.replace(old,new)
 (P/file).write_text(text)
edit('quests.js',[
 ("blackreach:'Blackreach'","blackreach:'Blackreach',elsweyr:'Elsweyr',variable:'Travel-dependent / variable'"),
 ("function mapURL(p){if(!p)return null;","function mapURL(p){if(!p||['elsweyr','variable'].includes(p.world))return null;"),
 ("if(k==='start')return[q.start.area];","if(k==='batch')return[q.batch||'Original collection'];if(k==='start')return[q.start.area];"),
 ("q.start.area==='Starting area pending'||q.id==='Q015'","q.start.known===false||q.start.area==='Starting area pending'||q.id==='Q015'"),
 ('quests-data.json?v=1','quests-data.json?v=2'),
 ('quests.length!==22','quests.length!==46'),
 ("groups=[['start'","groups=[['batch','Quest collection',['Original collection','Expansion 2']],['start'"),
 ("d.open=['start','category']","d.open=['batch','start','category']")])
edit('site-quests.js',[('quests-data.json?v=1','quests-data.json?v=2')])
edit('site-top.js',[('site-quests.js?v=1','site-quests.js?v=2')])
for name in ['index.html','load-order.html','map.html','worlds.html','quests.html','shrines.html','standing-stones.html','blessings.html']:
 text=re.sub(r'site-top.js\?v=\d+','site-top.js?v=7',BASE[name])
 if name=='quests.html':
  text=text.replace('quests.js?v=1','quests.js?v=2').replace('What this first quest collection covers','What this quest collection covers').replace('22 curated cards:','46 curated cards (including 24 new additions):')
 (P/name).write_text(text)
edit('tests/quest-browser.py',[
 ('22 distinct quest cards','46 distinct quest cards'),('SaqrimQuests.quests.length===22','SaqrimQuests.quests.length===46'),('q.id)).size===22','q.id)).size===46'),
 ("found()==['Q018']","set(found())=={'Q018','Q028','Q041'}"),
 ("set(found())=={'Q018','Q022'}","set(found())=={'Q018','Q022','Q025','Q028','Q041'}"),
 ("check('ring rewards from both areas',set(found())=={'Q018','Q022','Q025','Q028','Q041'})","check('ring rewards from both areas',set(found())=={'Q018','Q022','Q041'})"),
 ("check('realm quest marker rendered',page.locator('.quest-start-icon').count()==1)","check('realm quest marker rendered',page.locator('.quest-start-icon').count()==3)"),
 ("'questCards':22","'questCards':46")])
edit('tests/navigation-browser.py',[
 (",'quests-data.json','quests.js','site-quests.js'",''),
 ('document.querySelectorAll(".quest-card").length===22','document.querySelectorAll(".quest-card").length===46')])
content=(P/'site-quests.js').read_bytes();sha=hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()
edit('tests/blessings-browser.py',[('92ceb6bdc66e3e3f9dbd47a093699ddb5c7b2a1c',sha)])
(P/'QUESTS-EXPANSION.md').write_text('''# Quest expansion 2 — 18 September 2026

## Collection

The quest collection grows from 22 to **46 cards** with **24 additions, Q023–Q046**. The original 22 quest objects remain exactly as before. Use **Quest collection → Expansion 2** in the checkbox filters, or open `quests.html?batch=Expansion%202`.

### Mod adventures and expanded quests (10)
The Breathing Abyss; Skragmjor dungeon adventure; Moonpath to Elsweyr overview; Lucien’s The Oblivion Engine and Intruders; JaySerpa’s Heart of Dibella, Innocence Lost, Destroy the Dark Brotherhood and Infiltration; Knight of the North’s Crusader relic hunt.

### College quests (5)
Illusion, Conjuration, Destruction, Alteration and Restoration Ritual Spell. Free base-game rewards and purchasable spells are separated. Linked Apocalypse master tomes are unlocks, not free awards. The 90/100 skill-gate variation and the installed magic stack remain qualified rather than asserted as PS5-tested.

### Artifact quests (9)
The Cursed Tribe, Waking Nightmare, A Night to Remember, The Taste of Death, The Wolf Queen Awakened, Forbidden Legend, The Black Star, Unearthed and Deathbrand.

## Research boundaries

Every card has source URLs and scope. Original-author documentation supports mod features; base-game references support the older quest routes and rewards. The recorded load order establishes the installed mods or visible bundle components; a port’s menu version does not establish every upstream feature.

Only the four JaySerpa quest components visible in the recorded source have been added. No Penitus Oculatus, Legacy of the Dragonborn, alternate Namira quest, Cutting Room Floor or unrelated patch is silently assumed.

The Breathing Abyss author added a permanent buff in 1.0.6, but its exact effect and the PS5 port’s inclusion are still unverified. It remains a lead, excluded from ordinary final-reward filtering. Skragmjor and Moonpath have adventure directions but no verified full ending payout in this collection.

Lucien’s Intruders unlocks horse riding **for Lucien**, not a new player horse. Its starter travels with the companion, so it has no fabricated fixed town pin. Moonpath’s older inn start versus newer outside-Falkreath start remains explicitly version-qualified. Elsweyr has no Saqrim map layer yet; its destination does not open a different world by mistake.

Quest choices stay separate: Erandur versus Skull of Corruption, Azura’s Star versus Black Star, and Namira’s reward versus rescuing Verulus. Distributed Crusader gear, Deathbrand armor and excavation finds are route loot, not automatic final payments. Owning a separately placed Crusader item legitimately is labeled an unlock.

## Integration and preservation

The expanded data drives the quest page, reverse catalog links and quest-start map markers. Existing map reference coordinates are reused without new calibration. Loot, quest, shrine and stone visibility remain independent. The two separate reference tabs and six-tab navigation order are unchanged.

All 617 original catalog records, 220 recorded load-order rows, thumbnails, sizes, shrine/stone facts, local storage keys and Q001–Q022 records are preserved. Rewards without W-numbers are quest labels; this does not silently increase the item catalog count.

## Checks

Batch tests verify all 46 IDs, original-record equality, reward roles, all five school filters, artifact/ring filters, exact map references, no Elsweyr fallback, old and new progress persistence, backup round trips, browser-local storage isolation, mobile layout and six-tab navigation. The existing quest, navigation, shrine/stone, mainland and separate-world suites are also run. Browser checks do not certify gameplay behavior.
''')
text=BASE['QUESTS.md'].replace('is a first collection of **22 quest and adventure cards**','contains **46 quest and adventure cards**').replace('Q016–Q022 cover existing quest routes with modded loot.','Q016–Q022 cover existing quest routes with modded loot. Expansion 2 adds Q023–Q046; see [the expansion notes](QUESTS-EXPANSION.md).')
(P/'QUESTS.md').write_text(text)
assert json.loads((P/'quests-data.json').read_text())['quests'][:22]==base['quests']
print('Generated 46 quest cards; original objects, source data and navigation retained.')
