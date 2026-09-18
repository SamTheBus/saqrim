"""Expansion content, filters, compatibility and browser regressions."""
import functools,http.server,json,pathlib,subprocess,threading
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parents[1]; OUT=ROOT/'test-results';OUT.mkdir(exist_ok=True)
BASE='fa3967e753b2e923c4ec0aae59fc07ea08a9cd19'
checks=[]
def check(name,ok):
 assert ok,name
 checks.append(name);print('PASS',name,flush=True)
old=json.loads(subprocess.check_output(['git','show',BASE+':quests-data.json'],cwd=ROOT))['quests']
new=json.loads((ROOT/'quests-data.json').read_text())['quests']; by={q['id']:q for q in new}
check('original 22 quest objects preserved exactly',new[:22]==old)
check('46 stable sequential unique IDs',[q['id'] for q in new]==[f'Q{i:03}' for i in range(1,47)])
check('24 explicit expansion records',sum(q.get('batch')=='Expansion 2' for q in new)==24)
check('every new card has sources and start instructions',all(q.get('sources') and q['start'].get('trigger') for q in new[22:]))
for n in ['catalog-source.html','catalog-tags.js','catalog.js','load-order.tsv','load-order.js','faith-data.js','stones-data.js','map-locations.json','world-data.js','map.js','worlds.js']:
 check('unchanged '+n,(ROOT/n).read_bytes()==subprocess.check_output(['git','show',BASE+':'+n],cwd=ROOT))
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{server.server_port}/'
with sync_playwright() as p:
 browser=p.chromium.launch();ctx=browser.new_context(viewport={'width':1400,'height':1000});ctx.route('https://**',lambda r:r.abort())
 page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 def go(path,ready='window.SaqrimQuests'):
  page.goto(url+path);page.wait_for_function(ready)
 def ev(s):return page.evaluate(s)
 def reset():ev('SaqrimQuests.reset()');page.locator('#quest-filters').evaluate('(e)=>e.open=true');page.locator('.facet').evaluate_all('(es)=>es.forEach(e=>e.open=true)')
 def ids():return ev('SaqrimQuests.filtered.map(q=>q.id)')
 go('quests.html?batch=Expansion%202')
 check('new batch share link selects exactly 24',ids()==[q['id'] for q in new[22:]])
 check('old plus new full catalog available',ev('SaqrimQuests.catalog.size===617&&SaqrimQuests.quests.length===46'))
 check('quest tab navigation still has six destinations',page.locator('.nav a:not(.brand)').count()==6)
 check('all manual reward tags use exact vocabulary',ev('SaqrimQuests.quests.every(q=>q.rewards.every(r=>Object.entries(r.tags).every(([k,v])=>v.every(x=>SaqrimTags.groups.find(g=>g[0]===k)[2].includes(x)))))'))
 for i,school in enumerate(['Illusion','Conjuration','Destruction','Alteration','Restoration'],33):
  reset();page.fill('#quest-search',school+' Ritual Spell');page.check(f'input[data-group="school"][value="{school}"]')
  check(school+' ritual matches end-reward school filter',ids()==[f'Q{i:03}'])
 check('master Apocalypse tomes are unlocks not free rewards',ev('SaqrimQuests.quests.filter(q=>+q.id.slice(1)>=33&&+q.id.slice(1)<=37).every(q=>q.rewards.filter(r=>r.catalog).every(r=>r.kind==="unlock"))'))
 go('quests.html#Q023')
 check('unverified Abyss buff excluded from final payout',all(r['kind']=='lead' for r in by['Q023']['rewards']))
 check('only verified JaySerpa components expanded',set(q['id'] for q in new[22:] if q['lo']==145)=={'Q028','Q029','Q030','Q031'})
 check('Crusader distributed pieces not final awards',all(r['kind']=='optional' for r in by['Q032']['rewards']))
 check('Lucien riding reward not player horse','not a new horse' in by['Q027']['rewards'][0]['note'])
 check('Lucien quest starts are variable and unpinned',all(by[x]['start']['world']=='variable' and not by[x]['start'].get('mapPlace') for x in ['Q026','Q027']))
 go('quests.html#Q025')
 check('Elsweyr destination has no false world map',page.locator('#Q025 a[href*="world=elsweyr"]').count()==0 and ev('SaqrimQuests.mapURL({world:"elsweyr"})===null'))
 reset();page.check('input[data-group="slot"][value="Ring"]');check('Namira final ring found','Q041' in ids());check('excavation ring not falsely final','Q045' not in ids())
 page.select_option('#reward-scope','all');check('excavation ring found with route loot','Q045' in ids())
 page.check('input[data-group="armor"][value="Heavy armor"]');check('ring does not borrow heavy set tag','Q045' not in ids())
 go('quests.html#Q027');page.wait_for_selector('#Q027[open]')
 ev('localStorage.setItem("skyrimLootChoices_v202_20260917",JSON.stringify({W310:"Want"}));localStorage.setItem("saqrimObservedStats_v1",JSON.stringify({W012:{armor:123}}));localStorage.setItem("saqrim-load-order-220-2026-09-17","[1,2]")')
 previous=ev('JSON.stringify([localStorage.getItem("skyrimLootChoices_v202_20260917"),localStorage.getItem("saqrimObservedStats_v1"),localStorage.getItem("saqrim-load-order-220-2026-09-17")])')
 page.select_option('#status-Q027','In progress');page.check('#reward-Q027');page.fill('#notes-Q027','Waiting for Lucien');page.locator('#Q027 form button').click()
 backup=ev('SaqrimQuests.backup()');go('quests.html#Q027');check('new progress survives reload',page.input_value('#status-Q027')=='In progress' and page.is_checked('#reward-Q027') and page.input_value('#notes-Q027')=='Waiting for Lucien')
 page.evaluate('(s)=>SaqrimQuests.importProgress(s)',backup);check('new backup round trip',ev('SaqrimQuests.progress.Q027.notes==="Waiting for Lucien"'))
 check('item, stat and console saves unchanged',previous==ev('JSON.stringify([localStorage.getItem("skyrimLootChoices_v202_20260917"),localStorage.getItem("saqrimObservedStats_v1"),localStorage.getItem("saqrim-load-order-220-2026-09-17")])'))
 go('index.html#W310','window.SaqrimCatalog');page.wait_for_selector('#W310 .quest-catalog-links a[href="quests.html#Q045"]',state='attached');check('Unearthed reverse catalog link works',True)
 go('map.html#place=College%20of%20Winterhold','window.SaqrimQuestMap&&window.SaqrimBlessingsMap');page.wait_for_selector('#details .quest-starts')
 for i in range(33,38):check('map College link Q'+str(i),page.locator(f'#details .quest-starts a[href="quests.html#Q{i:03}"]').count()==1)
 # Original Q021's Fort Dawnguard reference is outside this atlas; this batch must not invent its coordinates.
 check('new mainland start references resolve',ev('SaqrimQuestMap.candidates().filter(q=>+q.id.slice(1)>=23).every(q=>SaqrimMap.places.some(p=>p.name===q.start.mapPlace))'))
 go('worlds.html?world=solstheim','window.SaqrimQuestMap&&window.SaqrimBlessingsMap')
 check('all Solstheim quest references resolve',ev('SaqrimQuestMap.candidates().every(q=>SaqrimWorlds.places.some(p=>p.world==="solstheim"&&p.name===q.start.mapPlace&&p.pin))'))
 check('three Solstheim start groups rendered',page.locator('.quest-start-icon').count()==3)
 for width in [390,320]:
  page.set_viewport_size({'width':width,'height':844});go('quests.html?batch=Expansion%202');check('new batch mobile fit '+str(width),ev('document.documentElement.scrollWidth<=innerWidth+1'))
 page.set_viewport_size({'width':390,'height':844});go('quests.html#Q033');page.wait_for_selector('#Q033[open]');page.locator('#Q033').scroll_into_view_if_needed();page.screenshot(path=str(OUT/'quest-expansion-mobile.png'))
 check('no JavaScript errors',not errors)
 report={'checks':len(checks),'errors':errors,'questCards':46,'added':24,'first':'Q023','last':'Q046'};(OUT/'quest-expansion-checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True);browser.close()
server.shutdown()
