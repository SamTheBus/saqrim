"""Build a reviewed current catalog from the immutable 617-entry research snapshot."""
import collections, copy, html, json, os, pathlib, re, runpy, subprocess
from bs4 import BeautifulSoup
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE='0d86612cb4a2a8853490747fab37919ca5c75a19'
def old(path):
    local=os.environ.get('SAQRIM_BASE_SOURCE')
    return (pathlib.Path(local)/path).read_text() if local else subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT).decode()
def put(path,text):
    out=ROOT/path;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text,encoding='utf-8')
def replace(text,a,b):
    if a not in text:raise RuntimeError('Missing expected integration anchor: '+a[:120])
    return text.replace(a,b)
def esc(x):return html.escape(str(x),quote=True)
def js(x):return json.dumps(x,ensure_ascii=False).replace('<','\\u003c')
def counts(text):return re.sub(r'(?<![A-Za-z0-9])617(?![A-Za-z0-9])','633',text)
spec=runpy.run_path(str(ROOT/'tools/artifact-review-data.py'))
original=json.loads(BeautifulSoup(old('catalog-source.html'),'html.parser').select_one('#dataset').string)
rows,audits=spec['build'](original)
for r in rows:
    if r['Catalog ID'] in audits:r['Artifact audit']=audits[r['Catalog ID']]

AUDIT_FIELDS=[('basis','Evidence level'),('expected','Expected version / unresolved winner'),('chain','Recorded order / scope'),('earlierEffect','Earlier documented benefit — not a final effect'),('appearance','Appearance / assets'),('acquisition','Acquisition / distribution'),('verification','What is not verified')]
def audit_html(a):
    fields=''.join('<h4>'+esc(label)+'</h4><p>'+esc(a[key])+'</p>' for key,label in AUDIT_FIELDS if a.get(key))
    links=''.join('<p><a href="'+esc(u)+'" target="_blank" rel="noopener noreferrer">Review source '+str(n)+'</a></p>' for n,u in enumerate(a['sources'],1))
    return '<details class="artifact-audit"><summary>Load-order review · '+esc(a['status'])+'</summary>'+fields+links+'</details>'
def card(r):
    ident=r['Catalog ID'];a=r.get('Artifact audit');audit=audit_html(a) if a else ''
    badge='<p class="artifact-status">'+esc(a['status'])+' · winning PS5 records uninspected</p>' if a else ''
    fields=''.join('<h4>'+esc(k)+'</h4><p>'+esc(r.get(k,''))+'</p>' for k in ['Evidence status','Qualifications','Source scope'])
    sources=''.join('<li><a href="'+esc(u)+'" target="_blank" rel="noopener noreferrer">Source '+str(i)+'</a></li>' for i,u in enumerate(re.split(r'\s*[|\n]\s*',r.get('Source URL','')),1) if u.startswith('https://'))
    return '<details class="card" id="'+ident+'" data-id="'+ident+'" data-choice="'+esc(r['My choice'])+'" open><summary><div class="card-meta"><span class="id">'+ident+'</span><span class="saved-choice" id="badge_'+ident+'"></span></div><h3>'+esc(r['Target'])+'</h3>'+badge+'<p class="hook">'+esc(r['Effect / interest'])+'</p><p class="mod-name">Documented source · #'+esc(r['LO #'])+' · '+esc(r['Installed mod'])+'</p><span class="expand-label">Open location, load-order review & sources</span></summary><div class="card-body"><h4>Where / how</h4><p class="location">'+esc(r['Where / unlock'])+'</p><p class="tier">'+esc(r['Type'])+' · '+esc(r['When to look'])+'</p><div class="choice-tools js-only" hidden><label for="pick_'+ident+'">My choice</label><select id="pick_'+ident+'" class="pick-select" data-pick-id="'+ident+'" disabled>'+''.join('<option>'+x+'</option>' for x in ['Undecided','Want','Maybe','Skip'])+'</select></div>'+audit+fields+'<p><b>Acquisition:</b> '+esc(r['Acquisition'])+'<br><b>Region:</b> '+esc(r['Region / route'])+'</p><ul class="sources">'+sources+'</ul><p class="record-status">Found: '+esc(r['Found?'])+' · Source check: '+esc(r['Checked on'])+'</p><a class="back-link" href="#top">Back to top</a></div></details>'
nav=re.search(r'<nav class="nav".*?</nav>',old('index.html'),re.S).group(0)
nav=counts(nav)
# Static cards and JSON share the same source, while the original file remains byte-for-byte intact.
page='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Saqrim · Current catalog reading view</title><link rel="stylesheet" href="catalog.css?v=4"><script defer src="site-top.js?v=9"></script></head><body id="top">'+nav+'<header class="hero"><div class="eyebrow">CURRENT REFERENCE · DOCUMENTED EXPECTATIONS, NOT A PLUGIN SCAN</div><h1>633 things to discover.</h1><p>16 familiar unique items added. Relevant existing entries now separate documented effects, later-editor risks, appearance and acquisition. No item is certified as the final PS5 record by this review.</p><p><a href="./?batch=Familiar%20uniques%201">Browse the new familiar uniques</a> · <a href="ARTIFACT-REVIEW.md">Review scope</a> · <a href="catalog-source.html">Unmodified 617-entry research archive</a></p></header><main class="layout" style="display:block"><div id="catalog" class="grid">'+''.join(card(r) for r in rows)+'</div></main><script id="dataset" type="application/json">'+js(rows)+'</script><footer>Current catalog reading view. Use the interactive catalog to save choices. Original item IDs and your existing browser progress are retained.</footer></body></html>'
put('catalog-current.html',page)
put('artifact-review.json',json.dumps({'version':1,'date':'2026-09-18','baseline':BASE,'catalogCount':633,'added':16,'recordVerified':0,'scope':'Recorded-order and public-documentation review; NOT an xEdit or PS5 plugin scan.','reviews':audits,'screenedRoles':[{'lo':lo,'name':name,'scope':scope} for lo,name,scope in spec['ROLES']]},ensure_ascii=False,indent=2)+'\n')

# Shared tags and a safe DOM renderer work in the catalog, maps and quest reward cards.
t=old('catalog-tags.js')
t=replace(t,'return {tags,stats,notes,urls:[...urls]};',"tags.origin=[r['Artifact origin']||'Unreviewed / other'];tags.review=r['Artifact review status']?[r['Artifact review status']]:[];\n  return {tags,stats,notes,urls:[...urls]};")
t=replace(t,"['choice','My choices'", "['origin','Item origin',['Changed vanilla / DLC unique','Replacement thane reward','Creation relic','Mod-added / other','Unreviewed / other']],\n  ['review','Artifact review',['Expected from documentation','Documented overlap','Possible later edit','Identity / acquisition check']],\n  ['choice','My choices'")
renderer=r'''function auditNode(raw){
 const a=raw['Artifact audit'];if(!a)return null;const box=document.createElement('details');box.className='artifact-audit';box.style.cssText='border:1px solid #c5ab76;border-radius:8px;padding:12px;margin:14px 0;font-size:14px;overflow-wrap:anywhere';
 const summary=document.createElement('summary');summary.textContent='Load-order review · '+a.status;box.append(summary);
 for(const [key,label]of FIELD_LIST){if(!a[key])continue;const h=document.createElement('h4'),p=document.createElement('p');h.textContent=label;p.textContent=a[key];box.append(h,p);}
 for(const [i,url]of a.sources.entries()){if(!url.startsWith('https://'))continue;const p=document.createElement('p'),link=document.createElement('a');link.textContent='Review source '+(i+1);link.href=url;link.target='_blank';link.rel='noopener noreferrer';p.append(link);box.append(p);}return box;
 }
'''.replace('FIELD_LIST',js(AUDIT_FIELDS))
t=replace(t,'return {classify,groups};',renderer+' return {classify,groups,auditNode};');put('catalog-tags.js',t)

# Only the current runtime switches to the reviewed derivative. Archive contents are untouched.
for name in ['catalog.js','map.js','worlds.js','quests.js']:
    t=old(name).replace("fetch('catalog-source.html')","fetch('catalog-current.html?v=1')")
    t=counts(t)
    if name=='catalog.js':
        t=replace(t,"if($('only-new').checked&&Number(item.id.slice(1))<=551)return false;","if($('only-new').checked&&(Number(item.id.slice(1))<=551||Number(item.id.slice(1))>617))return false;\n  if($('only-artifact-batch').checked&&r['Artifact batch']!=='Familiar uniques 1')return false;")
        t=replace(t,"$('only-new').checked=false;","$('only-new').checked=false;$('only-artifact-batch').checked=false;")
        t=replace(t,"'only-new','stat-source'","'only-new','only-artifact-batch','stat-source'")
        t=replace(t,'catalogTargets:633','catalogTargets:data.length')
        t=replace(t,"storageNote();render();openHash();", "storageNote();\n  const query=new URLSearchParams(location.search);for(const [group,,vals]of SaqrimTags.groups)for(const value of query.getAll(group))if(vals.includes(value)){selected[group].add(value);inputs.find(i=>i.group===group&&i.val===value).input.checked=true;}if(query.get('batch')==='Familiar uniques 1')$('only-artifact-batch').checked=true;\n  render();openHash();")
    if name=='map.js':
        t=replace(t,"a.append(el('p','',r.raw['Effect / interest']));","a.append(el('p','',r.raw['Effect / interest']));const audit=SaqrimTags.auditNode(r.raw);if(audit)a.append(audit);")
    if name=='worlds.js':
        t=replace(t,"const refs=node('div','source-links');", "const audit=SaqrimTags.auditNode(r.raw);if(audit)a.append(audit);const refs=node('div','source-links');")
    if name=='quests.js':
        t=t.replace("'armor','slot']);","'armor','slot','origin','review']);")
        t=replace(t,"const rewardRows=[...(q.rewards||[])];", "const rewardRows=(q.rewards||[]).map(r=>({...r,...(pack.catalogLinks?.[q.id]?.[r.label]||{})}));")
        t=replace(t,"a.append(node('p','',item['Effect / interest']));", "a.append(node('p','',item['Effect / interest']));const audit=SaqrimTags.auditNode(item);if(audit)a.append(audit);")
        t=t.replace("quests-data.json?v=2","quests-data.json?v=3")
    # Old sources can contain both pipe and newline separators.
    t=t.replace(r".split(/\s*\|\s*/)",r".split(/\s*[|\n]\s*/)")
    put(name,t)

# Keep every original quest object identical; add explicit, quest-scoped item links separately.
pack=json.loads(old('quests-data.json'));pack['catalogLinks']=spec['QUEST_LINKS'];pack['catalogLinksScope']='Links to current artifact review; original quest records and reward roles are unchanged.'
put('quests-data.json',json.dumps(pack,ensure_ascii=False,indent=1)+'\n')
t=old('site-quests.js').replace('quests-data.json?v=2','quests-data.json?v=3')
t=replace(t,"const rewards=[...(q.rewards||[])];", "const rewards=(q.rewards||[]).map(r=>({...r,...(pack.catalogLinks?.[q.id]?.[r.label]||{})}));")
put('site-quests.js',t)
t=old('site-top.js').replace('Loot catalog · 617','Loot catalog · 633').replace('site-quests.js?v=2','site-quests.js?v=3')
# The current reading view is still a Loot catalog destination.
t=t.replace("'catalog-source.html']","'catalog-source.html','catalog-current.html']")
put('site-top.js',t)

for name in ['index.html','load-order.html','map.html','worlds.html','quests.html','shrines.html','standing-stones.html','blessings.html']:
    t=counts(old(name))
    for file,version in [('catalog-tags.js',4),('catalog.js',4),('site-top.js',9),('map.js',2),('worlds.js',2),('quests.js',3),('catalog.css',4)]:
        t=re.sub(re.escape(file)+r'\?v=\d+',file+'?v='+str(version),t)
    if name=='index.html':
        t=replace(t,'<div id="facets"></div>', '<div id="facets"></div><label class="tick"><input id="only-artifact-batch" type="checkbox" disabled>New familiar uniques · W618–W633 (16)</label>')
        t=t.replace('New batch only · W552–W617','Earlier discovery batch · W552–W617')
        t=replace(t,'<div class="hero-pills">','<p><a href="./?batch=Familiar%20uniques%201">New familiar uniques →</a> · <a href="./?origin=Changed%20vanilla%20%2F%20DLC%20unique">Changed vanilla / DLC uniques →</a></p><div class="hero-pills">')
        t=t.replace('All 633 original records, evidence notes and sources are retained.','The original 617-entry research archive is retained. This current view adds 16 records and explicitly revises the reviewed artifact summaries; original IDs and saved choices are preserved.')
        t=t.replace('Original reading version and research snapshot','Original 617-entry research archive')
        t=t.replace('Filter update 17 September 2026','Artifact review 18 September 2026')
        t=t.replace('<details class="scope">','<p class="notice">Artifact effects are documentation-based expectations, not certified PS5 winning records. Open an item\'s load-order review for later-editor risks. <a href="ARTIFACT-REVIEW.md">Audit scope and sources</a>.</p><details class="scope">')
    if name in ['map.html','worlds.html','quests.html']:
        t=t.replace('Original 633','Current 633').replace('All 633 original','All 633 current').replace('original 633','current 633')
    put(name,t)
put('catalog.css',old('catalog.css')+'\n/* Artifact provenance is independent of the numeric-stat and choice controls. */\n.artifact-status{font-size:12px;color:#efcc8a;border-left:3px solid #efcc8a;padding-left:9px}.artifact-audit{margin:14px 0;border:1px solid #9d885f;padding:12px;border-radius:8px;overflow-wrap:anywhere}.artifact-audit>summary{padding:0;color:#efcc8a;cursor:pointer;font-size:14px}.artifact-audit h4{margin-top:15px}.artifact-audit a{overflow-wrap:anywhere}\n')

# Historical byte-equality assertions no longer apply to these intentionally modified UI modules.
# Keep all untouched-data guards; the new suite verifies archive equality and every allowed data change.
changed_core={'catalog-tags.js','catalog.js','map.js','worlds.js','site-quests.js'}
for name in ['blessings-browser.py','map-browser.py','world-browser.py','navigation-browser.py','quest-browser.py','quest-expansion-browser.py']:
    t=old('tests/'+name)
    for file in changed_core:
        t=re.sub(r"^\s*'"+re.escape(file)+r"':'[a-f0-9]+',?\n",'',t,flags=re.M)
        t=t.replace("'"+file+"',",'').replace(",'"+file+"'",'')
    t=counts(t)
    t=t.replace('original 633','current 633').replace('all 633 original','all 633 current')
    if name=='map-browser.py':
        # 633 current records minus the unchanged 103 mainland associations.
        t=replace(t,'all 514 unpinned notes available','all 530 unpinned notes available')
        t=replace(t,'SaqrimMap.filteredItems.length===514','SaqrimMap.filteredItems.length===530 && SaqrimMap.filteredItems.length===SaqrimMap.records.filter(r=>!r.links.length).length')
    put('tests/'+name,t)

summary=collections.Counter(a['status'] for a in audits.values())
report={'baseline':BASE,'original':617,'current':633,'added':16,'reviewed':len(audits),'statusCounts':dict(summary),'recordVerified':0,'newIDs':[f'W{i}' for i in range(618,634)]}
put('artifact-build-report.json',json.dumps(report,indent=2)+'\n')
roles='\n'.join(f'| {lo} | {name} | {scope} |' for lo,name,scope in spec['ROLES'])
put('ARTIFACT-REVIEW.md',f'''# Familiar uniques and load-order review — 18 September 2026

## Coverage

The current catalog contains **633 records**: the original 617 IDs plus **16 additions, W618–W633**. The archived `catalog-source.html` remains byte-for-byte unchanged. The current rendering uses `catalog-current.html`, which adds the new items and revises reviewed existing entries. {len(audits)} records have item-specific provenance panels. No record is certified as the final PS5 winner.

New items: Dawnbreaker, Ebony Blade, Ebony Mail, Mace of Molag Bal, Mehrunes' Razor, Savior's Hide, Auriel's Bow, Bloodskal Blade, Gauldur Amulet, Staff of Magnus, Arch-Mage's Robes, Dragonbane, Ghostblade, Soulrender, Bloodscythe and Shield of Solitude.

Use the Item origin and Artifact review checkbox groups. The separate New familiar uniques checkbox selects exactly W618–W633. `?batch=Familiar%20uniques%201` opens that batch. The earlier W552–W617 discovery checkbox still selects its original 66 records.

## What follows the load order

This reviews the recorded 220-entry order and cited public descriptions, not the actual ESP/ESM records or a save. For two plugins overriding the same FormID, the later whole record normally wins; arbitrary fields are not automatically combined. Referenced enchantments, effects, scripts, quest rewards, placed references and texture/mesh assets require their own checks. An item name or visual purpose alone does not establish record identity.

- **Fiery Souls:** #61 Artificer, #71 Truly Unique, then #91 ArteFakes. ArteFakes is the latest documented named-item editor. The final enchantment is unresolved, not automatically the #71 Emberwisp version or a guaranteed vanilla reversion.
- **Other #91 overlaps:** Bow of the Stag Prince, Dawnguard Rune Axe and Hammer, Dragonbane, Ghostblade, Soulrender, Bloodscythe and Shield of Solitude. Earlier Artificer effects are not displayed as certified final effects.
- **Thane rewards:** #72 Unique Thane Weapons follows #61 Artificer. Quest assignment and item records are distinct. No combined enchantment or retroactive inventory replacement is assumed.
- **Rings:** #110 Wear Multiple Rings is later; its individual ring-record membership and enchantment forwarding remain uninspected. This is a possible-overlap warning, not a proven winner.
- **Identity:** #74 Volkihar Relic Sword is not assumed to replace Harkon's Sword. Shared names for restored/added Prelate's Mace and Briarheart Geis need identity checks. Halidil carrying an Aetherial Shield is not proof of an ARMO override.

No separately named Artificer–ArteFakes reconciliation patch appears in the recorded list. The existing #62 Artificer–USSEP patch is not assumed to forward later mods. A public third-party patch is cited only as compatibility evidence; it is NOT treated as installed.

## Versions and effects

New Artificer summaries use author-reference **1.0.11**; the recorded PS5 menu says **v1.00**, which does not identify the upstream build. ArteFakes author-reference SE **2.0** and recorded **v2.0.1** are likewise not proof of identical payloads. Source documentation mixes some LE/SE features; those are not imported as guaranteed PS5 reforging options.

Numeric base armor/damage is not filled from vanilla tables, enchantment damage, armor bonuses or unrelated port versions. New base ratings remain unknown. Existing manually observed ratings stay separate. In particular Ebony Mail's armor bonus is not its base armor, and Bloodskal's projectile damage is not sword base damage.

## Documented-role screening

These are review priorities and distinctions, not a complete record-conflict matrix. Non-artifact-looking plugins and bundles may still contain relevant records. Exact winning effects require matching plugin records or scoped in-game evidence.

| Recorded order | Mod / group | Review scope |
|---|---|---|
{roles}

## Sources

Each new item carries its own original-author effects source and separately labeled base-game acquisition source. Existing research remains in the immutable archive. Relevant primary sources:

- [Artificer author](https://www.nexusmods.com/skyrimspecialedition/mods/99619)
- [ArteFakes author roster / compatibility](https://www.nexusmods.com/skyrimspecialedition/mods/41254)
- [Truly Unique axe author](https://www.nexusmods.com/skyrimspecialedition/mods/154943)
- [Unique Thane Weapons author](https://www.nexusmods.com/skyrimspecialedition/mods/35497)
- [Compatibility patch author — NOT installed](https://www.nexusmods.com/skyrimspecialedition/mods/99684)
- [xEdit conflict-resolution documentation](https://tes5edit.github.io/docs/5-conflict-detection-and-resolution.html)
- [Recorded PS5 order](https://www.youtube.com/watch?v=4uyqCADqwPo)

## Integration and preservation

The catalog, mainland map, realm indexes and quest rewards read the same reviewed data. All existing 46 quest objects remain identical; six explicit quest reward links connect the newly indexed items to existing cards through separate metadata. No extra quests or geographic coordinates are invented.

The six navigation destinations remain unchanged, with the current loot count updated everywhere. The 220-entry TSV, console checklist, thumbnails, file sizes, faith/stone data and all browser storage keys are unchanged. The archive preserves all old source wording. Opening a page does not migrate or overwrite item choices, personal ratings or quest progress.

## Validation scope

Tests check the original archive and untouched-data hashes, stable old and new IDs, allowed reviewed-record changes, unchanged quest objects, real item-source precedence flags, absence of invented base ratings, checkbox combinations, quest/catalog reverse links, map/realm data parity, mobile navigation, backup round trips and no save writes on startup. Browser tests do not certify gameplay behavior or PS5 winning records.
''')
print(json.dumps(report),flush=True)
