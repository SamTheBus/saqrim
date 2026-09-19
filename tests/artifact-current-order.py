"""Validate artifact/site precedence against Sam's current 18 September load order."""
import functools, http.server, json, pathlib, subprocess, threading
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE='0d86612cb4a2a8853490747fab37919ca5c75a19'
checks=[]
def check(name,ok):
 assert ok,name
 checks.append(name);print('PASS',name,flush=True)
def current_lo(n):
 if n<=32:return n
 if 33<=n<=37:return n+183
 fixed={38:33,39:35,40:34,41:39,42:40,43:41,44:36,45:38,46:37,47:42,48:43,91:56}
 if n in fixed:return fixed[n]
 if 49<=n<=60:return n-5
 if 61<=n<=90:return n-4
 if 92<=n<=220:return n-5
 return n

lo=[]
for line in (ROOT/'load-order.tsv').read_text().splitlines():
 p=line.split('\t');lo.append((int(p[0]),p[1]))
bypos=dict(lo)
expected={32:'Triumvirate - Mage Archetypes',33:'Mysticism - A Magic Overhaul',34:'Mysticism - Vokrii Patch',35:'Mysticism - Ordinator Patch',36:'Odin - Skyrim Magic Overhaul',37:'Odin - Vokrii Compatibility Patch',38:'Odin - Ordinator Compatibility Patch',39:'Apocalypse - Magic of Skyrim',40:'Apocalypse - Ordinator Compatibility Patch',41:'Apocalypse - Vokrii Compatibility Patch',42:'Ordinator - 50 Percent More Perk Points',43:"Kittytail's Spells AIO [PS5]",55:"Praedy's Staves - USSEP Patch",56:'ArteFakes - Unique Artifacts Replacer',57:'Artificer - An Artifact Overhaul',58:'Artificer - USSEP Patch',59:'Guns of Skyrim (formerly Lore Friendly Rifles)',67:'Steel Battleaxe of Fiery Souls - Truly Unique (PS5)',68:'Unique Thane Weapons (PS5)',215:'Enhanced Blood Textures Lite',216:'Vokrii - Minimalistic Perks of Skyrim',217:'Ordinator - Perks of Skyrim',218:'Ordinator - Fix - PS5 (textures)',219:'Ordinator - Bone Collector (Windhelm altar fix)',220:'Vokriinator [EN]'}
check('220 unique current load-order positions',len(lo)==220 and [n for n,_ in lo]==list(range(1,221)))
for n,name in expected.items():check(f'load order #{n} {name}',bypos[n]==name)

soup=BeautifulSoup((ROOT/'catalog-current.html').read_text(),'html.parser')
rows=json.loads(soup.select_one('#dataset').string);by={r['Catalog ID']:r for r in rows}
check('633 current catalog records',len(rows)==633 and len(by)==633)
check('Artificer catalog labels use #57',all(str(r['LO #'])=='57' for r in rows if r['Installed mod']=='Artificer - An Artifact Overhaul'))
check('Fiery Souls catalog label uses #67',by['W180']['LO #']=='67')
check('Thane reward labels use #68',all(by[f'W{i:03}']['LO #']=='68' for i in range(39,49)))
check('Knight relic labels use #154',all(by[f'W{i:03}']['LO #']=='154' for i in range(358,365)))

pack=json.loads((ROOT/'artifact-review.json').read_text());audit=pack['reviews']
for ident in ['W539','W544','W545','W629','W630','W631','W632','W633']:
 check(ident+' Artificer wins documented item priority',audit[ident]['status']=='Documented overlap' and '#56 ArteFakes' in audit[ident]['chain'] and '#57 Artificer' in audit[ident]['chain'] and 'Artificer #57 loads after ArteFakes #56' in audit[ident]['expected'])
 check(ident+' no stale ArteFakes-winner headline','latest documented editor' not in by[ident]['Effect / interest'].lower() and 'Expected Artificer reference:' in by[ident]['Effect / interest'])
check('Fiery Souls dedicated mod is latest expected editor','#56 ArteFakes' in audit['W180']['chain'] and '#57 Artificer' in audit['W180']['chain'] and '#67 Fiery Souls' in audit['W180']['chain'] and 'expected candidate' in audit['W180']['expected'])
check('Fiery Souls headline restores dedicated mechanics','Emberwisp' in by['W180']['Effect / interest'])
for ident in ['W307','W310','W367','W368','W542']:
 check(ident+' ring warning renumbered','#105 Wear Multiple Rings' in audit[ident]['chain'] and '#57 Artificer' in audit[ident]['chain'])
for ident in [f'W{i:03}' for i in range(39,49)]:
 check(ident+' thane chain renumbered','#57 Artificer' in audit[ident]['chain'] and '#68 Unique Thane Weapons' in audit[ident]['chain'])
check('Staff of Magnus flags missing Praedy compatibility','#51 Praedy' in audit['W627']['chain'] and '#57 Artificer' in audit['W627']['chain'] and 'compatibility' in audit['W627']['expected'].lower())

oldq=json.loads(subprocess.check_output(['git','show',BASE+':quests-data.json'],cwd=ROOT))['quests']
newq=json.loads((ROOT/'quests-data.json').read_text())['quests']
check('quest IDs and count preserved',[q['id'] for q in newq]==[q['id'] for q in oldq])
check('quest load-order numbers remapped',all(q['lo']==current_lo(o['lo']) for q,o in zip(newq,oldq)))
check('all quest text preserved except explicit Q030 compatibility enrichment',all(({k:v for k,v in q.items() if k not in ['lo','notes','sources']}=={k:v for k,v in o.items() if k not in ['lo','notes','sources']} if q['id']=='Q030' else {k:v for k,v in q.items() if k!='lo'}=={k:v for k,v in o.items() if k!='lo'}) for q,o in zip(newq,oldq)))
q30=next(q for q in newq if q['id']=='Q030')
check('Destroy Dark Brotherhood quest points to current #140',q30['lo']==140)
check('Destroy Dark Brotherhood surfaces Artificer acquisition conflict',any('Windshear' in n and "Firiniel's End" in n and 'unobtainable' in n for n in q30.get('notes',[])))
check('Destroy Dark Brotherhood links compatibility source',any(s.get('url')=='https://www.nexusmods.com/skyrimspecialedition/mods/151173' for s in q30.get('sources',[])))

class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();URL=f'http://127.0.0.1:{server.server_port}/'
with sync_playwright() as p:
 browser=p.chromium.launch();ctx=browser.new_context(viewport={'width':390,'height':844});ctx.route('https://**',lambda r:r.abort());page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(URL+'load-order.html#mod-056');page.wait_for_selector('#mod-056');check('browser load order shows ArteFakes #56','ArteFakes' in page.locator('#mod-056').inner_text());check('browser Artificer #57','Artificer' in page.locator('#mod-057').inner_text())
 page.evaluate('localStorage.clear();localStorage.setItem("saqrim-load-order-220-2026-09-17","[61,71,91]")');page.reload();page.wait_for_selector('#mod-056');check('old checklist migrates by mod identity positions',page.is_checked('#mod-056 input[type=checkbox]') and page.is_checked('#mod-057 input[type=checkbox]') and page.is_checked('#mod-067 input[type=checkbox]'))
 page.goto(URL+'index.html#W180');page.wait_for_function('window.SaqrimCatalog');page.wait_for_selector('#W180[open]');check('axe visible summary uses dedicated mechanics','Emberwisp' in page.locator('#W180>summary').inner_text())
 page.goto(URL+'index.html#W629');page.wait_for_function('window.SaqrimCatalog');page.wait_for_selector('#W629[open]');check('Dragonbane summary shows Artificer expected','Expected Artificer reference' in page.locator('#W629>summary').inner_text())
 page.goto(URL+'index.html#W627');page.wait_for_function('window.SaqrimCatalog');page.wait_for_selector('#W627[open]');check('Staff Magnus audit visible','Praedy' in page.locator('#W627 .artifact-audit').inner_text())
 page.goto(URL+'quests.html#Q030');page.wait_for_function('window.SaqrimQuests');page.wait_for_selector('#Q030[open]');check('quest links current load order #140',page.locator('#Q030 a[href="load-order.html#mod-140"]').count()==1)
 check('mobile pages fit',page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
 check('no JavaScript errors',not errors)
 browser.close()
server.shutdown()
print('RESULT',json.dumps({'checks':len(checks),'errors':[]}),flush=True)
