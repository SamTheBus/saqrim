# Saqrim

Personal Skyrim PS5 reference: a 637-target loot catalog and a 224-entry current load-order checklist.

- Website: https://samthebus.github.io/saqrim/
- Console load order: https://samthebus.github.io/saqrim/load-order.html
- Current load-order source: `1a12e7fc6d46-master_playlist.mp4` plus Sam’s final confirmed swaps and placements
- Earlier public source recording: https://www.youtube.com/watch?v=4uyqCADqwPo

## Checkbox filters and sorting

The loot catalog now has separate checkbox groups for item category, spell school, weapon handling, weapon type, armor class, equipment slot, and Want/Maybe/Skip choices. Within a group selections use OR; across groups selections use AND. A full set is not automatically an individually indexed helmet. Search, mod selection, live result counts, and removable filter chips work with the checkbox selections. On narrow screens, open Filters and use Show results.

The floating Top button is available on the loot catalog and load-order page and returns instantly to the page top. The recorded load-order numbers are never rearranged.

Armor-rating and weapon-damage sorts support ascending and descending order, keep unknown values last, and can show only records with numeric values. Author base values are separate from optional manually entered in-game values. Eight Artifact of Might weapons currently have source-documented base damage (https://www.nexusmods.com/skyrimspecialedition/mods/104381). No author base armor ratings have been indexed in this update. Missing numbers are null, never zero; enchantment magnitudes, armor bonuses and whole-set totals are not substituted for base stats. Classification coverage is incomplete: Unknown options expose unresolved types/schools/classes. Tags use existing catalog descriptions, descriptive names and cited original author documentation, not an extracted PS5 plugin manifest.

## Load-order provenance

The current order has 224 entries, from the October load-order recording plus Sam's final confirmed corrections. Opening browse results are excluded. KALLAX and full SMIM are absent; SMIM Essentials occupies the former SMIM slot. Dagoth Ur is immediately above Alternate Start, followed by the 33.4 KB Legacy of Orsinium patch and the perk stack. Daedra Pack is immediately above Mihail High Fantasy Monsters. Lucien and both patches, Deadly Dragons Armory and The Restless Dead remain.

`data/load-order-october-confirmed.txt` is the readable current snapshot; `load-order.tsv` feeds the site. `load-order-snapshot.json` separates October size/position evidence, later user updates, and version/thumbnail information retained from September. New versions or exact identities not captured remain unknown. The 14.73 GB total is historical, before the final swaps, not a current free-space estimate.

The TSV retains eight columns: position, name, displayed size, retained version label, locator, category, identification title, thumbnail index. Thumbnail -1 means no matching crop; existing indices still address the original sheets. No fake screenshot or guessed art is assigned to new mods.

## Preservation and local progress

`catalog-source.html` preserves the previous 617-record `loot.html` byte-for-byte (Git blob 364f4210b13f51a67610ec4946ef6fd4ef9fafd8). It remains the source for every original card, W-number, location, qualification, research URL and found field, and can be opened as a reading fallback. The new `index.html` loads those cards directly, without a nested scrolling frame. `loot.html` redirects old links to the updated catalog and preserves their query/hash.

Loot choices retain localStorage key `skyrimLootChoices_v202_20260917`. Optional observed ratings use `saqrimObservedStats_v1`. Backups include choices and observed ratings. Older choices-only backups remain supported and do not erase existing ratings. No cloud syncing or authentication was added.

The current load-order checklist uses localStorage key `saqrim-load-order-224-october-v1` (migrated by mod identity from `saqrim-load-order-210-2026-09-23-v2`); older checklist keys are left untouched. Checkmarks do not modify a console and do not sync between browsers. No mod download buttons are provided.

## Validation

32 local browser checks passed using the actual catalog data and a test-only localStorage/fetch fixture, including all 617 records, legacy choices, checkbox OR/AND behavior, rings versus amulets, weapon handling, numeric sorting in both directions, null handling, observed ratings, backup compatibility, mobile layout, deep links and instant Top behavior. Local rendering checks are not a claim of a live-site browser test.

Static HTML/CSS/JavaScript only; no build step, package dependencies or external analytics.


## Reference overhaul · Batch 01

The Load Order page now adds ten sourced description cards, a research-coverage filter, description/requirement search, source locators and current-number cross-links. `load-order-reference.json` stores claims and evidence independently of recorded TSV rows and historical Bethesda snapshots. `load-order-reference.js` is optional: a failed research request must not break the checklist. The current 210-row order, catalog, quest data, IDs and localStorage keys are preserved.

The source recording exposes Animated Armoury/GDB and GDB/Wear Multiple Rings warnings, the explicit Custom Placed Weapons instruction to load below GDB, and ambiguous Lux Master wording. The reported draw fix followed two simultaneous changes; it is not a complete compatibility certification. See `REFERENCE-OVERHAUL.md` for scope and open questions.

## October synchronization validation

`tests/october-sync.py` validates the full 224-entry order, final eight entries, current cross-references, saved-state migration, reference cards, and desktop/mobile rendering. The earlier tests with fixed September baselines remain historical; current CI uses the October-aware regression checks. No changes to actual console installations are made.


## October adventure content

The current collection has 637 loot/power records, 56 quest/adventure guides, and 15 expanded mod descriptions. The 224-entry console order is unchanged. Content batch 02 covers Legacy of Orsinium, Undeath, The Final Cataclysm, Rotdyflissa and a qualified Dagoth recruitment profile. See [CONTENT-BATCH-02.md](CONTENT-BATCH-02.md). Earlier validation sections above describe historical batches.
