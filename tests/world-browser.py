"""Test actual repository pages. Remote terrain failures are deliberately injected;
these checks do not claim that an external host serves its images successfully."""
import functools, hashlib, http.server, json, pathlib, threading
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parents[1]
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
URL=f'http://127.0.0.1:{server.server_port}'
checks=[]
def check(name,ok):
    assert ok,name
    checks.append(name);print('PASS',name,flush=True)
def git_blob(path):
    b=(ROOT/path).read_bytes();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
for path,sha in {
    'catalog-source.html':'364f4210b13f51a67610ec4946ef6fd4ef9fafd8',
    'catalog-tags.js':'d4923e76a68f5f35208ae9821c5bcb938768d7c4',
    'catalog.js':'0664aeab0f9324ea201f9e66511c607ea7d4fa58',
    'load-order.tsv':'efeab917b1bcc2a2913c7c3ff6fde46c16c5170a',
    'load-order.js':'d2707aa2dafc3378637258549136e113c34a5db7',
    'map.js':'203ffe2a9eea53db288d8878392f9baab5289c39'
}.items():check('unchanged '+path,git_blob(path)==sha)
with sync_playwright() as p:
    browser=p.chromium.launch()
    context=browser.new_context(viewport={'width':1440,'height':1000})
    # The application must work even when its optional terrain host refuses a request.
    context.route('https://images.uesp.net/**',lambda route:route.abort('failed'))
    page=context.new_page();errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_default_timeout(15000)
    def ready(url):
        page.goto(URL+url);page.wait_for_function('window.SaqrimWorlds')
    ready('/worlds.html?world=solstheim')
    check('617 records retained',page.evaluate('SaqrimWorlds.records.length===617'))
    check('nine named realm views plus mainland',page.locator('#map-world option').count()==10)
    check('Solstheim selected',page.evaluate('SaqrimWorlds.world.id==="solstheim"'))
    check('36 Solstheim geographic reference places',page.evaluate('SaqrimWorlds.places.filter(p=>p.world==="solstheim"&&p.pin).length===36'))
    check('finite geographic points within their world frames',page.evaluate('SaqrimWorlds.places.filter(p=>p.pin).every(p=>{const w=SaqrimWorlds.worlds.find(w=>w.id===p.world);return p.x>=0&&p.y>=0&&p.x<=w.width&&p.y<=w.height})'))
    page.wait_for_function('SaqrimWorlds.imageFailed')
    check('terrain failure explicitly disclosed',page.locator('#image-status').is_visible() and 'not serve' in page.locator('#image-status').inner_text())
    check('Solstheim reference pins survive terrain failure',page.locator('#map-shell').is_visible() and page.locator('.leaflet-interactive').count()>20)
    page.evaluate('SaqrimWorlds.selectItem("W007",{focus:false})')
    check('Solstheim item keeps actual source location','Stalhrim Source' in page.locator('#selection').inner_text())
    check('shareable realm item URL','world=solstheim' in page.url and page.url.endswith('#W007'))
    page.evaluate('SaqrimWorlds.selectItem("W614",{focus:false})')
    check('recipe clue not confused with merchant pickup','NOT the reward position' in page.locator('#selection').inner_text() and 'west of the barrow' in page.locator('#selection').inner_text())
    page.select_option('#map-world','icemoth')
    page.wait_for_function('document.querySelector(".leaflet-image-layer")?.naturalWidth===1025')
    check('Icemoth terrain self-hosted and loaded',page.locator('.leaflet-image-layer').get_attribute('src')=='assets/map/worlds/icemoth.webp')
    check('14 Icemoth reference places',page.evaluate('SaqrimWorlds.places.filter(p=>p.world==="icemoth"&&p.pin).length===14'))
    page.evaluate('SaqrimWorlds.selectItem("W170",{focus:false})')
    check('Crimson Kiss uses a nearby wreck reference','NOT the pickup spot' in page.locator('#selection').inner_text() and 'seafloor' in page.locator('#selection').inner_text().lower())
    page.select_option('#map-world','evergloam')
    check('Evergloam clearly a guide, not imaginary geography',page.locator('#guide').is_visible() and not page.locator('#map-shell').is_visible())
    check('all 22 Aberrations records in its realm',page.evaluate('SaqrimWorlds.filtered.length===22'))
    check('no invented Evergloam pins',page.evaluate('SaqrimWorlds.places.filter(p=>p.world==="evergloam").every(p=>!p.pin)'))
    page.evaluate('SaqrimWorlds.selectPlace("Plankside",{focus:false})')
    check('Plankside groups weapon and home key',page.locator('#selection [data-item="W552"]').count()==1 and page.locator('#selection [data-item="W573"]').count()==1)
    check('original house-key directions preserved','wooden plate' in page.locator('#selection').inner_text())
    page.select_option('#map-world','beyond-reach')
    check('50 Beyond Reach records retained',page.evaluate('SaqrimWorlds.filtered.length===50'))
    check('Beyond Reach map uncertainty visible','Location guide' in page.locator('#world-mode').inner_text())
    page.evaluate('SaqrimWorlds.selectItem("W581",{focus:false})')
    check('historical route remains qualified','Historical lead' in page.locator('#selection').inner_text())
    page.select_option('#map-world','atmora')
    check('six Crucible rewards present',page.evaluate('SaqrimWorlds.filtered.length===6'))
    for wid in ['soul-cairn','forgotten-vale','blackreach']:
        page.select_option('#map-world',wid);page.wait_for_function('SaqrimWorlds.imageFailed')
        check(wid+' shows readable notes when its terrain fails',page.locator('#guide').is_visible() and page.locator('#image-status').is_visible())
        check(wid+' has no invented geographic coordinates',page.evaluate('(id)=>SaqrimWorlds.places.filter(p=>p.world===id).every(p=>!p.pin)',wid))
    page.select_option('#map-world','apocrypha')
    check('Apocrypha distinct unpinned guide',page.locator('#guide').is_visible())
    page.evaluate('SaqrimWorlds.selectItem("W007",{focus:false})')
    check('cross-world item selection switches to correct map',page.evaluate('SaqrimWorlds.world.id==="solstheim"'))
    page.select_option('#map-world','evergloam');page.locator('#filters').evaluate('(n)=>n.open=true');page.locator('.facet').evaluate_all('(ns)=>ns.forEach(n=>n.open=true)')
    page.check('input[data-group="slot"][value="Feet / boots"]')
    check('equipment checkbox works within world',page.evaluate('SaqrimWorlds.filtered.length>0&&SaqrimWorlds.filtered.every(r=>r.meta.tags.slot.includes("Feet / boots"))'))
    page.check('input[data-group="slot"][value="Ring"]')
    check('same-group OR',page.evaluate('SaqrimWorlds.filtered.some(r=>r.meta.tags.slot.includes("Ring"))&&SaqrimWorlds.filtered.some(r=>r.meta.tags.slot.includes("Feet / boots"))'))
    page.check('input[data-group="category"][value="Armor / clothing"]')
    check('cross-group AND',page.evaluate('SaqrimWorlds.filtered.length>0&&SaqrimWorlds.filtered.every(r=>r.meta.tags.category.includes("Armor / clothing")&&r.meta.tags.slot.includes("Feet / boots"))'))
    page.evaluate('SaqrimWorlds.reset();localStorage.setItem("skyrimLootChoices_v202_20260917",JSON.stringify({W552:"Want",W573:"Maybe",W170:"Skip"}));localStorage.setItem("saqrimObservedStats_v1",JSON.stringify({W012:{armor:500}}));localStorage.setItem("saqrim-load-order-220-2026-09-17","[1,2,3]")')
    before=page.evaluate('JSON.stringify({...localStorage})');page.reload();page.wait_for_function('window.SaqrimWorlds');page.locator('#filters').evaluate('(n)=>n.open=true');page.check('#picks-only')
    check('old browser picks available without migration',page.evaluate('SaqrimWorlds.filtered.map(r=>r.id).sort().join(",")==="W552,W573"'))
    check('no saved choices, ratings or checklist writes',before==page.evaluate('JSON.stringify({...localStorage})'))
    ready('/worlds.html?world=icemoth#W170')
    check('world item deep link restored',page.locator('#selection [data-item="W170"]').count()==1)
    page.wait_for_function('document.querySelector(".leaflet-image-layer")?.naturalWidth===1025')
    page.click('#large-map');check('larger map enabled',page.evaluate('document.body.classList.contains("map-expanded")'));page.keyboard.press('Escape');check('Escape restores page',not page.evaluate('document.body.classList.contains("map-expanded")'))
    check('desktop without horizontal overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    (ROOT/'test-results').mkdir(exist_ok=True)
    page.screenshot(path=str(ROOT/'test-results/world-icemoth-desktop.png'),full_page=True)
    page.set_viewport_size({'width':390,'height':844})
    check('mobile without horizontal overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    page.screenshot(path=str(ROOT/'test-results/world-icemoth-mobile.png'),full_page=True)
    page.select_option('#map-world','evergloam')
    check('guide without horizontal mobile overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    page.screenshot(path=str(ROOT/'test-results/world-evergloam-mobile.png'),full_page=True)
    page.goto(URL+'/map.html#W552');page.wait_for_function('window.SaqrimMap');page.wait_for_selector('.open-realm')
    check('legacy mainland URL preserved',page.url.endswith('/map.html#W552'))
    check('old item link offers correct realm',page.locator('.open-realm').get_attribute('href')=='worlds.html?world=evergloam#W552')
    check('mainland selector is present once',page.locator('#map-world').count()==1)
    page.select_option('#map-world','icemoth');page.wait_for_function('window.SaqrimWorlds&&SaqrimWorlds.world.id==="icemoth"')
    check('mainland selector opens chosen world',page.evaluate('SaqrimWorlds.world.id==="icemoth"'))
    check('no browser JavaScript errors',not errors)
    print('WORLD_TEST_RESULTS',json.dumps({'checks':len(checks),'errors':errors,'remoteTerrain':'failure deliberately injected; availability not certified'}),flush=True)
    browser.close()
server.shutdown()
