"""Idempotent integration of Batch 01. Never renumber or rewrite the load-order data."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
def change(text,old,new):
    if old not in text:
        if new in text:return text
        raise RuntimeError('Expected source marker missing: '+old[:100])
    return text.replace(old,new)
js=(ROOT/'load-order.js').read_text()
if '// Saqrim reference layer v1' not in js:
    js=change(js,"node.hidden = !matches ||", "node.hidden = !matches || (window.SaqrimReference && !window.SaqrimReference.matches(item.name, $('reference-view')?.value || '')) ||")
    js=change(js,"function resetFilters() { $('search')", "function resetFilters() { if ($('reference-view')) $('reference-view').value = ''; $('search')")
    js=change(js,"    node.append(top, actions, details);", "    node.append(top, actions);\n    if (window.SaqrimReference) window.SaqrimReference.decorate(item, node);\n    node.append(details);")
    js=change(js,"JSON.stringify(item.bethesda || {})].join", "JSON.stringify(item.bethesda || {}), window.SaqrimReference?.searchText(item.name) || ''].join")
    js=change(js,"      const fragment = document.createDocumentFragment(); rows = data.map(makeRow);", "      if (window.SaqrimReference) { await window.SaqrimReference.ready; window.SaqrimReference.setOrder(data); }\n      const fragment = document.createDocumentFragment(); rows = data.map(makeRow);")
    js=change(js,"      document.querySelectorAll('.tools [disabled]')", "      if (window.SaqrimReference) window.SaqrimReference.mountControls(filter, data.length);\n      document.querySelectorAll('.tools [disabled]')")
    js=js.replace("'Bethesda listing, console source & notes' : 'Bethesda listing status & console source'", "'Earlier listing snapshot & console metadata' : 'Listing match status & console metadata'")
    js=js.replace('Current Bethesda listing: ', 'Stored Bethesda listing snapshot: ')
    js=js.replace('The current listing metadata differs from the recorded menu.', 'The stored listing metadata differs from the recorded menu.')
    js+='\n// Saqrim reference layer v1\n'
h=(ROOT/'load-order.html').read_text()
if 'load-order-reference.css' not in h:
    h=change(h,'<link rel="stylesheet" href="load-order.css?v=2">','<link rel="stylesheet" href="load-order.css?v=2"><link rel="stylesheet" href="load-order-reference.css?v=1">')
if 'load-order-reference.js' not in h:
    h=change(h,'<script src="load-order.js?v=6"></script>','<script src="load-order-reference.js?v=1"></script><script src="load-order.js?v=7"></script>')
h=re.sub(r'<p class="intro">.*?</p>', '<p class="intro">Your current 210-mod setup, with searchable PS5 descriptions, requirements, compatibility notes and source labels. Batch 01 expands the foundations, Lux modules and animation block. Current numbering, recorded metadata and your browser checklist stay intact.</p>',h,count=1)
h=h.replace("This preserves Sam's current tested top-to-bottom order after the 23 September animation cleanup.","This preserves Sam's current top-to-bottom order after the 23 September animation cleanup. The overall setup is not compatibility-certified.")
h=h.replace('This change was tested in game: the one-handed weapon now draws from its back sheath instead of using the hip-draw animation.', 'Sam reported that the back-sheath draw problem was fixed after moving XPMSSE and removing Simple Visible Favorited Gear together. That was not an isolated test of either change, and it does not verify the rest of the animation stack.')
h=h.replace('Search name, size, version or #number','Search name, description, requirement or #number').replace('Try Lux, 1.93 GB, or #68','Try ragdoll, Wear Multiple Rings, or #99')
h=h.replace('JavaScript is needed to show this checklist. The source recording linked above remains available.','JavaScript is needed for the checklist and expandable reference cards. <a href="REFERENCE-OVERHAUL.md">Read the research scope</a> or <a href="load-order-reference.json">open the sourced reference data</a>.')
h=re.sub(r'<footer>.*?</footer>', '<footer><p><b>Console checklist, not a mod download page.</b> All 210 current positions are kept when filtering. Your checkmarks remain separate from enabled status in the recording.</p><p>Current order: the 23 September recording plus the same-day XPMSSE move and removal of Simple Visible Favorited Gear. Reference Batch 01 reviewed 24 September 2026. The original video shows 211 enabled entries; its timestamps remain source locators, not present positions.</p><p>Mod imagery belongs to its creators. Unofficial personal reference; no Bethesda affiliation.</p><a href="#top">Back to top ↑</a></footer>',h,flags=re.S)
readme=(ROOT/'README.md').read_text()
heading='## Reference overhaul · Batch 01'
if heading not in readme:
    readme+='\n\n'+heading+'\n\nThe Load Order page now adds ten sourced description cards, a research-coverage filter, description/requirement search, source locators and current-number cross-links. `load-order-reference.json` stores claims and evidence independently of recorded TSV rows and historical Bethesda snapshots. `load-order-reference.js` is optional: a failed research request must not break the checklist. The current 210-row order, catalog, quest data, IDs and localStorage keys are preserved.\n\nThe source recording exposes Animated Armoury/GDB and GDB/Wear Multiple Rings warnings, the explicit Custom Placed Weapons instruction to load below GDB, and ambiguous Lux Master wording. The reported draw fix followed two simultaneous changes; it is not a complete compatibility certification. See `REFERENCE-OVERHAUL.md` for scope and open questions.\n'
readme=readme.replace('That change restored the correct back-sheathed one-handed draw animation in game.','Sam reported the back-sheathed draw fixed after both changes together; neither change was isolated in that test.')
for p,c in [('load-order.js',js),('load-order.html',h),('README.md',readme)]: (ROOT/p).write_text(c)
print('Reference layer integrated; recorded order and storage keys untouched.')
