"""Current October load-order, reference and browser regressions."""
from pathlib import Path
import functools, http.server, json, re, subprocess, threading
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1]
BASE = 'fdf1282fdb7a26596a64cf9aee1708005103af17'
OUT = ROOT/'test-results'; OUT.mkdir(exist_ok=True)
checks = []
def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)
    print('PASS',name,flush=True)
def old(path):
    return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def read(path):
    return (ROOT/path).read_text(encoding='utf-8')
def parse(text):
    rows = []
    for line in text.splitlines():
        if line.strip():
            n,name,size,version,time,category,title,thumb = line.split('\t')
            rows.append(dict(n=int(n),name=name,size=size,version=version,time=time,category=category,title=title,thumb=int(thumb)))
    return rows
lo = parse(read('load-order.tsv')); by = {r['name']:r for r in lo}; nums = {r['n']:r for r in lo}
prior = parse(old('load-order.tsv').decode())
check('224 contiguous unique entries',len(lo)==224 and len(by)==224 and [r['n'] for r in lo]==list(range(1,225)))
input_rows = []
for line in read('data/load-order-october-confirmed.txt').splitlines():
    if re.match(r'^\d{3} \| ',line):
        n,name,size,time = [x.strip() for x in line.split('|')]
        input_rows.append((int(n),name,size,time))
check('all rows exactly match final confirmed snapshot',[(r['n'],r['name'],r['size'],r['time']) for r in lo]==input_rows)
for name,n in {'SMIM Essentials':84,'Daedra Pack - Mihail':96,'Mihail High Fantasy Monsters':97,'Animated Armoury':103,'Heavy Armory - Animated Armoury Patch':104,"GDB's Elden Beast Lite Edition":105,'XPMSSE Plus - Custom Skeleton / bundle (PS5)':106,'Comprehensive First Person Animation Overhaul - alternative Lite port':107,'Lucien - Fully Voiced Follower':159,'Lucien - Anniversary Edition All-in-One Patch':160,'Lucien - Moonpath to Elsweyr Patch':161,'Dagoth Ur':217,'Alternate Start - Live Another Life':218,'Vokriinator [EN]':224}.items():
    check('position '+name,by[name]['n']==n)
check('both Orsinium patches distinct',nums[15]['size']=='33.3 KB' and nums[219]['size']=='33.4 KB' and nums[15]['name']!=nums[219]['name'])
check('exact final eight entries',[nums[n]['name'] for n in range(217,225)]==['Dagoth Ur','Alternate Start - Live Another Life','Legacy of Orsinium - [clipped title; v1.0.3.2 PS ONLY]','Vokrii - Minimalistic Perks of Skyrim','Ordinator - Perks of Skyrim','Ordinator - Fix - PS5 (textures)','Ordinator - Bone Collector (Windhelm altar fix)','Vokriinator [EN]'])
for name in ['KALLAX Storageborn','SMIM - Static Mesh Improvement Mod','Beyond Reach Part 1 (PS)','Beyond Reach Part 2 (PS)','Beyond Reach Revoiced','Simple Visible Favorited Gear']:
    check('not current '+name,name not in by)
for name in ['Deadly Dragons Armory','The Restless Dead (A Draugr [clipped title])','Xavbio 1K Base + DLC','Xavbio 1K AE/CC','A Ghibli Skyrim AIO 1K512 (PS)']:
    check('kept '+name,name in by)
for name,size in [('SMIM Essentials','98.94 MB'),('Dagoth Ur','1.37 GB'),("Morrowind's Bloodmoon Solstheim Content Restoration",'8.60 MB'),('DAWN - Dramatic Atmospheres, Weathers & Nature','98.47 MB'),("JaySerpa's Lines Expansion Bundle",'163.01 MB')]:
    check('current size '+name,by[name]['size']==size)
meta = json.loads(read('load-order-snapshot.json'))
check('provenance every row',set(meta['entries'])==set(by))
check('no invented post-swap storage reading',meta['currentUsed'] is None and meta['recordedUsed']=='14.73 GB')
for name in ['SMIM Essentials','Dagoth Ur']:
    check('user source '+name,meta['entries'][name]['sourceKind']=='user' and meta['entries'][name]['locator'] is None)
    check('no guessed version/art '+name,by[name]['version']=='Version not captured' and by[name]['thumb']==-1)
check('older metadata attributed',all('September' in meta['entries'][r['name']]['versionSource'] for r in prior if r['name'] in by))
for path in ['catalog-source.html','map-locations.json','world-data.js','faith-data.js','stones-data.js','map-links.js']:
    check('preserved '+path,(ROOT/path).read_bytes()==old(path))
new_soup = BeautifulSoup(read('catalog-current.html'),'html.parser')
cat = json.loads(new_soup.select_one('#dataset').string)
oldcat = json.loads(BeautifulSoup(old('catalog-current.html').decode(),'html.parser').select_one('#dataset').string)
check('633 catalog IDs retained',[r['Catalog ID'] for r in cat[:633]]==[r['Catalog ID'] for r in oldcat] and len(cat)==637)
mapping = {r['n']:by.get(r['name'],{}).get('n') for r in prior}
for r,o in zip(cat,oldcat):
    value = str(o.get('LO #','')).strip()
    prev = int(value) if value.isdigit() else None
    now = by.get(o.get('Installed mod',''),{}).get('n',mapping.get(prev))
    assert r['LO #']==(str(now) if now else ''),(r['Catalog ID'],r['LO #'],now)
    assert r['Installed mod']==o['Installed mod']
    label = new_soup.find(id=r['Catalog ID']).select_one('.mod-name')
    if label:
        assert ('#'+str(now)+' · ') in label.text if now else 'Not currently installed' in label.text
check('catalog numbers and retired labels match source identities',True)
retired = [r for r in cat if r['Installed mod'].startswith('Beyond Reach')]
check('Beyond Reach research kept but not labeled installed',bool(retired) and all(not r['LO #'] for r in retired))
qp = json.loads(read('quests-data.json'))
op = json.loads(old('quests-data.json'))
check('quest IDs and count retained',[q['id'] for q in qp['quests'][:46]]==[q['id'] for q in op['quests']])
for q,o in zip(qp['quests'],op['quests']):
    if isinstance(o.get('lo'),int):
        assert q['lo']==mapping.get(o['lo']),(q['id'],q['lo'],o['lo'])
    if isinstance(o.get('rewardMod'),dict) and isinstance(o['rewardMod'].get('lo'),int):
        assert q['rewardMod']['lo']==mapping.get(o['rewardMod']['lo'])
check('quest and reward-mod positions remapped once',True)
check('Q030 correct source bundle',next(q for q in qp['quests'] if q['id']=='Q030')['lo']==139)
ref = json.loads(read('load-order-reference.json'))
oref = json.loads(old('load-order-reference.json'))
check('original ten content descriptions retained',set(oref['entries'])<=set(ref['entries']) and len(ref['entries'])==15)
check('research sources and video locators unchanged',all(ref['sources'].get(k)==v for k,v in oref['sources'].items()) and ref['recording']==oref['recording'] and ref['reviewed']==oref['reviewed'])
check('related references resolve',all(n in by for e in ref['entries'].values() for n in e.get('related',[])))
check('every reference claim sourced',all(c.get('refs') and all(s in ref['sources'] for s in c['refs']) for e in ref['entries'].values() for c in [e['summary']]+[c for s in e['sections'] for c in s.get('claims',[])]))
check('artifact review IDs retained',set(json.loads(read('artifact-review.json'))['reviews'])==set(json.loads(old('artifact-review.json'))['reviews']))
listing = json.loads(read('load-order-bethesda.json'))
check('Bethesda matches are current or removed explicitly',set(listing['entries'])<=set(by))
for path in ROOT.glob('*.js'):
    subprocess.run(['node','--check',str(path)],check=True,capture_output=True)
check('all live JavaScript parses',True)
check('dynamic quest loader cache refreshed','site-quests.js?v=reward-research-01' in read('site-top.js'))
for path in ['index.html','load-order.html','map.html','quests.html','shrines.html','standing-stones.html','worlds.html','blessings.html']:
    soup = BeautifulSoup(read(path),'html.parser')
    check('current navigation '+path,soup.select_one('.nav a[href="load-order.html"]').text=='Load order · 224')
check('source hashes are valid existing assets',all(r['thumb']==-1 or 0<=r['thumb']<188 for r in lo))

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server = http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url = 'http://127.0.0.1:'+str(server.server_port)+'/'
errors = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={'width':390,'height':844})
    context.route('https://**',lambda route:route.abort())
    page = context.new_page()
    page.on('pageerror',lambda e:errors.append(str(e)))
    def load(path='load-order.html'):
        response = page.goto(url+path)
        assert response.ok
        page.wait_for_selector('#mods .row',timeout=20000)
    load()
    check('browser renders 224 entries',page.locator('#mods>.row').count()==224 and page.locator('#error').is_hidden())
    check('224 progress maximum',page.locator('#progress').get_attribute('max')=='224')
    page.fill('#search','Dagoth')
    check('Dagoth search correct identity',page.locator('#mods>.row:visible').count()==1 and page.locator('#mod-217').is_visible())
    page.click('#show-all');page.fill('#search','SMIM')
    check('SMIM search only Essentials',page.locator('#mods>.row:visible').count()==1 and 'Essentials' in page.locator('#mod-084 h2').inner_text())
    page.click('#show-all')
    check('fifteen expanded references render',page.locator('.ref-card').count()==15)
    page.select_option('#reference-view','expanded')
    check('expanded filter stays functional',page.locator('#mods>.row:visible').count()==15)
    page.fill('#jump-number','217');page.click('#jump-form button')
    check('jump clears description filter',page.locator('#mod-217').is_visible() and page.locator('#reference-view').input_value()=='')
    page.locator('#mod-217>details').last.evaluate('(d)=>d.open=true')
    check('Dagoth marked post-recording, not guessed', 'No video timestamp or version is invented' in page.locator('#mod-217').inner_text())
    page.locator('#mod-096>details').last.evaluate('(d)=>d.open=true')
    check('Daedra correction visible','Sam moved it immediately above' in page.locator('#mod-096').inner_text())
    page.locator('#mod-106 .ref-card').evaluate('(d)=>d.open=true')
    check('reference links use new GDB number',page.locator('#mod-106 .ref-related a[href="load-order.html#mod-105"]').count()>=1)
    check('no duplicate element IDs',page.evaluate('(()=>{const a=[...document.querySelectorAll("[id]")].map(n=>n.id);return a.length===new Set(a).size})()'))
    for width in [320,390,1400]:
        page.set_viewport_size({'width':width,'height':900})
        check('expanded rows fit '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
    page.set_viewport_size({'width':390,'height':844})
    page.screenshot(path=str(OUT/'load-order-october-mobile.png'),full_page=False)
    seed = {'saqrim-load-order-210-2026-09-23-v2':'[14,84,99,100,148,210]','skyrimLootChoices_v202_20260917':'{"W180":"Want"}','saqrimObservedStats_v1':'{"W180":{"damage":99}}','saqrimQuestProgress_v1':'{"Q001":{"status":"Completed","notes":"Keep my progress"}}'}
    page.evaluate('(seed)=>{localStorage.removeItem("saqrim-load-order-224-october-v1");for(const [k,v] of Object.entries(seed))localStorage.setItem(k,v)}',seed)
    page.reload();page.wait_for_selector('#mods>.row')
    checked = page.locator('#mods input[type="checkbox"]:checked').evaluate_all('(ns)=>ns.map(n=>Number(n.closest(".row").value)).sort((a,b)=>a-b)')
    check('old checkmarks follow identity, removed ones dropped',checked==[105,106,159,224])
    check('new additions not accidentally checked',not page.is_checked('#mod-084 input[type=checkbox]') and not page.is_checked('#mod-217 input[type=checkbox]'))
    check('all original saved keys untouched',page.evaluate('(seed)=>Object.entries(seed).every(([k,v])=>localStorage.getItem(k)===v)',seed))
    page.check('#mod-217 input[type=checkbox]');page.reload();page.wait_for_selector('#mod-217')
    check('current checkmarks persist',page.is_checked('#mod-217 input[type=checkbox]'))
    page.check('#hide-added')
    check('hide-added works',page.locator('#mod-217').is_hidden())
    page.goto(url+'index.html');page.wait_for_function('window.SaqrimCatalog',timeout=25000)
    check('catalog still loads all records',page.locator('#catalog>.card').count()==637)
    check('catalog uses current Artificer position','#56' in page.locator('#W629 .mod-name').inner_text())
    check('item choice remains saved',page.locator('#pick_W180').input_value()=='Want')
    page.goto(url+'quests.html#Q030');page.wait_for_function('window.SaqrimQuests',timeout=25000)
    check('quest link reaches current bundle',page.locator('#Q030 a[href="load-order.html#mod-139"]').count()==1)
    check('archived reward expansion preserved',page.evaluate('SaqrimQuests.quests.find(q=>q.id==="Q015").rewards.length')==sum(r['Installed mod']=='Beyond Reach Part 1 (PS)' for r in cat))
    retired_q = [q for q in qp['quests'] if q.get('lo') is None]
    for q in retired_q:
        check('retired quest has no incorrect current link '+q['id'],page.locator('#'+q['id']+' a[href^="load-order.html#mod-"]').count()==0)
    for path,ready in [('map.html','window.SaqrimMap'),('worlds.html?world=solstheim','window.SaqrimWorlds'),('shrines.html','window.SaqrimBlessingsPage'),('standing-stones.html','window.SaqrimBlessingsPage')]:
        page.goto(url+path);page.wait_for_function(ready,timeout=25000)
        check('page loads with updated navigation '+path,page.locator('.nav a[href="load-order.html"]').inner_text()=='Load order · 224')
    check('other saved state remains unchanged after browsing',page.evaluate('(seed)=>Object.entries(seed).every(([k,v])=>localStorage.getItem(k)===v)',seed))
    for mode in ['missing','malformed']:
        testctx = browser.new_context(viewport={'width':390,'height':844})
        testctx.route('**/load-order-reference.json*',lambda route:route.fulfill(status=404,body='missing'))
        testctx.route('**/load-order-snapshot.json*',lambda route:route.fulfill(status=404 if mode=='missing' else 200,body='not json'))
        tab=testctx.new_page();tab.on('pageerror',lambda e:errors.append(str(e)))
        tab.goto(url+'load-order.html');tab.wait_for_selector('#mods>.row')
        check(mode+' optional metadata does not break checklist',tab.locator('#mods>.row').count()==224)
        testctx.close()
    check('no browser JavaScript errors',not errors)
    browser.close()
server.shutdown()
report = {'checks':len(checks),'errors':errors,'currentEntries':224,'catalogEntries':len(cat),'referenceCards':len(ref['entries']),'baseline':BASE,'passed':checks}
(OUT/'october-sync-results.json').write_text(json.dumps(report,indent=2))
print('OCTOBER_SYNC_RESULT',json.dumps({k:v for k,v in report.items() if k!='passed'}),flush=True)

# The accepted content extension is also exercised by the existing main-branch CI.
import sys
subprocess.run([sys.executable,str(ROOT/"tests/content-batch-02.py")],cwd=ROOT,check=True)
