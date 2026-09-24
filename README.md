# Saqrim

Personal Skyrim PS5 reference: a 633-target loot catalog and a 210-entry current load-order checklist.

- Website: https://samthebus.github.io/saqrim/
- Console load order: https://samthebus.github.io/saqrim/load-order.html
- Current load-order source: `Skyrim_LO.mp4`, supplied directly on 23 September 2026
- Earlier public source recording: https://www.youtube.com/watch?v=4uyqCADqwPo

## Checkbox filters and sorting

The loot catalog now has separate checkbox groups for item category, spell school, weapon handling, weapon type, armor class, equipment slot, and Want/Maybe/Skip choices. Within a group selections use OR; across groups selections use AND. A full set is not automatically an individually indexed helmet. Search, mod selection, live result counts, and removable filter chips work with the checkbox selections. On narrow screens, open Filters and use Show results.

The floating Top button is available on the loot catalog and load-order page and returns instantly to the page top. The recorded load-order numbers are never rearranged.

Armor-rating and weapon-damage sorts support ascending and descending order, keep unknown values last, and can show only records with numeric values. Author base values are separate from optional manually entered in-game values. Eight Artifact of Might weapons currently have source-documented base damage (https://www.nexusmods.com/skyrimspecialedition/mods/104381). No author base armor ratings have been indexed in this update. Missing numbers are null, never zero; enchantment magnitudes, armor bonuses and whole-set totals are not substituted for base stats. Classification coverage is incomplete: Unknown options expose unresolved types/schools/classes. Tags use existing catalog descriptions, descriptive names and cited original author documentation, not an extracted PS5 plugin manifest.

## Load-order provenance

The current 210-entry order is the 23 September 2026 recording with one same-day tested adjustment: Simple Visible Favorited Gear was removed, and XPMSSE Plus was moved below GDB's Elden Beast Lite. Sam reported the back-sheathed draw fixed after both changes together; neither change was isolated in that test. The source recording itself shows 211 of 211 Creations enabled and 14.94 GB used; the removed mod was only 6.8 KB. This is not a compatibility-certified setup.

Thumbnails come from the user's recorded Creations menu, not newly fetched Bethesda listing art. Four AVIF sheets retain 186 prior menu tiles for entries that remain installed; `assets/load-order-new-2026-09-23.jpg` adds the two current-only thumbnails for Mihail High Fantasy Monsters and Skytone: Compendium of Beasts. Generic menu placeholders are retained rather than replaced with guessed pictures. Artwork belongs to its respective creators.

`load-order.tsv` has no header. Columns: order, identified name, displayed size, menu version, video timestamp, category, clipped console title, zero-based thumbnail tile. For tile indices 0–185, sheet=floor(i/48), column=i%8, row=floor((i%48)/8). Indices 186–187 use the two-tile supplemental JPEG handled by `load-order.js`.

## Preservation and local progress

`catalog-source.html` preserves the previous 617-record `loot.html` byte-for-byte (Git blob 364f4210b13f51a67610ec4946ef6fd4ef9fafd8). It remains the source for every original card, W-number, location, qualification, research URL and found field, and can be opened as a reading fallback. The new `index.html` loads those cards directly, without a nested scrolling frame. `loot.html` redirects old links to the updated catalog and preserves their query/hash.

Loot choices retain localStorage key `skyrimLootChoices_v202_20260917`. Optional observed ratings use `saqrimObservedStats_v1`. Backups include choices and observed ratings. Older choices-only backups remain supported and do not erase existing ratings. No cloud syncing or authentication was added.

The current load-order checklist uses localStorage key `saqrim-load-order-210-2026-09-23-v2`; older checklist keys are left untouched. Checkmarks do not modify a console and do not sync between browsers. No mod download buttons are provided.

## Validation

32 local browser checks passed using the actual catalog data and a test-only localStorage/fetch fixture, including all 617 records, legacy choices, checkbox OR/AND behavior, rings versus amulets, weapon handling, numeric sorting in both directions, null handling, observed ratings, backup compatibility, mobile layout, deep links and instant Top behavior. Local rendering checks are not a claim of a live-site browser test.

Static HTML/CSS/JavaScript only; no build step, package dependencies or external analytics.


## Reference overhaul · Batch 01

The Load Order page now adds ten sourced description cards, a research-coverage filter, description/requirement search, source locators and current-number cross-links. `load-order-reference.json` stores claims and evidence independently of recorded TSV rows and historical Bethesda snapshots. `load-order-reference.js` is optional: a failed research request must not break the checklist. The current 210-row order, catalog, quest data, IDs and localStorage keys are preserved.

The source recording exposes Animated Armoury/GDB and GDB/Wear Multiple Rings warnings, the explicit Custom Placed Weapons instruction to load below GDB, and ambiguous Lux Master wording. The reported draw fix followed two simultaneous changes; it is not a complete compatibility certification. See `REFERENCE-OVERHAUL.md` for scope and open questions.
