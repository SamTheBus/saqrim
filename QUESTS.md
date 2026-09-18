# Quests & Rewards

`quests.html` contains **46 quest and adventure cards** for the recorded PS5 installation, not every quest in Skyrim or every installed mod. Cards Q001–Q015 cover mod-added quests, encounters and clearly labeled adventure-wide guides. Q016–Q022 cover existing quest routes with modded loot. Expansion 2 adds Q023–Q046; see [the expansion notes](QUESTS-EXPANSION.md).

## Starting points and destinations

Each card separates its starting world/area, first contact or trigger, main destinations and prerequisites. Recommendations are not presented as hard level gates. Starting areas that have not been established remain pending. The mod title can identify an adventure or encounter chain; it is not always the exact name displayed in the journal.

Sources on each card distinguish original author documentation, recorded PS5 entry instructions, retained catalog research and base-game/community references. New PC documentation and community routes are not certified behavior for the recorded PS5 ports.

## Rewards and filters

Reward roles are **completion**, **conditional/choice**, **completion unlock**, **boss/NPC loot**, **optional discovery**, and **unverified lead**. Missing final payouts say not documented, not no reward. A credited NPC outfit is not automatically a player reward; Amelia's W617 outfit is deliberately excluded from Akavir reward filters.

The reward-filter default examines completion rewards, choices and unlocks. Documented route loot requires selecting the expanded scope. Unverified leads require a separate checkbox. Adventure-wide rosters for Aberrations and Beyond Reach retain the original W-number qualifications; they do not become lists of final quest payouts.

Checkbox groups cover starting area/world, destination world, installed mod, quest/guide type, progress, reward category, spell school, weapon handling/type, armor class and equipment slot. Choices use OR within a group and AND across groups. All item filters must match the **same reward**. A ring and a separate light-armor item cannot create a false combined match. Want-only filtering uses the existing item picks and the same eligible reward, not an unrelated object elsewhere in the quest.

Outcome spoilers start collapsed. Reward names remain visible. Optional loot and detailed item acquisition notes are expandable. Every linked W-number opens the original catalog entry and its source/evidence notes.

## Personal quest journal

Quest status (Not started / In progress / Completed), chosen-rewards-collected and notes are independent manual controls. No action reads a console or updates a game save. Completing a quest does not automatically collect a reward or alter the Want list.

Only `saqrimQuestProgress_v1` is written. Existing item choices, personal ratings and console-install checklist retain their keys and values. Separate versioned quest backups validate known Q-numbers and merge recognized fields; they do not replace other saves. Sharing a view includes filters, not private notes or progress. A recipient's Want/progress filters use that recipient's own browser state.

## Connected maps and catalog

All sections receive Quests & rewards navigation. Related catalog entries link back to quest/adventure cards, including the expanded adventure rosters.

A separately toggleable green exclamation-marker layer shows reviewed quest-start **reference areas** on existing mainland and Solstheim positions. Nearby landmarks such as Northwatch Keep for the Old Wooden Jetty are explicitly not exact quest-giver coordinates. Pending start positions are not invented. Place details list quests starting there or nearby. Other realm views link to their existing location guides rather than falsely claiming geographic coverage.

## Preservation and testing

The original 617 catalog records, recorded 220-mod load order, thumbnails and sizes remain unchanged. Core catalog/classification/load-order/map data and JavaScript are preserved; integration is additive through `site-quests.js` and a loader in `site-top.js`.

`tests/quest-browser.py` exercises real repository files via a local HTTP server. It verifies reward scopes, same-reward filtering, starting versus destination worlds, original Want selections, independent status fields, safe notes, reload persistence, import validation, old-save preservation, catalog/mod/map links, overlay toggles and phone layout. The dedicated workflow also runs existing mainland-map and realm regressions. Optional external map-image failure is not represented as successful image delivery.
