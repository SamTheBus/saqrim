"""Research preservation, evidence, filtering and real browser regressions.

Local: SAQRIM_BASELINE_DIR=/path/to/published/baseline
       SAQRIM_CHROMIUM=/usr/bin/chromium python tests/reward-research-01.py
CI: baseline is read directly from the pinned published Git commit.
"""
from pathlib import Path
import functools, hashlib, http.server, json, os, subprocess, threading
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
BASE='37c08fbf5033658490700f1ada2e808ea85d1edb'
OUT=ROOT/'test-results'; OUT.mkdir(exist_ok=True)
checks=[]
def check(name, ok):
    if not ok: raise AssertionError(name)
    checks.append(name); print('PASS RESEARCH',name,flush=True)
def before(name):
    directory=os.environ.get('SAQRIM_BASELINE_DIR')
    return (Path(directory)/name).read_bytes() if directory else subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
def read(name): return (ROOT/name).read_text(encoding='utf-8')
def data(name): return json.loads(read(name))
pack=data('data/reward-research-01.json'); report=data('REWARD-RESEARCH-01-REPORT.json')
for path in ['load-order.tsv','load-order-snapshot.json','load-order-bethesda.json','catalog-current.html','catalog-source.html','artifact-review.json','catalog-tags.js','map-locations.json','world-data.js','faith-data.js','stones-data.js','map-links.js']:
    check('byte-preserved '+path,(ROOT/path).read_bytes()==before(path))
oldq=json.loads(before('quests-data.json')); newq=data('quests-data.json')
qb={q['id']:q for q in newq['quests']}; ob={q['id']:q for q in oldq['quests']}
check('56 stable quest identities',list(qb)==list(ob) and len(qb)==56)
check('only six intended guide objects changed',{k for k in qb if qb[k]!=ob[k]}==set(pack['questUpdates']))
check('all existing starts and geographical positions unchanged',all(qb[k]['start']==ob[k]['start'] and qb[k]['destinations']==ob[k]['destinations'] and qb[k]['lo']==ob[k]['lo'] for k in qb))
check('all previously indexed real rewards preserved',all([r for r in qb[k]['rewards'] if r['kind']!='lead']==[r for r in ob[k]['rewards'] if r['kind']!='lead'] for k in qb))
check('Orsinium has 15 named leads',len(qb['Q047']['rewards'])==15 and all(r['kind']=='lead' and not r.get('catalog') for r in qb['Q047']['rewards']))
check('Cataclysm has eight leads plus its original unlock',len(qb['Q053']['rewards'])==9 and sum(r['kind']=='lead' for r in qb['Q053']['rewards'])==8)
check('all new lead sources resolve',all(r.get('sources') and all(s['url'].startswith('https://') and s['scope'] for s in r['sources']) for k in ['Q047','Q050','Q053','Q056'] for r in qb[k]['rewards'] if r['kind']=='lead'))
check('no complete-roster claim',report['completeRosters'] is False and newq['rewardResearch']['completeRosters'] is False)
check('Dagoth creator trigger explicitly upstream',any('creator-confirmed upstream' in n and 'random line after combat' in n for n in qb['Q056']['notes']))
check('unknown PS5 starts not promoted',all(qb[k]['start']['known'] is False for k in ['Q053','Q054','Q056']))
check('mask is not arbitrarily identified','exact item name unresolved' in qb['Q050']['rewards'][0]['label'])
check('Mazel Tov and cooking tip separated from recruitment','Mazel Tov' in qb['Q056']['title'] and 'cooking station rather than an alchemy table' in qb['Q056']['spoilers'] and qb['Q056']['start']==ob['Q056']['start'])
refs=data('load-order-reference.json'); oldrefs=json.loads(before('load-order-reference.json'))
check('15 stable mod previews',len(refs['entries'])==15 and set(refs['entries'])==set(oldrefs['entries']))
check('only four intended previews changed',{k for k in refs['entries'] if refs['entries'][k]!=oldrefs['entries'][k]}==set(pack['referenceUpdates']))
check('all old source objects preserved',all(refs['sources'][k]==s for k,s in oldrefs['sources'].items()))
check('new reference evidence resolves',all(c['refs'] and all(sid in refs['sources'] for sid in c['refs']) for e in refs['entries'].values() for sec in e['sections'] for c in sec.get('claims',[])))
check('generated content hashes match',all(hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==sha for n,sha in report['outputHashes'].items()))
check('idempotent build is verified',subprocess.run(['python',str(ROOT/'tools/apply-reward-research-01.py')],cwd=ROOT,check=True,capture_output=True).returncode==0)
for path in ROOT.glob('*.js'): subprocess.run(['node','--check',str(path)],check=True,capture_output=True)
check('all site JavaScript parses',True)
if os.environ.get('SAQRIM_STATIC_ONLY')=='1':
    print('REWARD_STATIC_RESULT '+json.dumps({'checks':len(checks),'browserRun':False,'completeRosters':False}),flush=True)
    raise SystemExit(0)
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url='http://127.0.0.1:'+str(server.server_port)+'/'
errors=[]
try:
    with sync_playwright() as pw:
        opts={'args':['--no-sandbox']}
        if os.environ.get('SAQRIM_CHROMIUM'): opts['executable_path']=os.environ['SAQRIM_CHROMIUM']
        browser=pw.chromium.launch(**opts)
        ctx=browser.new_context(viewport={'width':390,'height':844})
        ctx.route('https://**',lambda route:route.abort())
        page=ctx.new_page(); page.set_default_timeout(12000);page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(url+'index.html');page.wait_for_function('window.SaqrimCatalog')
        seed={'skyrimLootChoices_v202_20260917':'{"W180":"Want"}','saqrimObservedStats_v1':'{"W180":{"damage":99}}','saqrimQuestProgress_v1':'{"Q001":{"status":"Completed","notes":"old journal"},"Q056":{"status":"In progress","notes":"old Dagoth note"}}','saqrim-load-order-224-october-v1':'[84,159,217]'}
        page.evaluate('(s)=>{for(const[k,v]of Object.entries(s))localStorage.setItem(k,v)}',seed)
        page.goto(url+'quests.html#Q047');page.wait_for_function('window.SaqrimQuests')
        check('guide deep link opens',page.locator('#Q047').get_attribute('open') is not None)
        check('research lead list initially collapsed',page.locator('#Q047 .loot-group[data-group="lead"]').get_attribute('open') is None)
        page.locator('#Q047 .loot-group[data-group="lead"]>summary').click()
        check('15 named leads are visible with source links',page.locator('#Q047 .reward-row:visible').count()==15 and page.locator('#Q047 .reward-sources a').count()==15)
        check('external source links safe',page.locator('#Q047 .reward-sources a').evaluate_all('(a)=>a.every(x=>x.target==="_blank"&&x.rel.includes("noopener"))'))
        for width in [320,390,1400]:
            page.set_viewport_size({'width':width,'height':900})
            check('expanded research fits '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
        page.set_viewport_size({'width':390,'height':844})
        page.goto(url+'quests.html?mod=Legacy%20of%20Orsinium&category=Jewelry');page.wait_for_function('window.SaqrimQuests')
        check('lead ring excluded from default reward filter',page.evaluate('SaqrimQuests.filtered.length')==0)
        page.locator('#quest-filters>summary').click();page.check('#include-leads')
        check('lead ring explicitly opt-in',page.evaluate('SaqrimQuests.filtered.map(q=>q.id)')==['Q047'])
        page.goto(url+'quests.html?q=post-combat');page.wait_for_function('window.SaqrimQuests')
        check('creator trigger discoverable by search','Q056' in page.evaluate('SaqrimQuests.filtered.map(q=>q.id)'))
        page.goto(url+'quests.html#Q056');page.wait_for_function('window.SaqrimQuests')
        check('new title retains existing Dagoth progress',page.locator('#status-Q056').input_value()=='In progress' and page.locator('#notes-Q056').input_value()=='old Dagoth note')
        check('all saved keys untouched just by browsing',page.evaluate('(s)=>Object.entries(s).every(([k,v])=>localStorage.getItem(k)===v)',seed))
        check('crafting spoilers initially hidden',page.locator('#Q056 .outcome-spoilers').get_attribute('open') is None)
        page.fill('#notes-Q056','Listen after combat');page.locator('#Q056 form button').click();page.reload();page.wait_for_function('window.SaqrimQuests')
        check('journal save reload works',page.locator('#notes-Q056').input_value()=='Listen after combat' and page.evaluate('SaqrimQuests.progress.Q001.notes')=='old journal')
        check('journal backup includes same stable ID','Q056' in json.loads(page.evaluate('SaqrimQuests.backup()'))['quests'])
        page.locator('#Q056 .hook').scroll_into_view_if_needed()
        page.screenshot(path=str(OUT/'reward-research-mobile.png'),full_page=False)
        page.goto(url+'quests.html#Q053');page.wait_for_function('window.SaqrimQuests')
        check('Cataclysm bonus unlock still renders',page.locator('#Q053 .reward-row[data-kind="unlock"]').count()==1)
        page.goto(url+'load-order.html?reference=content');page.wait_for_selector('#mods>.row:visible')
        check('current list and content previews load',page.locator('#mods>.row').count()==224 and page.locator('#mods>.row:visible').count()==5 and not page.evaluate('SaqrimReference.failed'))
        check('saved installation marks unchanged',page.locator('#mods input[type=checkbox]:checked').count()==3)
        page.locator('#mod-014 .ref-card').evaluate('(d)=>d.open=true')
        check('community evidence is labeled', 'Community reference' in page.locator('#mod-014 .ref-card').inner_text())
        page.goto(url+'map.html');page.wait_for_function('window.SaqrimQuestMap')
        check('quest overlay still loads',page.evaluate('SaqrimQuestMap.layer.getLayers().length')>0)
        check('no fabricated Cataclysm start pin',page.evaluate('SaqrimQuestMap.candidates().every(q=>!["Q053","Q054"].includes(q.id))'))
        page.goto(url+'index.html#W635');page.wait_for_function('window.SaqrimCatalog');page.wait_for_selector('#W635 .quest-catalog-links',state='attached')
        check('637 catalog records still load',page.locator('#catalog>.card').count()==637)
        check('existing reverse quest links preserved',page.locator('#W635 a[href="quests.html#Q051"]').count()==1)
        check('item picks and ratings preserved',page.evaluate('(s)=>["skyrimLootChoices_v202_20260917","saqrimObservedStats_v1","saqrim-load-order-224-october-v1"].every(k=>localStorage.getItem(k)===s[k])',seed))
        check('no browser JavaScript errors',not errors)
        browser.close()
finally:
    server.shutdown()
result={'checks':len(checks),'errors':errors,'baseline':BASE,'completeRosters':False,'catalogEntries':637,'questEntries':56,'loadOrderEntries':224}
(OUT/'reward-research-01.json').write_text(json.dumps(result,indent=2)+'\n')
print('REWARD_RESEARCH_RESULT '+json.dumps(result),flush=True)
