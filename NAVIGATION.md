# Site navigation and separate guides

The public navigation now has the same six destinations, in the same order, on the catalog, load-order checklist, quest journal, mainland map, other-world maps and both new reference pages:

1. Loot catalog · 617
2. Load order · 220
3. Map
4. Quests & rewards
5. Shrines & Gods — `shrines.html`
6. Standing Stones — `standing-stones.html`

The missing tab was caused by `site-blessings.js` adding a navigation link only when that map integration was loaded. Navigation now belongs to the shared `site-top.js` module. It does not require a map or any shrine data to load. The primary pages also contain the complete navigation directly in their HTML, with versioned script references so refreshed pages request the update. There is exactly one active top-level destination; all world views belong to Map.

## Separate pages

`shrines.html` is the Wintersun guide. It contains the Gods & benefits and Shrine locations views. It includes shrine blessings, follower benefits, 100%-favor Devotee abilities, eligibility, worship requirements, locations and their existing evidence caveats. It does not display the stone race selector.

`standing-stones.html` opens the thirteen Freyr stones directly. It contains the race preview, all ten race comparisons and the separate Breton Stones of Galen effects. It has its own heading and search; there is no god/stone subtab switch and no visible pantheon filter.

Both pages share the existing reference data and renderers instead of copying the mechanics. A cross-section deity/shrine/stone deep link moves to the appropriate page while retaining its query and fragment. The previous `blessings.html` combined view remains available for older bookmarks and existing profile links, but it is no longer a top-level navigation destination. Map controls offer distinct links to both new guides.

## Preserved

No loot, quest, faith, race, stone or location facts were added or removed. The 617 catalog records, 220 recorded mods, 22 quest cards, map positions, thumbnails and file sizes retain their original data. Existing browser storage keys for choices, observed ratings, console checklist and quest progress are unchanged. Navigation never clears or transfers progress. New quest research is paused while this navigation fix is completed.

## Validation

`tests/navigation-browser.py` checks the complete menu at 1400, 390 and 320-pixel widths, active states, navigation from each primary section, dedicated guide content, filters, race preview, Back/Forward, old bookmarks, cross-section deep links, static HTML links without JavaScript, and saved-state preservation. The workflow also runs the previous shrine/stone, mainland map, realm and quest-journal regressions. Runtime results are recorded in the Navigation and separate guides workflow; this document does not itself certify a passing run.
