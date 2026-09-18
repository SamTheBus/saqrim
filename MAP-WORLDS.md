# Separate-world map views

The mainland map now has a **Map / world** selector. Separate worlds open in `worlds.html?world=<id>`. Item links use the existing W-number hash, for example `worlds.html?world=solstheim#W007`. These additions do not change the original catalog, its classifications or numbers, or the recorded load order.

## Coverage and limitations

| World | Implemented view | What is and is not positioned |
| --- | --- | --- |
| Skyrim | Existing self-hosted mainland terrain | Existing 364 reference places and 103 linked catalog records are unchanged. |
| Solstheim | Geographic reference-coordinate layer with optional external terrain | 36 named place pins. Source-documented item associations distinguish pickup-area references, vendor camps, quest starts and nearby landmarks. The background image is requested from UESP; successful delivery by that host is not certified. A clearly labeled coordinate grid and pins remain when the image fails. |
| Icemoth / Hjorkvild Isles | Self-hosted creator-posted reference map | 14 approximate places read from the printed map symbols. Crimson Kiss links to Eyndis’ Folly as a nearby wreck reference, not the exact seafloor chest. Other Icemoth reward positions remain unverified. |
| Soul Cairn | External reference image and named location notes | No calibrated geographic pins in this release. If the image host refuses the request, the interface shows the item-location guide instead of an empty map. |
| Forgotten Vale | External reference image and named location notes | No invented coordinates for Vyrthur, a specific entrance, or interior treasure. Image delivery is host-dependent. |
| Blackreach | External reference image and location notes | Tower of Mzark is an access/reference association. No new interior pickup coordinates are claimed; the existing mainland tower references remain unchanged. |
| Evergloam / Aberrations of the Dwemer | Dedicated interactive location guide, **not a geographic map** | All 22 catalog records are grouped by the creator-documented places. Plankside, the Vault, Altar of Lies and other named sites have no fabricated compass positions or routes. |
| Beyond Reach | Dedicated interactive location guide, **not a geographic map** | All 50 catalog records remain accessible. Historical spell leads and unverified current-port placements retain their caveats. The standalone Tomes of Want merchant locations are not imported. |
| Atmora / Crucible | Dedicated interactive location guide, **not a geographic map** | Six named catalog rewards, with individual holders and calibrated island positions still pending. |
| Apocrypha | Dedicated location guide, **not a geographic map** | Multiple Black Book spaces and random chest distribution are not collapsed into one invented pickup location. |

**This is a partial geographic expansion, not a claim that every realm now has a finished terrain map.** UESP image requests returned HTTP 403 during asset preparation; the native-world images therefore remain optional external references with explicit failure handling rather than falsely labeled self-hosted assets.

## Controls

World switching, per-world item and location lists, search, checkbox item filters, Want/Maybe filtering, shareable world/item URLs, pan/zoom on available geographic layers, larger-map mode and the instant Top button are available. The checkbox logic remains OR within each group and AND across groups. Unpinned filtering tests actual numeric coordinates, not merely whether a record has a named location association.

Old `map.html#Wxxx` links still open the unchanged mainland index and offer an explicit link to the corresponding realm view. The old mainland index’s unpinned count means **without a mainland pin**, not without a pin in any realm.

## Geographic sources and attribution

- Solstheim terrain: [UESP contributor Roger’s Solstheim Map 02](https://en.uesp.net/wiki/File:User-Roger-Solstheim_Map_02.jpg). Original image is 3456 × 3072 pixels, at 128 pixels per cell, for 27 × 24 cells: x=0 through 26, y=2 through 25. Geographic reference coordinates use that stated frame. This is approximate alignment, not verification of mod-added object records.
- Solstheim named game-coordinate facts: [Itemaps Solstheim reference index](https://www.itemaps.com/maps/skyrim/solstheim). Only place names and factual position values are used; the publisher’s prose and application code are not imported.
- Icemoth map: [Siege at Icemoth creator gallery](https://www.nexusmods.com/skyrimspecialedition/mods/109541?tab=images), image `109541-1731800006-736173188.png`. Reference map posted by RoastGorilla439; map icons credited to Klime. The image is converted to WebP at its original 1025 × 769 dimensions. Approximate point positions are read from its displayed symbols.
- Soul Cairn, Forgotten Vale and Blackreach reference maps: UESP image pages `File:SR-map-Soul_Cairn.jpg`, `File:SR-map-Forgotten_Vale.jpg` and `File:SR-map-Blackreach.jpg`, linked by the relevant world view. Bethesda game imagery and UESP contributor work remain credited.
- Evergloam names and reward associations are taken from the original creator’s source already preserved in the catalog. Beyond Reach and the remaining worlds retain their original record-level research URLs and limitations.

Source maps are navigation references, not proof that the exact PS5 ports place an item at the indicated spot. The old Bloodmoon location names in a restoration mod are not assigned Morrowind-era coordinates on the Dragonborn map.

## Preservation, privacy and validation

`catalog-source.html` retains Git blob `364f4210b13f51a67610ec4946ef6fd4ef9fafd8`. All 617 W-numbers, original directions, evidence qualifications and research sources remain. No numeric-stat research is overwritten. All 220 load-order positions, file sizes and thumbnail assets are unchanged.

The realm views read `skyrimLootChoices_v202_20260917` without writing to it. Personal ratings and the console-install checklist keep their existing storage keys and values. No geolocation, console connection, user account or analytics is added. Optional native-world image requests disclose the visitor’s ordinary network request to the external image host; Icemoth terrain is served by this repository.

`tests/world-browser.py` tests actual site files through a local HTTP server and deliberately simulates optional image-host failures. It checks navigation, coordinate bounds, record preservation, filtered lists, evidence distinctions, local-storage preservation and mobile overflow. Those failure-injection tests do not certify successful delivery of remote terrain images. The existing `tests/map-browser.py` remains a regression check for the original mainland map and catalog.
