"""Apply a reviewed, source-qualified research patch to an exact published baseline.

No load-order, catalog, coordinates or saved-state identifiers are changed.
Run once against the declared baseline. A second run verifies the previous output.
"""
from pathlib import Path
import copy, hashlib, json, re

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/reward-research-01.json'
REPORT = ROOT / 'REWARD-RESEARCH-01-REPORT.json'
VERSION = 'reward-research-01'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def dumps(data):
    return json.dumps(data, ensure_ascii=False, indent=2) + '\n'

def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError('Expected one matching code fragment: ' + old[:90])
    return text.replace(old, new, 1)

pack = json.loads(DATA.read_text(encoding='utf-8'))
if pack['completeRosters'] is not False:
    raise ValueError('This patch must not claim complete rosters.')
if REPORT.exists():
    previous = json.loads(REPORT.read_text(encoding='utf-8'))
    if previous['inputHash'] != digest(DATA.read_bytes()):
        raise ValueError('Input changed after the patch was applied; start from its baseline.')
    for name, sha in previous['outputHashes'].items():
        if digest((ROOT/name).read_bytes()) != sha:
            raise ValueError('Previously generated output changed: ' + name)
    print('Research patch already applied; exact output verified.')
    raise SystemExit(0)

texts = {}
for name, sha in pack['baseHashes'].items():
    data = (ROOT/name).read_bytes()
    if digest(data) != sha:
        raise ValueError('Baseline changed; reconcile before applying: ' + name)
    texts[name] = data.decode('utf-8')
output = {}
qpack = json.loads(texts['quests-data.json'])
by_id = {q['id']: q for q in qpack['quests']}
if len(by_id) != 56:
    raise ValueError('Unexpected quest collection')
sources = pack['sources']

def expand_reward(value):
    row = copy.deepcopy(value)
    if row['kind'] != 'lead' or row.get('catalog'):
        raise ValueError('Research leads cannot become verified catalog rewards')
    row['sources'] = [sources[sid] for sid in row.pop('sourceIds')]
    return row

for qid, changes in pack['questUpdates'].items():
    q = by_id[qid]
    if 'setTitle' in changes:
        q['title'] = changes['setTitle']
    if 'replaceLeadRewards' in changes:
        # Preserve real rewards/unlocks, especially Cataclysm's bonus-adventure unlock.
        q['rewards'] = [r for r in q['rewards'] if r['kind'] != 'lead'] + [expand_reward(r) for r in changes['replaceLeadRewards']]
    q['rewards'].extend(expand_reward(r) for r in changes.get('appendRewards', []))
    q.setdefault('notes', []).extend(changes.get('appendNotes', []))
    if 'setSpoilers' in changes:
        q['spoilers'] = changes['setSpoilers']
    urls = {s['url'] for s in q['sources']}
    for sid in changes['sourceIds']:
        source = sources[sid]
        if source['url'] not in urls:
            q['sources'].append(copy.deepcopy(source)); urls.add(source['url'])
qpack['rewardResearch'] = {'batch': VERSION, 'reviewed': pack['reviewed'], 'completeRosters': False, 'guideIds': list(pack['questUpdates'])}
output['quests-data.json'] = dumps(qpack)

refs = json.loads(texts['load-order-reference.json'])
for sid, source in sources.items():
    key = 'rr01-' + sid
    if key in refs['sources']:
        raise ValueError('Research source key collision: ' + key)
    refs['sources'][key] = {
        'kind': 'upstream' if sid in ['dagoth-trigger', 'cataclysm-translator', 'rotd-rebuild'] else 'community',
        'label': source['label'], 'url': source['url'], 'note': source['scope']
    }
for name, changes in pack['referenceUpdates'].items():
    entry = refs['entries'][name]
    entry['sections'].append({'title': 'Reward and quest research — partial coverage', 'claims': [
        {'text': changes['text'], 'refs': ['rr01-' + sid for sid in changes['sourceIds']]}
    ]})
    for guide in entry.get('guides', []):
        if guide['url'] == 'quests.html#Q056':
            guide['label'] = by_id['Q056']['title']
output['load-order-reference.json'] = dumps(refs)

js = texts['quests.js']
js = replace_once(js, '  return a;\n }\n function makeCard(q)', '''  if(r.sources?.length){const links=node('div','quest-links reward-sources');for(const source of r.sources)addLink(links,source.url,source.label);a.append(links);}
  return a;
 }
 function makeCard(q)''')
# Index gameplay notes, not private journal notes. Spoiler details stay collapsed.
js = replace_once(js, 'q.mod,q.hook,JSON.stringify(q.start)', "q.mod,q.hook,...q.notes,JSON.stringify(q.start)")
js = replace_once(js, "fetch('quests-data.json?v=content-batch-02')", "fetch('quests-data.json?v=" + VERSION + "')")
output['quests.js'] = js
output['site-quests.js'] = replace_once(texts['site-quests.js'], 'quests-data.json?v=content-batch-02', 'quests-data.json?v=' + VERSION)
output['site-top.js'] = replace_once(texts['site-top.js'], 'site-quests.js?v=content-batch-02', 'site-quests.js?v=' + VERSION)
output['tests/october-sync.py'] = replace_once(texts['tests/october-sync.py'], 'site-quests.js?v=content-batch-02', 'site-quests.js?v=' + VERSION)
refjs = texts['load-order-reference.js']
refjs = replace_once(refjs, "user:'User-reported test'", "user:'User-reported test', community:'Community reference'")
refjs = replace_once(refjs, 'load-order-reference.json?v=content-batch-02', 'load-order-reference.json?v=' + VERSION)
refjs = replace_once(refjs, 'User-reported test: your observation, not an independent plugin inspection.', 'User-reported test: your observation, not an independent plugin inspection. Community reference: third-party documentation or player reports, with their limitations stated.')
output['load-order-reference.js'] = refjs
for name in ['quests.html','index.html','load-order.html','map.html','worlds.html','shrines.html','standing-stones.html','blessings.html']:
    text = texts[name]
    for asset in ['quests.js','site-top.js','load-order-reference.js']:
        text = text.replace(asset + '?v=content-batch-02', asset + '?v=' + VERSION)
    if name == 'quests.html':
        text = replace_once(text, '46 curated cards (including 24 new additions)', '56 curated cards (including the 10 October adventure guides)')
        text = replace_once(text, 'Current 633-item catalog', 'Current 637-entry catalog')
        text = replace_once(text, 'Browse this content batch →</a>', 'Browse this content batch →</a><a href="REWARD-RESEARCH-01.md">Reward and trigger research · partial findings →</a>')
    output[name] = text

lines = ['# Reward and trigger research — partial findings', '',
    'This review updates six existing guides and four mod previews. It does **not** close the four complete-roster gaps, establish Cataclysm’s first PS5 contact, or identify the exact 1.37 GB Dagoth build.', '',
    'The 637 catalog records, 56 guide IDs, 15 previews and 224-mod installation order are unchanged. Named or identifiable leads are not new verified W-number entries.', '',
    '## Browse the findings', '',
    '- [Orsinium equipment names](quests.html#Q047) and [the unnamed Riften mask route](quests.html#Q050)',
    '- [Cataclysm content leads](quests.html#Q053)',
    '- [Rotdyflissa version and coverage notes](quests.html#Q055)',
    '- [Dagoth’s creator-described trigger and Mazel Tov research](quests.html#Q056)', '',
    'Open **Unverified leads** within a guide to see the research list. To include those entries in reward-category filters, also check **Include unverified leads**. They are never silently included among verified completion rewards.', '',
    '## Orsinium: 15 equipment-name leads', '',
    'The following names were visible in indexed excerpts of UESP’s expansion-specific equipment index. The full article was unavailable. This is not a complete list or a mapping to Mor Khazgur ending rewards.', '']
lines.extend('- '+r['label'] for r in pack['questUpdates']['Q047']['replaceLeadRewards'])
lines += ['', 'The separate Largashbur/Riften route remains an **unnamed mask**: the comments do not establish which named mask it is. Its route is kept in a collapsed spoiler section.', '',
    '## Cataclysm: eight identifiable leads', '']
lines.extend('- '+r['label'] for r in pack['questUpdates']['Q053']['replaceLeadRewards'])
lines += ['', 'Only some are exact English display names. The Ouroboros summon and three translated travel labels are explicitly descriptive. Reports of recipe materials do not establish a complete formula. Infinity is not equated with the separately installed Infinity Sword mod. The existing confirmed upstream bonus-adventure unlock remains intact.', '',
    'The initial PS5 contact is still unresolved. Level 50 and completion of The Horn of Jurgen Windcaller are gates, not the name of a quest giver, courier note or portal.', '',
    '## Dagoth: an upstream trigger, not a matched console build', '',
    'Der_kernel’s creator reply attributes the quest start to a random post-combat dialogue line. PC players identify the collection quest as Mazel Tov and describe a cooking-station step. No fixed level, kill count or timer is established. The exact 1.37 GB PS5 author/porter and version, final potion name/effects and full gifts roster remain open.', '',
    '## Rotdyflissa: recorded location retained, no invented roster', '',
    'The recorded Rooted In Madness entrance near Movarth’s Lair remains unchanged. The upstream v3.0 rebuild and the console menu v1.00 label are not directly equivalent. A complete named reward list was not available.', '',
    '## Sources and limits', '']
for source in sources.values():
    lines += ['### '+source['label'], '', source['url'], '', source['scope'], '']
output['REWARD-RESEARCH-01.md'] = '\n'.join(lines) + '\n'
output['README.md'] = texts['README.md'] + '\n## Reward and trigger research\n\n[Partial findings and source scopes](REWARD-RESEARCH-01.md) expand six existing guides. The catalog and installation counts are unchanged; incomplete rosters and unverified PS5 build parity stay explicit. `tests/reward-research-01.py` checks preservation, lead-only filtering, sources, progress and mobile rendering.\n'
# Build every file in memory before touching the working tree.
report = {'baseline': pack['baseline'], 'inputHash': digest(DATA.read_bytes()), 'completeRosters': False,
          'changedGuides': list(pack['questUpdates']), 'orsiniumEquipmentNames': 15, 'cataclysmContentLeads': 8,
          'catalogEntries': 637, 'questEntries': 56, 'loadOrderEntries': 224, 'referenceCards': 15,
          'outstanding': pack['outstanding'], 'changedPaths': sorted(output),
          'outputHashes': {name: digest(text.encode('utf-8')) for name, text in output.items()}}
for name, text in output.items():
    (ROOT/name).write_text(text, encoding='utf-8')
REPORT.write_text(dumps(report), encoding='utf-8')
print(dumps({k:v for k,v in report.items() if k not in ['outputHashes','inputHash','changedPaths']}))
