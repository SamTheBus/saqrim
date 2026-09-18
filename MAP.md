# Map and location index

`map.html` adds a self-hosted, pannable/zoomable Skyrim reference map. `map-locations.json` contains 364 approximate reference-place positions derived from a pinned public exterior-cell atlas and its settlement reference positions. They are not exact item or entrance coordinates.

`map-links.js` explicitly associates 103 existing catalog records with 44 reference areas. Association kinds distinguish named sites, town/vendor hubs, quest clues and nearby landmarks. Original locations, evidence, source URLs and PS5 caveats are displayed from the immutable 617-record `catalog-source.html`. All 617 records are searchable in the item index; the remaining 514 do not receive invented coordinates. Separate-world records do not have map layers in this release.

Map/category/spell-school/weapon/armor/slot checkbox filters use OR within groups and AND across groups. Want/Maybe filtering reads the existing choice key, without writing it. No geolocation, console access, tracking, authentication or remote runtime map API is used. Leaflet 1.9.4, map artwork and location data are served from this repository; attribution and Leaflet license are in `assets/map/`.

`site-top.js` adds the Map tab to existing navigation and a map/index link to each catalog card. Existing catalog data, numeric metadata and all 220 load-order positions, file sizes and thumbnails remain unchanged. Old deep links and storage keys are retained.

Automated browser checks are in `tests/map-browser.py`; run with Python Playwright and installed Chromium. The checks use the actual repository files served over a local HTTP server.
