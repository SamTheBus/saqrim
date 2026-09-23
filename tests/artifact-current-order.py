"""Validate artifact/site precedence against Sam's current 23 September load order."""
import functools, http.server, json, pathlib, subprocess, threading
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE='0d86612cb4a2a8853490747fab37919ca5c75a19'
checks=[]
def check(name,ok):
 assert ok,name
 checks.append(name);print('PASS',name,flush=True)
FINAL214_ORDER=[n for n in range(1,215) if n not in {15,80,83,86,87}]
_p=FINAL214_ORDER.index(55)
FINAL214_ORDER[_p+1:_p+1]=[87,86]
FINAL214_POS={old:i+1 for i,old in enumerate(FINAL214_ORDER)}
def current_lo(n):
 if n<=32:m=n
 elif 33<=n<=37:m=n+183
 else:
  fixed={38:33,39:35,40:34,41:39,42:40,43:41,44:36,45:38,46:37,47:42,48:43,91:56}
  if n in fixed:m=fixed[n]
  elif 49<=n<=60:m=n-5
  elif 61<=n<=90:m=n-4
  elif 92<=n<=220:m=n-5
  else:m=n
 if m==100:return None
 m=m-1 if m>100 else m
 removed={86,89,91,93,94}
 if m in removed:return None
 m-=sum(x<m for x in removed)
 return FINAL214_POS.get(m)

lo=[]
for line in (ROOT/'load-order.tsv').read_text().splitlines():
 p=line.split('\t');lo.append((int(p[0]),p[1]))
bypos=dict(lo)
expected={24:'Thaumaturgy - An Enchanting Overhaul',25:'Summermyst - Enchantments of Skyrim',32:'Mysticism - A Magic Overhaul',35:'Odin - Skyrim Magic Overhaul',44:'Open World Loot SE',54:"Praedy's Staves - USSEP Patch",55:'Xavbio 1K Base + DLC',56:'Xavbio 1K AE/CC',57:'ArteFakes - Unique Artifacts Replacer',58:'Artificer - An Artifact Overhaul',59:'Artificer - USSEP Patch',68:'Steel Battleaxe of Fiery Souls - Truly Unique (PS5)',69:'Unique Thane Weapons (PS5)',96:'Wear Multiple Rings',131:"JaySerpa's Quest Expansion Bundle",145:'Knight of the North - Divine Crusader Reworked (PS5)',205:'Lux - PS5',206:'Enhanced Blood Textures Lite',207:'Vokrii - Minimalistic Perks of Skyrim',208:'Ordinator - Perks of Skyrim',209:'Ordinator - Fix - PS5 (textures)',210:'Ordinator - Bone Collector (Windhelm altar fix)',211:'Vokriinator [EN]'}
check('211 unique current load-order positions',len(lo)==211 and [n for n,_ in lo]==list(range(1,212)))
for n,name in expected.items():check(f'load order #{n} {name}',bypos[n]==name)

soup=BeautifulSoup((ROOT/'catalog-current.html').read_text(),'html.parser')
rows=json.loads(soup.select_one('#dataset').string);by={r['Catalog ID']:r for r in rows}
check('633 current catalog records',len(rows)==633 and len(by)==633)
check('Artificer catalog labels use #58',all(str(r['LO #'])=='58' for r in rows if r['Installed mod']=='Artificer - An Artifact Overhaul'))
check('Fiery Souls catalog label uses #68',by['W180']['LO #']=='68')
check('Thane reward labels use #69',all(by[f'W{i:03}']['LO #']=='69' for i in range(39,49)))
check('Knight relic labels use #145',all(by[f'W{i:03}']['LO #']=='145' for i in range(358,365)))

pack=json.loads((ROOT/'artifact-review.json').read_text());audit=pack['reviews']
for ident in ['W539','W544','W545','W629','W630','W631','W632','W633']:
 check(ident+' Artificer wins documented item priority',audit[ident]['status']=='Documented overlap' and '#57 ArteFakes' in audit[ident]['chain'] and '#58 Artificer' in audit[ident]['chain'] and 'Artificer #58 loads after ArteFakes #57' in audit[ident]['expected'])
 check(ident+' no stale ArteFakes-winner headline','latest documented editor' not in by[ident]['Effect / interest'].lower() and 'Expected Artificer reference:' in by[ident]['Effect / interest'])
check('Fiery Souls dedicated mod is latest expected editor','#57 ArteFakes' in audit['W180']['chain'] and '#58 Artificer' in audit['W180']['chain'] and '#68 Fiery Souls' in audit['W180']['chain'] and 'expected candidate' in audit['W180']['expected'])
check('Fiery Souls headline restores dedicated mechanics','Emberwisp' in by['W180']['Effect / interest'])
for ident in ['W307','W310','W367','W368','W542']:
 check(ident+' ring warning renumbered','#96 Wear Multiple Rings' in audit[ident]['chain'] and '#58 Artificer' in audit[ident]['chain'])
for ident in [f'W{i:03}' for i in range(39,49)]:
 check(ident+' thane chain renumbered','#58 Artificer' in audit[ident]['chain'] and '#69 Unique Thane Weapons' in audit[ident]['chain'])
check('Staff of Magnus flags missing Praedy compatibility','#50 Praedy' in audit['W627']['chain'] and '#58 Artificer' in audit['W627']['chain'] and 'compatibility' in audit['W627']['expected'].lower())

oldq=json.loads(subprocess.check_output(['git','show',BASE+':quests-data.json'],cwd=ROOT))['quests']
newq=json.loads((ROOT/'quests-data.json').read_text())['quests']
check('quest IDs and count preserved',[q['id'] for q in newq]==[q['id'] for q in oldq])
check('quest load-order numbers remapped',all(q['lo']==current_lo(o['lo']) for q,o in zip(newq,oldq)))
check('all quest text preserved except explicit Q030 compatibility enrichment',all(({k:v for k,v in q.items() if k not in ['lo','notes','sources']}=={k:v for k,v in o.items() if k not in ['lo','notes','sources']} if q['id']=='Q030' else {k:v for k,v in q.items() if k!='lo'}=={k:v for k,v in o.items() if k!='lo'}) for q,o in zip(newq,oldq)))
q30=next(q for q in newq if q['id']=='Q030')
check('Destroy Dark Brotherhood quest points to current #131',q30['lo']==131)
check('Destroy Dark Brotherhood surfaces Artificer acquisition conflict',any('Windshear' in n and "Firiniel's End" in n and 'unobtainable' in n for n in q30.get('notes',[])))
check('Destroy Dark Brotherhood links compatibility source',any(s.get('url')=='https://www.nexusmods.com/skyrimspecialedition/mods/151173' for s in q30.get('sources',[])))

class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();URL=f'http://127.0.0.1:{server.server_port}/'
with sync_playwright() as p:
 browser=p.chromium.launch();ctx=browser.new_context(viewport={'width':390,'height':844});ctx.route('https://**',lambda r:r.abort());page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(URL+'load-order.html#mod-055');page.wait_for_selector('#mod-055');check('browser Xavbio Base #55','Xavbio 1K Base + DLC' in page.locator('#mod-055').inner_text());check('browser Xavbio AE #56','Xavbio 1K AE/CC' in page.locator('#mod-056').inner_text());check('browser ArteFakes #57','ArteFakes' in page.locator('#mod-057').inner_text());check('browser Artificer #58','Artificer' in page.locator('#mod-058').inner_text())
 page.evaluate('localStorage.clear();localStorage.setItem("saqrim-load-order-214-2026-09-23-v4","[15,55,86,87,214]")');page.reload();page.wait_for_selector('#mod-055');check('previous checklist drops removed mods and follows moved Xavbio entries',page.is_checked('#mod-054 input[type=checkbox]') and page.is_checked('#mod-055 input[type=checkbox]') and page.is_checked('#mod-056 input[type=checkbox]') and page.is_checked('#mod-211 input[type=checkbox]') and page.evaluate('JSON.parse(localStorage.getItem("saqrim-load-order-211-2026-09-23-v5")).length===4'))
 page.goto(URL+'index.html#W180');page.wait_for_function('window.SaqrimCatalog');page.wait_for_selector('#W180[open]');check('axe visible summary uses dedicated mechanics','Emberwisp' in page.locator('#W180>summary').inner_text())
 page.goto(URL+'index.html#W629');page.wait_for_function('window.SaqrimCatalog');page.wait_for_selector('#W629[open]');check('Dragonbane summary shows Artificer expected','Expected Artificer reference' in page.locator('#W629>summary').inner_text())
 page.goto(URL+'index.html#W627');page.wait_for_function('window.SaqrimCatalog');page.wait_for_selector('#W627[open]');page.locator('#W627 .artifact-audit').evaluate('(n)=>n.open=true');check('Staff Magnus audit visible','Praedy' in page.locator('#W627 .artifact-audit').inner_text())
 page.goto(URL+'quests.html#Q030');page.wait_for_function('window.SaqrimQuests');page.wait_for_selector('#Q030[open]');check('quest links current load order #131',page.locator('#Q030 a[href="load-order.html#mod-131"]').count()==1)
 check('mobile pages fit',page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
 check('no JavaScript errors',not errors)
 browser.close()
server.shutdown()
print('RESULT',json.dumps({'checks':len(checks),'errors':[]}),flush=True)
