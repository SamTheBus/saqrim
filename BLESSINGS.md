# Shrines & standing stones

The map now has independent **Shrines**, **Standing stones**, and **Names when zoomed in** checkboxes. Purple star markers identify shrine references; turquoise triangle markers identify standing stones. Select a marker or open the reference list to read the benefits. Shared positions open a menu rather than hiding overlapping entries.

`blessings.html` provides three searchable views: **Gods & benefits**, **Shrine locations**, and **Standing stones**. The map and world pages link to this reference page. Pantheon checkboxes, a location-world selector and a map-reference filter help browse the deity and shrine lists. The race selector is explicitly a preview, not automatic character detection.

## Coverage

- **51 individually named Wintersun deity profiles**, each with shrine blessing, follower benefit, Devotee ability unlocked at 100% favor, eligibility, and summarized worship requirements. The author's headline says 50; the index follows the 51 named profiles in the description.
- **52 shrine-location records**. Some are shared temples containing several gods, and others are alternate shrine locations. This is not a census of every duplicate vanilla altar.
- **47 of those records resolve to existing map reference points**. These include named sites, towns, dungeon entrances, and nearby landmarks. They are not 47 surveyed altar coordinates or necessarily 47 distinct geographic positions.
- **13 Skyrim standing stones**, all linked to existing mainland reference sites. The Mage, Thief and Warrior stones share the Guardian Stones reference, making 11 distinct standing-stone map sites.
- **130 race–stone combinations**: all 13 stones for all 10 playable races. All 13 Breton stone entries additionally show their separate Stones of Galen effect.

The five shrine records without calibrated references are Hermaeus Mora in Apocrypha, Hircine at Snowclad Ruins, Auriel in the Inner Sanctum, the Auriel clue northeast of White Ridge Barrow, and the All-Maker's cleansed-stone worship entry. Their directions and benefits remain readable; no substitute coordinates were invented.

## Benefits and installed-mod scope

**100% means the favor threshold that unlocks the Devotee ability. It does not mean every god grants a +100% stat bonus.** Shrine blessings, follower benefits and Devotee benefits have separate sections. Where the author gives a favor-dependent value as X, the site does not manufacture an exact value at 100% favor. Favor costs and activation conditions remain attached to the ability.

The recorded installation contains Wintersun #27, Mannaz #28 and Freyr #29. Wintersun's recorded menu version is 3.2.0. Mannaz and Freyr each show menu version 1.00; those labels do not prove the upstream PC builds contained in the ports.

Stone mechanics are summaries of the **Freyr 1.2.0** and **Mannaz 3.0.1** author references. Wintersun mechanics and its shrine list use the author's **3.2.0** documentation. These references were consulted on 18 September 2026. The final PS5 behavior, winning overrides, individual shrine accessibility and exact numerical effects have not been independently play-tested.

Freyr replaces the normal standing-stone effects with race-specific effects. Do not add vanilla, Andromeda or Imperious stone bonuses to the displayed values. Bretons receive two separately displayed effects through Stones of Galen; this is not an arbitrary extra multiplier. Drawbacks such as the Breton Ritual/Serpent resource penalties and the Khajiit Atronach loan repayment condition are retained.

Solstheim's All-Maker Stones are a different system from the 13 Freyr stones. Their individual powers, the Mannaz Nord Roots passives and further All-Maker worship interactions are not represented as an additional completed Freyr table.

## Map precision and controls

The layer reuses `map-locations.json` and `world-data.js` positions. For example, the Temple of the Ancestors entry points to **Morvunskar as a reference**, while its instructions say to search south of that landmark. A town pin is not an exact temple door, and a dungeon-entrance reference is not an interior altar. On worlds without calibrated geography, the location guide remains available without markers.

Names appear as persistent labels when zoomed in; disabling that checkbox leaves tooltips. Shrine and stone visibility are independent of one another and of the pre-existing quest and item layers. Shrine deity filtering and benefit search apply to the new layer. The existing map text search also narrows it, but loot-type/Want filters do not silently hide religious reference markers.

Race selection updates the selected stone and the comparison cards. Shareable examples: `map.html?race=Breton#stone=shadow`, `worlds.html?world=solstheim&race=Breton#shrine=reclamations`, and `blessings.html?tab=stones&race=Breton#stone=shadow`. The original W-number and place links remain supported.

## Sources

- [Wintersun original author description](https://www.nexusmods.com/skyrimspecialedition/mods/22506)
- [Wintersun author readme and shrine locations](https://www.nexusmods.com/skyrimspecialedition/mods/22506?tab=docs)
- [Freyr original author description](https://www.nexusmods.com/skyrimspecialedition/mods/88043)
- [Mannaz original author description](https://www.nexusmods.com/skyrimspecialedition/mods/87219)

Temple and town references carry their UESP source links individually. Existing geographic-reference sources are retained in `MAP.md` and `MAP-WORLDS.md`. Each card retains its own source/version qualification. The deity profiles summarize rather than replace the full tenet and favor documentation.

## Preservation and testing

The new reference modules do not write local storage, contact a console, or change the recorded load order. Item choices, personal ratings, the console-install checklist and quest statuses/notes retain their existing keys and values. All 617 item records, all 220 mod entries, thumbnails, file sizes and 22 quest cards remain unchanged.

`tests/blessings-browser.py` checks all race–stone combinations, Breton-only second effects, data integrity, reference-coordinate reuse, independent layer switches, grouped Guardian Stones, deity filters, click handling, cross-world deep links, read-only storage, phone layout and the instant Top button. The workflow also runs the existing mainland-map, separate-world and quest-journal regressions. Tests use the actual site through a local HTTP server and do not certify gameplay behavior or optional remote terrain-image delivery.
