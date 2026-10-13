"""Finalize display totals after add-content-batch-02.py; never touches load-order data."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
rp=ROOT/'CONTENT-BATCH-02-REPORT.json'
report=json.loads(rp.read_text())
changed=set(report['changedPaths'])
def edit(path,fn):
    p=ROOT/path;s=p.read_text();p.write_text(fn(s));changed.add(path)
def index(s):
    s=s.replace('633 Skyrim loot','637 Skyrim loot').replace('633 things to find','637 things to find')
    s=s.replace('not 633 guaranteed unique artifacts','not 637 guaranteed unique artifacts')
    s=s.replace('This current view adds 16 records and explicitly revises the reviewed artifact summaries;','The current view includes the artifact review and four October adventure unlock/book records;')
    s=s.replace('<a href="catalog-source.html">Open the complete reading version.</a>','<a href="catalog-current.html">Open the current reading version.</a>')
    s=s.replace('<a href="catalog-source.html">Read all 633 entries without JavaScript.</a>','<a href="catalog-current.html">Read all 637 entries without JavaScript.</a>')
    s=s.replace('Load order synced 23 September 2026.','October load order and adventure content.')
    assert '637 things to find' in s
    return s
edit('index.html',index)
def tests(s):
    s=re.sub(r'''(["']catalogEntries["']\s*:\s*)633''',lambda m:m[1]+'len(cat)',s)
    s=re.sub(r'''(["']referenceCards["']\s*:\s*)10''',lambda m:m[1]+"len(ref['entries'])",s)
    compile(s,'tests/october-sync.py','exec')
    return s
edit('tests/october-sync.py',tests)
def docs(s):
    s=s.replace('contains **46 quest and adventure cards**','contains **56 quest and adventure cards**',1)
    s=s.replace('## Starting points and destinations','## October adventure addition\n\nQ047–Q056 add four Orsinium stronghold entry points, two Undeath routes, two Cataclysm guides, Rooted In Madness and a qualified Dagoth companion profile. [Browse the batch](quests.html?batch=October%20adventures). Earlier collection and validation sections below describe their original releases.\n\n## Starting points and destinations',1)
    return s
edit('QUESTS.md',docs)
edit('README.md',lambda s:s.replace('633-target loot catalog','637-target loot catalog'))
p=ROOT/'load-order-reference.json';ref=json.loads(p.read_text())
ref['scope']='Ten earlier foundation/animation reviews plus five October adventure/companion previews. Linked quest guides carry starting instructions and content details. Exact unknown reward rosters are not fabricated.'
p.write_text(json.dumps(ref,ensure_ascii=False,indent=2)+'\n');changed.add('load-order-reference.json')
report['changedPaths']=sorted(changed)
rp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Content display totals reconciled: 637 catalog, 56 guides, 15 previews; 224-mod order unchanged.')
