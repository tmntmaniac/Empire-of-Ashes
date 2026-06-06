"""
Idempotent: appends Knight Household and Legio Titanicus factions to
backend/data/factions.json. Re-running replaces existing entries by id.

Source: /app/pdf_work/eoa.txt — Empire of Ashes, pp. 36–40, 59–61.
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "factions.json"

COMP_LIMITS_2_3 = {"maxSupportPerLine": 2, "maxUpgradesPerLine": 3, "lowPct": 0.33}
COMP_RULES_2_3 = [
    "Max 2 Support detachments per Line detachment in the army.",
    "Max 3 Upgrades per formation.",
    "Max 1/3 of total points value may be spent on Lords of War or Allies.",
]


# =====================================================================
# KNIGHT HOUSEHOLD
# =====================================================================
knight_household = {
    "id": "knight-household",
    "name": "Knight Households",
    "subtitle": "Noble Lances · Houses of Adamantium",
    "color": "#7A2E2E",
    "lore": (
        "Hereditary noble lineages whose pilots bond with towering Knight "
        "engines forged in the Martian temples. Lesser than Titans but far "
        "more responsive, the Knights of House Devine, House Vyronii and a "
        "hundred others ride to war in resplendent heraldry — and the fires "
        "of the Heresy will see those ancient names raised in glory or "
        "ground to dust."
    ),
    "legionTrait": {
        "name": "Noble Lances",
        "description": (
            "Strategy Rating 3 · Initiative 2+. Formations gain +1 to Engage "
            "Action tests and +1 to Rally tests. 2 Support per Line, max 3 "
            "Upgrades per formation. Optional Household Trait: Second Greatest "
            "Predator — +1 to hit in assault vs AV character units; force "
            "enemy critical-hit rerolls."
        ),
    },
    "compositionLimits": COMP_LIMITS_2_3,
    "compositionRules": COMP_RULES_2_3 + [
        "Strategy Rating 3, Initiative 2+; +1 to Engage actions and Rally tests.",
        "Special Rules: Ion Gauntlet and Ion Shield (4+ saves vs shooting/Firefight, vs CC for Gauntlet).",
        "Cerastus Lance and Grand Quesetorius Lance: 1 per 2,000 pts each.",
        "Optional Household Trait: Second Greatest Predator.",
    ],
    "allies": {
        "cohesive": ["Imperialis Militia", "Mechanicum Taghmata", "Solar Auxilia"],
        "disruptive": [
            "Daemons of the Ruinstorm (Traitor only)",
            "Legiones Astartes",
            "Legio Custodes (Loyalist only)",
            "Legio Titanicus",
        ],
    },
    "formations": [
        # ----- Line -----
        {
            "id": "quesetorius-lance",
            "name": "Quesetorius Lance",
            "category": "Line",
            "baseCost": 325,
            "composition": "3 Quesetorius Knights (+100 each, up to 5)",
            "unitOptions": [
                {"label": "3 Quesetorius Knights",
                 "units": [{"unit": "quesetorius-knight", "count": 3}]}
            ],
            "extraUnit": {"unit": "quesetorius-knight", "cost": 100, "max": 2,
                          "label": "Additional Quesetorius Knight"},
            "allowedUpgrades": ["aspirants", "noble", "noble-senechal", "exalted-armoury"],
        },
        {
            "id": "mechanicum-lance",
            "name": "Mechanicum Lance",
            "category": "Line",
            "baseCost": 325,
            "composition": "3 Mechanicum House Knights",
            "unitOptions": [
                {"label": "3 Mechanicum House Knights",
                 "units": [{"unit": "mechanicum-house-knight", "count": 3}]}
            ],
            "allowedUpgrades": ["noble", "noble-senechal", "enhanced-forges", "martian-support"],
        },

        # ----- Support -----
        {
            "id": "armiger-lance",
            "name": "Armiger Lance",
            "category": "Support",
            "baseCost": 200,
            "composition": "5 Helverins, Warglaives OR Moirax",
            "unitOptions": [
                {"label": "5 Helverins", "units": [{"unit": "helverin", "count": 5}]},
                {"label": "5 Warglaives", "units": [{"unit": "warglaive", "count": 5}]},
                {"label": "5 Moirax", "units": [{"unit": "moirax", "count": 5}]},
            ],
            "allowedUpgrades": ["aspirants", "noble", "noble-senechal"],
        },
        {
            "id": "cerastus-lance",
            "name": "Cerastus Lance",
            "category": "Support",
            "baseCost": 375,
            "composition": "3 Lancers OR Castigators (+125 each, up to 5; 1 per 2,000 pts)",
            "unitOptions": [
                {"label": "3 Lancers", "units": [{"unit": "lancer", "count": 3}]},
                {"label": "3 Castigators", "units": [{"unit": "castigator", "count": 3}]},
            ],
            "extraUnit": {"unit": "lancer", "cost": 125, "max": 2,
                          "label": "Additional Lancer/Castigator"},
            "allowedUpgrades": ["noble", "noble-senechal", "enhanced-forges"],
        },
        {
            "id": "dominus-lance",
            "name": "Dominus Lance",
            "category": "Support",
            "baseCost": 425,
            "composition": "3 Castellan",
            "unitOptions": [
                {"label": "3 Castellan", "units": [{"unit": "castellan", "count": 3}]}
            ],
            "allowedUpgrades": ["noble", "noble-senechal", "martian-support"],
        },
        {
            "id": "grand-quesetorius-lance",
            "name": "Grand Quesetorius Lance",
            "category": "Support",
            "baseCost": 375,
            "composition": "3 Quesetorius Grand Knights (+125 each, up to 4; 1 per 2,000 pts)",
            "unitOptions": [
                {"label": "3 Quesetorius Grand Knights",
                 "units": [{"unit": "quesetorius-grand-knight", "count": 3}]}
            ],
            "extraUnit": {"unit": "quesetorius-grand-knight", "cost": 125, "max": 1,
                          "label": "Additional Quesetorius Grand Knight"},
            "allowedUpgrades": ["noble", "noble-senechal", "enhanced-forges", "exalted-armoury"],
        },

        # ----- Lords of War -----
        {
            "id": "acastus-porphyrion",
            "name": "Acastus Knight Porphyrion",
            "category": "Lords of War",
            "baseCost": 250,
            "composition": "1 Acastus Knight Porphyrion (+250 for 2nd)",
            "unitOptions": [
                {"label": "1 Acastus Porphyrion",
                 "units": [{"unit": "porphyrion", "count": 1}]}
            ],
            "extraUnit": {"unit": "porphyrion", "cost": 250, "max": 1,
                          "label": "Additional Acastus Porphyrion"},
            "allowedUpgrades": ["noble", "noble-senechal", "martian-support"],
        },
    ],
    "upgrades": [
        {"id": "aspirants", "name": "Aspirants", "type": "flag", "cost": -50,
         "description": "Formation suffers -1 to Advance, Overwatch, March, Marshall, "
                        "and Sustained Fire action rolls (reduces cost)."},
        {"id": "enhanced-forges", "name": "Enhanced Forges", "type": "flag", "cost": 25,
         "description": "Upgrade any Knight in the formation to an Acheron or Atropos (Cerastus variant)."},
        {"id": "exalted-armoury", "name": "Exalted Armoury", "type": "flag", "cost": 25,
         "description": "Upgrade 1-2 Knights to a Quesetorius Grand Knight or Mechanicum House Knight."},
        {"id": "martian-support", "name": "Martian Support", "type": "multi", "max": 5,
         "description": "Add 1-2 Mechanicum House Knights and/or 1-3 Armiger Moirax.",
         "variants": [
             {"id": "mechanicum-house-knight", "name": "Mechanicum House Knight", "cost": 100},
             {"id": "moirax", "name": "Armiger Moirax", "cost": 50},
         ]},
        {"id": "noble", "name": "Noble", "type": "single", "cost": 25,
         "description": "Add 1 Lord Scion OR Preceptor character.",
         "variants": [
             {"id": "lord-scion", "name": "Lord Scion", "cost": 25},
             {"id": "preceptor", "name": "Preceptor", "cost": 25},
         ]},
        {"id": "noble-senechal", "name": "Noble: Senechal", "type": "flag", "cost": 50,
         "description": "Upgrade one Lord Scion in the formation to a Senechal (max 1 per force). Requires Noble upgrade.",
         "addedUnits": [{"unit": "senechal", "count": 1}]},
    ],
    "units": {
        # Characters
        "lord-scion": {
            "name": "Lord Scion", "type": "CH",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [{"name": "Master Knight Commander", "range": "(base)",
                         "firepower": "(assault) EA (+1)"}],
            "notes": ["Leader."],
        },
        "senechal": {
            "name": "Senechal", "type": "CH",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [{"name": "Master Knight Commander", "range": "(base)",
                         "firepower": "(assault) EA (+1)"}],
            "notes": ["Invulnerable save.", "Supreme Commander."],
        },
        "preceptor": {
            "name": "Preceptor", "type": "CH",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [],
            "notes": ["Commander.", "Leader."],
        },

        # Armigers (LV)
        "helverin": {
            "name": "Armiger Helverin", "type": "LV",
            "speed": "30cm", "armour": "5+", "cc": "5+", "ff": "4+",
            "weapons": [{"name": "Armiger Autocannons", "range": "45cm",
                         "firepower": "2× AP3+/AT5+"}],
            "notes": ["Ion shield (5+).", "Scout.", "Walker."],
        },
        "moirax": {
            "name": "Armiger Moirax", "type": "LV",
            "speed": "30cm", "armour": "5+", "cc": "4+", "ff": "4+",
            "weapons": [
                {"name": "Siege Claw", "range": "(base)",
                 "firepower": "(assault) Siege, EA (+1)"},
                {"name": "Volkite Veuglaire", "range": "15cm",
                 "firepower": "2× AP4+/AT6+, Disrupt, Ignore cover"},
            ],
            "notes": ["Ion shield (5+).", "Walker."],
        },
        "warglaive": {
            "name": "Armiger Warglaive", "type": "LV",
            "speed": "30cm", "armour": "5+", "cc": "4+", "ff": "4+",
            "weapons": [
                {"name": "Reaper Chain-cleaver", "range": "(base)",
                 "firepower": "(assault) MW, EA (+1)"},
                {"name": "Thermal Spear", "range": "15cm & (15cm)",
                 "firepower": "AP4+/AT4+, MW / (small arms) MW"},
            ],
            "notes": ["Ion shield (5+).", "Scout.", "Walker."],
        },

        # Questoris Knights (WE)
        "quesetorius-knight": {
            "name": "Quesetorius Knight (Errant / Paladin)", "type": "WE",
            "speed": "25cm", "armour": "5+", "cc": "4+", "ff": "4+ (3+)",
            "weapons": [
                {"name": "Knight Battlecannon", "range": "75cm",
                 "firepower": "AP4+/AT4+"},
                {"name": "Avenger Gatling Cannon", "range": "30cm & (15cm)",
                 "firepower": "2× AP3+/AT5+ / (small arms) EA (+1)"},
                {"name": "Thermal Cannon", "range": "30cm & (15cm)",
                 "firepower": "AP4+/AT4+, MW / (small arms) MW"},
                {"name": "Reaper Chainsword", "range": "(base)",
                 "firepower": "(assault) MW, EA (+1)"},
                {"name": "Thunderstrike Gauntlet", "range": "(base)",
                 "firepower": "(assault) TK, EA (+1)"},
            ],
            "notes": ["DC2.", "Ion shield.", "Reinforced armour.", "Walker.",
                      "Must select 2 arm weapons from the weapons list."],
        },
        "quesetorius-grand-knight": {
            "name": "Quesetorius Grand Knight (Crusader / Gallant / Warden)", "type": "WE",
            "speed": "25cm", "armour": "5+", "cc": "4+", "ff": "4+ (3+)",
            "weapons": [
                {"name": "Avenger Cannon", "range": "30cm & (15cm)",
                 "firepower": "2× AP3+/AT5+ / (small arms) EA (+1)"},
                {"name": "Knight Battlecannon", "range": "75cm",
                 "firepower": "AP4+/AT4+"},
                {"name": "Thermal Cannon", "range": "30cm & (15cm)",
                 "firepower": "AP4+/AT4+, MW / (small arms) MW"},
                {"name": "Reaper Chainsword", "range": "(base)",
                 "firepower": "(assault) MW, EA (+1)"},
                {"name": "Thunderstrike Gauntlet", "range": "(base)",
                 "firepower": "(assault) TK, EA (+1)"},
                {"name": "Icarus Battery (+15)", "range": "45cm",
                 "firepower": "AP4+/AT5+/AA5+"},
                {"name": "Ironstorm Missile Pod (+20)", "range": "60cm",
                 "firepower": "1 BP, Indirect fire"},
                {"name": "Stormspear Missile Pod (+free)", "range": "45cm",
                 "firepower": "2× AT5+"},
            ],
            "notes": ["DC2.", "Ion shield.", "Reinforced armour.", "Walker.",
                      "Select 2 arm weapons + 1 carapace weapon."],
        },
        "mechanicum-house-knight": {
            "name": "Mechanicum House Knight (Magaera / Stryix)", "type": "WE",
            "speed": "20cm", "armour": "4+", "cc": "3+", "ff": "4+",
            "weapons": [
                {"name": "Volkite Chieorovile OR", "range": "45cm",
                 "firepower": "2× AP3+/AT6+, Disrupt"},
                {"name": "Lightning Cannon", "range": "45cm & (15cm)",
                 "firepower": "AP5+/AT5+, MW / (small arms) MW"},
                {"name": "TL Rad Cleanser", "range": "15cm",
                 "firepower": "AP3+, Ignore cover"},
                {"name": "Hekaton Siege Claw", "range": "(base)",
                 "firepower": "(assault) EA (+1), Siege"},
            ],
            "notes": ["DC2.", "Ion shield.", "Cortex controller.",
                      "Reinforced armour.", "Walker."],
        },

        # Cerastus Knights (WE)
        "acheron": {
            "name": "Cerastus Knight-Acheron", "type": "WE",
            "speed": "30cm", "armour": "5+", "cc": "4+", "ff": "4+",
            "weapons": [
                {"name": "Flame Cannon", "range": "30cm & (15cm)",
                 "firepower": "2× AP3+/AT6+, Ignore cover / (small arms) EA (+1), Ignore cover"},
                {"name": "TL Heavy Bolter", "range": "30cm", "firepower": "AP4+"},
                {"name": "Destroyer Chainfist", "range": "(base)",
                 "firepower": "(assault) TK, EA (+1)"},
            ],
            "notes": ["DC2.", "Ion shield.", "Reinforced armour.", "Walker."],
        },
        "atropos": {
            "name": "Cerastus Knight-Atropos", "type": "WE",
            "speed": "30cm", "armour": "5+", "cc": "4+", "ff": "4+",
            "weapons": [
                {"name": "Atropos Lascutter", "range": "(15cm) & (base)",
                 "firepower": "(small arms) MW, EA (+1) / (assault) MW, EA (+1)"},
                {"name": "Graviton Singularity Cannon", "range": "30cm",
                 "firepower": "2× AP5+/AT4+, Lance, Singularity"},
            ],
            "notes": ["DC2.", "Ion shield.", "Reinforced armour.", "Walker."],
        },
        "castigator": {
            "name": "Cerastus Knight-Castigator", "type": "WE",
            "speed": "30cm", "armour": "5+", "cc": "4+", "ff": "4+",
            "weapons": [
                {"name": "Castigator Bolt Cannon", "range": "45cm & (15cm)",
                 "firepower": "2× AP3+/AT5+ / (small arms) EA (+1)"},
                {"name": "Tempest Warblade", "range": "(base)",
                 "firepower": "(assault) MW, EA (+2)"},
            ],
            "notes": ["DC2.", "Ion shield.", "Reinforced armour.", "Walker."],
        },
        "lancer": {
            "name": "Cerastus Knight-Lancer", "type": "WE",
            "speed": "30cm", "armour": "5+", "cc": "4+", "ff": "5+",
            "weapons": [
                {"name": "Cerastus Shock Lance", "range": "(base)",
                 "firepower": "(assault) TK (1), EA (+1), First strike"},
                {"name": "Shock Blast", "range": "15cm",
                 "firepower": "AP4+/AT5+, Disrupt"},
            ],
            "notes": ["DC2.", "Ion gauntlet.", "Reinforced armour.", "Walker."],
        },

        # Acastus and Dominus (WE)
        "porphyrion": {
            "name": "Acastus Knight-Porphyrion", "type": "WE",
            "speed": "15cm", "armour": "4+", "cc": "6+", "ff": "4+",
            "weapons": [
                {"name": "Magna Lascannons", "range": "60cm",
                 "firepower": "3× AT3+, Lance"},
                {"name": "Lascannon", "range": "45cm", "firepower": "AT5+"},
                {"name": "Autocannon", "range": "45cm", "firepower": "AP5+/AT6+"},
                {"name": "Ironstorm Missile Pod", "range": "45cm",
                 "firepower": "3 BP / AA5+"},
            ],
            "notes": ["DC3.", "Ion shield.", "Reinforced armour.", "Walker.",
                      "Critical Hit: Destroyed."],
        },
        "castellan": {
            "name": "Dominus Castellan", "type": "WE",
            "speed": "15cm", "armour": "4+", "cc": "4+", "ff": "4+",
            "weapons": [
                {"name": "Plasma Decimator", "range": "30cm",
                 "firepower": "AP3+/AT4+, MW, Slow firing"},
                {"name": "Volcano Lance", "range": "45cm",
                 "firepower": "AT4+, TK (1)"},
                {"name": "TL Siegebreaker Cannon", "range": "15cm & (15cm)",
                 "firepower": "AP5+/AT5+ / (small arms) EA (+1)"},
                {"name": "Shieldbreaker Missiles", "range": "45cm",
                 "firepower": "AT4+, Single shot"},
            ],
            "notes": ["DC2.", "Ion shield.", "Reinforced armour.", "Walker.",
                      "Shieldbreaker missiles ignore Invulnerable saves and Void shields."],
        },
    },
}


# =====================================================================
# LEGIO TITANICUS
# =====================================================================
# Scout Titan Weapons + Battle Titan Weapons modelled as combined "Titan
# Weapons" upgrade with the variants list flagged (cost 0 for default
# choices, +25/+50/+75 for the upcharged options). Each formation's
# "Scout Weapons" or "Scout or Battle Weapons" rule is enforced via a
# distinct upgrade id with the correct `max` value.
SCOUT_WEAPONS = [
    {"id": "wpn-inferno-gun", "name": "Inferno Gun", "cost": 0},
    {"id": "wpn-plasma-blastgun", "name": "Plasma Blastgun", "cost": 0},
    {"id": "wpn-swarmer-missiles", "name": "Swarmer Missile System", "cost": 0},
    {"id": "wpn-ursus-claw", "name": "Ursus Claw", "cost": 0},
    {"id": "wpn-vulcan-megabolter", "name": "Vulcan Megabolter", "cost": 0},
    {"id": "wpn-melta-lance", "name": "Melta Lance", "cost": 25},
    {"id": "wpn-turbolaser-destructor", "name": "Turbolaser Destructor", "cost": 25},
]
BATTLE_WEAPONS = [
    {"id": "wpn-laser-burner", "name": "Laser Burner", "cost": 0},
    {"id": "wpn-corvus-pod", "name": "Corvus Assault Pod", "cost": 0},
    {"id": "wpn-carapace-landing-pad", "name": "Carapace Landing Pad", "cost": 0},
    {"id": "wpn-plasma-cannon", "name": "Plasma Cannon", "cost": 25},
    {"id": "wpn-gatling-blaster", "name": "Gatling Blaster", "cost": 25},
    {"id": "wpn-apocalypse-missile", "name": "Apocalypse Missile Launcher", "cost": 25},
    {"id": "wpn-close-combat", "name": "Close Combat Weapon", "cost": 25},
    {"id": "wpn-melta-cannon", "name": "Melta Cannon", "cost": 50},
    {"id": "wpn-laser-blaster", "name": "Laser Blaster", "cost": 50},
    {"id": "wpn-volcano-cannon", "name": "Volcano Cannon", "cost": 50},
    {"id": "wpn-plasma-destructor", "name": "Plasma Destructor", "cost": 75},
    {"id": "wpn-support-missile", "name": "Support Missile", "cost": 75},
    {"id": "wpn-quake-cannon", "name": "Quake Cannon", "cost": 75},
]


def titan_weapon_upgrade(uid, name, max_slots, allow_battle):
    variants = SCOUT_WEAPONS + (BATTLE_WEAPONS if allow_battle else [])
    label = "Scout or Battle Titan Weapons" if allow_battle else "Scout Titan Weapons"
    return {
        "id": uid,
        "name": name,
        "type": "multi",
        "max": max_slots,
        "conversion": True,  # weapon slot picks — not roster additions
        "description": f"Select up to {max_slots} {label}. Free variants are cost 0; "
                       "premium variants add +25 / +50 / +75 as marked.",
        "variants": variants,
    }


legio_titanicus = {
    "id": "legio-titanicus",
    "name": "Legio Titanicus",
    "subtitle": "Colleagia Titanica · The God-Machines",
    "color": "#4A6F8E",
    "lore": (
        "The towering colossi of Mars — Warhounds, Reavers, Warlords and "
        "their immortal cousins. Pilots called Princeps meld their minds with "
        "the machine spirits of their Titans, walking fortresses whose tread "
        "shakes continents. The Heresy will see Legio set against Legio and "
        "the gods of battle pitted against one another."
    ),
    "legionTrait": {
        "name": "Engines of the Omnissiah",
        "description": (
            "Strategy Rating 3 · Initiative 1+. 2 Support per Line; max 3 "
            "Upgrades per formation. Special rules: Void Shields. Optional "
            "Legio Trait: Heart of Steel (reroll critical-hit damage results) "
            "OR Warhorn (15cm AOE Blast markers on a 5+)."
        ),
    },
    "compositionLimits": COMP_LIMITS_2_3,
    "compositionRules": COMP_RULES_2_3 + [
        "Strategy Rating 3, Initiative 1+.",
        "Special Rules: Void Shields (each shield stops 1 hit, repairs 1 per end phase).",
        "Warhound Scout, Direwolf and Warbringer Support: 1 per 2,000 pts each.",
        "Emperor Titan Lord of War: 1 per 7,500 pts.",
        "Psi-Titan: Loyalist forces only.",
        "Optional Legio Traits: Heart of Steel OR Warhorn.",
    ],
    "allies": {
        "cohesive": ["Legiones Astartes", "Knight Households", "Mechanicum Taghmata"],
        "disruptive": [
            "Daemons of the Ruinstorm (Traitor only)",
            "Imperialis Militia",
            "Legio Custodes (Loyalist only)",
            "Solar Auxilia",
        ],
    },
    "formations": [
        # ----- Line -----
        {
            "id": "warhound-hunting-pack",
            "name": "Warhound Hunting Pack",
            "category": "Line",
            "baseCost": 500,
            "composition": "2 Warhound Scout Titans",
            "unitOptions": [
                {"label": "2 Warhound Scout Titans",
                 "units": [{"unit": "warhound-scout-titan", "count": 2}]}
            ],
            "allowedUpgrades": ["veteran-princepts", "vp-legate",
                                "titan-weapons-scout-4"],
        },
        {
            "id": "reaver-titan",
            "name": "Reaver Titan",
            "category": "Line",
            "baseCost": 575,
            "composition": "1 Reaver Battle Titan",
            "unitOptions": [
                {"label": "1 Reaver Battle Titan",
                 "units": [{"unit": "reaver-battle-titan", "count": 1}]}
            ],
            "allowedUpgrades": ["veteran-princepts", "vp-legate",
                                "titan-weapons-mixed-3",
                                "air-defence", "sacred-icon"],
        },
        {
            "id": "warlord-titan",
            "name": "Warlord Titan",
            "category": "Line",
            "baseCost": 725,
            "composition": "1 Warlord Battle Titan",
            "unitOptions": [
                {"label": "1 Warlord Battle Titan",
                 "units": [{"unit": "warlord-battle-titan", "count": 1}]}
            ],
            "allowedUpgrades": ["veteran-princepts", "vp-legate",
                                "titan-weapons-mixed-4",
                                "air-defence", "sacred-icon"],
        },

        # ----- Support -----
        {
            "id": "warhound-scout",
            "name": "Warhound Scout",
            "category": "Support",
            "baseCost": 275,
            "composition": "1 Warhound Scout Titan (1 per 2,000 pts)",
            "unitOptions": [
                {"label": "1 Warhound Scout Titan",
                 "units": [{"unit": "warhound-scout-titan", "count": 1}]}
            ],
            "allowedUpgrades": ["veteran-princepts", "vp-legate",
                                "titan-weapons-scout-2"],
        },
        {
            "id": "direwolf-heavy-scout",
            "name": "Direwolf Heavy Scout Titan",
            "category": "Support",
            "baseCost": 325,
            "composition": "1 Direwolf Heavy Scout Titan (1 per 2,000 pts)",
            "unitOptions": [
                {"label": "1 Direwolf Heavy Scout Titan",
                 "units": [{"unit": "direwolf-heavy-scout-titan", "count": 1}]}
            ],
            "allowedUpgrades": ["veteran-princepts", "vp-legate",
                                "titan-weapons-mixed-1", "sacred-icon"],
        },
        {
            "id": "warbringer-titan",
            "name": "Warbringer Titan",
            "category": "Support",
            "baseCost": 700,
            "composition": "1 Warbringer Nemesis Titan",
            "unitOptions": [
                {"label": "1 Warbringer Nemesis Titan",
                 "units": [{"unit": "warbringer-nemesis-titan", "count": 1}]}
            ],
            "allowedUpgrades": ["veteran-princepts", "vp-legate",
                                "titan-weapons-mixed-2", "sacred-icon"],
        },

        # ----- Lords of War -----
        {
            "id": "emperor-titan",
            "name": "Emperor Titan",
            "category": "Lords of War",
            "baseCost": 1350,
            "composition": "1 Emperor Titan (1 per 7,500 pts)",
            "unitOptions": [
                {"label": "1 Emperor Titan",
                 "units": [{"unit": "emperor-titan", "count": 1}]}
            ],
            "allowedUpgrades": ["veteran-princepts", "vp-legate",
                                "titan-weapons-mixed-2",
                                "air-defence", "sacred-icon"],
        },
        {
            "id": "psi-titan",
            "name": "Psi-Titan (Loyalist Only)",
            "category": "Lords of War",
            "baseCost": 875,
            "composition": "1 Warlord-Sinister Psi-Titan",
            "unitOptions": [
                {"label": "1 Warlord-Sinister",
                 "units": [{"unit": "warlord-sinister", "count": 1}]}
            ],
            "allowedUpgrades": ["veteran-princepts", "vp-legate",
                                "titan-weapons-mixed-3",
                                "air-defence", "sacred-icon"],
        },
        {
            "id": "warmaster-titan",
            "name": "Warmaster Titan",
            "category": "Lords of War",
            "baseCost": 1175,
            "composition": "1 Warlord-Heavy Battle Titan",
            "unitOptions": [
                {"label": "1 Warmaster Heavy Battle Titan",
                 "units": [{"unit": "warmaster-heavy-battle-titan", "count": 1}]}
            ],
            "allowedUpgrades": ["veteran-princepts", "vp-legate",
                                "titan-weapons-mixed-2",
                                "air-defence", "sacred-icon"],
        },
    ],
    "upgrades": [
        {"id": "air-defence", "name": "Air Defence", "type": "flag", "cost": 50,
         "description": "Add 1 Carapace Multilaser to the Titan.",
         "addedUnits": [{"unit": "carapace-multilaser", "count": 1}]},
        {"id": "sacred-icon", "name": "Sacred Icon", "type": "flag", "cost": 50,
         "description": "Add 1 Sacred Icon character (Inspiring).",
         "addedUnits": [{"unit": "sacred-icon", "count": 1}]},
        {"id": "veteran-princepts", "name": "Veteran Princepts", "type": "flag", "cost": 25,
         "description": "Add 1 Veteran Princepts character (Commander, Leader).",
         "addedUnits": [{"unit": "veteran-princepts", "count": 1}]},
        {"id": "vp-legate", "name": "Veteran Princepts: Legate", "type": "flag", "cost": 50,
         "description": "Upgrade one Veteran Princepts to a Legate (Supreme Commander, max 1 per force). Requires Veteran Princepts upgrade.",
         "addedUnits": [{"unit": "legate", "count": 1}]},

        # Titan weapon-slot upgrades
        titan_weapon_upgrade("titan-weapons-scout-2", "2 Scout Titan Weapons", 2, False),
        titan_weapon_upgrade("titan-weapons-scout-4", "4 Scout Titan Weapons", 4, False),
        titan_weapon_upgrade("titan-weapons-mixed-1", "1 Scout or Battle Titan Weapon", 1, True),
        titan_weapon_upgrade("titan-weapons-mixed-2", "2 Scout or Battle Titan Weapons", 2, True),
        titan_weapon_upgrade("titan-weapons-mixed-3", "3 Scout or Battle Titan Weapons", 3, True),
        titan_weapon_upgrade("titan-weapons-mixed-4", "4 Scout or Battle Titan Weapons", 4, True),
    ],
    "units": {
        # Characters and upgrades
        "legate": {
            "name": "Legate", "type": "CH",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [],
            "notes": ["Supreme Commander."],
        },
        "veteran-princepts": {
            "name": "Veteran Princepts", "type": "CH",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [],
            "notes": ["Commander.", "Leader."],
        },
        "sacred-icon": {
            "name": "Sacred Icon", "type": "CH",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [],
            "notes": ["Inspiring."],
        },
        "carapace-multilaser": {
            "name": "Carapace Multilaser", "type": "CH",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [{"name": "Carapace Multilaser", "range": "30cm",
                         "firepower": "2× AP5+/AT6+/AA5+"}],
            "notes": [],
        },

        # War Engines (Titans)
        "warhound-scout-titan": {
            "name": "Warhound Scout Titan", "type": "WE",
            "speed": "30cm", "armour": "5+", "cc": "4+", "ff": "5+",
            "weapons": [{"name": "2× Scout Titan Weapons", "range": "varies",
                         "firepower": "(2 Arm, Fwd)"}],
            "notes": ["DC3.", "2 Void shields.", "Fearless.",
                      "Reinforced armour.", "Walker.", "Cortex controller.",
                      "May step over impassable/dangerous terrain lower than knee height.",
                      "Critical Hit: stagger D6 random direction, takes extra DC, units in base contact hit on 6+."],
        },
        "direwolf-heavy-scout-titan": {
            "name": "Direwolf Heavy Scout Titan", "type": "WE",
            "speed": "25cm", "armour": "5+", "cc": "4+", "ff": "4+",
            "weapons": [
                {"name": "1× Scout or Battle Titan Weapon", "range": "varies",
                 "firepower": "(1 Carapace, FxF)"},
                {"name": "Ardax Defensor Megabolter", "range": "30cm",
                 "firepower": "2× AP3+/AT5+"},
            ],
            "notes": ["DC4.", "2 Void shields.", "Fearless.",
                      "Reinforced armour.", "Walker.", "Cortex controller.",
                      "Grand Stalker — may deploy as a garrison unit.",
                      "Critical Hit: stagger D6 random direction, takes extra DC."],
        },
        "reaver-battle-titan": {
            "name": "Reaver Battle Titan", "type": "WE",
            "speed": "20cm", "armour": "4+", "cc": "3+", "ff": "3+",
            "weapons": [{"name": "3× Scout or Battle Titan Weapons",
                         "range": "varies",
                         "firepower": "(2 Arm, Fwd; 1 Carapace)"}],
            "notes": ["DC6.", "4 Void shields.", "Fearless.",
                      "Reinforced armour.", "Walker.", "Cortex controller.",
                      "Critical Hit: reactor instability — D6 each end phase."],
        },
        "warbringer-nemesis-titan": {
            "name": "Warbringer Nemesis Titan", "type": "WE",
            "speed": "15cm", "armour": "4+", "cc": "4+", "ff": "3+",
            "weapons": [
                {"name": "Carapace Quake Cannon", "range": "90cm",
                 "firepower": "3 BP, MW, Indirect fire, FxF"},
                {"name": "Flak Battery", "range": "45cm",
                 "firepower": "2× AP4+/AT5+/AA5+"},
                {"name": "2× Battle Titan Weapons", "range": "varies",
                 "firepower": "(2 Carapace, FxF)"},
            ],
            "notes": ["DC7.", "3 Void shields.", "Fearless.",
                      "Reinforced armour.", "Walker.", "Cortex controller.",
                      "Critical Hit: reactor instability — D6 each end phase."],
        },
        "warlord-battle-titan": {
            "name": "Warlord Battle Titan", "type": "WE",
            "speed": "15cm", "armour": "4+", "cc": "2+", "ff": "3+",
            "weapons": [{"name": "4× Scout or Battle Titan Weapons",
                         "range": "varies",
                         "firepower": "(2 Arm, Fwd; 2 Carapace, FxF)"}],
            "notes": ["DC8.", "6 Void shields.", "Fearless.",
                      "Reinforced armour.", "Walker.", "Cortex controller.",
                      "Critical Hit: reactor instability — D6 each end phase."],
        },
        "warmaster-heavy-battle-titan": {
            "name": "Warmaster Heavy Battle Titan", "type": "WE",
            "speed": "20cm", "armour": "4+", "cc": "3+", "ff": "3+ (2+)",
            "weapons": [
                {"name": "2× Scout or Battle Titan Weapons",
                 "range": "varies", "firepower": "(2 Carapace, FxF)"},
                {"name": "2× Heavy Plasma Destructors OR", "range": "90cm",
                 "firepower": "4× AP2+/AT2+, MW, Slow firing"},
                {"name": "2× Close Combat Weapons", "range": "(base)",
                 "firepower": "(assault) TK (D3), EA (+3)"},
                {"name": "Revelator Missile Launcher", "range": "45cm",
                 "firepower": "2× Warhead Missile, 3 BP, MW, Ignore cover, Fwd, One shot"},
            ],
            "notes": ["DC9.", "7 Void shields.", "Fearless.",
                      "Reinforced armour.", "Thick rear armour.", "Walker.",
                      "Cortex controller.",
                      "Critical Hit: reactor instability — D6 each end phase."],
        },
        "warlord-sinister": {
            "name": "Warlord-Sinister Psi-Titan", "type": "WE",
            "speed": "15cm", "armour": "4+", "cc": "2+", "ff": "3+",
            "weapons": [
                {"name": "Sinistramanus Tenebrae", "range": "90cm",
                 "firepower": "AP2+/AT2+, TK (2), Singularity, Fwd"},
                {"name": "3× Scout or Battle Titan Weapons",
                 "range": "varies",
                 "firepower": "(1 Arm, Fwd; 2 Carapace, FxF)"},
            ],
            "notes": ["DC8.", "6 Void shields.", "Fearless.",
                      "Reinforced armour.", "Inspiring.", "Invulnerable save.",
                      "Walker.", "Cortex controller.",
                      "Sinistramanus Tenebrae ignores Void shields and Invulnerable saves.",
                      "Critical Hit: reactor instability — D6 each end phase."],
        },
        "emperor-titan": {
            "name": "Emperor Titan", "type": "WE",
            "speed": "15cm", "armour": "4+", "cc": "4+", "ff": "5+",
            "weapons": [
                {"name": "Plasma Annihilator", "range": "90cm",
                 "firepower": "4× AP2+/AT2+, TK (D3), Slow firing, Fwd"},
                {"name": "Hellstorm Cannon", "range": "60cm",
                 "firepower": "10 BP, Fwd"},
                {"name": "2× Flak Towers", "range": "60cm",
                 "firepower": "2× AP4+/AT6+/AA5+"},
                {"name": "4× Battlecannon", "range": "75cm",
                 "firepower": "AP4+/AT4+"},
                {"name": "Quake Cannon", "range": "90cm",
                 "firepower": "3 BP, MW, FxF"},
                {"name": "Tertiary Armaments", "range": "(15cm)",
                 "firepower": "(small arms), EA (+2)"},
                {"name": "Leg Bastions", "range": "-",
                 "firepower": "Counts as Corvus Assault Pod"},
            ],
            "notes": ["DC12.", "8 Void shields.", "Cortex controller.",
                      "Fearless.", "Inspiring.", "Reinforced armour.", "Walker.",
                      "Secondary firing protocols: may pick a 2nd target for Battlecannons and/or Flak Towers.",
                      "Critical Hit: reactor instability — apocalyptic explosion on 1 hits all in 15cm."],
        },
    },
}


def main():
    doc = json.loads(DATA.read_text(encoding="utf-8"))
    factions = doc["factions"]
    new_ids = {knight_household["id"], legio_titanicus["id"]}
    factions = [f for f in factions if f["id"] not in new_ids]
    factions.append(knight_household)
    factions.append(legio_titanicus)
    doc["factions"] = factions
    DATA.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
                     encoding="utf-8")
    print(f"OK wrote {len(factions)} factions")
    for fac in (knight_household, legio_titanicus):
        print(f"  {fac['id']:20s} formations={len(fac['formations'])}, "
              f"units={len(fac['units'])}, upgrades={len(fac['upgrades'])}")


if __name__ == "__main__":
    main()
