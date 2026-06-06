"""
One-shot script: appends Solar Auxilia and Imperialis Militia factions to
backend/data/factions.json. Idempotent — re-running replaces the entries
if they already exist (matched by id).

Source: /app/pdf_work/eoa.txt — Empire of Ashes, pages 31–58.
"""
import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "factions.json"


# ---------- Shared chrome ----------
COMP_LIMITS_2_3 = {  # 2 Support per Line, max 3 upgrades, 1/3 LoW
    "maxSupportPerLine": 2,
    "maxUpgradesPerLine": 3,
    "lowPct": 0.33,
}

COMP_RULES_2_3 = [
    "Max 2 Support detachments per Line detachment in the army.",
    "Max 3 Upgrades per formation.",
    "Max 1/3 of total points value may be spent on Lords of War or Allies.",
]


# =====================================================================
# SOLAR AUXILIA
# =====================================================================
solar_auxilia = {
    "id": "solar-auxilia",
    "name": "Solar Auxilia",
    "subtitle": "Excertus Imperialis · Cohorts of the Hundred Worlds",
    "color": "#8A6E2F",
    "lore": (
        "The elite of the mortal Excertus Imperialis. Drawn from Terra's "
        "solar domains and moulded by the Principia Belicosa, the Solar "
        "Auxilia Cohorts march in serried ranks behind armoured spearheads "
        "of Leman Russ, Malcadors and ancient war engines. Less numerous "
        "than the Imperial Army but disciplined, professional and "
        "exquisitely equipped — the backstop of the Legiones Astartes."
    ),
    "legionTrait": {
        "name": "Cohorts of the Solar Auxilia",
        "description": (
            "Strategy Rating 3 · Initiative 2+. May field 2 Support per "
            "Line, with up to 3 Upgrades per formation. One free Legate "
            "Commander per full 750 points (does not cost points)."
        ),
    },
    "compositionLimits": COMP_LIMITS_2_3,
    "compositionRules": COMP_RULES_2_3 + [
        "Strategy Rating 3, Initiative 2+.",
        "Includes 1 free Legate Commander per full 750 points; first attaches to the Lord Marshall's formation (or most expensive Line if none).",
        "Armoured Spearhead: may garrison one formation with 3+ AV units per full 2,000 pts.",
        "Orbital Support: 1 per force.",
        "Command Retinue: 1 per force.",
    ],
    "allies": {
        "cohesive": [
            "Knight Households",
            "Legiones Astartes",
            "Legio Titanicus",
        ],
        "disruptive": [
            "Daemons of the Ruinstorm (Traitor only)",
            "Mechanicum Taghmata",
        ],
    },
    "formations": [
        # ----- Line -----
        {
            "id": "command-retinue",
            "name": "Command Retinue",
            "category": "Line",
            "baseCost": 300,
            "composition": "1 Lord Marshall and 7 Veletaris Storm units (1 per force)",
            "unitOptions": [
                {"label": "Lord Marshall + 7 Veletaris Storm",
                 "units": [{"unit": "lord-marshall", "count": 1}, {"unit": "veletaris-storm", "count": 7}]}
            ],
            "maxPerArmy": 1,
            "allowedUpgrades": [
                "sa-transport", "sa-infantry-support-tank", "sa-ogryn-charonite",
                "sa-support"
            ],
        },
        {
            "id": "strike-squadron",
            "name": "Strike Squadron",
            "category": "Line",
            "baseCost": 200,
            "composition": "4 Leman Russ Battle Tank or Exterminator (+50 each, up to 6)",
            "unitOptions": [
                {"label": "4 Leman Russ Battle Tank",
                 "units": [{"unit": "sa-leman-russ-battle", "count": 4}]},
                {"label": "4 Leman Russ Exterminator",
                 "units": [{"unit": "sa-leman-russ-exterminator", "count": 4}]},
            ],
            "extraUnit": {"unit": "sa-leman-russ-battle", "cost": 50, "max": 2,
                          "label": "Additional Leman Russ (Battle/Exterminator)"},
            "allowedUpgrades": ["sa-vanquisher", "sa-executioner"],
        },
        {
            "id": "infantry-tercio",
            "name": "Infantry Tercio",
            "category": "Line",
            "baseCost": 150,
            "composition": "1 Auxilia Tactical Command Section and 7 Solar Auxilia Infantry Section units",
            "unitOptions": [
                {"label": "Auxilia Command + 7 Infantry Section",
                 "units": [{"unit": "sa-tactical-command", "count": 1},
                           {"unit": "sa-infantry-section", "count": 7}]}
            ],
            "allowedUpgrades": [
                "sa-transport", "sa-infantry-support-tank", "sa-ogryn-charonite",
                "sa-rapier-battery", "sa-support"
            ],
        },
        {
            "id": "veletaris-storm-cohort",
            "name": "Veletaris Storm Cohort",
            "category": "Line",
            "baseCost": 200,
            "composition": "1 Auxilia Tactical Command Section and 7 Veletaris Storm units",
            "unitOptions": [
                {"label": "Auxilia Command + 7 Veletaris Storm",
                 "units": [{"unit": "sa-tactical-command", "count": 1},
                           {"unit": "veletaris-storm", "count": 7}]}
            ],
            "allowedUpgrades": [
                "sa-transport", "sa-infantry-support-tank", "sa-ogryn-charonite"
            ],
        },

        # ----- Support -----
        {
            "id": "sa-sentinel-squadron",
            "name": "Sentinel Squadron",
            "category": "Support",
            "baseCost": 125,
            "composition": "4 Aethon Heavy Sentinels OR Hermes Light Sentinels",
            "unitOptions": [
                {"label": "4 Aethon Heavy Sentinels",
                 "units": [{"unit": "aethon-heavy-sentinel", "count": 4}]},
                {"label": "4 Hermes Light Sentinels",
                 "units": [{"unit": "hermes-light-sentinel", "count": 4}]},
            ],
            "allowedUpgrades": [],
        },
        {
            "id": "tarantula-battery",
            "name": "Tarantula Battery",
            "category": "Support",
            "baseCost": 100,
            "composition": "5 Tarantulas",
            "unitOptions": [
                {"label": "5 Tarantulas",
                 "units": [{"unit": "tarantula", "count": 5}]}
            ],
            "allowedUpgrades": ["sa-hyperios-platform"],
        },
        {
            "id": "sa-artillery-tank-battery",
            "name": "Artillery Tank Battery",
            "category": "Support",
            "baseCost": 250,
            "composition": "3 Basilisk OR Bombard OR Medusa",
            "unitOptions": [
                {"label": "3 Basilisk", "units": [{"unit": "sa-basilisk", "count": 3}]},
                {"label": "3 Bombard", "units": [{"unit": "sa-bombard", "count": 3}]},
                {"label": "3 Medusa", "units": [{"unit": "sa-medusa", "count": 3}]},
            ],
            "allowedUpgrades": [],
        },
        {
            "id": "carnodon-squadron",
            "name": "Carnodon Squadron",
            "category": "Support",
            "baseCost": 250,
            "composition": "5 Carnodons (+50 each, up to 8)",
            "unitOptions": [
                {"label": "5 Carnodons",
                 "units": [{"unit": "carnodon", "count": 5}]}
            ],
            "extraUnit": {"unit": "carnodon", "cost": 50, "max": 3, "label": "Additional Carnodon"},
            "allowedUpgrades": [],
        },
        {
            "id": "close-support-tank-squadron",
            "name": "Close Support Tank Squadron",
            "category": "Support",
            "baseCost": 200,
            "composition": "3 Leman Russ Demolisher or Incinerator (+65 each, up to 4)",
            "unitOptions": [
                {"label": "3 Leman Russ Demolisher",
                 "units": [{"unit": "sa-leman-russ-demolisher", "count": 3}]},
                {"label": "3 Leman Russ Incinerator",
                 "units": [{"unit": "sa-leman-russ-incinerator", "count": 3}]},
            ],
            "extraUnit": {"unit": "sa-leman-russ-demolisher", "cost": 65, "max": 1,
                          "label": "Additional Demolisher/Incinerator"},
            "allowedUpgrades": ["sa-executioner"],
        },
        {
            "id": "malcador-squadron",
            "name": "Malcador Squadron",
            "category": "Support",
            "baseCost": 300,
            "composition": "4 Malcador Heavy Tank or Malcador Infernus (+50 each, up to 6)",
            "unitOptions": [
                {"label": "4 Malcador Heavy Tank",
                 "units": [{"unit": "sa-malcador-heavy", "count": 4}]},
                {"label": "4 Malcador Infernus",
                 "units": [{"unit": "sa-malcador-infernus", "count": 4}]},
            ],
            "extraUnit": {"unit": "sa-malcador-heavy", "cost": 50, "max": 2,
                          "label": "Additional Malcador"},
            "allowedUpgrades": [],
        },
        {
            "id": "tank-hunter-squadron",
            "name": "Tank Hunter Squadron",
            "category": "Support",
            "baseCost": 200,
            "composition": "3 Valdor Tank Hunter",
            "unitOptions": [
                {"label": "3 Valdor",
                 "units": [{"unit": "valdor-tank-hunter", "count": 3}]}
            ],
            "allowedUpgrades": [],
        },
        {
            "id": "sa-super-heavy-tank",
            "name": "Super Heavy Tank",
            "category": "Support",
            "baseCost": 200,
            "composition": "1 Baneblade OR Shadowsword OR Stormsword OR Stormblade OR Stormhammer",
            "unitOptions": [
                {"label": "1 Baneblade", "units": [{"unit": "sa-baneblade", "count": 1}]},
                {"label": "1 Shadowsword", "units": [{"unit": "sa-shadowsword", "count": 1}]},
                {"label": "1 Stormsword", "units": [{"unit": "sa-stormsword", "count": 1}]},
                {"label": "1 Stormblade", "units": [{"unit": "sa-stormblade", "count": 1}]},
                {"label": "1 Stormhammer", "units": [{"unit": "sa-stormhammer", "count": 1}]},
            ],
            "allowedUpgrades": [],
        },

        # ----- Lords of War -----
        {
            "id": "sa-super-heavy-tank-squadron",
            "name": "Solar Auxilia Super Heavy Tank Squadron",
            "category": "Lords of War",
            "baseCost": 500,
            "composition": "3 Baneblade OR Shadowsword OR Stormsword OR Stormblade OR Stormhammer",
            "unitOptions": [
                {"label": "3 Baneblade", "units": [{"unit": "sa-baneblade", "count": 3}]},
                {"label": "3 Shadowsword", "units": [{"unit": "sa-shadowsword", "count": 3}]},
                {"label": "3 Stormsword", "units": [{"unit": "sa-stormsword", "count": 3}]},
                {"label": "3 Stormblade", "units": [{"unit": "sa-stormblade", "count": 3}]},
                {"label": "3 Stormhammer", "units": [{"unit": "sa-stormhammer", "count": 3}]},
            ],
            "allowedUpgrades": [],
        },
        {
            "id": "sa-avenger-flight",
            "name": "Solar Auxilia Avenger Flight",
            "category": "Lords of War",
            "baseCost": 225,
            "composition": "2 Avenger Strike Fighters (+125 each, up to 3)",
            "unitOptions": [
                {"label": "2 Avenger Strike Fighters",
                 "units": [{"unit": "avenger-strike-fighter", "count": 2}]}
            ],
            "extraUnit": {"unit": "avenger-strike-fighter", "cost": 125, "max": 1,
                          "label": "Additional Avenger Strike Fighter"},
            "allowedUpgrades": [],
        },
        {
            "id": "sa-lightning-flight",
            "name": "Solar Auxilia Lightning Flight",
            "category": "Lords of War",
            "baseCost": 225,
            "composition": "2 Lightning Interceptors (+125 each, up to 3)",
            "unitOptions": [
                {"label": "2 Lightning Interceptors",
                 "units": [{"unit": "lightning-interceptor", "count": 2}]}
            ],
            "extraUnit": {"unit": "lightning-interceptor", "cost": 125, "max": 1,
                          "label": "Additional Lightning Interceptor"},
            "allowedUpgrades": [],
        },
        {
            "id": "sa-marauder-heavy-bomber",
            "name": "Solar Auxilia Marauder Heavy Bomber",
            "category": "Lords of War",
            "baseCost": 325,
            "composition": "2 Marauder Heavy Bombers",
            "unitOptions": [
                {"label": "2 Marauder Heavy Bombers",
                 "units": [{"unit": "marauder-heavy-bomber", "count": 2}]}
            ],
            "allowedUpgrades": [],
        },
        {
            "id": "sa-orbital-support",
            "name": "Solar Auxilia Orbital Support",
            "category": "Lords of War",
            "baseCost": 150,
            "composition": "1 Dauntless cruiser OR Emperor battleship (1 per force)",
            "unitOptions": [
                {"label": "1 Dauntless Light Cruiser",
                 "units": [{"unit": "dauntless-cruiser", "count": 1}]},
                {"label": "1 Emperor Battleship",
                 "units": [{"unit": "emperor-battleship", "count": 1}],
                 "costOverride": 300},
            ],
            "maxPerArmy": 1,
            "allowedUpgrades": [],
        },
    ],
    "upgrades": [
        {"id": "sa-executioner", "name": "Executioner", "type": "flag", "cost": 25,
         "description": "Upgrade one Leman Russ unit to a Leman Russ Executioner."},
        {"id": "sa-hyperios-platform", "name": "Hyperios Platform", "type": "multi", "max": 3,
         "description": "Upgrade 1-3 Tarantula Platforms to Tarantula Hyperios Platforms.",
         "variants": [{"id": "tarantula-hyperios", "name": "Tarantula Hyperios", "cost": 40}]},
        {"id": "sa-infantry-support-tank", "name": "Infantry Support Tank", "type": "multi", "max": 2,
         "description": "Add 1-2 Leman Russ Demolisher OR Malcador Infernus.",
         "variants": [
             {"id": "sa-leman-russ-demolisher", "name": "Leman Russ Demolisher", "cost": 50},
             {"id": "sa-malcador-infernus", "name": "Malcador Infernus", "cost": 50},
         ]},
        {"id": "sa-ogryn-charonite", "name": "Ogryn Charonite Squad", "type": "flag", "cost": 75,
         "description": "Add 2 Ogryn Charonite units."},
        {"id": "sa-rapier-battery", "name": "Rapier Battery", "type": "flag", "cost": 125,
         "description": "Add 4 Solar Auxilia Rapier Platform units."},
        {"id": "sa-support", "name": "Solar Auxilia Support", "type": "flag", "cost": 75,
         "description": "Add 4 Auxilia Close Support (Flamer) Sections or Veletaris Storm units in any combination."},
        {"id": "sa-transport", "name": "Transport", "type": "multi",
         "description": "Add enough Aurox, Dracosan, Stormlord, Arvus or Termites to carry the formation.",
         "variants": [
             {"id": "aurox", "name": "Aurox Transport", "cost": 10},
             {"id": "dracosan", "name": "Dracosan Armoured Transport", "cost": 75},
             {"id": "stormlord", "name": "Stormlord Superheavy Carrier", "cost": 200},
             {"id": "arvus", "name": "Arvus Lighter", "cost": 25},
             {"id": "termite", "name": "Termite Assault Drill", "cost": 75},
         ]},
        {"id": "sa-vanquisher", "name": "Vanquisher", "type": "flag", "cost": 25,
         "description": "Upgrade 1 Leman Russ unit to a Leman Russ Vanquisher."},
    ],
    "units": {
        # Characters & infantry
        "legate-commander": {
            "name": "Legate Commander", "type": "CH",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [{"name": "Power Fist", "range": "(base)",
                        "firepower": "(assault) MW, EA (+1)"}],
            "notes": ["Leader.", "Inspiring."],
        },
        "lord-marshall": {
            "name": "Lord Marshall", "type": "INF",
            "speed": "15cm", "armour": "5+", "cc": "5+", "ff": "4+",
            "weapons": [
                {"name": "Archeotech Pistol", "range": "(15cm)",
                 "firepower": "(small arms) MW, EA (+1)"},
                {"name": "Volkite Chargers", "range": "15cm",
                 "firepower": "AP5+, Disrupt"},
            ],
            "notes": ["Supreme Commander.", "Invulnerable save.",
                      "Counts as a character unit for Bodyguard / Strategic Value."],
        },
        "ogryn-charonite": {
            "name": "Ogryn Charonite Squad", "type": "INF",
            "speed": "15cm", "armour": "3+", "cc": "3+", "ff": "5+",
            "weapons": [{"name": "Charonite Claws", "range": "(base)",
                        "firepower": "(assault) MW, EA (+1)"}],
            "notes": ["Bodyguard.", "Each Ogryn counts as 2 units for transport."],
        },
        "sa-rapier-platform": {
            "name": "Solar Auxilia Rapier Platform", "type": "INF",
            "speed": "10cm", "armour": "5+", "cc": "4+", "ff": "6+ (4+)",
            "weapons": [
                {"name": "Laser Destroyer OR", "range": "45cm",
                 "firepower": "AT4+, Armourbane"},
                {"name": "Quad Mortar OR", "range": "45cm",
                 "firepower": "AP5+/AT6+, Indirect fire, Disrupt"},
                {"name": "Quad Heavy Bolter", "range": "30cm",
                 "firepower": "2× AP4+"},
            ],
            "notes": ["Mounted."],
        },
        "sa-tactical-command": {
            "name": "Solar Auxilia Tactical Command Section", "type": "INF",
            "speed": "15cm", "armour": "5+", "cc": "5+", "ff": "5+",
            "weapons": [{"name": "Support Weapon", "range": "15cm",
                        "firepower": "AP5+/AT5+"}],
            "notes": ["Commander.",
                      "Counts as a character unit for Bodyguard / Strategic Value."],
        },
        "sa-infantry-section": {
            "name": "Solar Auxilia Infantry Section", "type": "INF",
            "speed": "15cm", "armour": "5+", "cc": "5+", "ff": "5+",
            "weapons": [{"name": "Las-rifles", "range": "(15cm)",
                        "firepower": "(small arms)"}],
            "notes": [],
        },
        "sa-close-support-section": {
            "name": "Solar Auxilia Close Support Section", "type": "INF",
            "speed": "15cm", "armour": "5+", "cc": "5+", "ff": "4+",
            "weapons": [{"name": "Flamers", "range": "15cm & (15cm)",
                        "firepower": "AP5+, Ignore cover / (small arms) Ignore cover"}],
            "notes": [],
        },
        "veletaris-storm": {
            "name": "Veletaris Storm Section", "type": "INF",
            "speed": "15cm", "armour": "5+", "cc": "5+ / 4+", "ff": "4+ / 6+",
            "weapons": [
                {"name": "Volkite Chargers OR", "range": "15cm",
                 "firepower": "AP5+, Disrupt"},
                {"name": "Heavy Power Axes", "range": "(base)",
                 "firepower": "(assault) MW"},
            ],
            "notes": [],
        },

        # Light / armoured vehicles
        "hermes-light-sentinel": {
            "name": "Hermes Light Sentinel", "type": "LV",
            "speed": "25cm", "armour": "6+", "cc": "6+", "ff": "5+ (4+)",
            "weapons": [
                {"name": "Multilaser OR", "range": "45cm",
                 "firepower": "AP5+/AT6+"},
                {"name": "Heavy Flamer", "range": "15cm & (15cm)",
                 "firepower": "AP4+, Ignore cover / (small arms) Ignore cover"},
            ],
            "notes": ["Scout.", "Walker."],
        },
        "tarantula": {
            "name": "Tarantula", "type": "LV",
            "speed": "0cm", "armour": "6+", "cc": "6+", "ff": "6+ (5+)",
            "weapons": [
                {"name": "TL Lascannon OR", "range": "30cm",
                 "firepower": "AP4+"},
                {"name": "TL Heavy Bolter", "range": "45cm",
                 "firepower": "AT4+"},
            ],
            "notes": ["Teleport.", "Scout."],
        },
        "tarantula-hyperios": {
            "name": "Tarantula Hyperios", "type": "LV",
            "speed": "0cm", "armour": "6+", "cc": "6+", "ff": "6+",
            "weapons": [{"name": "Hyperios Missiles", "range": "60cm",
                        "firepower": "AA4+"}],
            "notes": ["Teleport.", "Scout."],
        },
        "aethon-heavy-sentinel": {
            "name": "Aethon Heavy Sentinel", "type": "AV",
            "speed": "15cm", "armour": "5+", "cc": "6+", "ff": "5+",
            "weapons": [
                {"name": "Missile Pods", "range": "45cm",
                 "firepower": "2× AP5+"},
                {"name": "Multilaser", "range": "45cm",
                 "firepower": "AP5+/AT6+"},
            ],
            "notes": ["Walker."],
        },
        "arvus": {
            "name": "Arvus Lighter Orbital Shuttle", "type": "AV",
            "speed": "40cm", "armour": "5+", "cc": "6+", "ff": "- (5+)",
            "weapons": [{"name": "Multilaser (optional, +10)",
                        "range": "30cm & (15cm)",
                        "firepower": "AP5+/AT6+ / (small arms)"}],
            "notes": ["Skimmer.", "Planetfall.", "Transport (2 INF)."],
        },
        "aurox": {
            "name": "Aurox Transport", "type": "AV",
            "speed": "30cm", "armour": "5+", "cc": "6+", "ff": "5+",
            "weapons": [{"name": "Heavy Stubber", "range": "(15cm)",
                        "firepower": "(small arms)"}],
            "notes": ["Transport (2 INF)."],
        },
        "sa-basilisk": {
            "name": "Basilisk", "type": "AV",
            "speed": "25cm", "armour": "5+", "cc": "6+", "ff": "6+",
            "weapons": [
                {"name": "Earthshaker Cannon", "range": "120cm",
                 "firepower": "AP4+/AT4+ OR 1 BP, Indirect fire"},
                {"name": "Heavy Bolter", "range": "30cm", "firepower": "AP5+"},
            ],
            "notes": [],
        },
        "sa-bombard": {
            "name": "Bombard", "type": "AV",
            "speed": "25cm", "armour": "5+", "cc": "6+", "ff": "6+",
            "weapons": [
                {"name": "Siege Mortar", "range": "45cm",
                 "firepower": "1 BP, Indirect fire, Ignore cover"},
                {"name": "Heavy Bolter", "range": "30cm", "firepower": "AP5+"},
            ],
            "notes": [],
        },
        "carnodon": {
            "name": "Carnodon", "type": "AV",
            "speed": "30cm", "armour": "4+", "cc": "6+", "ff": "5+ (4+)",
            "weapons": [
                {"name": "TL Lascannon OR", "range": "45cm", "firepower": "AT4+"},
                {"name": "Volkite Culverin", "range": "45cm",
                 "firepower": "AP4+/AT6+ Disrupt"},
                {"name": "2× Lascannon OR", "range": "45cm", "firepower": "AT5+"},
                {"name": "2× Heavy Bolters", "range": "30cm", "firepower": "AP5+"},
            ],
            "notes": [],
        },
        "sa-leman-russ-battle": {
            "name": "Leman Russ Battle Tank", "type": "AV",
            "speed": "25cm", "armour": "4+", "cc": "6+", "ff": "5+",
            "weapons": [
                {"name": "Battlecannon", "range": "75cm", "firepower": "AP4+/AT4+"},
                {"name": "Lascannon", "range": "45cm", "firepower": "AT5+"},
            ],
            "notes": ["Reinforced armour."],
        },
        "sa-leman-russ-exterminator": {
            "name": "Leman Russ Exterminator", "type": "AV",
            "speed": "25cm", "armour": "4+", "cc": "6+", "ff": "4+",
            "weapons": [
                {"name": "Exterminator Cannon", "range": "45cm",
                 "firepower": "2× AP4+/AT6+"},
                {"name": "Heavy Bolter", "range": "30cm", "firepower": "AP5+"},
            ],
            "notes": ["Reinforced armour."],
        },
        "sa-leman-russ-executioner": {
            "name": "Leman Russ Executioner", "type": "AV",
            "speed": "25cm", "armour": "4+", "cc": "6+", "ff": "5+",
            "weapons": [
                {"name": "Plasma Cannon", "range": "45cm",
                 "firepower": "AP4+/AT4+, MW"},
                {"name": "Lascannon", "range": "45cm", "firepower": "AT5+"},
            ],
            "notes": ["Reinforced armour.", "Thick rear armour."],
        },
        "sa-leman-russ-incinerator": {
            "name": "Leman Russ Incinerator", "type": "AV",
            "speed": "25cm", "armour": "4+", "cc": "6+", "ff": "4+",
            "weapons": [
                {"name": "TL Volkite Demiculverin", "range": "45cm",
                 "firepower": "2× AP3+/AT5+, Disrupt"},
                {"name": "Lascannon", "range": "45cm", "firepower": "AT5+"},
            ],
            "notes": ["Reinforced armour.", "Thick rear armour."],
        },
        "sa-leman-russ-vanquisher": {
            "name": "Leman Russ Vanquisher", "type": "AV",
            "speed": "25cm", "armour": "4+", "cc": "6+", "ff": "5+",
            "weapons": [
                {"name": "Vanquisher Cannon", "range": "75cm",
                 "firepower": "AP4+/AT3+, Armourbane"},
                {"name": "Lascannon", "range": "45cm", "firepower": "AT5+"},
            ],
            "notes": ["Reinforced armour."],
        },
        "sa-leman-russ-demolisher": {
            "name": "Leman Russ Demolisher", "type": "AV",
            "speed": "25cm", "armour": "4+", "cc": "6+", "ff": "5+",
            "weapons": [
                {"name": "Demolisher Cannon", "range": "15cm & (15cm)",
                 "firepower": "AP4+/AT4+, MW, Ignore cover / (small arms) MW, Ignore cover"},
                {"name": "Lascannon", "range": "45cm", "firepower": "AT5+"},
            ],
            "notes": ["Reinforced armour.", "Thick rear armour."],
        },
        "sa-malcador-heavy": {
            "name": "Malcador Heavy Tank", "type": "AV",
            "speed": "15cm", "armour": "4+", "cc": "6+", "ff": "5+",
            "weapons": [
                {"name": "Battlecannon", "range": "75cm", "firepower": "AP4+/AT4+"},
                {"name": "2× Autocannons", "range": "45cm", "firepower": "AP5+/AT6+"},
                {"name": "Heavy Bolter", "range": "30cm", "firepower": "AP5+"},
            ],
            "notes": ["Reinforced armour.", "Thick rear armour."],
        },
        "sa-malcador-infernus": {
            "name": "Malcador Infernus Tank", "type": "AV",
            "speed": "15cm", "armour": "4+", "cc": "6+", "ff": "3+",
            "weapons": [
                {"name": "Infernus Cannon", "range": "30cm",
                 "firepower": "2× AP3+, Ignore cover"},
                {"name": "2× Autocannons", "range": "45cm", "firepower": "AP5+/AT6+"},
            ],
            "notes": ["Reinforced armour.", "Thick rear armour."],
        },
        "sa-medusa": {
            "name": "Medusa", "type": "AV",
            "speed": "25cm", "armour": "5+", "cc": "6+", "ff": "5+",
            "weapons": [
                {"name": "Medusa Siege Mortar", "range": "30cm",
                 "firepower": "AP4+/AT4+, MW, Indirect fire, Ignore cover"},
                {"name": "Heavy Bolter", "range": "30cm", "firepower": "AP5+"},
            ],
            "notes": [],
        },
        "termite": {
            "name": "Termite Assault Drill", "type": "AV",
            "speed": "10cm", "armour": "5+", "cc": "4+", "ff": "5+",
            "weapons": [
                {"name": "Heavy Melta Cutter", "range": "(base)",
                 "firepower": "(assault) MW"},
                {"name": "TL Volkite Caliver", "range": "15cm",
                 "firepower": "AP4+, Disrupt"},
            ],
            "notes": ["Self planetfall (turn 2+).", "Reinforced armour.",
                      "Thick rear armour.", "Walker.", "Transport (2 INF)."],
        },
        "valdor-tank-hunter": {
            "name": "Valdor Tank Hunter", "type": "AV",
            "speed": "15cm", "armour": "4+", "cc": "6+", "ff": "5+",
            "weapons": [
                {"name": "Neutron Beamer", "range": "30cm",
                 "firepower": "2× AT3+, Armourbane, Disrupt, Feedback, FxF"},
                {"name": "Lascannon", "range": "45cm", "firepower": "AT5+"},
            ],
            "notes": ["Reinforced armour."],
        },

        # War engines
        "sa-baneblade": {
            "name": "Baneblade", "type": "WE",
            "speed": "15cm", "armour": "4+", "cc": "6+", "ff": "4+",
            "weapons": [
                {"name": "Baneblade Cannon", "range": "75cm",
                 "firepower": "AP3+/AT3+, MW"},
                {"name": "Coaxial Autocannon", "range": "45cm",
                 "firepower": "AP5+/AT6+"},
                {"name": "Demolisher Cannon", "range": "15cm & (15cm)",
                 "firepower": "AP4+/AT4+, MW, Ignore cover / (small arms) MW, EA (+1)"},
                {"name": "2× Lascannon", "range": "45cm", "firepower": "AT5+"},
                {"name": "3× TL Heavy Bolters", "range": "30cm", "firepower": "AP4+"},
            ],
            "notes": ["DC3.", "Reinforced armour.",
                      "Critical Hit: Destroyed, units within 5cm suffer a hit on 6+."],
        },
        "dracosan": {
            "name": "Dracosan Armoured Transport", "type": "WE",
            "speed": "20cm", "armour": "4+", "cc": "6+", "ff": "5+",
            "weapons": [
                {"name": "TL Lascannon OR", "range": "45cm", "firepower": "AT4+"},
                {"name": "Demolisher Cannon (+10)", "range": "15cm & (15cm)",
                 "firepower": "AP4+/AT4+, MW, Ignore cover / (small arms) MW, EA (+1)"},
            ],
            "notes": ["D2.", "Reinforced armour.", "Transport (4 INF)."],
        },
        "sa-shadowsword": {
            "name": "Shadowsword", "type": "WE",
            "speed": "15cm", "armour": "4+", "cc": "6+", "ff": "6+",
            "weapons": [
                {"name": "Volcano Cannon", "range": "90cm",
                 "firepower": "AP2+/AT2+, TK (D3), FxF"},
                {"name": "2× TL Heavy Bolters", "range": "30cm", "firepower": "AP4+"},
            ],
            "notes": ["DC3.", "Reinforced armour.",
                      "Critical Hit: Destroyed, units within 5cm suffer a hit on 6+."],
        },
        "sa-stormblade": {
            "name": "Stormblade", "type": "WE",
            "speed": "15cm", "armour": "4+", "cc": "6+", "ff": "6+",
            "weapons": [
                {"name": "Plasma Blastgun", "range": "45cm",
                 "firepower": "2× AP2+/AT2+, MW, FxF, Slow firing"},
                {"name": "2× Lascannon", "range": "45cm", "firepower": "AT5+"},
                {"name": "2× TL Heavy Bolter", "range": "30cm", "firepower": "AP4+"},
                {"name": "Heavy Bolter", "range": "30cm", "firepower": "AP5+, FxF"},
            ],
            "notes": ["DC3.", "Reinforced armour.",
                      "Critical Hit: Destroyed, units within 5cm suffer a hit on 6+."],
        },
        "sa-stormhammer": {
            "name": "Stormhammer", "type": "WE",
            "speed": "15cm", "armour": "4+", "cc": "6+", "ff": "4+",
            "weapons": [
                {"name": "Stormhammer Cannon", "range": "60cm",
                 "firepower": "AP3+/AT3+, Disrupt, Ignore cover"},
                {"name": "Dual Battlecannon", "range": "75cm",
                 "firepower": "AP3+/AT3+"},
                {"name": "Lascannon", "range": "45cm", "firepower": "AT5+, FxF"},
                {"name": "6× Heavy Bolters", "range": "30cm",
                 "firepower": "AP5+, (3L, 3R)"},
            ],
            "notes": ["DC3.", "Reinforced armour.",
                      "Critical Hit: Destroyed, units within 5cm suffer a hit on 6+."],
        },
        "stormlord": {
            "name": "Stormlord Superheavy Carrier", "type": "WE",
            "speed": "15cm", "armour": "4+", "cc": "6+", "ff": "3+",
            "weapons": [
                {"name": "Vulcan Megabolter", "range": "45cm",
                 "firepower": "4× AP3+/AT5+, FxF"},
                {"name": "2× Heavy Flamers", "range": "15cm & (15cm)",
                 "firepower": "AP5+, Ignore cover / (small arms) Ignore cover"},
                {"name": "3× TL Heavy Bolters", "range": "30cm", "firepower": "AP4+"},
            ],
            "notes": ["DC3.", "Reinforced armour.", "Transport (8 INF).",
                      "Critical Hit: Destroyed, units within 5cm suffer a hit on 6+."],
        },
        "sa-stormsword": {
            "name": "Stormsword", "type": "WE",
            "speed": "15cm", "armour": "4+", "cc": "6+", "ff": "5+",
            "weapons": [
                {"name": "Stormsword Siege Mortar", "range": "30cm & (15cm)",
                 "firepower": "3 BP, Disrupt, Ignore cover / (small arms) Ignore cover"},
                {"name": "2× TL Heavy Bolter", "range": "30cm", "firepower": "AP4+"},
                {"name": "2× Lascannon", "range": "45cm", "firepower": "AT5+"},
            ],
            "notes": ["DC3.", "Reinforced armour.",
                      "Critical Hit: Destroyed, units within 5cm suffer a hit on 6+."],
        },

        # Aircraft & spacecraft
        "avenger-strike-fighter": {
            "name": "Avenger Strike Fighter", "type": "AC",
            "speed": "Bomber", "armour": "5+", "cc": "-", "ff": "-",
            "weapons": [
                {"name": "Avenger Cannon", "range": "30cm",
                 "firepower": "2× AP3+/AT5+, FxF"},
                {"name": "TL Lascannon", "range": "30cm",
                 "firepower": "AT4+/AA5+, FxF"},
                {"name": "Heavy Stubber", "range": "30cm",
                 "firepower": "AA6+, Rwd"},
                {"name": "Kraken Missiles OR", "range": "30cm",
                 "firepower": "AT4+, Single shot, FxF"},
                {"name": "Unguided Bombs", "range": "15cm",
                 "firepower": "1 BP, Single shot, FxF"},
            ],
            "notes": [],
        },
        "lightning-interceptor": {
            "name": "Lightning Interceptor", "type": "AC",
            "speed": "Fighter-bomber", "armour": "6+", "cc": "-", "ff": "-",
            "weapons": [
                {"name": "TL Lascannon", "range": "30cm",
                 "firepower": "AT4+/AA5+, FxF"},
                {"name": "Autocannon", "range": "30cm",
                 "firepower": "AP5+/AT6+/AA5+, FxF"},
                {"name": "Kraken Missiles OR", "range": "30cm",
                 "firepower": "AT4+, Single shot, FxF"},
                {"name": "Skystrike Missiles OR", "range": "30cm",
                 "firepower": "AA5+, Single shot, FxF"},
                {"name": "Unguided Bombs", "range": "15cm",
                 "firepower": "1 BP, Single shot"},
            ],
            "notes": [],
        },
        "marauder-heavy-bomber": {
            "name": "Marauder Heavy Bomber", "type": "WE",
            "speed": "Bomber", "armour": "5+", "cc": "-", "ff": "-",
            "weapons": [
                {"name": "TL Lascannon", "range": "30cm",
                 "firepower": "AT4+/AA5+, FxF"},
                {"name": "2× Defence Turrets", "range": "30cm",
                 "firepower": "AA5+, (1 Rwd)"},
                {"name": "Bombs", "range": "15cm", "firepower": "3 BP"},
            ],
            "notes": ["DC2."],
        },
        "dauntless-cruiser": {
            "name": "Dauntless Light Cruiser", "type": "SC",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [
                {"name": "Orbital Bombardment", "range": "-",
                 "firepower": "3 BP, MW"},
                {"name": "Lance Battery", "range": "Point",
                 "firepower": "AP2+/AT2+, TK (D3)"},
            ],
            "notes": ["Transport (up to 20 INF + enough Arvus to carry them)."],
        },
        "emperor-battleship": {
            "name": "Emperor Battleship", "type": "SC",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [
                {"name": "Orbital Bombardment", "range": "-",
                 "firepower": "8 BP, MW"},
                {"name": "Lance Battery", "range": "Point",
                 "firepower": "AP2+/AT2+, TK (D3)"},
            ],
            "notes": ["Slow and steady — not on turn 1.",
                      "Transport (up to 60 INF + Arvus carriers)."],
        },
    },
}


# =====================================================================
# IMPERIALIS MILITIA
# =====================================================================
imperialis_militia = {
    "id": "imperialis-militia",
    "name": "Imperialis Militia",
    "subtitle": "Imperial Army · The Teeming Masses",
    "color": "#5C6F3C",
    "lore": (
        "The numerical backbone of the Imperium. Where the Astartes break "
        "the enemy line the Imperial Army holds it — billions of soldiers "
        "drawn from a thousand worlds, led by hetmen and watched over by "
        "discipline masters. They lack the lustre of the Legions but in "
        "their hordes of machines, infantry and provincial provenances "
        "they prove that Mankind's greatest weapon is sheer mortal will."
    ),
    "legionTrait": {
        "name": "Provenances of the Imperial Army",
        "description": (
            "Strategy Rating 2 · Initiative 2+. May field 2 Support per "
            "Line, with up to 3 Upgrades per formation. Select up to two "
            "Provenances; each formation chooses one to modify INF stats "
            "(Determined, Feral Warriors, Survivors, Traitors, Void Fighters, "
            "Warrior Elite)."
        ),
    },
    "compositionLimits": COMP_LIMITS_2_3,
    "compositionRules": COMP_RULES_2_3 + [
        "Strategy Rating 2, Initiative 2+.",
        "Includes 1 free Discipline Master per full 750 points (Rogue Psyker if Traitors provenance taken).",
        "Choose up to 2 Provenances for the army; each formation picks one.",
        "Field Gun Battery: 1 per 1,000 pts.  Hydra Flak Battery / Destroyer Tank Hunter: 1 per 2,000 pts.",
        "Militia Command Detachment: 1 per force.  Orbital Support: 1 per force.",
    ],
    "allies": {
        "cohesive": [
            "Knight Households",
            "Legiones Astartes",
            "Legio Titanicus",
        ],
        "disruptive": [
            "Daemons of the Ruinstorm (Traitors only)",
            "Mechanicum Taghmata",
            "Solar Auxilia",
        ],
    },
    "formations": [
        # ----- Line -----
        {
            "id": "conscript-levy-platoon",
            "name": "Conscript Levy Platoon",
            "category": "Line",
            "baseCost": 100,
            "composition": "10 Conscript Squad units",
            "unitOptions": [
                {"label": "10 Conscript Squad",
                 "units": [{"unit": "conscript-squad", "count": 10}]}
            ],
            "allowedUpgrades": ["im-ogryn-brute-squad"],
        },
        {
            "id": "grenadier-platoon",
            "name": "Grenadier Platoon",
            "category": "Line",
            "baseCost": 175,
            "composition": "8 Grenadier units",
            "unitOptions": [
                {"label": "8 Grenadier Squad",
                 "units": [{"unit": "grenadier-squad", "count": 8}]}
            ],
            "allowedUpgrades": ["im-transport", "im-heavy-transport", "im-armoured-support"],
        },
        {
            "id": "infantry-platoon",
            "name": "Infantry Platoon",
            "category": "Line",
            "baseCost": 125,
            "composition": "1 Command Platoon and 7 Infantry Squad units (+15 each additional, up to 11)",
            "unitOptions": [
                {"label": "Platoon Command + 7 Infantry Squad",
                 "units": [{"unit": "platoon-command", "count": 1},
                           {"unit": "infantry-squad", "count": 7}]}
            ],
            "extraUnit": {"unit": "infantry-squad", "cost": 15, "max": 4,
                          "label": "Additional Infantry Squad"},
            "allowedUpgrades": ["im-transport", "im-heavy-transport", "im-armoured-support",
                                "im-fire-support", "im-sniper", "im-ogryn-brute-squad"],
        },
        {
            "id": "militia-command-detachment",
            "name": "Militia Command Detachment",
            "category": "Line",
            "baseCost": 225,
            "composition": "1 Force Command Platoon and 7 Infantry Squad units (1 per force)",
            "unitOptions": [
                {"label": "Force Command + 7 Infantry Squad",
                 "units": [{"unit": "force-command", "count": 1},
                           {"unit": "infantry-squad", "count": 7}]}
            ],
            "maxPerArmy": 1,
            "allowedUpgrades": ["im-transport", "im-heavy-transport", "im-armoured-support",
                                "im-fire-support", "im-sniper", "im-ogryn-brute-squad"],
        },
        {
            "id": "motorcycle-platoon",
            "name": "Motorcycle Platoon",
            "category": "Line",
            "baseCost": 175,
            "composition": "1 Motorcycle Command and 7 Motorcycle Squad units",
            "unitOptions": [
                {"label": "Motorcycle Command + 7 Motorcycle Squad",
                 "units": [{"unit": "motorcycle-command", "count": 1},
                           {"unit": "motorcycle-squad", "count": 7}]}
            ],
            "allowedUpgrades": [],
        },

        # ----- Support -----
        {
            "id": "cavalry-squadron",
            "name": "Cavalry Squadron",
            "category": "Support",
            "baseCost": 175,
            "composition": "6 Cavalry units",
            "unitOptions": [
                {"label": "6 Cavalry",
                 "units": [{"unit": "cavalry-squadron", "count": 6}]}
            ],
            "allowedUpgrades": [],
        },
        {
            "id": "im-rapier-battery",
            "name": "Rapier Battery",
            "category": "Support",
            "baseCost": 125,
            "composition": "4 Rapier Platforms",
            "unitOptions": [
                {"label": "4 Rapier Platforms",
                 "units": [{"unit": "im-rapier-platform", "count": 4}]}
            ],
            "allowedUpgrades": [],
        },
        {
            "id": "field-gun-battery",
            "name": "Field Gun Battery",
            "category": "Support",
            "baseCost": 200,
            "composition": "3 Earthshaker OR Medusa Gun Carriages (1 per 1,000 pts)",
            "unitOptions": [
                {"label": "3 Earthshaker Gun Carriages",
                 "units": [{"unit": "earthshaker-gun-carriage", "count": 3}]},
                {"label": "3 Medusa Gun Carriages",
                 "units": [{"unit": "medusa-gun-carriage", "count": 3}]},
            ],
            "allowedUpgrades": [],
        },
        {
            "id": "hydra-flak-battery",
            "name": "Hydra Flak Battery",
            "category": "Support",
            "baseCost": 225,
            "composition": "3 Hydra Flak Vehicles (1 per 2,000 pts)",
            "unitOptions": [
                {"label": "3 Hydra Flak Vehicles",
                 "units": [{"unit": "hydra-flak", "count": 3}]}
            ],
            "allowedUpgrades": [],
        },
        {
            "id": "im-sentinel-squadron",
            "name": "Sentinel Squadron",
            "category": "Support",
            "baseCost": 100,
            "composition": "4 Sentinels",
            "unitOptions": [
                {"label": "4 Scout Sentinels",
                 "units": [{"unit": "scout-sentinel", "count": 4}]}
            ],
            "allowedUpgrades": [],
        },
        {
            "id": "salamander-squadron",
            "name": "Salamander Squadron",
            "category": "Support",
            "baseCost": 125,
            "composition": "3 Salamander Scout Tanks",
            "unitOptions": [
                {"label": "3 Salamander Scout Tanks",
                 "units": [{"unit": "salamander-scout-tank", "count": 3}]}
            ],
            "allowedUpgrades": [],
        },
        {
            "id": "battle-tank-squadron",
            "name": "Battle Tank Squadron",
            "category": "Support",
            "baseCost": 300,
            "composition": "4 Leman Russ Battle, Exterminator or Demolisher (+50 each, up to 6)",
            "unitOptions": [
                {"label": "4 Leman Russ Battle Tank",
                 "units": [{"unit": "im-leman-russ-battle", "count": 4}]},
                {"label": "4 Leman Russ Exterminator",
                 "units": [{"unit": "im-leman-russ-exterminator", "count": 4}]},
                {"label": "4 Leman Russ Demolisher",
                 "units": [{"unit": "im-leman-russ-demolisher", "count": 4}]},
            ],
            "extraUnit": {"unit": "im-leman-russ-battle", "cost": 50, "max": 2,
                          "label": "Additional Leman Russ"},
            "allowedUpgrades": ["im-vanquisher"],
        },
        {
            "id": "im-heavy-tank-squadron",
            "name": "Heavy Tank Squadron",
            "category": "Support",
            "baseCost": 300,
            "composition": "4 Malcadors or Malcador Annihilators (+50 each, up to 6)",
            "unitOptions": [
                {"label": "4 Malcador Heavy Tanks",
                 "units": [{"unit": "im-malcador-heavy", "count": 4}]},
                {"label": "4 Malcador Annihilators",
                 "units": [{"unit": "malcador-annihilator", "count": 4}]},
            ],
            "extraUnit": {"unit": "im-malcador-heavy", "cost": 50, "max": 2,
                          "label": "Additional Malcador"},
            "allowedUpgrades": [],
        },
        {
            "id": "im-super-heavy-tank",
            "name": "Super Heavy Tank",
            "category": "Support",
            "baseCost": 200,
            "composition": "1 Baneblade OR Shadowsword OR Stormhammer",
            "unitOptions": [
                {"label": "1 Baneblade", "units": [{"unit": "im-baneblade", "count": 1}]},
                {"label": "1 Shadowsword", "units": [{"unit": "im-shadowsword", "count": 1}]},
                {"label": "1 Stormhammer", "units": [{"unit": "im-stormhammer", "count": 1}]},
            ],
            "allowedUpgrades": [],
        },

        # ----- Lords of War -----
        {
            "id": "destroyer-tank-hunter-squadron",
            "name": "Destroyer Tank Hunter Squadron",
            "category": "Lords of War",
            "baseCost": 200,
            "composition": "3 Destroyer Tank Hunters (1 per 2,000 pts)",
            "unitOptions": [
                {"label": "3 Destroyer Hunters",
                 "units": [{"unit": "destroyer-hunter", "count": 3}]}
            ],
            "allowedUpgrades": [],
        },
        {
            "id": "im-super-heavy-tank-platoon",
            "name": "Super Heavy Tank Platoon",
            "category": "Lords of War",
            "baseCost": 500,
            "composition": "3 Baneblades or Stormhammers",
            "unitOptions": [
                {"label": "3 Baneblades", "units": [{"unit": "im-baneblade", "count": 3}]},
                {"label": "3 Stormhammers", "units": [{"unit": "im-stormhammer", "count": 3}]},
            ],
            "allowedUpgrades": [],
        },
        {
            "id": "im-navy-avenger-flight",
            "name": "Imperial Navy Avenger Strike Fighter Flight",
            "category": "Lords of War",
            "baseCost": 225,
            "composition": "2 Avenger Strike Fighters (+125 each, up to 3)",
            "unitOptions": [
                {"label": "2 Avenger Strike Fighters",
                 "units": [{"unit": "avenger-strike-fighter", "count": 2}]}
            ],
            "extraUnit": {"unit": "avenger-strike-fighter", "cost": 125, "max": 1,
                          "label": "Additional Avenger"},
            "allowedUpgrades": [],
        },
        {
            "id": "im-navy-lightning-flight",
            "name": "Imperial Navy Lightning Interceptor Flight",
            "category": "Lords of War",
            "baseCost": 225,
            "composition": "2 Lightning Interceptors (+125 each, up to 3)",
            "unitOptions": [
                {"label": "2 Lightning Interceptors",
                 "units": [{"unit": "lightning-interceptor", "count": 2}]}
            ],
            "extraUnit": {"unit": "lightning-interceptor", "cost": 125, "max": 1,
                          "label": "Additional Lightning"},
            "allowedUpgrades": [],
        },
        {
            "id": "im-navy-marauder",
            "name": "Imperial Navy Marauder Heavy Bomber",
            "category": "Lords of War",
            "baseCost": 325,
            "composition": "2 Marauder Heavy Bombers",
            "unitOptions": [
                {"label": "2 Marauder Heavy Bombers",
                 "units": [{"unit": "marauder-heavy-bomber", "count": 2}]}
            ],
            "allowedUpgrades": [],
        },
        {
            "id": "im-orbital-support",
            "name": "Orbital Support",
            "category": "Lords of War",
            "baseCost": 150,
            "composition": "1 Dauntless Cruiser OR Emperor Battleship (1 per force)",
            "unitOptions": [
                {"label": "1 Dauntless Light Cruiser",
                 "units": [{"unit": "dauntless-cruiser", "count": 1}]},
                {"label": "1 Emperor Battleship",
                 "units": [{"unit": "emperor-battleship", "count": 1}],
                 "costOverride": 300},
            ],
            "maxPerArmy": 1,
            "allowedUpgrades": [],
        },
    ],
    "upgrades": [
        {"id": "im-armoured-support", "name": "Armoured Support", "type": "multi", "max": 2,
         "description": "Add 1-2 Leman Russ Battle / Demolisher / Exterminator OR Malcador Heavy Tank.",
         "variants": [
             {"id": "im-leman-russ-battle", "name": "Leman Russ Battle Tank", "cost": 75},
             {"id": "im-leman-russ-demolisher", "name": "Leman Russ Demolisher", "cost": 75},
             {"id": "im-leman-russ-exterminator", "name": "Leman Russ Exterminator", "cost": 75},
             {"id": "im-malcador-heavy", "name": "Malcador Heavy Tank", "cost": 75},
         ]},
        {"id": "im-fire-support", "name": "Fire Support", "type": "flag", "cost": 100,
         "description": "Add 4 Fire Support Team units."},
        {"id": "im-heavy-transport", "name": "Heavy Transport", "type": "multi",
         "description": "Add enough Gorgon Heavy Transporters OR Stormlords to carry the formation.",
         "variants": [
             {"id": "gorgon", "name": "Gorgon Assault Transport", "cost": 100},
             {"id": "stormlord", "name": "Stormlord Superheavy Carrier", "cost": 200},
         ]},
        {"id": "im-ogryn-brute-squad", "name": "Ogryn Brute Squad", "type": "flag", "cost": 150,
         "description": "Add 4 Ogryn Brute units."},
        {"id": "im-sniper", "name": "Snipers", "type": "flag", "cost": 75,
         "description": "Add 4 Recon Team units."},
        {"id": "im-transport", "name": "Transport", "type": "multi",
         "description": "Add enough Aurox, Arvus Lighters OR Land Raider Proteus to carry the formation.",
         "variants": [
             {"id": "aurox", "name": "Aurox Transport", "cost": 10},
             {"id": "arvus", "name": "Arvus Lighter", "cost": 25},
             {"id": "land-raider-proteus", "name": "Land Raider Proteus", "cost": 50},
         ]},
        {"id": "im-vanquisher", "name": "Vanquisher", "type": "flag", "cost": 25,
         "description": "Upgrade 1 unit to a Leman Russ Vanquisher."},
    ],
    "units": {
        # Characters & infantry
        "discipline-master": {
            "name": "Discipline Master", "type": "CH",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [{"name": "Power Weapon", "range": "(base)",
                        "firepower": "(assault) Fleshbane, EA (+1)"}],
            "notes": ["Inspiring.", "Leader."],
        },
        "rogue-psyker": {
            "name": "Rogue Psyker", "type": "CH",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [{"name": "Psychic Bolt", "range": "(15cm)",
                        "firepower": "(small arms) MW, EA (+1)"}],
            "notes": ["Fearless.", "Inspiring."],
        },
        "cavalry-squadron": {
            "name": "Cavalry Squadron", "type": "INF",
            "speed": "20cm", "armour": "6+", "cc": "4+", "ff": "6+",
            "weapons": [{"name": "Power Lances", "range": "(base)",
                        "firepower": "(assault) First strike, EA (+1)"}],
            "notes": ["Infiltrate.", "Mounted.", "Scout."],
        },
        "conscript-squad": {
            "name": "Conscript Squad", "type": "INF",
            "speed": "15cm", "armour": "-", "cc": "6+", "ff": "6+",
            "weapons": [{"name": "Issued Weapons", "range": "(15cm)",
                        "firepower": "(small arms)"}],
            "notes": [],
        },
        "force-command": {
            "name": "Force Command", "type": "INF",
            "speed": "15cm", "armour": "5+", "cc": "5+", "ff": "5+",
            "weapons": [
                {"name": "Archeotech Pistol", "range": "(15cm)",
                 "firepower": "(small arms) MW, EA (+1)"},
                {"name": "Support Weapons", "range": "15cm",
                 "firepower": "2× AP5+/AT5+"},
            ],
            "notes": ["Supreme Commander.", "Invulnerable save.",
                      "Counts as a character unit for Bodyguard / Strategic Value."],
        },
        "fire-support-team": {
            "name": "Fire Support Team", "type": "INF",
            "speed": "15cm", "armour": "6+", "cc": "6+", "ff": "4+ (6+)",
            "weapons": [
                {"name": "Heavy Stubber OR", "range": "30cm",
                 "firepower": "2× AP5+"},
                {"name": "Missile Launcher", "range": "45cm & 30cm",
                 "firepower": "AT5+ / AA6+"},
            ],
            "notes": [],
        },
        "grenadier-squad": {
            "name": "Grenadier Squad", "type": "INF",
            "speed": "15cm", "armour": "5+", "cc": "5+", "ff": "5+",
            "weapons": [
                {"name": "Lascarbines", "range": "(15cm)",
                 "firepower": "(small arms)"},
                {"name": "Support Weapon", "range": "15cm",
                 "firepower": "AP5+/AT5+"},
            ],
            "notes": [],
        },
        "infantry-squad": {
            "name": "Infantry Squad", "type": "INF",
            "speed": "15cm", "armour": "6+", "cc": "6+ / 5+", "ff": "5+ / 6+",
            "weapons": [
                {"name": "Rifles OR", "range": "(15cm)",
                 "firepower": "(small arms)"},
                {"name": "Pistols and Blades", "range": "(base)",
                 "firepower": "(assault)"},
            ],
            "notes": [],
        },
        "motorcycle-command": {
            "name": "Motorcycle Command", "type": "INF",
            "speed": "30cm", "armour": "6+", "cc": "6+ / 5+", "ff": "5+ / 6+",
            "weapons": [
                {"name": "Rifles OR", "range": "(15cm)",
                 "firepower": "(small arms)"},
                {"name": "Pistols and Blades", "range": "(base)",
                 "firepower": "(assault)"},
            ],
            "notes": ["Commander.", "Mounted."],
        },
        "motorcycle-squad": {
            "name": "Motorcycle Squad", "type": "INF",
            "speed": "30cm", "armour": "6+", "cc": "6+ / 5+", "ff": "5+ / 6+",
            "weapons": [
                {"name": "Rifles OR", "range": "(15cm)",
                 "firepower": "(small arms)"},
                {"name": "Pistols and Blades", "range": "(base)",
                 "firepower": "(assault)"},
            ],
            "notes": ["Mounted."],
        },
        "ogryn-brute-squad": {
            "name": "Ogryn Brute Squad", "type": "INF",
            "speed": "15cm", "armour": "4+", "cc": "4+ / 5+ / 4+", "ff": "5+ / 3+ / 6+",
            "weapons": [
                {"name": "Power Weapons OR", "range": "(base)",
                 "firepower": "(assault) MW, EA (+1)"},
                {"name": "Ripper Guns OR", "range": "(15cm)",
                 "firepower": "(small arms) EA (+1)"},
                {"name": "Chaos Spawn Mutations (Traitors)", "range": "(base)",
                 "firepower": "(assault) EA (+D3)"},
            ],
            "notes": ["Bodyguard.", "Each Ogryn counts as 2 units for transport."],
        },
        "platoon-command": {
            "name": "Platoon Command", "type": "INF",
            "speed": "15cm", "armour": "6+", "cc": "5+", "ff": "4+",
            "weapons": [{"name": "Heavy Stubber", "range": "30cm",
                        "firepower": "2× AP5+"}],
            "notes": ["Commander.",
                      "Counts as a character unit for Bodyguard / Strategic Value."],
        },
        "im-rapier-platform": {
            "name": "Rapier Platform", "type": "INF",
            "speed": "10cm", "armour": "6+", "cc": "6+", "ff": "6+ (4+)",
            "weapons": [
                {"name": "Laser Destroyer OR", "range": "45cm",
                 "firepower": "AT4+, Armourbane"},
                {"name": "Quad Mortar OR", "range": "45cm",
                 "firepower": "AP5+/AT6+, Indirect fire, Disrupt"},
                {"name": "Quad Heavy Bolter", "range": "30cm",
                 "firepower": "2× AP4+"},
            ],
            "notes": ["Mounted."],
        },
        "recon-team": {
            "name": "Recon Team", "type": "INF",
            "speed": "15cm", "armour": "6+", "cc": "6+", "ff": "5+",
            "weapons": [{"name": "Sniper Rifles", "range": "30cm",
                        "firepower": "AP5+, Sniper"}],
            "notes": ["Scout."],
        },

        # Light / armoured vehicles
        "earthshaker-gun-carriage": {
            "name": "Earthshaker Gun Carriage", "type": "LV",
            "speed": "0cm", "armour": "5+", "cc": "6+", "ff": "6+",
            "weapons": [{"name": "Earthshaker Cannon", "range": "120cm",
                        "firepower": "AP4+/AT4+ OR 1 BP, Indirect fire"}],
            "notes": [],
        },
        "medusa-gun-carriage": {
            "name": "Medusa Gun Carriage", "type": "LV",
            "speed": "0cm", "armour": "5+", "cc": "6+", "ff": "6+",
            "weapons": [{"name": "Medusa Siege Mortar", "range": "30cm",
                        "firepower": "AP4+/AT4+, MW, Indirect fire, Ignore cover"}],
            "notes": [],
        },
        "scout-sentinel": {
            "name": "Scout Sentinel", "type": "LV",
            "speed": "20cm", "armour": "6+", "cc": "6+", "ff": "5+",
            "weapons": [{"name": "Multilaser", "range": "30cm",
                        "firepower": "AP5+/AT6+"}],
            "notes": ["Scout.", "Walker."],
        },
        "salamander-scout-tank": {
            "name": "Salamander Scout Tank", "type": "LV",
            "speed": "30cm", "armour": "6+", "cc": "6+", "ff": "5+",
            "weapons": [
                {"name": "Autocannon", "range": "45cm",
                 "firepower": "AP5+/AT6+"},
                {"name": "Heavy Bolter", "range": "30cm", "firepower": "AP5+"},
            ],
            "notes": ["Scout."],
        },
        "arvus": {
            "name": "Arvus Lighter Orbital Shuttle", "type": "AV",
            "speed": "40cm", "armour": "5+", "cc": "6+", "ff": "- (5+)",
            "weapons": [{"name": "Multilaser (+10 optional)", "range": "30cm & (15cm)",
                        "firepower": "AP5+/AT6+ / (small arms)"}],
            "notes": ["Skimmer.", "Planetfall.", "Transport (2 INF)."],
        },
        "aurox": {
            "name": "Aurox Transport", "type": "AV",
            "speed": "30cm", "armour": "5+", "cc": "6+", "ff": "5+",
            "weapons": [{"name": "Heavy Stubber", "range": "(15cm)",
                        "firepower": "(small arms)"}],
            "notes": ["Transport (2 INF)."],
        },
        "destroyer-hunter": {
            "name": "Destroyer Tank Hunter", "type": "AV",
            "speed": "25cm", "armour": "4+", "cc": "6+", "ff": "6+",
            "weapons": [{"name": "Heavy Laser Destroyer", "range": "75cm",
                        "firepower": "AT3+, Armourbane"}],
            "notes": ["Reinforced armour.", "Scout."],
        },
        "hydra-flak": {
            "name": "Hydra Flak Vehicle", "type": "AV",
            "speed": "30cm", "armour": "5+", "cc": "6+", "ff": "5+",
            "weapons": [
                {"name": "Hydra Autocannons", "range": "45cm",
                 "firepower": "2× AP4+/AT5+/AA5+"},
                {"name": "Heavy Bolter", "range": "30cm", "firepower": "AP5+"},
            ],
            "notes": [],
        },
        "land-raider-proteus": {
            "name": "Land Raider Proteus", "type": "AV",
            "speed": "25cm", "armour": "4+", "cc": "6+", "ff": "5+",
            "weapons": [{"name": "2× TL Lascannons", "range": "45cm",
                        "firepower": "AT4+"}],
            "notes": ["Reinforced armour.", "Thick rear armour.",
                      "Exploratory augury web.", "Transport (2 INF)."],
        },
        "im-leman-russ-battle": {
            "name": "Leman Russ Battle Tank", "type": "AV",
            "speed": "25cm", "armour": "4+", "cc": "6+", "ff": "4+",
            "weapons": [
                {"name": "Battlecannon", "range": "75cm", "firepower": "AP4+/AT4+"},
                {"name": "Lascannon", "range": "45cm", "firepower": "AT5+"},
                {"name": "2× Heavy Bolters", "range": "30cm", "firepower": "AP5+"},
            ],
            "notes": ["Reinforced armour."],
        },
        "im-leman-russ-demolisher": {
            "name": "Leman Russ Demolisher Siege Tank", "type": "AV",
            "speed": "20cm", "armour": "4+", "cc": "6+", "ff": "4+",
            "weapons": [
                {"name": "Demolisher Cannon", "range": "15cm & (15cm)",
                 "firepower": "AP4+/AT4+, MW, Ignore cover / (small arms) MW"},
                {"name": "Lascannon", "range": "45cm", "firepower": "AP5+"},
                {"name": "2× Heavy Bolters", "range": "30cm", "firepower": "AP4+"},
            ],
            "notes": ["Reinforced armour.", "Thick rear armour."],
        },
        "im-leman-russ-exterminator": {
            "name": "Leman Russ Exterminator", "type": "AV",
            "speed": "25cm", "armour": "4+", "cc": "6+", "ff": "4+",
            "weapons": [
                {"name": "Exterminator Cannon", "range": "45cm",
                 "firepower": "2× AP4+/AT6+"},
                {"name": "Lascannon", "range": "45cm", "firepower": "AT5+"},
                {"name": "2× Heavy Bolters", "range": "30cm", "firepower": "AP5+"},
            ],
            "notes": ["Reinforced armour."],
        },
        "im-leman-russ-vanquisher": {
            "name": "Leman Russ Vanquisher", "type": "AV",
            "speed": "25cm", "armour": "4+", "cc": "6+", "ff": "4+",
            "weapons": [
                {"name": "Vanquisher Cannon", "range": "75cm",
                 "firepower": "AP4+/AT3+, Armourbane"},
                {"name": "Lascannon", "range": "45cm", "firepower": "AT5+"},
                {"name": "2× Heavy Bolters", "range": "30cm", "firepower": "AP5+"},
            ],
            "notes": ["Reinforced armour."],
        },
        "im-malcador-heavy": {
            "name": "Malcador Heavy Tank", "type": "AV",
            "speed": "15cm", "armour": "4+", "cc": "6+", "ff": "5+",
            "weapons": [
                {"name": "Battlecannon", "range": "75cm", "firepower": "AP4+/AT4+"},
                {"name": "2× Lascannons", "range": "45cm", "firepower": "AT5+"},
                {"name": "Heavy Bolter", "range": "30cm", "firepower": "AP5+"},
            ],
            "notes": ["Reinforced armour."],
        },
        "malcador-annihilator": {
            "name": "Malcador Annihilator Heavy Tank", "type": "AV",
            "speed": "15cm", "armour": "4+", "cc": "6+", "ff": "5+",
            "weapons": [
                {"name": "TL Lascannon", "range": "45cm", "firepower": "AT4+"},
                {"name": "2× Lascannon", "range": "45cm", "firepower": "AT5+"},
                {"name": "Demolisher Cannon", "range": "15cm & (15cm)",
                 "firepower": "AP4+/AT4+, MW, Ignore cover / (small arms) MW"},
            ],
            "notes": ["Reinforced armour."],
        },

        # War engines
        "im-baneblade": {
            "name": "Baneblade Superheavy Tank", "type": "WE",
            "speed": "15cm", "armour": "4+", "cc": "6+", "ff": "4+",
            "weapons": [
                {"name": "Baneblade Cannon", "range": "75cm",
                 "firepower": "AP3+/AT3+, MW"},
                {"name": "Coaxial Autocannon", "range": "45cm",
                 "firepower": "AP5+/AT6+"},
                {"name": "Demolisher Cannon", "range": "15cm & (15cm)",
                 "firepower": "AP4+/AT4+, MW, Ignore cover / (small arms) MW, EA (+1)"},
                {"name": "2× Lascannon", "range": "45cm", "firepower": "AT5+"},
                {"name": "3× TL Heavy Bolter", "range": "30cm", "firepower": "AP4+"},
            ],
            "notes": ["DC3.", "Reinforced armour.",
                      "Critical Hit: Destroyed, units within 5cm suffer a hit on 6+."],
        },
        "gorgon": {
            "name": "Gorgon Assault Transport", "type": "WE",
            "speed": "15cm", "armour": "4+", "cc": "6+", "ff": "5+",
            "weapons": [
                {"name": "2× TL Autocannons", "range": "45cm",
                 "firepower": "AP4+/AT5+"},
                {"name": "Gorgon Mortars OR", "range": "30cm",
                 "firepower": "2 BP, Indirect fire, Single shot, Fwd"},
                {"name": "2× TL Heavy Bolters", "range": "30cm",
                 "firepower": "AP4+"},
            ],
            "notes": ["DC3.", "Reinforced armour.", "Transport (8 INF).",
                      "Critical Hit: Destroyed, units within 5cm suffer a hit on 6+."],
        },
        "im-shadowsword": {
            "name": "Shadowsword Superheavy Tank Destroyer", "type": "WE",
            "speed": "15cm", "armour": "4+", "cc": "6+", "ff": "5+",
            "weapons": [
                {"name": "Volcano Cannon", "range": "90cm",
                 "firepower": "AP2+/AT2+, TK(D3), FxF"},
                {"name": "2× TL Heavy Bolters", "range": "30cm", "firepower": "AP4+"},
            ],
            "notes": ["DC3.", "Reinforced armour.",
                      "Critical Hit: Destroyed, units within 5cm suffer a hit on 6+."],
        },
        "im-stormhammer": {
            "name": "Stormhammer Superheavy Tank", "type": "WE",
            "speed": "15cm", "armour": "4+", "cc": "6+", "ff": "4+",
            "weapons": [
                {"name": "Stormhammer Cannon", "range": "60cm",
                 "firepower": "AP3+/AT3+, Disrupt, Ignore cover"},
                {"name": "Dual Battlecannon", "range": "75cm",
                 "firepower": "AP3+/AT3+, FxF"},
                {"name": "Lascannon", "range": "45cm", "firepower": "AT5+"},
                {"name": "6× Heavy Bolters", "range": "30cm", "firepower": "AP5+"},
            ],
            "notes": ["DC3.", "Reinforced armour.",
                      "Critical Hit: Destroyed, units within 5cm suffer a hit on 6+."],
        },
        "stormlord": {
            "name": "Stormlord Superheavy Carrier", "type": "WE",
            "speed": "15cm", "armour": "4+", "cc": "6+", "ff": "3+",
            "weapons": [
                {"name": "Vulcan Megabolter", "range": "45cm",
                 "firepower": "4× AP3+/AT5+, FxF"},
                {"name": "2× Heavy Flamers", "range": "15cm & (15cm)",
                 "firepower": "AP5+, Ignore cover / (small arms) Ignore cover"},
                {"name": "3× TL Heavy Bolters", "range": "30cm", "firepower": "AP4+"},
            ],
            "notes": ["DC3.", "Reinforced armour.", "Transport (8 INF)."],
        },

        # Aircraft & spacecraft (shared rosters with SA)
        "avenger-strike-fighter": {
            "name": "Avenger Strike Fighter", "type": "AC",
            "speed": "Bomber", "armour": "5+", "cc": "-", "ff": "-",
            "weapons": [
                {"name": "Avenger Cannon", "range": "30cm",
                 "firepower": "2× AP3+/AT5+, FxF"},
                {"name": "TL Lascannon", "range": "30cm",
                 "firepower": "AT4+/AA5+, FxF"},
                {"name": "Heavy Stubber", "range": "30cm",
                 "firepower": "AA6+, Rwd"},
                {"name": "Kraken Missiles OR", "range": "30cm",
                 "firepower": "AT4+, Single shot, FxF"},
                {"name": "Unguided Bombs", "range": "15cm",
                 "firepower": "1 BP, Single shot, FxF"},
            ],
            "notes": [],
        },
        "lightning-interceptor": {
            "name": "Lightning Interceptor", "type": "AC",
            "speed": "Fighter-bomber", "armour": "6+", "cc": "-", "ff": "-",
            "weapons": [
                {"name": "TL Lascannon", "range": "30cm",
                 "firepower": "AT4+/AA5+, FxF"},
                {"name": "Autocannon", "range": "30cm",
                 "firepower": "AP5+/AT6+/AA5+, FxF"},
                {"name": "Kraken Missiles OR", "range": "30cm",
                 "firepower": "AT4+, Single shot, FxF"},
                {"name": "Skystrike Missiles OR", "range": "30cm",
                 "firepower": "AA5+, Single shot, FxF"},
                {"name": "Unguided Bombs", "range": "15cm",
                 "firepower": "1 BP, Single shot"},
            ],
            "notes": [],
        },
        "marauder-heavy-bomber": {
            "name": "Marauder Heavy Bomber", "type": "WE",
            "speed": "Bomber", "armour": "5+", "cc": "-", "ff": "-",
            "weapons": [
                {"name": "TL Lascannon", "range": "30cm",
                 "firepower": "AT4+/AA5+, FxF"},
                {"name": "2× Defence Turrets", "range": "30cm",
                 "firepower": "AA5+, (1 Rwd)"},
                {"name": "Bombs", "range": "15cm", "firepower": "3 BP"},
            ],
            "notes": ["DC2."],
        },
        "dauntless-cruiser": {
            "name": "Dauntless Light Cruiser", "type": "SC",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [
                {"name": "Orbital Bombardment", "range": "-",
                 "firepower": "3 BP, MW"},
                {"name": "Lance Battery", "range": "Point",
                 "firepower": "AP2+/AT2+, TK (D3)"},
            ],
            "notes": ["Transport (up to 20 INF + Arvus carriers)."],
        },
        "emperor-battleship": {
            "name": "Emperor Battleship", "type": "SC",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [
                {"name": "Orbital Bombardment", "range": "-",
                 "firepower": "8 BP, MW"},
                {"name": "Lance Battery", "range": "Point",
                 "firepower": "AP2+/AT2+, TK (D3)"},
            ],
            "notes": ["Slow and steady — not on turn 1.",
                      "Transport (up to 60 INF + Arvus carriers)."],
        },
    },
}


def main():
    doc = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    factions = doc["factions"]

    # Remove any existing entries with the same IDs (idempotent).
    new_ids = {solar_auxilia["id"], imperialis_militia["id"]}
    factions = [f for f in factions if f["id"] not in new_ids]
    factions.append(solar_auxilia)
    factions.append(imperialis_militia)

    doc["factions"] = factions
    DATA_PATH.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
                          encoding="utf-8")

    print(f"OK — wrote {len(factions)} factions to {DATA_PATH}")
    print(f"  Added/updated: solar-auxilia ({len(solar_auxilia['formations'])} forms, "
          f"{len(solar_auxilia['units'])} units)")
    print(f"  Added/updated: imperialis-militia ({len(imperialis_militia['formations'])} forms, "
          f"{len(imperialis_militia['units'])} units)")


if __name__ == "__main__":
    main()
