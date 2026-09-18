# Saqrim

Personal Skyrim PS5 reference: a 617-target loot catalog and a 220-entry recorded load-order checklist.

- Website: https://samthebus.github.io/saqrim/
- Console load order: https://samthebus.github.io/saqrim/load-order.html
- Source recording: https://www.youtube.com/watch?v=4uyqCADqwPo

## Load-order provenance

The 220 entries retain the workbook's recorded order, sizes, menu versions, clipped titles and per-entry timestamps. Sizes are the displayed values, not live measurements or exact-byte totals. The recorded console shows 220 entries enabled and 14.97 GB used. This is not a compatibility-certified setup.

Thumbnails are cropped from the user's actual recorded Creations menu, not newly fetched Bethesda listing art. Identical or near-identical repeated images share a tile. Four AVIF sheets contain 186 distinct tiles (8 columns x 6 rows of 96 x 54 pixels per sheet). Generic menu placeholders are retained rather than replaced with guessed pictures. Artwork belongs to its respective creators.

`load-order.tsv` has no header. Columns: order, identified name, displayed size, menu version, video timestamp, category, clipped console title, zero-based thumbnail tile. For a tile index i, sheet=floor(i/48), column=i%8, row=floor((i%48)/8).

## Preservation and local progress

`loot.html` preserves the former `index.html` byte-for-byte. The small new index adds navigation and displays that unchanged catalog in a same-origin frame. Existing loot choices keep their original browser storage keys. No cloud syncing or authentication was added.

The load-order checklist has a separate localStorage key, `saqrim-load-order-220-2026-09-17`. Checkmarks do not modify a console and do not sync between browsers. No mod download buttons are provided.

Static HTML/CSS/JavaScript only; no build step, package dependencies or external analytics.
