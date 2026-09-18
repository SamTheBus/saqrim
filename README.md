# Saqrim

Personal Skyrim PS5 reference: a 617-target loot catalog and a 220-entry recorded load-order checklist.

- Website: https://samthebus.github.io/saqrim/
- Console load order: https://samthebus.github.io/saqrim/load-order.html
- Source recording: https://www.youtube.com/watch?v=4uyqCADqwPo

## Checkbox filters and sorting

The loot catalog now has separate checkbox groups for item category, spell school, weapon handling, weapon type, armor class, equipment slot, and Want/Maybe/Skip choices. Within a group selections use OR; across groups selections use AND. A full set is not automatically an individually indexed helmet. Search, mod selection, live result counts, and removable filter chips work with the checkbox selections. On narrow screens, open Filters and use Show results.

The floating Top button is available on the loot catalog and load-order page and returns instantly to the page top. The recorded load-order numbers are never rearranged.

Armor-rating and weapon-damage sorts support ascending and descending order, keep unknown values last, and can show only records with numeric values. Author base values are separate from optional manually entered in-game values. Eight Artifact of Might weapons currently have source-documented base damage (https://www.nexusmods.com/skyrimspecialedition/mods/104381). No author base armor ratings have been indexed in this update. Missing numbers are null, never zero; enchantment magnitudes, armor bonuses and whole-set totals are not substituted for base stats. Classification coverage is incomplete: Unknown options expose unresolved types/schools/classes. Tags use existing catalog descriptions, descriptive names and cited original author documentation, not an extracted PS5 plugin manifest.

## Load-order provenance

The 220 entries retain the workbook's recorded order, sizes, menu versions, clipped titles and per-entry timestamps. Sizes are the displayed values, not live measurements or exact-byte totals. The recorded console shows 220 entries enabled and 14.97 GB used. This is not a compatibility-certified setup.

Thumbnails are cropped from the user's actual recorded Creations menu, not newly fetched Bethesda listing art. Identical or near-identical repeated images share a tile. Four AVIF sheets contain 186 distinct tiles (8 columns x 6 rows of 96 x 54 pixels per sheet). Generic menu placeholders are retained rather than replaced with guessed pictures. Artwork belongs to its respective creators.

`load-order.tsv` has no header. Columns: order, identified name, displayed size, menu version, video timestamp, category, clipped console title, zero-based thumbnail tile. For a tile index i, sheet=floor(i/48), column=i%8, row=floor((i%48)/8).

## Preservation and local progress

`catalog-source.html` preserves the previous 617-record `loot.html` byte-for-byte (Git blob 364f4210b13f51a67610ec4946ef6fd4ef9fafd8). It remains the source for every original card, W-number, location, qualification, research URL and found field, and can be opened as a reading fallback. The new `index.html` loads those cards directly, without a nested scrolling frame. `loot.html` redirects old links to the updated catalog and preserves their query/hash.

Loot choices retain localStorage key `skyrimLootChoices_v202_20260917`. Optional observed ratings use `saqrimObservedStats_v1`. Backups include choices and observed ratings. Older choices-only backups remain supported and do not erase existing ratings. No cloud syncing or authentication was added.

The load-order checklist has a separate localStorage key, `saqrim-load-order-220-2026-09-17`. Checkmarks do not modify a console and do not sync between browsers. No mod download buttons are provided.

## Validation

32 local browser checks passed using the actual catalog data and a test-only localStorage/fetch fixture, including all 617 records, legacy choices, checkbox OR/AND behavior, rings versus amulets, weapon handling, numeric sorting in both directions, null handling, observed ratings, backup compatibility, mobile layout, deep links and instant Top behavior. Local rendering checks are not a claim of a live-site browser test.

Static HTML/CSS/JavaScript only; no build step, package dependencies or external analytics.
