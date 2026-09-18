"""Regression coverage for the six-tab navigation and separate reference pages."""
import functools, http.server, json, pathlib, subprocess, threading
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'test-results';OUT.mkdir(exist_ok=True)
BASE='99076df867f6fb7b394a1603dd4509c3fde294fc'
checks=[]
def check(name,ok):
    assert ok,name
    checks.append(name);print('PASS',name,flush=True)
for path in ['catalog-source.html','catalog-tags.js','catalog.js','load-order.tsv','load-order.js','map.js','map-locations.json','worlds.js','world-data.js','faith-data.js','stones-data.js']:
    check('unchanged data / core '+path,(ROOT/path).read_bytes()==subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT))
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base='http://127.0.0.1:'+str(server.server_port)+'/'
expected=[['./','Loot catalog · 617'],['load-order.html','Load order · 220'],['map.html','Map'],['quests.html','Quests & rewards'],['shrines.html','Shrines & Gods'],['standing-stones.html','Standing Stones']]
cases=[
 ('index.html','./','window.SaqrimCatalog'),
 ('load-order.html','load-order.html','document.querySelector("#mods").children.length===220'),
 ('quests.html','quests.html','document.querySelectorAll(".quest-card").length===46'),
 ('map.html','map.html','window.SaqrimMap&&window.SaqrimQuestMap&&window.SaqrimBlessingsMap'),
 ('worlds.html?world=solstheim','map.html','window.SaqrimWorlds&&window.SaqrimQuestMap&&window.SaqrimBlessingsMap'),
 ('worlds.html?world=evergloam','map.html','window.SaqrimWorlds&&window.SaqrimQuestMap&&window.SaqrimBlessingsMap'),
 ('shrines.html','shrines.html','window.SaqrimBlessingsPage'),
 ('standing-stones.html','standing-stones.html','window.SaqrimBlessingsPage')]
with sync_playwright() as p:
    browser=p.chromium.launch()
    ctx=browser.new_context(viewport={'width':1400,'height':1000})
    ctx.route('https://**',lambda route:route.abort())
    page=ctx.new_page();errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    def go(path,ready='window.SaqrimBlessingsPage'):
        response=page.goto(base+path);assert response.ok,path
        page.wait_for_function('window.SaqrimNavigation',timeout=20000)
        page.wait_for_function(ready,timeout=20000)
    def menu(active,label):
        actual=page.locator('.nav a:not(.brand)').evaluate_all('(as)=>as.map(a=>[a.getAttribute("href"),a.textContent])')
        check(label+' exact same six links',actual==expected)
        check(label+' exactly one correct active tab',page.locator('.nav [aria-current="page"]').count()==1 and page.locator('.nav [aria-current="page"]').get_attribute('href')==active)
        check(label+' no combined tab',page.locator('.nav a[href="blessings.html"]').count()==0)
        check(label+' visible accessible tabs',all(page.locator('.nav a:not(.brand)').nth(i).is_visible() for i in range(6)))
        check(label+' menu stays within screen',page.locator('.nav a').evaluate_all('(as)=>as.every(a=>{const r=a.getBoundingClientRect();return r.x>=-1&&r.right<=innerWidth+1})'))
    for width in [1400,390,320]:
        page.set_viewport_size({'width':width,'height':844 if width<1000 else 1000})
        for path,active,ready in cases:
            go(path,ready);menu(active,path+' '+str(width))
            check(path+' '+str(width)+' no horizontal overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
            if width==390 and path in ['index.html','shrines.html','standing-stones.html']:
                page.evaluate('scrollTo(0,0)');page.screenshot(path=str(OUT/('nav-'+path.replace('.html','')+'-mobile.png')))
    go('shrines.html')
    check('shrine page has dedicated heading','Choose your patron.'==page.locator('h1').inner_text())
    check('shrine page has gods and locations only',page.locator('[data-faith-tab]').evaluate_all('(bs)=>bs.map(b=>b.dataset.faithTab)')==['deities','shrines'])
    check('all deity profiles preserved',page.locator('#faith-cards>.faith-deity').count()==51)
    check('race selector not shown in shrine guide',not page.locator('#faith-page-race').is_visible())
    page.fill('#faith-page-search','Julianos');check('deity search works',page.locator('#faith-cards>.faith-deity').count()==1)
    page.click('#faith-clear');page.click('#faith-tab-shrines');check('all shrine-location records preserved',page.locator('#faith-cards>.faith-location').count()==52)
    page.fill('#faith-page-search','Morvunskar');page.locator('#faith-cards button').click();check('shared shrine profiles still open',page.locator('#faith-single .faith-deity').count()==7)
    go('standing-stones.html')
    check('stone page has dedicated heading','Read your stars.'==page.locator('h1').inner_text())
    check('stone page has no mixed reference tabs',page.locator('[data-faith-tab]').count()==0)
    check('stone guide starts on all thirteen stones',page.locator('#faith-cards>.faith-stone').count()==13 and page.evaluate('SaqrimBlessingsPage.tab==="stones"'))
    check('stone guide hides pantheons',not page.locator('#faith-pantheons').is_visible())
    check('Breton extras preserved',page.locator('#faith-cards>.faith-stone .faith-extra-preview').count()==13)
    page.select_option('#faith-page-race-select','Orc');check('race selector switches all thirteen',page.locator('#faith-cards>.faith-stone[data-race="Orc"]').count()==13)
    check('no Breton extras in Orc summaries',page.locator('#faith-cards>.faith-stone .faith-extra-preview').count()==0)
    page.fill('#faith-page-search','Shadow');check('stone effect search works',page.locator('#faith-cards>.faith-stone').count()==1)
    page.locator('.nav a[href="shrines.html"]').click();page.wait_for_function('window.SaqrimBlessingsPage');menu('shrines.html','clicked shrine tab')
    page.go_back();page.wait_for_function('window.SaqrimBlessingsPage&&SaqrimBlessingsPage.race==="Orc"');menu('standing-stones.html','browser Back')
    check('back retains race and search',page.locator('#faith-page-search').input_value()=='Shadow')
    page.go_forward();page.wait_for_function('window.SaqrimBlessingsPage');menu('shrines.html','browser Forward')
    for old in ['blessings.html#deity=julianos','blessings.html?tab=stones&race=Breton#stone=shadow','blessings.html#shrine=reclamations']:
        go(old);check('old bookmark still functional '+old,page.locator('#faith-cards>.faith-card, #faith-single .faith-deity').count()>0)
    go('shrines.html?race=Breton#stone=shadow');page.wait_for_url('**/standing-stones.html?**#stone=shadow');page.wait_for_function('window.SaqrimBlessingsPage');check('wrong-section stone links route to stones',page.locator('#stone-shadow').get_attribute('open') is not None)
    go('standing-stones.html#deity=julianos');page.wait_for_url('**/shrines.html?**#deity=julianos');page.wait_for_function('window.SaqrimBlessingsPage');check('wrong-section deity links route to shrines',page.locator('#deity-julianos').get_attribute('open') is not None)
    seed={'skyrimLootChoices_v202_20260917':'{"W417":"Want","W012":"Maybe"}','saqrimObservedStats_v1':'{"W012":{"armor":500}}','saqrim-load-order-220-2026-09-17':'[1,2,3]','saqrimQuestProgress_v1':'{"Q001":{"status":"Completed","notes":"Keep my note"}}'}
    page.evaluate('(seed)=>Object.entries(seed).forEach(([k,v])=>localStorage.setItem(k,v))',seed)
    for path,_,ready in cases:go(path,ready)
    check('navigation and new views preserve saved state',page.evaluate('(seed)=>Object.entries(seed).every(([k,v])=>localStorage.getItem(k)===v)',seed))
    go('index.html','window.SaqrimCatalog')
    check('catalog navigation does not require map or faith data',page.locator('script[src^="faith-data.js"],script[src^="stones-data.js"]').count()==0)
    plain=browser.new_context(java_script_enabled=False);raw=plain.new_page()
    for path,_,_ in cases:
        raw.goto(base+path)
        check('static navigation survives disabled JavaScript '+path,raw.locator('.nav a:not(.brand)').evaluate_all('(as)=>as.map(a=>[a.getAttribute("href"),a.textContent])')==expected)
    plain.close();check('no JavaScript errors',not errors)
    print('NAVIGATION_RESULT',json.dumps({'checks':len(checks),'errors':errors}),flush=True)
    browser.close()
server.shutdown()
