"""Synchronize October's captured order and Sam's final edits; no mod recommendations.
Deterministic from the pinned published baseline. Run on the sync branch, then test.
"""
from pathlib import Path
import json, re, subprocess
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BASE = 'fdf1282fdb7a26596a64cf9aee1708005103af17'
TOKEN = 'october-sync-1'
SOURCE = '1a12e7fc6d46-master_playlist.mp4'
INPUT = ROOT / 'data/load-order-october-confirmed.txt'
CHANGED = set()

def baseline(path):
    return subprocess.check_output(['git','show',BASE+':'+path], cwd=ROOT).decode('utf-8')

def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists() or p.read_text(encoding='utf-8') != text:
        p.write_text(text, encoding='utf-8')
    CHANGED.add(path)

def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'

old = []
for line in baseline('load-order.tsv').splitlines():
    n,name,size,version,time,category,title,thumb = line.split('\t')
    old.append(dict(n=int(n),name=name,size=size,version=version,time=time,category=category,title=title,thumb=int(thumb)))
assert len(old) == 210
oldnames = {r['name']:r for r in old}
oldnums = {r['n']:r for r in old}
new = []
for line in INPUT.read_text(encoding='utf-8').splitlines():
    if not re.match(r'^\d{3} \| ', line):
        continue
    n,name,size,time = [s.strip() for s in line.split('|')]
    previous = oldnames.get(name)
    new.append(dict(n=int(n),name=name,size=size,time=time,
        version=previous['version'] if previous else 'Version not captured',
        category=previous['category'] if previous else 'Content / details pending',
        title=previous['title'] if previous else name,
        thumb=previous['thumb'] if previous else -1))
assert len(new) == 224 and [r['n'] for r in new] == list(range(1,225))
assert len({r['name'] for r in new}) == 224
byname = {r['name']:r for r in new}
bynum = {r['n']:r for r in new}
assert bynum[84]['name'] == 'SMIM Essentials'
assert bynum[96]['name'] == 'Daedra Pack - Mihail' and bynum[97]['name'] == 'Mihail High Fantasy Monsters'
assert [bynum[i]['name'] for i in range(217,225)] == ['Dagoth Ur','Alternate Start - Live Another Life','Legacy of Orsinium - [clipped title; v1.0.3.2 PS ONLY]','Vokrii - Minimalistic Perks of Skyrim','Ordinator - Perks of Skyrim','Ordinator - Fix - PS5 (textures)','Ordinator - Bone Collector (Windhelm altar fix)','Vokriinator [EN]']
assert all(name not in byname for name in ['KALLAX Storageborn','SMIM - Static Mesh Improvement Mod','Beyond Reach Part 1 (PS)','Beyond Reach Part 2 (PS)','Beyond Reach Revoiced'])
assert all(name in byname for name in ['Lucien - Fully Voiced Follower','Lucien - Anniversary Edition All-in-One Patch','Lucien - Moonpath to Elsweyr Patch','Deadly Dragons Armory','The Restless Dead (A Draugr [clipped title])'])
for name,category in {
    'SMIM Essentials':'Meshes / environment', 'Dagoth Ur':'New content / details pending',
    'Legacy of Orsinium':'New world / quest',
    'LegacyOrsinium - Overhaul [clipped title]':'Quest / patch',
    'Legacy of Orsinium - [clipped title; v1.0.3.2 PS ONLY]':'Quest / patch',
    'Argonian Funerary Masks [clipped title]':'Equipment',
    'Pigs - Mihail Monsters and Animals':'Creatures',
    'Troll Cubs - Mihail Monsters and Animals':'Creatures',
    'The Killer Rabbit of [clipped title]':'Creatures / details pending',
    'Vampire Lord Expansion [clipped title]':'Vampire content / details pending',
    'Daedra Pack - Mihail':'Creatures / bundle',
    'The Restless Dead (A Draugr [clipped title])':'Undead / details pending',
    'Spider SE':'Creature visuals', 'Replaces Nirnroot Plant':'Plant visuals',
    'Rotdyflissa':'Quest / dungeon', 'Undeath (PS5 version)':'Quest',
    'The Final Cataclysm 2020':'Quest', 'Stuck Effects Cleaner (SWF)':'Utilities'
}.items():
    byname[name]['category'] = category
byname['XPMSSE Plus - Custom Skeleton / bundle (PS5)']['title'] = 'XPMSE.ESP'
patch = byname['Legacy of Orsinium - [clipped title; v1.0.3.2 PS ONLY]']
patch['version'] = 'v1.0.3.2'

mapping = {r['n']:byname[r['name']]['n'] if r['name'] in byname else None for r in old}
metadata = {}
for r in new:
    p = oldnames.get(r['name'])
    user = r['time'] == 'User update'
    metadata[r['name']] = {
        'sourceKind':'user' if user else 'recorded',
        'sourceFile':None if user else SOURCE,
        'locator':None if user else r['time'],
        'sizeSource':'Sam\u2019s confirmed replacement/download size after the recording' if user else 'October load-order recording',
        'versionSource':'September recording; retained, not reverified in the October capture' if p else 'Not captured',
        'titleSource':'Earlier clipped menu title retained for identification' if p else 'October capture; normalized name, clipping retained',
        'thumbnailSource':'Earlier recording crop' if p else 'No matching crop captured',
        'notes':[]
    }
    if user:
        metadata[r['name']]['titleSource'] = 'Sam\u2019s confirmed mod name'
    if r['name'] == 'Daedra Pack - Mihail':
        metadata[r['name']]['notes'].append('The source video shows this entry last. Sam moved it immediately above Mihail High Fantasy Monsters; the displayed order applies that instruction.')
    if r['name'] == 'XPMSSE Plus - Custom Skeleton / bundle (PS5)':
        metadata[r['name']]['titleSource'] = 'October visible filename: XPMSE.ESP; identity retained from the matching earlier entry'
    if r['name'] == patch['name']:
        metadata[r['name']]['versionSource'] = 'October capture, v1.0.3.2 PS ONLY'
        metadata[r['name']]['notes'].append('This is the 33.4 KB patch below Alternate Start, distinct from the 33.3 KB entry near the top.')
    if r['name'] == 'Dagoth Ur':
        metadata[r['name']]['notes'].append('Sam\u2019s final placement: immediately above Alternate Start. Not the superseded position above Vokrii.')

write('load-order.tsv', '\n'.join('\t'.join(str(r[k]) for k in ['n','name','size','version','time','category','title','thumb']) for r in new)+'\n')
write('load-order-snapshot.json', dump({'version':1,'label':'October recording + confirmed changes','currentCount':224,'sourceFile':SOURCE,'recordedCount':224,'recordedUsed':'14.73 GB','currentUsed':None,'note':'The 14.73 GB reading predates the KALLAX/SMIM/Dagoth swaps. No post-swap storage measurement was supplied.','previousToCurrent':mapping,'entries':metadata}))

# Remap each reference exactly once. Do not alter URLs, timestamps, entity escapes or W/Q IDs.
number_pattern = re.compile(r'(?<![&\w])#([1-9]\d{0,2})(?:[–-]#?([1-9]\d{0,2}))?\b')
def remap_text(text):
    def change(m):
        a,b = int(m[1]), int(m[2]) if m[2] else None
        def one(n):
            if n not in mapping:
                return '#'+str(n)
            return '#'+str(mapping[n]) if mapping[n] is not None else 'not installed (previous #'+str(n)+')'
        if b is None:
            return one(a)
        return one(a)+'–'+one(b).lstrip('#')
    return number_pattern.sub(change, text).replace('current 210-entry order', 'current 224-entry order').replace('recorded 210-entry current order', 'current 224-entry reference (research retained)')

def walk(value):
    if isinstance(value,str):
        return value if re.match(r'^(https?://|www\.)',value) else remap_text(value)
    if isinstance(value,list):
        return [walk(v) for v in value]
    if isinstance(value,dict):
        return {k:(v if k in ['url','source','sources','Source URL','locator','recording'] else walk(v)) for k,v in value.items()}
    return value

# Keep the original research and source dates. Only current-position references change.
pack = json.loads(baseline('load-order-bethesda.json'))
pack['entries'] = {name:e for name,e in pack['entries'].items() if name in byname}
write('load-order-bethesda.json',dump(pack))
reference = json.loads(baseline('load-order-reference.json'))
reference['entries'] = {name:walk(e) for name,e in reference['entries'].items() if name in byname}
reference['scope'] = 'Existing September description research retained; current links follow the October 224-entry setup. New additions are not marked description-reviewed.'
write('load-order-reference.json',dump(reference))

# Preserve all catalog records and choices; mark removed source mods rather than deleting their research.
soup = BeautifulSoup(baseline('catalog-current.html'),'html.parser')
data_node = soup.select_one('#dataset')
catalog_old = json.loads(data_node.string)
catalog = []
for r in catalog_old:
    out = walk(r)
    raw = str(r.get('LO #','')).strip()
    oldn = int(raw) if raw.isdigit() else None
    now = byname.get(r.get('Installed mod',''),{}).get('n', mapping.get(oldn))
    out['LO #'] = str(now) if now else ''
    out['Source mod status'] = 'In current load order' if now else 'Not in current load order'
    catalog.append(out)
for text in list(soup.find_all(string=True)):
    if text.parent.name not in ['script','style'] and '#' in str(text):
        text.replace_with(remap_text(str(text)))
for a in soup.find_all('a',href=True):
    match = re.fullmatch(r'load-order\.html#mod-(\d+)',a['href'])
    if match:
        now = mapping.get(int(match[1]))
        if now:
            a['href'] = 'load-order.html#mod-'+str(now).zfill(3)
        else:
            del a['href']
            a['title'] = 'Source mod is not in the current load order'
for r in catalog:
    card = soup.find(id=r['Catalog ID'])
    assert card is not None
    label = card.select_one('.mod-name')
    if label:
        label.string = ('Documented source · #'+r['LO #']+' · ' if r['LO #'] else 'Not currently installed · ')+r['Installed mod']
    card['data-source-installed'] = 'true' if r['LO #'] else 'false'
data_node.string = json.dumps(catalog,ensure_ascii=False).replace('</','<\/')
write('catalog-current.html',str(soup))

art = walk(json.loads(baseline('artifact-review.json')))
art['scope'] = 'Existing artifact research retained; current load-order numbers synchronized to the October 224-entry setup. No new plugin scan or gameplay verification.'
write('artifact-review.json',dump(art))
md = remap_text(baseline('ARTIFACT-REVIEW.md'))
md = re.sub(r'^\| (\d{1,3}) \|',lambda m:'| '+str(mapping.get(int(m[1])) or 'Not current')+' |',md,flags=re.M)
md = md.replace('current 210-entry order','current 224-entry order')
md = md.split('\n',1)[0]+'\n\nCurrent-position references synchronized to the October recording and confirmed swaps. The research dates and qualifications below remain historical.\n'+md.split('\n',1)[1]
write('ARTIFACT-REVIEW.md',md)
qpack = json.loads(baseline('quests-data.json'))
for i,q in enumerate(qpack['quests']):
    out = walk(q)
    if isinstance(q.get('lo'),int):
        out['lo'] = mapping.get(q['lo'])
    if isinstance(q.get('rewardMod'),dict) and isinstance(q['rewardMod'].get('lo'),int):
        out['rewardMod']['lo'] = mapping.get(q['rewardMod']['lo'])
    # ARCHIVE_SOURCE_FIX: source citations are historical, not current installation links.
    for source in out.get('sources', []):
        if 'load-order.html#mod-' in source.get('url', ''):
            source['url'] = 'https://github.com/SamTheBus/saqrim/blob/'+BASE+'/load-order.tsv'
            source['scope'] = 'Historical September source snapshot. Use the separate current source-mod link only when the mod is still installed.'
    if isinstance(q.get('rewardMod'), dict) and isinstance(q['rewardMod'].get('lo'), int):
        out['rewardMod']['name'] = oldnums[q['rewardMod']['lo']]['name']
    qpack['quests'][i] = out
write('quests-data.json',dump(qpack))

js = baseline('load-order.js')
# Retain checkmarks by mod identity, not old position. Old storage is never changed.
a = js.index('  const key =')
b = js.index('  const notes =')
js = js[:a]+"  const key = 'saqrim-load-order-224-october-v1';\n  const priorKey = 'saqrim-load-order-210-2026-09-23-v2';\n  const priorToCurrent = "+json.dumps(mapping)+";\n"+js[b:]
a = js.index('  const notes =')
b = js.index('  let data =',a)
js = js[:a]+remap_text(js[a:b])+js[b:]
js = js.replace('canSave = true, bethesdaMeta = {};','canSave = true, bethesdaMeta = {}, snapshotMeta = {};')
a = js.index('  try {\n    const stored =')
b = js.index('  function say',a)
js = js[:a]+'''  try {
    const existing = localStorage.getItem(key);
    const stored = JSON.parse(existing !== null ? existing : (localStorage.getItem(priorKey) || '[]'));
    if (Array.isArray(stored)) {
      const numbers = stored.filter(v => Number.isInteger(v) && v >= 1 && v <= (existing !== null ? 224 : 210));
      added = new Set(numbers.map(n => existing !== null ? n : priorToCurrent[n]).filter(n => Number.isInteger(n) && n >= 1 && n <= 224));
    }
    localStorage.setItem(key, JSON.stringify([...added]));
  } catch (_) { canSave = false; }
'''+js[b:]
for a,b in [(' / 210 shown',' / 224 shown'),(' / 210 added',' / 224 added'),('n > 210','n > 224'),('from 1 to 210','from 1 to 224'),('data.length !== 210','data.length !== 224'),('All 210 mods','All 224 mods')]:
    js = js.replace(a,b)
js = js.replace('d.thumb < 0','d.thumb < -1')
js = js.replace('    if (item.thumb >= 186) {','''    if (item.thumb < 0) {
      thumb.textContent = 'SAQ';
      thumb.classList.add('thumb-pending');
      thumb.setAttribute('aria-label', 'Thumbnail not captured for ' + item.name);
    } else if (item.thumb >= 186) {''')
js = re.sub(r"fetch\('load-order.tsv\?[^']+'\)","fetch('load-order.tsv?v="+TOKEN+"')",js)
js = re.sub(r"load-order-bethesda.json\?v=[^']+","load-order-bethesda.json?v="+TOKEN,js)
needle = "      data = text.trim().split(/\\r?\\n/).map(line => {"
assert needle in js
js = js.replace(needle,'''      try {
        const snapshotResponse = await fetch('load-order-snapshot.json?v=october-sync-1');
        if (snapshotResponse.ok) snapshotMeta = (await snapshotResponse.json()).entries || {};
      } catch (_) { snapshotMeta = {}; }
'''+needle)
js = js.replace('bethesda:bethesdaMeta[name] || null','bethesda:bethesdaMeta[name] || null,provenance:snapshotMeta[name] || null')
a = js.index("    details.append(el('h3', 'recording-heading'")
b = js.index('    node.append(top, actions);',a)
js = js[:a]+'''    details.append(el('h3', 'recording-heading', 'Recorded metadata & current changes'));
    const provenance = item.provenance;
    details.append(el('p', '', 'Identification label (may be clipped or normalized): ' + item.title));
    details.append(el('p', '', 'Size: ' + item.size + ' · Menu version label: ' + item.version));
    if (provenance) {
      details.append(el('p', '', 'Size source: ' + provenance.sizeSource + '.'));
      details.append(el('p', '', 'Version source: ' + provenance.versionSource + '.'));
      details.append(el('p', '', 'Title source: ' + provenance.titleSource + '.'));
      if (provenance.sourceKind === 'recorded') details.append(el('p', '', 'Recording: ' + provenance.sourceFile + ' · ' + provenance.locator + '. The opening browse results are not installed entries.'));
      else details.append(el('p', '', 'Added/replaced after the recording, as confirmed by Sam. No video timestamp or version is invented.'));
      (provenance.notes || []).forEach(note => details.append(el('p', '', note)));
      details.append(el('p', '', 'Image: ' + provenance.thumbnailSource + '.'));
    } else {
      details.append(el('p', '', 'October capture / user updates: ' + item.time + '. Detailed provenance is temporarily unavailable; retained version labels may be from the earlier recording.'));
    }
    if (notes[item.name]) details.append(el('p', 'warning', notes[item.name]));
'''+js[b:]
js = js.replace("'Recorded on your console: ' + recorded", "'Stored console metadata (see source dates below): ' + recorded")
write('load-order.js',js)
css = baseline('load-order.css')+'\n.thumb-pending{display:flex;align-items:center;justify-content:center;font:600 13px system-ui;opacity:.65;background:none!important}.stats span{white-space:normal} .stats{flex-wrap:wrap}\n'
write('load-order.css',css)

h = baseline('load-order.html')
h = re.sub(r'<p class="intro">.*?</p>','<p class="intro">Your current 224-mod setup, synchronized from the October load-order recording and your confirmed changes. Search mods and existing content notes, or use the checklist in this exact order.</p>',h)
h = re.sub(r'<div class="stats">.*?</div>','<div class="stats"><span><b>224</b> current entries</span><span><b>October recording</b> + confirmed changes</span><span><b>14.73 GB</b> in the video, before the final swaps</span></div>',h)
h = re.sub(r'<details class="about">.*?</details>','<details class="about"><summary>Recording and current changes</summary><p>The October recording\u2019s load-order section is the source, not the browsing at the start. Sam subsequently removed KALLAX, replaced full SMIM with 98.94 MB SMIM Essentials, and added 1.37 GB Dagoth Ur directly above Alternate Start. Daedra Pack is immediately above Mihail High Fantasy Monsters. The 33.4 KB Legacy of Orsinium patch remains below Alternate Start.</p><p>Sizes and positions come from that capture plus Sam\u2019s corrections. Older version labels and thumbnails are retained for matching mods and dated in each source panel; missing versions/artwork are not guessed. September description research remains available. There is no new measurement of free storage and no automatic change to the console.</p><p><a href="data/load-order-october-confirmed.txt">Read the complete current order and source locators</a></p></details>',h,flags=re.S)
h = re.sub(r'<footer>.*?</footer>','<footer><p>All 224 current positions are retained when filtering. Existing checkmarks migrate by matching mod identity; other saved choices and progress remain separate.</p><p>Current order: October recording plus confirmed swaps. Existing description research keeps its original dates. Unofficial personal reference.</p><a href="#top">Back to top ↑</a></footer>',h,flags=re.S)
h = h.replace('210-mod','224-mod').replace('Load order · 210','Load order · 224').replace('max="210"','max="224"').replace('1–210','1–224').replace('0 / 210','0 / 224')
write('load-order.html',h)

# Renumber live in-page references while keeping source locators untouched.
refjs = baseline('load-order-reference.js').replace('The 210-mod checklist','The 224-mod checklist')
refjs = refjs.replace("fetch('load-order-reference.json?v=1'", "fetch('load-order-reference.json?v="+TOKEN+"'")
write('load-order-reference.js',refjs)
write('site-top.js',baseline('site-top.js').replace('Load order · 210','Load order · 224').replace('site-quests.js?v=3','site-quests.js?v=october-sync-1')) # OCTOBER_DYNAMIC_CACHE

# Refresh consumers together so old cached datasets cannot mix with the new numbers.
consumer_scripts = ['catalog.js','map.js','worlds.js','quests.js','site-quests.js']
for path in consumer_scripts:
    c = baseline(path)
    if path in ['quests.js', 'site-quests.js']:
        variable = 'r' if path == 'quests.js' else 'raw'
        needle = "Number("+variable+"['LO #'])===q.rewardMod.lo"
        assert needle in c, path
        c = c.replace(needle, "(q.rewardMod.name ? "+variable+"['Installed mod']===q.rewardMod.name : "+needle+")")
    for filename in ['catalog-current.html','quests-data.json','artifact-review.json']:
        c = re.sub(re.escape(filename)+r'\?v=[A-Za-z0-9_-]+',filename+'?v='+TOKEN,c)
    write(path,c)

# Visible navigation and script versioning; the original research archive is immutable.
html_pages = ['index.html','load-order.html','map.html','worlds.html','quests.html','shrines.html','standing-stones.html','blessings.html','catalog-current.html']
assets = ['site-top.js','catalog.js','map.js','worlds.js','quests.js','site-quests.js','load-order.js','load-order-reference.js','load-order.css']
for path in html_pages:
    c = (ROOT/path).read_text(encoding='utf-8') if path in CHANGED else baseline(path)
    c = c.replace('Load order · 210','Load order · 224').replace('210-mod','224-mod').replace('210-MOD','224-MOD').replace('210-entry','224-entry')
    for asset in assets:
        c = re.sub(re.escape(asset)+r'\?v=[A-Za-z0-9_-]+',asset+'?v='+TOKEN,c)
    write(path,c)

readme = baseline('README.md')
readme = re.sub(r'^- Current load-order source:.*$', '- Current load-order source: `1a12e7fc6d46-master_playlist.mp4` plus Sam’s final confirmed swaps and placements', readme, flags=re.M)
readme = readme.replace('210-entry current load-order checklist','224-entry current load-order checklist')
a = readme.index('## Load-order provenance')
b = readme.index('## Preservation',a)
readme = readme[:a]+'''## Load-order provenance

The current order has 224 entries, from the October load-order recording plus Sam's final confirmed corrections. Opening browse results are excluded. KALLAX and full SMIM are absent; SMIM Essentials occupies the former SMIM slot. Dagoth Ur is immediately above Alternate Start, followed by the 33.4 KB Legacy of Orsinium patch and the perk stack. Daedra Pack is immediately above Mihail High Fantasy Monsters. Lucien and both patches, Deadly Dragons Armory and The Restless Dead remain.

`data/load-order-october-confirmed.txt` is the readable current snapshot; `load-order.tsv` feeds the site. `load-order-snapshot.json` separates October size/position evidence, later user updates, and version/thumbnail information retained from September. New versions or exact identities not captured remain unknown. The 14.73 GB total is historical, before the final swaps, not a current free-space estimate.

The TSV retains eight columns: position, name, displayed size, retained version label, locator, category, identification title, thumbnail index. Thumbnail -1 means no matching crop; existing indices still address the original sheets. No fake screenshot or guessed art is assigned to new mods.

'''+readme[b:]
readme = readme.replace('`saqrim-load-order-210-2026-09-23-v2`','`saqrim-load-order-224-october-v1` (migrated by mod identity from `saqrim-load-order-210-2026-09-23-v2`)')
readme += '\n## October synchronization validation\n\n`tests/october-sync.py` validates the full 224-entry order, final eight entries, current cross-references, saved-state migration, reference cards, and desktop/mobile rendering. The earlier tests with fixed September baselines remain historical; current CI uses the October-aware regression checks. No changes to actual console installations are made.\n'
write('README.md',readme)

# Update the current listing validator instead of allowing the stale count to fail.
wf = baseline('.github/workflows/load-order-listings-check.yml').replace('len(rows)==210','len(rows)==224').replace('range(1,211)','range(1,225)').replace('210 load-order rows','224 load-order rows')
write('.github/workflows/load-order-listings-check.yml',wf)
# The old integrator writes September copy; do not run it on current main.
write('.github/workflows/reference-overhaul.yml','''name: Reference overhaul checks
on:
  push:
    branches: [main]
    paths:
      - 'load-order*'
      - 'catalog-current.html'
      - 'quests-data.json'
      - 'artifact-review.json'
      - 'site-top.js'
      - 'tests/october-sync.py'
      - '.github/workflows/reference-overhaul.yml'
permissions:
  contents: read
jobs:
  reference:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - run: |
          python -m pip install beautifulsoup4==4.13.5 playwright==1.55.0
          python -m playwright install --with-deps chromium
      - run: python tests/october-sync.py
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: current-load-order-checks
          path: test-results/
          retention-days: 7
''')

report = {'baseline':BASE,'currentCount':224,'retainedFromPublished':sum(r['name'] in byname for r in old),'addedToPublished':[r['name'] for r in new if r['name'] not in oldnames],'removedFromPublished':[r['name'] for r in old if r['name'] not in byname],'sizeChanges':[{'name':r['name'],'before':oldnames[r['name']]['size'],'after':r['size']} for r in new if r['name'] in oldnames and r['size'] != oldnames[r['name']]['size']],'catalogRecords':len(catalog),'questRecords':len(qpack['quests']),'descriptionCards':len(reference['entries']),'positions':{name:byname[name]['n'] for name in ['SMIM Essentials','Daedra Pack - Mihail','Mihail High Fantasy Monsters','Dagoth Ur','Alternate Start - Live Another Life','Lucien - Fully Voiced Follower','Vokriinator [EN]']},'changedPaths':sorted(CHANGED)}
write('load-order-sync-report.json',dump(report))
print(json.dumps(report,ensure_ascii=False,indent=2))
