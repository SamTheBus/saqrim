# Saqrim reference overhaul · Batch 01

Reviewed 24 September 2026. Scope: ten foundation, lighting and animation entries. The other 200 current mods keep their previous metadata and are **not** marked description-reviewed.

## Current coverage

USSEP; Simple Workaround Framework; Lux Resources; Lux Master; Animated Armoury; Heavy Armory–Animated Armoury Patch; GDB's Elden Beast Lite; XPMSSE Plus Custom Placed Weapons; the alternative CFPAO Lite port; and Lux PS5's interior module.

Each expanded card includes a sourced summary, relevant requirements, compatibility or placement notes, remaining uncertainties, and links to related entries using their current positions. Acquisition notes are included where the video actually supplies them. No invented spell lists, pickup coordinates, item counts or compatibility patches have been added.

## Evidence

- **Recorded PS5:** manually reviewed description text in `Skyrim_LO.mp4`, supplied 23 September. Claim-level source links give timestamps. The upload is not publicly hosted on this site.
- **Official listing match:** an official search-index identity/excerpt match only, explicitly qualified where the full live description was not readable.
- **Upstream docs:** original author or maintainer documentation. PC/Xbox implementation details are not silently assigned to the installed PS5 port.
- **User-reported test:** Sam's observed outcome. Moving XPMSSE and removing Simple Visible Favorited Gear happened together; this was not an isolated causality test.
- **Assessment:** a sourced interpretation or unresolved question, not a claim of measured plugin behavior.

Recording SHA-256: `219dd3f5f83f13570d9bcebfabb4652b9e8bcf31a74b29a3e7b4a259cba89fcf`. Duration: 685.94068 seconds. Current source metadata remain attached to the existing TSV rows. The 211-entry recording predates the 210-entry cleanup.

## Important recorded findings

**Animated Armoury, 07:30.60–07:31.00:** the porter's notes explicitly name GDB's Elden Beast and Ultimate Dodge as conflicts. The installed distribution patch only describes leveled-list integration; it is not evidence of a behavior-conflict fix.

**GDB Lite, 07:50.90:** the description names Visible Favorited Gear and Wear Multiple Rings as incompatible. The former was removed from this setup; Wear Multiple Rings remains. This is a recorded warning, not a newly diagnosed crash.

**XPMSSE, 07:26.00:** this Custom Placed Weapons variant explicitly instructs placement below GDB. GDB's generic panel gives the reverse order. Both are documented, along with Sam's narrow reported draw result.

**Lux Master, 00:52.30–00:53.50:** the description mentions Lux Via Master and contains both bottom-placement and automatic-top-placement wording. The current plugin's actual master dependencies have not been inspected. No automatic installation or reorder follows from that ambiguity.

**SWF, 00:07.70–00:12.70:** the PS5 description says its scripts and plugin differ from Xbox's. An equivalent AllGUD/favorited-weapons switch is not established for this PS5 build. The earlier unqualified replacement suggestion is not retained as a fact.

**CFPAO, 07:51.80–07:52.50:** the extra Nexus link resolves to SIGMA first-person magic animations. This improves source identification but does not establish the port's full animation roster.

## Explicitly still open

The exact source of the unarmed left-trigger block; whether this Lite build exposes a working toggle for it; the full payloads and exact Bethesda identities of incompletely matched ports; Lux Master dependency wording; and actual behavior compatibility of the remaining animation stack. No further mods were moved or removed for this reference update.

## Implementation and validation

Optional reference JSON/UI/CSS on the existing Load Order page; no new storage key. The integration script is idempotent. The browser regression checks exercise all 210 rows, expanded/flagged filters, description search, checkmark persistence, number and source links, small-screen layout, invalid/missing optional data, and preservation of the original catalog/quest/reference files. Test results describe the website, not gameplay.
