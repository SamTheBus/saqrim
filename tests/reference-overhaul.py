"""Actual-repository regression coverage for the optional ten-mod reference layer."""
import functools, hashlib, http.server, json, pathlib, subprocess, threading
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE='91f371206675fa7f26333efd53550c3723c7635d'
OUT=ROOT/'test-results';OUT.mkdir(exist_ok=True)
checks=[]
def check(label,ok):
    assert ok,label
    checks.append(label);print('PASS',label,flush=True)
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
for f in ['load-order.tsv','load-order-bethesda.json','catalog-source.html','catalog-current.html','artifact-review.json','quests-data.json','faith-data.js','stones-data.js','world-data.js','map-locations.json','site-top.js']:
    check('unchanged '+f,(ROOT/f).read_bytes()==prior(f))
rows=[l.split('\t') for l in (ROOT/'load-order.tsv').read_text().splitlines() if l.strip()]
check('210 contiguous rows',len(rows)==210 and [int(r[0]) for r in rows]==list(range(1,211)))
names={r[1]:int(r[0]) for r in rows}
pack=json.loads((ROOT/'load-order-reference.json').read_text())
check('exactly ten expanded current mods',len(pack['entries'])==10 and set(pack['entries'])<=names.keys())
expected={1,2,10,11,97,98,99,100,101,203}
check('expected batch positions',{names[n] for n in pack['entries']}==expected)
claims=[c for e in pack['entries'].values() for c in [e['summary']]+[c for s in e['sections'] for c in s['claims']]]
check('all claims have resolvable sources',all(c.get('refs') and set(c['refs'])<=pack['sources'].keys() for c in claims))
check('all related entries resolve',all(n in names for e in pack['entries'].values() for n in e.get('related',[])))
check('all ten reference IDs unique',len({e['id'] for e in pack['entries'].values()})==10)
for id in ['r-gdb','r-xpmsse','r-armoury','r-lux-master']:
    check('exact video locator '+id,pack['sources'][id]['locator'].startswith('Skyrim_LO.mp4'))
check('video hash recorded',pack['recording']['sha256']=='219dd3f5f83f13570d9bcebfabb4652b9e8bcf31a74b29a3e7b4a259cba89fcf')
check('only three warning/question cards',sum(bool(e['attention']) for e in pack['entries'].values())==3)
before={p:(ROOT/p).read_bytes() for p in ['load-order.html','load-order.js','README.md']}
subprocess.run(['python','tools/apply-reference-overhaul.py'],cwd=ROOT,check=True)
check('integration idempotent',all((ROOT/p).read_bytes()==c for p,c in before.items()))
for p in ['load-order.js','load-order-reference.js']:subprocess.run(['node','--check',p],cwd=ROOT,check=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url='http://127.0.0.1:'+str(server.server_port)+'/'
errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch()
    ctx=browser.new_context(viewport={'width':390,'height':844})
    ctx.route('https://**',lambda route:route.abort())
    page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
    def go(path='load-order.html'):
        page.goto(url+path);page.wait_for_function('document.querySelectorAll("#mods>.row").length===210',timeout=20000)
    def count():return page.locator('#mods>.row:visible').count()
    go()
    check('all 210 rows render',count()==210)
    check('ten expandable reference cards',page.locator('.ref-card').count()==10)
    check('coverage honest','10 / 210' in page.locator('#reference-overview').inner_text() and '200' in page.locator('#reference-overview').inner_text())
    check('original storage key retained','saqrim-load-order-210-2026-09-23-v2' in (ROOT/'load-order.js').read_text())
    page.select_option('#reference-view','expanded');check('expanded filter',count()==10)
    page.select_option('#reference-view','attention');check('attention filter',count()==3)
    page.click('#show-all');page.fill('#search','ragdoll');check('search finds description-only content',page.locator('#mod-100').is_visible() and count()<210)
    page.click('#show-all');page.fill('#search','#99');check('number search retains identity',count()==1 and page.locator('#mod-099').is_visible())
    page.click('#show-all');page.select_option('#reference-view','attention');page.fill('#jump-number','100');page.locator('#jump-form button').click()
    check('jump clears reference filter',page.input_value('#reference-view')=='' and page.locator('#mod-100').is_visible())
    page.locator('#mod-100 .row-actions input').check();page.reload();page.wait_for_selector('#mod-100')
    check('checkmarks persist',page.locator('#mod-100 .row-actions input').is_checked())
    page.select_option('#reference-view','expanded');page.check('#hide-added');check('checklist and reference filters compose',count()==9 and not page.locator('#mod-100').is_visible())
    page.click('#show-all');page.locator('#reference-gdb-elden-beast-lite>summary').click()
    gdb=page.locator('#reference-gdb-elden-beast-lite')
    check('GDB manifest and unproven block note visible','SkySA' in gdb.inner_text() and 'Wear Multiple Rings' in gdb.inner_text() and 'still unproven' in gdb.inner_text())
    check('current related XPMSSE number',gdb.locator('.ref-related a[href="load-order.html#mod-100"]').count()==1)
    gdb.locator('a[href="#ref-source-gdb-elden-beast-lite-r-gdb"]').first.click()
    check('source click opens locators',gdb.locator('.ref-sources').get_attribute('open') is not None and '07:50.90' in page.locator('#ref-source-gdb-elden-beast-lite-r-gdb').inner_text())
    check('official match limitations remain visible','full body' in gdb.inner_text())
    check('no duplicate element IDs',page.evaluate('(()=>{const a=[...document.querySelectorAll("[id]")].map(x=>x.id);return a.length===new Set(a).size})()'))
    for width in [320,390,1400]:
        page.set_viewport_size({'width':width,'height':900})
        go('load-order.html#mod-099');page.locator('#reference-gdb-elden-beast-lite').evaluate('(n)=>n.open=true')
        check('no overflow at '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
        if width==390:
            page.locator('#reference-gdb-elden-beast-lite').scroll_into_view_if_needed();page.screenshot(path=str(OUT/'reference-gdb-mobile.png'),full_page=False)
    go('load-order.html?reference=expanded');check('shareable expanded view',count()==10)
    page.locator('#reference-ussep-ps5>summary').focus();page.keyboard.press('Enter');check('keyboard expands card',page.locator('#reference-ussep-ps5').get_attribute('open') is not None)
    for mode in ['missing','malformed']:
        fresh=browser.new_context();q=fresh.new_page()
        q.on('pageerror',lambda e:errors.append(str(e)))
        def intercept(route,kind=mode):
            route.fulfill(status=404 if kind=='missing' else 200,content_type='application/json',body='{}')
        fresh.route('**/load-order-reference.json*',intercept)
        q.goto(url+'load-order.html');q.wait_for_function('document.querySelectorAll("#mods>.row").length===210',timeout=20000)
        check(mode+' optional data does not break checklist',q.locator('#mods>.row').count()==210 and 'could not load' in q.locator('#reference-overview').inner_text())
        fresh.close()
    check('no browser JavaScript errors',not errors)
    browser.close()
server.shutdown()
report={'checks':len(checks),'passed':checks,'errors':errors,'expanded':10,'currentEntries':210,'sourcedClaims':len(claims),'baseline':BASE}
(OUT/'reference-report.json').write_text(json.dumps(report,indent=2))
print('REFERENCE_RESULT',json.dumps({k:v for k,v in report.items() if k!='passed'}),flush=True)
