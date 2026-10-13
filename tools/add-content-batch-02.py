"""Add the sourced October adventures without changing the console load order.
Run on the content-batch-02 review branch; publishing is a separate reviewed action.
"""
from pathlib import Path
import copy, html, json, re, subprocess
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
BASE='92ef40a387cc8d4bf76b1ecb8e6192f8d9803813'
CACHE='content-batch-02'
P=json.loads((ROOT/'data/content-batch-02.json').read_text())
BATCH=P['batch']
assert P['baseline']==BASE

def baseline(path):
    return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT).decode('utf-8')
changed=[]
def put(path,text):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
    if not p.exists() or p.read_text()!=text:
        p.write_text(text,encoding='utf-8')
    changed.append(path)
def dumps(value):return json.dumps(value,ensure_ascii=False,indent=2)+'\n'
def replace_once(text,a,b):
    assert a in text, 'Missing integration anchor: '+a[:120]
    return text.replace(a,b)
def bust(text):
    names=['catalog.js','catalog-current.html','quests.js','quests-data.json','site-quests.js','site-top.js','map.js','worlds.js','load-order-reference.js','load-order-reference.json']
    for name in names:
        text=re.sub(re.escape(name)+r'\?v=[A-Za-z0-9_.-]+',name+'?v='+CACHE,text)
    return text
lo=[line.split('\t') for line in baseline('load-order.tsv').splitlines() if line.strip()]
by={r[1]:int(r[0]) for r in lo}
assert len(lo)==224
assert all(q['mod'] in by for q in P['quests'])

# Preserve Q001-Q046 verbatim; only append new guides.
qp=json.loads(baseline('quests-data.json'))
assert len(qp['quests'])==46
src=P['sources']
newq=[]
for raw in P['quests']:
    q=copy.deepcopy(raw)
    q['lo']=by[q['mod']];q['batch']=BATCH
    refs=q.pop('sourceRefs')
    q['sources']=[]
    for sid in refs:
        s=src[sid]
        q['sources'].append({'url':s.get('url','CONTENT-BATCH-02.md#recorded-description-evidence'), 'label':s['label'], 'scope':s.get('locator',s['note'])+(' · '+s['note'] if s.get('locator') else '')})
    for key in ['requirements','destinations','notes','chain']:
        q.setdefault(key,[])
    title=q.pop('connectTitle',None)
    if title:
        hits=[old for old in qp['quests'] if title.lower() in old['title'].lower()]
        assert len(hits)==1,(title,len(hits))
        q['chain'].append(hits[0]['id'])
    newq.append(q)
qp['quests'].extend(newq)
assert len(qp['quests'])==56
put('quests-data.json',dumps(qp))

# Append four catalog records and matching standalone HTML cards.
source=baseline('catalog-current.html')
soup=BeautifulSoup(source,'html.parser')
cat=json.loads(soup.select_one('#dataset').string)
assert len(cat)==633
newcards=[]
def esc(s):return html.escape(str(s),quote=True)
for item in P['loot']:
    sid=item['sourceRef'];s=src[sid];n=by[item['mod']]
    row={'Target':item['name'],'LO #':str(n),'Installed mod':item['mod'],
         'Where / unlock':item['where'],'Effect / interest':item['effect'],
         'When to look':item['when'],'Evidence status':'Author-documented; PS5 playthrough not independently tested',
         'Qualifications':item['note'],'Source URL':s['url'],'Found?':'Not checked','Type':item['type'],
         'Acquisition':item['acquisition'],'Region / route':'Undeath adventure','My choice':'Undecided',
         'Checked on':P['reviewed'],'Source scope':s['label'],'Catalog ID':item['id'],
         'Browse category':item['category'],'Content batch':BATCH}
    cat.append(row)
    rid=item['id']
    opts=''.join('<option value="'+v+'">'+v+'</option>' for v in ['Undecided','Want','Maybe','Skip'])
    card=f'''<details class="card" id="{rid}" data-id="{rid}" data-choice="Undecided">
<summary><span class="card-meta"><span class="id">{rid}</span><span class="saved-choice" id="badge_{rid}"></span></span>
<h3>{esc(item['name'])}</h3><p class="hook">{esc(item['effect'])}</p><p class="mod-name">#{n} · {esc(item['mod'])}</p>
<span class="expand-label"><span class="closed-label">Open location &amp; sources</span><span class="open-label">Location &amp; sources below</span></span></summary>
<div class="card-body"><h4>Where / how</h4><p class="location">{esc(item['where'])}</p><p class="tier">{esc(item['type'])} · {esc(item['when'])}</p>
<div class="choice-tools js-only" hidden><label for="pick_{rid}">My choice</label><select id="pick_{rid}" class="pick-select" data-pick-id="{rid}" disabled>{opts}</select></div>
<h4>Evidence &amp; caveats</h4><p class="evidence">Author-documented; PS5 playthrough not independently tested</p><p>{esc(item['note'])}</p>
<p><b>Acquisition:</b> {esc(item['acquisition'])}</p><p class="source-scope">{esc(s['label'])}</p>
<ul class="sources"><li><a href="{esc(s['url'])}" target="_blank" rel="noopener noreferrer">Original author documentation</a></li></ul>
<p class="record-status">Found: Not checked · Content batch: {esc(BATCH)}</p><a class="back-link" href="#top">Back to top</a></div></details>'''
    newcards.append(card)
assert len(cat)==637
pattern=r'(<script\b[^>]*\bid=[\"\x27]dataset[\"\x27][^>]*>).*?(</script>)'
assert len(re.findall(pattern,source,flags=re.S))==1
source=re.sub(pattern,lambda m:m[1]+json.dumps(cat,ensure_ascii=False).replace('</','<\\/')+m[2],source,flags=re.S)
source=replace_once(source,'</main>','\n'+ '\n'.join(newcards)+'\n</main>')
source=source.replace('Loot catalog · 633','Loot catalog · 637')
put('catalog-current.html',source)

# Five content previews link into the actual quest journal, not parallel articles.
rp=json.loads(baseline('load-order-reference.json'))
assert len(rp['entries'])==10
assert not(set(src)&set(rp['sources']))
rp['sources'].update(src)
qby={q['id']:q for q in newq}
for r in P['references']:
    guides=[{'label':qby[qid]['title'],'url':'quests.html#'+qid} for qid in r['guideIds']]
    if r['mod']=='Undeath (PS5 version)':
        guides.append({'label':'Browse the four new ritual / book records','url':'index.html?batch=October%20adventures'})
    rp['entries'][r['mod']]={'id':r['id'],'attention':False,'summary':{'text':r['summary'],'refs':r['refs']},
                            'sections':[],'related':[],'guides':guides,'reviewed':P['reviewed'],'batch':BATCH}
rp['contentBatches']=[{'name':BATCH,'reviewed':P['reviewed'],'questCount':10,'catalogCount':4}]
put('load-order-reference.json',dumps(rp))

# New current counts; unchanged IDs and save keys. Historical source files stay frozen.
for path in ['catalog.js','quests.js','map.js','worlds.js','site-top.js']:
    text=baseline(path)
    text=re.sub(r'\b633\b','637',text)
    if path=='quests.js':
        text=replace_once(text,'quests.length!==46','quests.length!==56')
        text=replace_once(text,"['Original collection','Expansion 2']","[...new Set(quests.map(q=>q.batch||'Original collection'))]")
    if path=='catalog.js':
        text=replace_once(text,'single=null, canSave=true','single=null, contentBatch=false, canSave=true')
        text=replace_once(text,"  if($('only-new').checked", "  if(contentBatch&&r['Content batch']!=="+json.dumps(BATCH)+")return false;\n  if($('only-new').checked")
        text=replace_once(text,"single=null;render();}\n function scrollResults", "single=null;contentBatch=false;render();}\n function scrollResults")
        text=replace_once(text,"if(single){const b=node('button','chip','Show other matches ×');", "if(contentBatch){const b=node('button','chip','October adventures ×');b.type='button';b.onclick=()=>{contentBatch=false;render();};active.append(b);}\n  if(single){const b=node('button','chip','Show other matches ×');")
        text=replace_once(text,"  render();openHash();", "  contentBatch=query.get('batch')==="+json.dumps(BATCH)+";\n  render();openHash();")
    put(path,bust(text))
put('site-quests.js',bust(baseline('site-quests.js')))

text=baseline('load-order-reference.js')
text=text.replace('Read mod reference · requirements, compatibility & sources','Read mod content & sources')
text=replace_once(text,"+state.pack.reviewed+' · '+state.pack.batch+", "+(e.reviewed||state.pack.reviewed)+' · '+(e.batch||state.pack.batch)+")
text=replace_once(text,"view==='attention'?Boolean(e?.attention):true", "view==='attention'?Boolean(e?.attention):view==='content'?e?.batch==='October adventures':true")
text=text.replace("'REFERENCE OVERHAUL · BATCH 01'","'ADVENTURES & MOD CONTENT'")
text=replace_once(text,"'Foundations, Lux modules and the animation block now have sourced reference cards. The other '","'New adventure and companion guides join the existing descriptions. The other '")
# Keep existing warnings inside their cards/filter; do not lead the content browser with troubleshooting.
text='\n'.join(line for line in text.splitlines() if "overview.append(node('p','ref-alert'" not in line)+'\n'
text=replace_once(text,"new Option('Expanded descriptions · '+names.length,'expanded')", "new Option('New adventures · 5','content'),new Option('Expanded descriptions · '+names.length,'expanded')")
text=replace_once(text,"[['Browse this batch','expanded'],['Review flagged cards','attention']]", "[['Browse new adventures','content'],['All expanded entries','expanded']]")
text=text.replace("['expanded','attention'].includes(requested)","['expanded','attention','content'].includes(requested)")
put('load-order-reference.js',bust(text))

# Discoverable shortcuts, shared navigation counts and refreshed script requests.
for path in ['index.html','load-order.html','quests.html','map.html','worlds.html','shrines.html','standing-stones.html','blessings.html']:
    text=baseline(path).replace('Loot catalog · 633','Loot catalog · 637')
    if path=='index.html':
        text=text.replace('633 targets','637 targets').replace('633 loot','637 loot')
        banner='<aside class="content-batch-callout"><strong>New: October adventures</strong><p>Orc strongholds, necromancy, endgame dungeons and a new companion.</p><a href="quests.html?batch=October%20adventures">Browse 10 new adventure / companion guides →</a> <a href="index.html?batch=October%20adventures">Four new ritual and book records →</a></aside>'
        text=replace_once(text,'</header>',banner+'</header>')
    if path=='quests.html':
        text=text.replace('46 quest','56 quest').replace('46 adventure','56 adventure')
        banner='<aside class="content-batch-callout"><strong>October adventures · 10 new guides</strong><p>Legacy of Orsinium · Undeath · The Final Cataclysm · Rotdyflissa · Dagoth Ur</p><a href="quests.html?batch=October%20adventures">Browse this content batch →</a></aside>'
        text=replace_once(text,'</header>',banner+'</header>')
    if path=='load-order.html':
        text=re.sub(r'<p class="intro">.*?</p>','<p class="intro">Your current 224-mod setup. Open the new adventure previews for starting instructions, things to discover, and linked quest and loot guides.</p>',text,flags=re.S)
    if path in ['index.html','quests.html']:
        style='<style>.content-batch-callout{margin:1.2rem 0;padding:1rem;border:1px solid currentColor;border-radius:10px;line-height:1.6;overflow-wrap:anywhere}.content-batch-callout p{margin:.4rem 0}.content-batch-callout a{display:inline-block;margin:.35rem 1rem .35rem 0}</style>'
        text=replace_once(text,'</head>',style+'</head>')
    put(path,bust(text))

# Additive, human-readable research record. Recording observations are timestamped, never presented as gameplay tests.
report={'baseline':BASE,'batch':BATCH,'questCount':56,'addedQuestIds':[q['id'] for q in newq],
        'catalogCount':637,'addedCatalogIds':[x['id'] for x in P['loot']],
        'referenceCount':15,'expandedMods':[r['mod'] for r in P['references']],
        'loadOrderCount':224,'loadOrderChanged':False,
        'mapReferencePlaces':[q['start']['mapPlace'] for q in newq if q['start'].get('mapPlace')],
        'unresolved':['Dagoth exact installed port and custom-quest trigger','Final Cataclysm initial PS5 contact','Individual reward rosters for Orsinium, Rotdyflissa, Cataclysm and Dagoth']}
md='''# Content batch 02 — October adventures

Ten new adventure / companion guides, four named ritual or book records, and five load-order content previews. The console order remains 224 entries.

## Browse

- [New quest and companion guides](quests.html?batch=October%20adventures)
- [Four new ritual and book records](index.html?batch=October%20adventures)
- [New mod content previews](load-order.html?reference=content)

Guide titles are editorial labels unless an actual quest title is supplied. A stronghold lead is not a complete quest walkthrough. Generic item categories remain leads, excluded from the normal end-reward view; they do not inflate the named loot catalog.

## Recorded description evidence

Source: the privately supplied `1a12e7fc6d46-master_playlist.mp4`. No new video hosting is implied.

- **00:55:** Legacy of Orsinium, menu v1.0.5. The description identifies the expanded Mor Khazgur mines, Agra Crun, other strongholds and Orsinium-inspired artifacts.
- **02:03.30–02:03.50:** Rotdyflissa, menu v1.00, 6.43 MB. Its description says that entering the tree near Movarth's Lair in Hjaalmarch starts **Rooted In Madness**. The magical roots, spellsword and new items/enemies are described. Old Whiterun instructions are not used for this recording.
- **02:03.80–02:04.00:** Undeath, PS5 v1.00. Credits Antioch08 and links Nexus 6180; this establishes the upstream project used for the FAQ, not proof that every PC feature was tested here.
- **02:13.00:** Final Cataclysm 2020, menu v1.00. Credits KittyTails and links Nexus 33167; names the dungeon adventure, bosses, equipment, weapons, spells and hub.
- Dagoth was added after the video. Public Creations descriptions provide a recruitment lead and project features; the precise 1.37 GB port is still unmatched.

## Scope

Mor Khazgur, Dushnikh Yal, Narzulbur and Largashbur have separate entry-point guides. Undeath's pursuit and optional transformation are separate routes. Cataclysm's main and bonus gates are separate. Rotdyflissa has a recording-confirmed start. Dagoth has a qualified companion / recruitment profile.

Existing calibrated exterior areas are reused. Movarth's Lair is a nearby landmark, Riverwood a town reference; neither is an invented exact spawn pin. No Cataclysm portal or Dragontail map was fabricated.

All original 633 catalog records, 46 quest objects and ten description objects remain unchanged. New identifiers append to those collections. Their browser-local choices, quest progress, ratings and installation checkmarks retain the same storage keys.

## Sources
'''
for sid,s in src.items():
    md+='\n### '+sid+'\n'+s['label']+'\n\n'+(s.get('url') or s.get('locator',''))+'\n\n'+s.get('note','')+'\n'
put('CONTENT-BATCH-02.md',md)
readme=baseline('README.md')+'\n\n## October adventure content\n\nThe current collection has 637 loot/power records, 56 quest/adventure guides, and 15 expanded mod descriptions. The 224-entry console order is unchanged. Content batch 02 covers Legacy of Orsinium, Undeath, The Final Cataclysm, Rotdyflissa and a qualified Dagoth recruitment profile. See [CONTENT-BATCH-02.md](CONTENT-BATCH-02.md). Earlier validation sections above describe historical batches.\n'
put('README.md',readme)

# Retain existing regression logic while allowing explicitly appended content.
t=baseline('tests/october-sync.py')
t=replace_once(t,"[r['Catalog ID'] for r in cat]==[r['Catalog ID'] for r in oldcat] and len(cat)==633", "[r['Catalog ID'] for r in cat[:633]]==[r['Catalog ID'] for r in oldcat] and len(cat)==637")
t=replace_once(t,"[q['id'] for q in qp['quests']]==[q['id'] for q in op['quests']]", "[q['id'] for q in qp['quests'][:46]]==[q['id'] for q in op['quests']]")
t=replace_once(t,"set(ref['entries'])==set(oref['entries']) and len(ref['entries'])==10", "set(oref['entries'])<=set(ref['entries']) and len(ref['entries'])==15")
t=replace_once(t,"ref['sources']==oref['sources']", "all(ref['sources'].get(k)==v for k,v in oref['sources'].items())")
t=t.replace(".count()==633", ".count()==637").replace(".count()==10", ".count()==15")
t=t.replace('site-quests.js?v=october-sync-1','site-quests.js?v='+CACHE)
t=t.replace("'ten existing content descriptions retained'","'original ten content descriptions retained'").replace("'ten expanded references still render'","'fifteen expanded references render'")
t=t.replace("'catalogEntries': 633","'catalogEntries': len(cat)").replace("'referenceCards': 10","'referenceCards': len(ref['entries'])")
t+='\n# The accepted content extension is also exercised by the existing main-branch CI.\nimport sys\nsubprocess.run([sys.executable,str(ROOT/"tests/content-batch-02.py")],cwd=ROOT,check=True)\n'
put('tests/october-sync.py',t)
report['changedPaths']=sorted(set(changed+['CONTENT-BATCH-02-REPORT.json']))
put('CONTENT-BATCH-02-REPORT.json',dumps(report))
print(json.dumps(report,indent=2))
