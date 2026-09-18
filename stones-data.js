/* Mechanics reference: Enai Siaion's Freyr 1.2.0 and Mannaz 3.0.1.
   PS5 menu versions are v1.00 for both; upstream equivalence is NOT established. */
'use strict';
window.SaqrimStonesData=(()=>{
 const source='https://www.nexusmods.com/skyrimspecialedition/mods/88043';
 const raceSource='https://www.nexusmods.com/skyrimspecialedition/mods/87219';
 const order=['Mage','Thief','Warrior','Apprentice','Atronach','Lady','Lord','Lover','Ritual','Serpent','Shadow','Steed','Tower'];
 const blocks={
 'Argonian':`Mage|Caustic Burn|Caustic Spit duration doubles.
Thief|Chameleon|While stationary, detection is 25% harder.
Warrior|Histskin|Additional Health recovery of 2% maximum Health/second.
Apprentice|Regrow Limbs|Below 25% Health, recover 5% maximum Health/second.
Atronach|Hist Spores|Caustic Spit adds 20 seconds of random aggression to creatures and people.
Lady|Swamp Dweller|Additional 25% resistance to both disease and poison.
Lord|Dissolve|Caustic Spit disintegrates targets under 20% Health.
Lover|Waterhome|Amphibious also replenishes Magicka and Stamina.
Ritual|Blood in the Water|Attack and critical damage +25% when a nearby foe is below 25% Health.
Serpent|Basilisk|Caustic Spit adds a 3-second paralysis.
Shadow|Swamp Poison|Foes within 20 feet lose 25% Poison Resist.
Steed|Polished Scales|Amphibious grants an additional 100% swim speed.
Tower|Melt Lock|Locks become trivial to pick only while Caustic Spit is hitting the locked object; no lingering duration.`,
 'Breton':`Mage|Arcane Mastery|Spell and scroll effectiveness +15%.|Mage's Path|Mage-skill experience +15%.
Thief|Shadow Mastery|Sneaking detection is 15% harder; sneak-attack damage +15%.|Thief's Path|Thief-skill experience +15%.
Warrior|Combat Mastery|Attack and critical damage +15%.|Warrior's Path|Warrior-skill experience +15%.
Apprentice|Arcane Initiate|Once each battle, activate a foe for random elemental damage equal to half your Destruction level.|Dragonheart|Power attacks, bashes and sneak attacks add random elemental damage equal to half your Destruction level.
Atronach|Coven Magic|Spell and scroll effectiveness +50%, consuming Briarheart, Human Heart or Human Flesh from inventory.|Wyrdcraft|15% chance for humans you kill to carry Human Heart or Human Flesh.
Lady|Blessing of the Lake|20% incoming-spell absorption chance; absorbed spells restore Magicka.|Kingmaker|Periodic gold, valuable-item or enchanted-item gifts; average interval 10–20 minutes.
Lord|Crown of Autumn|Power-attack and critical damage +30%, but combat Stamina regeneration stops.|Old Stone|Power attacks remain possible with empty Stamina, with a 50% damage/critical penalty. Both Lord effects apply; not a free full-strength attack.
Lover|Poetry in Motion|Entering combat makes you ethereal for up to 5 seconds, ending when you attack.|Slam Poetry|Breaking ethereal state early releases a nearby staggering Warstomp.
Ritual|Druidom|With a staff drawn, spells gain 50% power and cost 50% more Magicka.|Circle of Galen|Normal Magicka regeneration stops. A drawn staff supplies Magicka by losing charge; left staff drains first when dual-wielding.
Serpent|Dark Constellation|In combat, your Magicka and Stamina stop regenerating and drain 5 points/second.|Star Curse|Applies Dark Constellation to foes within 33 feet as well; it does not remove your own drawback.
Shadow|Dead Noon|A drawn bow marks targets after 1 second per 25 Health; hitting a marked foe scores 10× critical damage, not 10× total bow damage.|Outlaw|Movement speed +20% while a bow is drawn.
Steed|Horsemanship|Your horse and nearby allies gain 25% speed.|Roadside Rest|While stationary with hands lowered, Magicka/Stamina regeneration +50%.
Tower|Iron Mask|During combat, sneaking is 50% better and sneak attacks gain 25% damage.|The Donjon|Sneak outside combat and activate a living target: 20-second mental slumber or until attacked, costing 50 Magicka; also increases pickpocket chance by 20%.`,
 'Dark Elf':`Mage|Spite|Spell effectiveness rises as Health falls, up to +25%.
Thief|Blinding Ash|Fireblood also blinds targets and ends their combat.
Warrior|Dishonor|Attack and critical damage +20% against a lone target.
Apprentice|Spirit Walker|Ancestral Protector becomes once-per-battle rather than once-per-day.
Atronach|Embers|Additional Fire Resist +25%.
Lady|Walk Alone|Additional Magicka and Stamina recovery of 1% maximum/second.
Lord|Heart of Ash|Toggle costs 25 Magicka; drains about 10 Health/second for +30% attacks, criticals and spells. Cast again to stop.
Lover|Ancestral Hearth|Ancestral Protector can also attack a Fireblood-burning enemy; it still spends its daily activation.
Ritual|Passion|Fireblood captures fire automatically on entering combat.
Serpent|Ancestral Vengeance|Ancestral Protector adds damage equal to your Fire Resist value.
Shadow|Vendetta|Attack and critical damage +25% while Ancestral Protector is on cooldown.
Steed|Blazing Speed|Fireblood also gives +10% movement speed.
Tower|Unwelcome Guest|Spend stored Fireblood to open an Expert-or-lower lock.`,
 'High Elf':`Mage|Highborn|Magicka +50 while an Inborn Magic effect is active.
Thief|Mischievous|Replaces Faerielight with a brief disarm.
Warrior|Autumn|Replaces Faerielight with Stamina absorption equal to 20 + 5×level.
Apprentice|Mythal|Inborn Magic effects last 10 extra seconds.
Atronach|Faerie Fire|Replaces Faerielight with 50% magic weakness for 10 seconds.
Lady|Glare|Replaces Faerielight with -500 armor for 10 seconds.
Lord|Superiority|Inborn Magic strength +50%.
Lover|Unseelie|Replaces Faerielight with Magicka absorption equal to 20 + 5×level.
Ritual|Crystalline|Magicka/Stamina regeneration +200%, with -250 armor and -50% magic resistance.
Serpent|Will o'Wisp|Replaces Faerielight with a 20-second blind that ends the target's combat.
Shadow|Eclipse|Sneaking speed +15%.
Steed|Unicorn|Spell and enchantment costs -25% while an Inborn Magic effect is active.
Tower|Cellar|Inborn Magic activation also gives 10 seconds of invisibility.`,
 'Imperial':`Mage|Wisdom of Saints|Magicka regeneration +50%.
Thief|Cunning of Saints|Stamina regeneration +50%.
Warrior|Strength of Saints|Health regeneration +50%.
Apprentice|Dedication|All skill experience +8%.
Atronach|Faith|Healing spells/effects +20% effectiveness.
Lady|Zeal|Attack and critical damage +20% when fighting multiple opponents.
Lord|Ardor|Incoming attack damage -15% when fighting multiple opponents.
Lover|Fidelity|Bribe duration doubles.
Ritual|Devotion|Bribed targets follow you; Bribe lasts five times as long, but only one person can be bribed at once.
Serpent|Prosperity|Imperial Gold gets an 8% rare-item chance, including enchanted items.
Shadow|Diplomacy|Bribe also gives +25% pickpocket chance and sneak-attack damage.
Steed|Vigor|Allies within 25 feet move 20% faster, including your horse.
Tower|Fervor|Allies within 25 feet gain 20% attack damage.`,
 'Khajiit':`Mage|Glimmering Gold|Spell costs decrease 5% per digit in carried gold, capped at 50%.
Thief|Lucky Coin|Detection becomes 5% harder per digit in carried gold, capped at 50%.
Warrior|Bulging Pockets|Incoming power-attack damage drops 5% per digit in carried gold, capped at 50%.
Apprentice|Agility|Additional movement speed +10%.
Atronach|At the Crossroads|Choose a 1K, 10K or 100K gold loan; losing this stone without carrying repayment plus 10% interest kills you. You may decline the stone.
Lady|Moondew|Consumed potions and ingredients +20% effectiveness.
Lord|Knead|Enables single-claw power attacks while sneaking; claw damage +10.
Lover|Purr|A nearby ally and you gain +50% Magicka/Stamina regeneration while close together.
Ritual|Lunar Rush|Jump to cancel attacks/spellcasts; incoming attack damage -15% while jumping.
Serpent|Shiny Distraction|Activate a humanoid foe and pay 40 gold per level to take all their Magicka and Stamina.
Shadow|Prowl|Sneaking speed +10% and detection is 40% harder, but sneaking drains 10 Magicka/second.
Steed|Lunar Sprint|Enter sneak while sprinting; sneaking speed +15%, with detection 30% easier.
Tower|Whiskers|Humanoid kills have 30% chance for extra gold and 10% chance for small valuables.`,
 'Nord':`Mage|Owl's Insight|Rage drains Stamina instead of Magicka.
Thief|Wolf's Hunger|Sneak attacks heal you according to the opponent's level.
Warrior|Bear's Strength|Additional armor +100.
Apprentice|Elder of Runes|Move half your base Stamina regeneration to Magicka regeneration.
Atronach|Shamanic Trance|Use an All-Maker power during Rage, then maintain Rage another 8 seconds to recover that power.
Lady|Dream Journey|Sleeping gives a random All-Maker Stone power when you do not already hold one.
Lord|Atmoran Heritage|Additional Frost Resist +50%.
Lover|Moth's Grace|During Rage, resist stagger from power attacks and bashes entirely.
Ritual|Hakkerskaldyr|Shouts during Rage have 50% chance of a 3-second cooldown.
Serpent|Fox's Cunning|Damage +25% against targets drawing bows, casting spells or power attacking.
Shadow|Blackbraid|During Rage, detection is 40% harder.
Steed|Rockslide|During Rage, movement speed +15%.
Tower|Frith|Rage restores Health equal to half its drained Magicka.`,
 'Orc':`Mage|Warlockstomp|Warstomp also causes 50% magic weakness for 10 seconds.
Thief|Pillage|Humanoid kills have a 5% rare-item chance, including enchanted gear.
Warrior|Orc Smash|Power-attack and critical damage +20%.
Apprentice|Berserk|At-will power, 100 Magicka: double attack/critical damage and halve incoming attack damage for 10 seconds.
Atronach|Bloodhowl|Falling below 25% Health triggers 10-second Berserk; 30-second cooldown.
Lady|Carnage|Kills have 15% chance of a 10-second Berserk; 30-second cooldown.
Lord|Warlordstomp|Warstomp also removes 500 armor for 10 seconds.
Lover|Bloodthirst|Kills heal you for 25% of the target's negative Health (overkill).
Ritual|Bloodrite|Combat attack/critical damage +25%, but you start each battle missing 50% Health.
Serpent|Shock Trooper|Additional Shock Resist +50%.
Shadow|Stampede|Combat movement speed +10%.
Steed|Warthogstomp|Warstomp adds damage equal to 20% of the target's current Health.
Tower|Tower Dive|Warstomp prevents falling damage.`,
 'Redguard':`Mage|Mummy's Touch|Spells and scrolls are 20% stronger on targets in melee range.
Thief|Shamshir|Shehai hits have 15% chance of briefly disarming.
Warrior|Coyote|Attack and critical damage +25% while considered stronger than the opponent.
Apprentice|Contemplation|Out of combat, recover an extra 5% maximum Magicka/second.
Atronach|Adrenaline Rush|Replaces Shehai with +15% movement speed and recovery of 5% maximum Stamina/second; retains Shehai's duration.
Lady|Conditioning|Disease resistance +50%.
Lord|Ibex|Incoming attack damage -20% while considered stronger than the opponent.
Lover|Shahrazad|Replaces Shehai with a spellcasting spirit; power scales with attributes and duration matches Shehai.
Ritual|Dust Storm|Power attacks, bashes and sneak attacks have 20% chance to knock down.
Serpent|Black Obelisk|While considered stronger, poisons nearby living foes each second for 20% of your Alteration level.
Shadow|Jinniya of the Lamp|One wish each 1,001 minutes: choose wealth/items, attributes, perks or dragon souls. Countdown appears in Active Effects.
Steed|Endurance|Sprinting costs an additional 2 less Stamina/second.
Tower|Starlit Shores|Once per day, spend 50 Magicka outdoors in Skyrim to teleport to a random world location.`,
 'Wood Elf':`Mage|Wicker Man|Harrier adds 25% weakness to fire, frost and shock.
Thief|Bushman|Targets observed with Wild Senses have 50% more difficulty detecting you.
Warrior|Thunderbird|Harrier has 50% chance to launch combat targets into the air.
Apprentice|Wanderer|Outdoors, Magicka/Stamina regeneration +50%.
Atronach|Firewatch|A Wild Senses target entering combat within 10 seconds loses 25% Health.
Lady|Skyclad|Harrier has 33% chance to remove a humanoid combat target's armor.
Lord|Green Pact|Consume a dead humanoid marked by Harrier during combat; all attributes rise by its level for 15 minutes.
Lover|Magpie|Harrier finds two rare items instead, including enchanted loot.
Ritual|Apex Predator|Harrier may select people as hunt targets.
Serpent|Green Man|Additional Disease Resist +50%.
Shadow|Hunter's Eye|Wild Senses study removes 500 armor for 10 seconds; lingers after leaving Wild Senses.
Steed|Forestwalk|Outdoor movement speed +10%.
Tower|Aerie|When Harrier is neither hunting nor fighting, its company restores 4% maximum Health/second.`};
 const raceNotes={
 'Argonian':'Mannaz reference: Amphibious grants water breathing, +50% swimming speed and enhanced underwater/rain healing. Caustic Spit costs 75 Magicka, reducing armor by 200 and magic resistance by 25% for 20 seconds. Omnivore adds 25% disease/poison resistance.',
 'Breton':'Mannaz reference: Dragonskin grants 10% magic resistance. Questing Culture concerns three lost cultural artifacts, not automatic free bonuses. Stones of Galen supplies the second stone effect below. Freyr replaces the generic Mannaz stone bonuses; do not stack the vanilla or Imperious list on top.',
 'Dark Elf':'Mannaz reference: Ashborn gives 25% fire resistance. Ancestral Protector automatically intervenes once per day against a lethal blow. Fireblood stores fire from fire attacks or forges, granting 25% fire resistance until expended against a foe.',
 'High Elf':'Mannaz reference: Faerielight can dispel and drain an opponent once per battle. Inborn Magic configures a conditional effect once per day; the configured effect can trigger repeatedly. Shimmering improves enchantments by 15%.',
 'Imperial':'Mannaz reference: Discipline improves armor/shields by 10%. Imperial Gold adds valuables and allows humanoid bribes at 40 gold per level; bribed foes fight for you for 60 seconds. Star of the West adds two perk points.',
 'Khajiit':'Mannaz reference: Night Eye lasts 60 seconds. Sandwalkers expands caravan stock. Two-Moons-Dance adds 20% speed, reduces fall damage by 75% and adds 10 claw damage. Read the Atronach repayment warning before selecting it.',
 'Nord':'Mannaz reference: Glacier gives 25% frost resistance. Rage toggles +25% attacks/criticals/spells while draining Magicka. Roots grants additional passives from Solstheim All-Maker Stones. Those are a different system from the thirteen Freyr stones.',
 'Orc':'Mannaz reference: Stormrunner gives 25% shock resistance; Stronghold Supplies expands Orc smith stock. Warstomp costs 100 Magicka and is activated in midair to stagger on landing with reduced falling damage.',
 'Redguard':'Mannaz reference: Endurance gives +75 armor. Nomadic Heritage gives +30% sprint speed and reduces sprint cost by 5 Stamina/second. Shehai costs 75 Magicka and scales with current attributes. Freyr stronger-than checks consider enemy count, levels and current Health, not level alone.',
 'Wood Elf':'Mannaz reference: Harrier marks hunts or combat targets and reduces armor/magic resistance. Resilient grants 25% disease/poison resistance. Wild Senses detects targets after sneaking still with hands lowered for 4 seconds.'};
 const raceCaveats={
 'Breton':'Both effects are part of one selected stone. Ritual and Serpent have real resource penalties. Dead Noon multiplies critical damage, not total weapon damage. The author notes the Lord pair counteracts itself; exact installed damage calculation is not certified.',
 'High Elf':'Faerielight replacements remove the original effect. The author says an Aetherial Crown can preserve two replacements; this site does not assume the final Artificer/crown interaction has been tested.',
 'Orc':'Multiple Berserk sources do not stack, according to the Freyr author.',
 'Nord':'No automatic vanilla All-Maker bonuses or unrelated Audugan changes are added here.',
 'Redguard':'Adrenaline Rush and Shahrazad replace rather than add a second ordinary Shehai. Conditional strength checks are not a simple character-level comparison.'};
 const effects={};for(const [race,lines]of Object.entries(blocks)){effects[race]={};for(const line of lines.split('\n')){const [stone,name,text,extraName,extraText]=line.split('|');effects[race][stone]={name,text,...(extraName?{extra:{name:extraName,text:extraText}}:{})};}}
 const hints={Mage:'One of the three Guardian Stones, southwest of Riverwood.',Thief:'One of the three Guardian Stones, southwest of Riverwood.',Warrior:'One of the three Guardian Stones, southwest of Riverwood.',Apprentice:'Marshes near Morthal; use the existing named-stone reference.',Atronach:'Eastmarch hot-spring region; use the named-stone reference.',Lady:'Lake Ilinalta island; use the named-stone reference.',Lord:'Mountain east of Morthal; use the named-stone reference.',Lover:'Reach region near Markarth; use the named-stone reference.',Ritual:'East of Whiterun; use the named-stone reference.',Serpent:'Island east of Winterhold; use the named-stone reference.',Shadow:'South of Riften; use the named-stone reference.',Steed:'Northwest of Solitude; use the named-stone reference.',Tower:'Coast between Dawnstar and Winterhold; use the named-stone reference.'};
 const stones=order.map(name=>({id:name.toLowerCase(),name:name+' Stone',key:name,world:'skyrim',mapPlace:['Mage','Thief','Warrior'].includes(name)?'The Guardian Stones':'The '+name+' Stone',directions:hints[name],source,precision:['Mage','Thief','Warrior'].includes(name)?'shared-site':'site'}));
 return{version:1,source,raceSource,races:Object.keys(blocks),stones,effects,raceNotes,raceCaveats,notes:['Recorded PS5 ports: Mannaz #28 v1.00 and Freyr #29 v1.00. These menu versions do not establish their underlying PC versions.','Mechanics displayed are author-reference Freyr 1.2.0 and Mannaz 3.0.1, checked 18 September 2026; PS5 parity and winning overrides remain untested.','Freyr REPLACES the normal standing-stone effects with race-specific effects. Do not add vanilla, Andromeda or Imperious bonuses to this list.','Bretons get two effects per stone through Stones of Galen. Both are shown separately; this is not a blanket percentage multiplier.','The thirteen Skyrim standing stones and Solstheim All-Maker Stones are separate. The latter have additional Nord/All-Maker worship interactions, not a second Freyr race table.']};
})();
