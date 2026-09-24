# Familiar uniques and load-order review — research 18 September 2026 · load order synced 23 September 2026

## Coverage

The current catalog contains **633 records**: the original 617 IDs plus **16 additions, W618–W633**. The archived `catalog-source.html` remains byte-for-byte unchanged. The current rendering uses `catalog-current.html`, which adds the new items and revises reviewed existing entries. 77 records have item-specific provenance panels. No record is certified as the final PS5 winner.

New items: Dawnbreaker, Ebony Blade, Ebony Mail, Mace of Molag Bal, Mehrunes' Razor, Savior's Hide, Auriel's Bow, Bloodskal Blade, Gauldur Amulet, Staff of Magnus, Arch-Mage's Robes, Dragonbane, Ghostblade, Soulrender, Bloodscythe and Shield of Solitude.

Use the Item origin and Artifact review checkbox groups. The separate New familiar uniques checkbox selects exactly W618–W633. `?batch=Familiar%20uniques%201` opens that batch. The earlier W552–W617 discovery checkbox still selects its original 66 records.

## What follows the load order

This reviews Sam's current 210-entry order and cited public descriptions, not the actual ESP/ESM records or a save. For two plugins overriding the same FormID, the later whole record normally wins; arbitrary fields are not automatically combined. Referenced enchantments, effects, scripts, quest rewards, placed references and texture/mesh assets require their own checks. An item name or visual purpose alone does not establish record identity.

- **ArteFakes / Artificer:** ArteFakes is now #56 and Artificer is #57. For documented shared item records, Artificer is therefore the later mechanics candidate. Without the separate compatibility patch, ArteFakes models are **not** promised to survive the later Artificer record.
- **Fiery Souls:** #56 ArteFakes → #57 Artificer → #67 Truly Unique. The dedicated axe is now the latest documented same-item editor, so its Emberwisp / Flameclaim version is the expected candidate rather than ArteFakes or Soulbrand.
- **Thane rewards:** #68 Unique Thane Weapons follows #57 Artificer. Quest assignment and item records are distinct; the dedicated thane overhaul remains the expected reward candidate.
- **Praedy's Staves:** #47–53 load before Artificer #57. Published Praedy/Artificer patches exist; none is in this load order, so Staff of Magnus mechanics are expected from Artificer while the Praedy model is unresolved.
- **Destroy the Dark Brotherhood:** JaySerpa's Quest Expansion Bundle #131 is later than Artificer. A published compatibility patch states the unpatched combination can prevent **Windshear** and **Firiniel's End** from being obtainable. The current #133 Wintersun and #132 USSEP patches are not that Artificer patch.
- **Rings:** #96 Wear Multiple Rings is later; exact unique-ring coverage in the PS5 port remains uninspected. This stays a possible-overlap warning, not a proven winner.
- **Identity:** #70 Volkihar Relic Sword is not assumed to replace Harkon's Sword. Shared names for restored/added Prelate's Mace and Briarheart Geis still need identity checks. Halidil carrying an Aetherial Shield is not proof of an ARMO override.

No separately named Artificer–ArteFakes reconciliation patch, Artificer–Praedy patch, or Destroy-the-Dark-Brotherhood–Artificer patch appears in the current list. The existing #58 Artificer–USSEP patch is not assumed to forward later #67 or #68 changes. Public third-party patches are cited only as compatibility evidence; they are **not** treated as installed.

## Versions and effects

New Artificer summaries use author-reference **1.0.11**; the recorded PS5 menu says **v1.00**, which does not identify the upstream build. ArteFakes author-reference SE **2.0** and recorded **v2.0.1** are likewise not proof of identical payloads. Source documentation mixes some LE/SE features; those are not imported as guaranteed PS5 reforging options.

Numeric base armor/damage is not filled from vanilla tables, enchantment damage, armor bonuses or unrelated port versions. New base ratings remain unknown. Existing manually observed ratings stay separate. In particular Ebony Mail's armor bonus is not its base armor, and Bloodskal's projectile damage is not sword base damage.

## Documented-role screening

These are review priorities and distinctions, not a complete record-conflict matrix. Non-artifact-looking plugins and bundles may still contain relevant records. Exact winning effects require matching plugin records or scoped in-game evidence.

| Recorded order | Mod / group | Review scope |
|---|---|---|
| 1 | USSEP | Earlier fixes. Later copies of records can forward or replace fixes. |
| 23 | Thaumaturgy | Artificer dependency; Summermyst remains a separate installed enchanting overhaul whose broader compatibility is not resolved here. |
| 24 | Summermyst | New enchantments/distribution. Same enchantment theme does not prove identical artifact records. |
| 31 | Mysticism | Artificer dependency. Linked effects and spells require their own record checks. |
| 34 | Odin | Magic overhaul; shared magic effects can matter independently of an item record. |
| 43 | OWL | Loot and level-list changes; do not equate distribution with an item enchantment. |
| 44 | OWL randomized special loot | Distribution/variant selection is separate from weapon stats. |
| 45 | OWL Summermyst patch | Named compatibility scope, not a catch-all artifact patch. |
| 48 | Simply More Variety AE | Creation loot integration; not proof every vanilla artifact is replaced. |
| 49 | Praedy staves and patches #48–53 | Visual staff records and named magic integrations. Artificer loads later at #57; no Artificer–Praedy patch is in this load order. |
| 56 | ArteFakes | Unique-item model/record edits now intentionally placed above Artificer. If both edit the same item record, #57 Artificer is the later candidate; ArteFakes models are not assumed to survive without a patch. |
| 57 | Artificer | Documented artifact and unique-item changes; current priority is below ArteFakes and above the dedicated Fiery Souls / thane replacers. |
| 58 | Artificer–USSEP patch | Named fix integration. No evidence that it merges later #67 or #68 changes. |
| 61 | Heavy Armory | New weapon families and distribution; not a global artifact override inferred from its title. |
| 62 | More Unique weapons #62–64 | Hand-placed additions are not automatically replacements for similarly themed vanilla artifacts. |
| 65 | Artifact of Might | Eight added weapons. Not another name for Artificer. |
| 66 | Eidolon sword | Standalone port; no Harkon/Daedric artifact identity inferred. |
| 67 | Fiery Souls Truly Unique | Direct named axe overlap and now the latest of ArteFakes #56, Artificer #57 and the dedicated axe. |
| 68 | Unique Thane Weapons | Later than Artificer; documented thane-reward replacement remains the expected reward candidate. |
| 69 | Minecraft Weapon Pack | Recorded PS5 description says craftable. Do not import the source PC replacer behavior. |
| 70 | Volkihar Relic Sword | A standalone relic story; not established as replacing Harkon's Sword. |
| 71 | Infinity Sword / Occiglacies #71–72 | Separate pickups; matching dungeon or theme is not a shared FormID. |
| 74 | Psyche artifacts | Port book and exact item identities remain incomplete; no guessed vanilla collisions. |
| 75 | Dwarven Power Armor | Halidil offers an Aetherial Shield acquisition route; giving an NPC an item is not proof its ARMO record is overwritten. |
| 76 | Race Armor / outfits / cloaks #76–81 | NPC outfit, appearance and new gear roles are not automatically artifact enchantment edits. |
| 82 | Deadly Dragons Armory | Additional dragon loot; not assumed to overwrite every existing artifact. |
| 55 | Xavbio #52–55 | Later texture assets. Do not infer a final enchantment from texture priority; exact asset paths/bundled plugins are uninspected. |
| 96 | Wear Multiple Rings | Later equipment editor. Unique-ring coverage in this exact PS5 port remains unverified, so ring-record conflicts stay possible rather than certified. |
| 97 | Animated Armoury / patch #98 | Weapon families, animations and list integration; no blanket overwrite of named vanilla artifacts inferred. |
| 131 | JaySerpa quest bundle / #125–133 patches | Later quest edits. Destroy the Dark Brotherhood has a documented Artificer incompatibility affecting Windshear and Firiniel's End unless specifically patched. |
| 141 | Forbidden Goods | Merchant acquisition is not the same thing as changing the base item. |
| 145 | Knight of the North | Creation relic hunt and access rules. Keep Creation gear separate from vanilla/DLC uniques. |
| 148 | Lucien / patches #141–150 | Follower and Creation integration; not presumed to repair artifact conflicts. |
| 154 | Cities / world edits #154 onward | Interior, reference, access and placement conflicts may remain even when an item effect is expected. |
| 198 | Bedlam | Dungeon encounters are not automatically unique-item records. |
| 199 | High King location patches #190–200 | Specific world integrations, not a generic artifact conflict resolver. |
| 201 | AFT / addon #202 | Follower inventory behavior is separate from a documented base-weapon override. |
| 203 | Lux | Late interior/reference changes must not be mistaken for a blanket final enchantment provider. |

## Sources

Each new item carries its own original-author effects source and separately labeled base-game acquisition source. Existing research remains in the immutable archive. Relevant primary sources:

- [Artificer author](https://www.nexusmods.com/skyrimspecialedition/mods/99619)
- [ArteFakes author roster / compatibility](https://www.nexusmods.com/skyrimspecialedition/mods/41254)
- [Truly Unique axe author](https://www.nexusmods.com/skyrimspecialedition/mods/154943)
- [Unique Thane Weapons author](https://www.nexusmods.com/skyrimspecialedition/mods/35497)
- [Compatibility patch author — NOT installed](https://www.nexusmods.com/skyrimspecialedition/mods/99684)
- [xEdit conflict-resolution documentation](https://tes5edit.github.io/docs/5-conflict-detection-and-resolution.html)
- [Recorded PS5 order](https://www.youtube.com/watch?v=4uyqCADqwPo)

## Integration and preservation

The catalog, mainland map, realm indexes and quest rewards read the same reviewed data. All existing 46 quest objects remain identical; six explicit quest reward links connect the newly indexed items to existing cards through separate metadata. No extra quests or geographic coordinates are invented.

The six navigation destinations remain unchanged, with the current loot count updated everywhere. The 219-entry mod set, thumbnails, file sizes, faith/stone data and browser storage keys are preserved; current load-order numbering and checklist migration are retained. The archive preserves all old source wording. Opening a page does not migrate or overwrite item choices, personal ratings or quest progress.

## Validation scope

Tests check the original archive and untouched-data hashes, stable old and new IDs, allowed reviewed-record changes, unchanged quest objects, real item-source precedence flags, absence of invented base ratings, checkbox combinations, quest/catalog reverse links, map/realm data parity, mobile navigation, backup round trips and no save writes on startup. Browser tests do not certify gameplay behavior or PS5 winning records.
