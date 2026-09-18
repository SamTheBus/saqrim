"""Documentation-level artifact audit tests, not proof of gameplay behavior."""
import functools, hashlib, http.server, json, pathlib, subprocess, threading
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parents[1];BASE='0d86612cb4a2a8853490747fab37919ca5c75a19'
OUT=ROOT/'test-results';OUT.mkdir(exist_ok=True);checks=[]
def check(name,ok):
 assert ok,name
 checks.append(name);print('PASS',name,flush=True)
def old(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def data(text):return json.loads(BeautifulSoup(text,'html.parser').select_one('#dataset').string)
archive=data(old('catalog-source.html'));current=data((ROOT/'catalog-current.html').read_text());by={r['Catalog ID']:r for r in current};audit=json.loads((ROOT/'artifact-review.json').read_text())['reviews']
check('633 unique records, stable W001–W633',[*sorted(by)]==[f'W{i:03}' for i in range(1,634)])
check('new familiar unique batch exactly 16',sum(r.get('Artifact batch')=='Familiar uniques 1' for r in current)==16)
check('original record ordering retained',[r['Catalog ID'] for r in current[:617]]==[r['Catalog ID'] for r in archive])
check('unreviewed original records equal archived objects',all(r==by[r['Catalog ID']] for r in archive if r['Catalog ID'] not in audit))
check('old choice and found fields never rewritten',all(all(r[k]==by[r['Catalog ID']][k] for k in ['My choice','Found?','Catalog ID']) for r in archive))
for file in ['catalog-source.html','load-order.tsv','load-order.js','map-locations.json','map-links.js','world-data.js','faith-data.js','stones-data.js']:
 check('unchanged '+file,(ROOT/file).read_bytes()==old(file))
oldq=json.loads(old('quests-data.json'));newq=json.loads((ROOT/'quests-data.json').read_text())
check('all 46 original quest objects preserved',newq['quests']==oldq['quests'])
check('six explicit quest-to-item additions',sum(map(len,newq['catalogLinks'].values()))==6)
check('zero claims of record verification',json.loads((ROOT/'artifact-review.json').read_text())['recordVerified']==0)
check('Fiery Souls includes final documented #91 after #71',audit['W180']['chain'].index('#61')<audit['W180']['chain'].index('#71')<audit['W180']['chain'].index('#91'))
for ident in ['W180','W539','W544','W545','W629','W630','W631','W632','W633']:
 check(ident+' later ArteFakes overlap visible',audit[ident]['status']=='Documented overlap' and '#91' in by[ident]['Effect / interest'] and 'unresolved' in by[ident]['Effect / interest'])
for ident in ['W307','W310','W367','W368','W542']:
 check(ident+' later ring edit possible not certified',audit[ident]['status']=='Possible later edit' and '#110' in audit[ident]['chain'] and 'NOT a proven' in audit[ident]['chain'])
check('Harkon sword not conflated with standalone Volkihar relic',audit['W547']['status']=='Expected from documentation' and 'NOT established' in audit['W177']['expected'])
check('NPC shield acquisition is not an assumed ARMO override','not prove' in audit['W187']['expected'])
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
with sync_playwright() as p:
 browser=p.chromium.launch();ctx=browser.new_context(viewport={'width':1440,'height':960});ctx.route('https://**',lambda r:r.abort());page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 def ev(s):return page.evaluate(s)
 def go(path,ready='window.SaqrimCatalog'):
  page.goto(base+path);page.wait_for_function(ready,timeout=25000)
 def ids():return ev('SaqrimCatalog.records.filter(i=>!i.card.hidden).map(i=>i.id)')
 def filter_group(group,value):
  page.locator('#filter-panel').evaluate('(n)=>n.open=true');page.locator('.facet').evaluate_all('(ns)=>ns.forEach(n=>n.open=true)');page.check('input[data-group="'+group+'"][value="'+value+'"]')
 go('index.html?batch=Familiar%20uniques%201');check('batch URL shows exactly new 16',ids()==[f'W{i}' for i in range(618,634)])
 check('all original and new cards render',page.locator('#catalog>.card').count()==633)
 check('all manual classification vocabulary valid',ev('SaqrimCatalog.records.every(r=>Object.entries(r.meta.tags).every(([k,v])=>v.every(x=>SaqrimTags.groups.find(g=>g[0]===k)?.[2].includes(x))))'))
 check('new base damage/armor are unknown not borrowed',ev('SaqrimCatalog.records.filter(r=>+r.id.slice(1)>617).every(r=>r.meta.stats.damage===null&&r.meta.stats.armor===null)'))
 ev('SaqrimCatalog.reset()');filter_group('origin','Changed vanilla / DLC unique');filter_group('review','Documented overlap')
 check('origin AND overlap isolates nine known overlaps',set(ids())=={'W180','W539','W544','W545','W629','W630','W631','W632','W633'})
 ev('SaqrimCatalog.reset()');filter_group('origin','Changed vanilla / DLC unique');filter_group('armor','Heavy armor');filter_group('slot','Body / robes')
 check('heavy torso filter includes new Ebony Mail','W620' in ids())
 ev('SaqrimCatalog.reset()');page.check('#only-new');check('earlier discovery batch remains 66',len(ids())==66 and set(ids())=={f'W{i}' for i in range(552,618)})
 go('index.html#W180');page.wait_for_selector('#W180[open]');check('axe headline does not promise Emberwisps','Emberwisp' not in page.locator('#W180>summary').inner_text())
 page.locator('#W180 .artifact-audit>summary').click();check('old axe benefit retained as earlier reference','Emberwisps' in page.locator('#W180 .artifact-audit').inner_text())
 ev('localStorage.setItem("skyrimLootChoices_v202_20260917",JSON.stringify({W180:"Want",W633:"Maybe"}));localStorage.setItem("saqrimObservedStats_v1",JSON.stringify({W012:{armor:123}}));localStorage.setItem("saqrim-load-order-220-2026-09-17","[1,2]");localStorage.setItem("saqrimQuestProgress_v1",JSON.stringify({Q033:{status:"In progress",notes:"Keep my note",rewardCollected:false}}))')
 saved=ev('JSON.stringify({...localStorage})');go('index.html#W633');check('old and new picks are read',page.input_value('#pick_W180')=='Want' and page.input_value('#pick_W633')=='Maybe')
 page.click('#backup');backup=page.input_value('#transfer-text');check('backup covers 633 and preserves personal stats',json.loads(backup)['catalogTargets']==633 and json.loads(backup)['ratings']['W012']['armor']==123)
 page.click('#close-transfer');page.click('#import');page.fill('#transfer-text',backup);page.click('#apply-import');check('new item choice round trip',page.input_value('#pick_W633')=='Maybe')
 # Import writes choices intentionally. Snapshot after import, then verify navigation performs no writes.
 saved=ev('JSON.stringify({...localStorage})')
 go('quests.html#Q042','window.SaqrimQuests');page.wait_for_selector('#Q042[open]')
 check('shield quest displays reviewed conflict',page.locator('#Q042 [data-catalog="W633"] .artifact-audit').count()==1 and '#91' in page.locator('#Q042 [data-catalog="W633"]').inner_text())
 check('quest data includes all 633 current records',ev('SaqrimQuests.catalog.size===633'))
 check('quest receives current artifact tags, not old guessed armor class',ev('SaqrimQuests.quests.find(q=>q.id==="Q042").rewards.find(r=>r.catalog==="W633").tags.armor.includes("Unknown")'))
 go('quests.html#Q046','window.SaqrimQuests');check('Deathbrand preserves separate reward roles',ev('SaqrimQuests.quests.find(q=>q.id==="Q046").rewards.some(r=>r.catalog==="W631"&&r.kind==="completion")&&SaqrimQuests.quests.find(q=>q.id==="Q046").rewards.some(r=>r.catalog==="W632"&&r.kind==="optional")'))
 go('index.html#W624');page.wait_for_selector('#W624 .quest-catalog-links a[href="quests.html#Q020"]',state='attached');check('new item reverse quest link works',True)
 go('map.html#W180','window.SaqrimMap&&window.SaqrimQuestMap&&window.SaqrimBlessingsMap');check('mainland shows current audit',page.locator('#details .artifact-audit').count()>0 and ev('SaqrimMap.records.length===633'))
 go('worlds.html?world=solstheim','window.SaqrimWorlds&&window.SaqrimQuestMap&&window.SaqrimBlessingsMap');check('realm index uses current dataset',ev('SaqrimWorlds.records.length===633&&SaqrimWorlds.records.find(r=>r.id==="W631").raw["Artifact review status"]==="Documented overlap"'))
 check('no save writes while browsing',saved==ev('JSON.stringify({...localStorage})'))
 for width in [390,320]:
  page.set_viewport_size({'width':width,'height':844});go('index.html?batch=Familiar%20uniques%201');check('mobile new catalog fits '+str(width),ev('document.documentElement.scrollWidth<=innerWidth+1'));check('six tabs and updated count '+str(width),page.locator('.nav a:not(.brand)').count()==6 and '633' in page.locator('.nav').inner_text())
 page.set_viewport_size({'width':390,'height':844});go('index.html#W180');page.locator('#W180 .artifact-audit>summary').click();page.locator('#W180').scroll_into_view_if_needed();page.screenshot(path=str(OUT/'artifact-review-mobile.png'))
 page.evaluate('window.scrollTo(0,document.body.scrollHeight)');page.wait_for_function('!document.getElementById("saqrim-top").hidden');page.click('#saqrim-top');check('Top remains instant',ev('scrollY===0'))
 check('no JavaScript errors',not errors)
 report={'checks':len(checks),'errors':errors,'catalogCount':633,'added':16,'reviewed':len(audit),'recordVerified':0};(OUT/'artifact-review-checks.json').write_text(json.dumps(report,indent=2));print('RESULT',json.dumps(report),flush=True);browser.close()
server.shutdown()
