"""
Idempotent: appends Mechanicum Taghmata, Legio Custodes and Daemons of
the Ruinstorm to backend/data/factions.json.

Source: /app/pdf_work/eoa.txt — Empire of Ashes, pp. 41–46, 63–68.
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "factions.json"

# Mechanicum uses default Astartes limits (3 Support / 4 Upgrades / 33% LoW).
# Legio Custodes: 3/4 but 50% LoW.
# Daemons: 1 Support per Line, any number of Upgrades (each once), 33% LoW.
LIMITS_MECH = None  # falls back to defaults
LIMITS_CUSTODES = {"maxSupportPerLine": 3, "maxUpgradesPerLine": 4, "lowPct": 0.50}
LIMITS_DAEMONS = {"maxSupportPerLine": 1, "maxUpgradesPerLine": 99, "lowPct": 0.33}


# =====================================================================
# MECHANICUM TAGHMATA
# =====================================================================
mechanicum = {
    "id": "mechanicum-taghmata",
    "name": "Mechanicum Taghmata",
    "subtitle": "Cult of Mars · Phalanx of the Omnissiah",
    "color": "#6B0F0F",
    "lore": (
        "The techno-guard of the Mechanicum, second only to the Titan Legions "
        "in might. Adsecularis thralls, lightning-armed Thallax, insectoid Vorax "
        "and towering Thanatar cybernetica march beneath the gear-and-skull "
        "icon of Mars. As the Heresy fractures the priesthood itself, the "
        "forge-worlds align with Loyalist or Traitor, and their forbidden "
        "knowledge becomes both prize and weapon."
    ),
    "legionTrait": {
        "name": "Servants of the Omnissiah",
        "description": (
            "Strategy Rating 3 · Initiative 2+. 3 Support per Line, max 4 "
            "Upgrades per formation, 1/3 cap on Lords of War/Allies. Special "
            "Rules: Automaton, Cortex Controller / Cybernetica Cortex. "
            "Optional Mechanicum Trait: Targeting Algorithm — Tech-Priest or "
            "Magos formations may forgo countercharge to add +1 Firefight in assault."
        ),
    },
    "compositionLimits": LIMITS_MECH,
    "compositionRules": [
        "Strategy Rating 3, Initiative 2+.",
        "Max 3 Support per Line, max 4 Upgrades per formation, max 1/3 of points on Lords of War/Allies.",
        "Special: Automaton (no Blast marker on destruction; Disrupt overrides).",
        "Special: Cybernetica Cortex — -1 Action tests, no March/Overwatch unless within 15cm of a Cortex Controller.",
        "Ordinatus Minorus Tormenta: 1 per 2,000 pts.",
        "Ordinatus Majoris and Ark Mechanicus: 1 per force each.",
        "Optional Trait: Targeting Algorithm.",
    ],
    "allies": {
        "cohesive": ["Legiones Astartes", "Knight Households", "Legio Titanicus"],
        "disruptive": ["Imperialis Militia", "Solar Auxilia"],
    },
    "formations": [
        # ----- Line -----
        {"id": "adsecularis-covenant", "name": "Adsecularis Covenant", "category": "Line",
         "baseCost": 150,
         "composition": "10 Tech-thrall and 2 Tech-Priest units",
         "unitOptions": [{"label": "10 Tech-Thrall + 2 Tech-Priests",
                          "units": [{"unit": "tech-thrall", "count": 10},
                                    {"unit": "tech-priest", "count": 2}]}],
         "allowedUpgrades": ["mech-transport", "mech-magos", "mech-scyllax", "mech-krios"]},
        {"id": "thallax-cohort", "name": "Thallax Cohort", "category": "Line",
         "baseCost": 300,
         "composition": "6 Thallax units",
         "unitOptions": [{"label": "6 Thallax",
                          "units": [{"unit": "thallax", "count": 6}]}],
         "allowedUpgrades": ["mech-transport", "mech-magos", "mech-tech-priest",
                             "mech-scyllax", "mech-krios"]},
        {"id": "ursarax-cohort", "name": "Ursarax Cohort", "category": "Line",
         "baseCost": 250,
         "composition": "6 Ursarax units",
         "unitOptions": [{"label": "6 Ursarax",
                          "units": [{"unit": "ursarax", "count": 6}]}],
         "allowedUpgrades": ["mech-transport", "mech-tech-priest"]},
        {"id": "vorax-maniple", "name": "Vorax Maniple", "category": "Line",
         "baseCost": 250,
         "composition": "6 Vorax Battle Automata",
         "unitOptions": [{"label": "6 Vorax",
                          "units": [{"unit": "vorax", "count": 6}]}],
         "allowedUpgrades": ["mech-tech-priest"]},
        {"id": "castellax-maniple", "name": "Castellax Maniple", "category": "Line",
         "baseCost": 250,
         "composition": "4 Castellax and 2 Tech-Priests (+40 each Castellax, up to 6)",
         "unitOptions": [{"label": "4 Castellax + 2 Tech-Priests",
                          "units": [{"unit": "castellax", "count": 4},
                                    {"unit": "tech-priest", "count": 2}]}],
         "extraUnit": {"unit": "castellax", "cost": 40, "max": 2,
                       "label": "Additional Castellax"},
         "allowedUpgrades": ["mech-magos", "mech-scyllax", "mech-thanatar"]},

        # ----- Support -----
        {"id": "myrmidon-sect", "name": "Myrmidon Sect", "category": "Support",
         "baseCost": 300,
         "composition": "6 Myrmidon Secutor OR Destructor units",
         "unitOptions": [{"label": "6 Myrmidon Secutors",
                          "units": [{"unit": "myrmidon-secutor", "count": 6}]},
                         {"label": "6 Myrmidon Destructors",
                          "units": [{"unit": "myrmidon-destructor", "count": 6}]}],
         "allowedUpgrades": ["mech-transport", "mech-magos", "mech-scyllax", "mech-krios"]},
        {"id": "arletax-maniple", "name": "Arletax Maniple", "category": "Support",
         "baseCost": 250,
         "composition": "4 Arletax Battle-Automata (+60 each, up to 6)",
         "unitOptions": [{"label": "4 Arletax",
                          "units": [{"unit": "arletax", "count": 4}]}],
         "extraUnit": {"unit": "arletax", "cost": 60, "max": 2, "label": "Additional Arletax"},
         "allowedUpgrades": ["mech-magos", "mech-tech-priest", "mech-scyllax"]},
        {"id": "domitar-maniple", "name": "Domitar Maniple", "category": "Support",
         "baseCost": 225,
         "composition": "4 Domitar Battle-Automata (+50 each, up to 6)",
         "unitOptions": [{"label": "4 Domitar",
                          "units": [{"unit": "domitar", "count": 4}]}],
         "extraUnit": {"unit": "domitar", "cost": 50, "max": 2, "label": "Additional Domitar"},
         "allowedUpgrades": ["mech-magos", "mech-tech-priest", "mech-scyllax", "mech-thanatar"]},
        {"id": "mech-tarantula-battery", "name": "Tarantula Battery", "category": "Support",
         "baseCost": 125,
         "composition": "5 Tarantula Platforms",
         "unitOptions": [{"label": "5 Tarantulas",
                          "units": [{"unit": "mech-tarantula", "count": 5}]}],
         "allowedUpgrades": ["mech-hyperios"]},
        {"id": "thanatar-maniple", "name": "Thanatar Maniple", "category": "Support",
         "baseCost": 200,
         "composition": "3 Thanatar Battle-Automata",
         "unitOptions": [{"label": "3 Thanatar",
                          "units": [{"unit": "thanatar", "count": 3}]}],
         "allowedUpgrades": ["mech-magos", "mech-tech-priest", "mech-scyllax"]},
        {"id": "vulturax-maniple", "name": "Vulturax Maniple", "category": "Support",
         "baseCost": 250,
         "composition": "6 Vulturax Stratos-Automata",
         "unitOptions": [{"label": "6 Vulturax",
                          "units": [{"unit": "vulturax", "count": 6}]}],
         "allowedUpgrades": []},
        {"id": "krios-battle-squadron", "name": "Krios Battle Squadron", "category": "Support",
         "baseCost": 250,
         "composition": "4 Krios Battle Tanks of any configuration (+50 each, up to 6)",
         "unitOptions": [{"label": "4 Krios", "units": [{"unit": "krios", "count": 4}]}],
         "extraUnit": {"unit": "krios", "cost": 50, "max": 2, "label": "Additional Krios"},
         "allowedUpgrades": []},
        {"id": "karacnos-squadron", "name": "Karacnos Squadron", "category": "Support",
         "baseCost": 300,
         "composition": "4 Karacnos Assault Tanks",
         "unitOptions": [{"label": "4 Karacnos", "units": [{"unit": "karacnos", "count": 4}]}],
         "allowedUpgrades": []},
        {"id": "minotaur-battery", "name": "Minotaur Battery", "category": "Support",
         "baseCost": 350,
         "composition": "3 Minotaur Artillery Tanks",
         "unitOptions": [{"label": "3 Minotaurs",
                          "units": [{"unit": "minotaur", "count": 3}]}],
         "allowedUpgrades": []},
        {"id": "ordinatus-minorus", "name": "Ordinatus Minorus Tormenta",
         "category": "Support", "baseCost": 500,
         "composition": "3 Ordinatus Minorus of any configuration (1 per 2,000 pts)",
         "unitOptions": [{"label": "3 Ordinatus Minorus",
                          "units": [{"unit": "ordinatus-minoris", "count": 3}]}],
         "allowedUpgrades": []},

        # ----- Lords of War -----
        {"id": "mech-avenger-flight", "name": "Avenger Strike Fighter Flight",
         "category": "Lords of War", "baseCost": 225,
         "composition": "2 Avenger Strike Fighters (+125 each, up to 3)",
         "unitOptions": [{"label": "2 Mechanicum Avengers",
                          "units": [{"unit": "mech-avenger", "count": 2}]}],
         "extraUnit": {"unit": "mech-avenger", "cost": 125, "max": 1,
                       "label": "Additional Avenger"},
         "allowedUpgrades": []},
        {"id": "mech-lightning-flight", "name": "Lightning Interceptor Flight",
         "category": "Lords of War", "baseCost": 225,
         "composition": "2 Lightning Interceptors",
         "unitOptions": [{"label": "2 Mechanicum Lightnings",
                          "units": [{"unit": "mech-lightning", "count": 2}]}],
         "allowedUpgrades": []},
        {"id": "mech-falchion", "name": "Superheavy Tank Destroyer",
         "category": "Lords of War", "baseCost": 250,
         "composition": "1 Mechanicum Falchion",
         "unitOptions": [{"label": "1 Mechanicum Falchion",
                          "units": [{"unit": "mech-falchion", "count": 1}]}],
         "allowedUpgrades": []},
        {"id": "ordinatus-majoris", "name": "Ordinatus Majoris",
         "category": "Lords of War", "baseCost": 450,
         "composition": "1 Ordinatus Majoris (1 per force)",
         "unitOptions": [{"label": "1 Ordinatus Majoris",
                          "units": [{"unit": "ordinatus-majoris", "count": 1}]}],
         "maxPerArmy": 1, "allowedUpgrades": []},
        {"id": "ark-mechanicus", "name": "Ark Mechanicus",
         "category": "Lords of War", "baseCost": 250,
         "composition": "1 Ark Mechanicus (1 per force)",
         "unitOptions": [{"label": "1 Ark Mechanicus",
                          "units": [{"unit": "ark-mechanicus", "count": 1}]}],
         "maxPerArmy": 1, "allowedUpgrades": []},
    ],
    "upgrades": [
        {"id": "mech-magos", "name": "Magos", "type": "flag", "cost": 50,
         "description": "Upgrade 1 Tech-Priest or Myrmidon to a Magos Prime. May further upgrade to Archmagos Prime (max 1 per force).",
         "addedUnits": [{"unit": "magos-prime", "count": 1}]},
        {"id": "mech-tech-priest", "name": "Tech-Priest", "type": "multi", "max": 3,
         "description": "Add 1-3 Tech-Priests.",
         "variants": [{"id": "tech-priest", "name": "Tech-Priest", "cost": 25}]},
        {"id": "mech-transport", "name": "Transport", "type": "multi",
         "description": "Add enough Triaros OR Mechanicum Land Raiders to carry the formation.",
         "variants": [
             {"id": "triaros", "name": "Triaros Armoured Conveyor", "cost": 75},
             {"id": "mech-land-raider", "name": "Mechanicum Land Raider", "cost": 75},
         ]},
        {"id": "mech-krios", "name": "Krios", "type": "multi", "max": 3,
         "description": "Add 1-3 Krios Battle Tanks.",
         "variants": [{"id": "krios", "name": "Krios Battle Tank", "cost": 50}]},
        {"id": "mech-karacnos", "name": "Karacnos", "type": "multi", "max": 3,
         "description": "Add 1-3 Karacnos Assault Tanks.",
         "variants": [{"id": "karacnos", "name": "Karacnos", "cost": 75}]},
        {"id": "mech-thanatar", "name": "Thanatar", "type": "multi", "max": 3,
         "description": "Add 1-3 Thanatar Battle-Automata.",
         "variants": [{"id": "thanatar", "name": "Thanatar", "cost": 75}]},
        {"id": "mech-hyperios", "name": "Hyperios Platform", "type": "multi", "max": 3,
         "description": "Upgrade 1-3 Tarantula Platforms to Hyperios Platforms.",
         "variants": [{"id": "hyperios-platform", "name": "Hyperios Platform", "cost": 40}]},
        {"id": "mech-scyllax", "name": "Scyllax", "type": "multi", "max": 3,
         "description": "Add 1-3 Scyllax Guardian Automata.",
         "variants": [{"id": "scyllax", "name": "Scyllax Guardian", "cost": 50}]},
    ],
    "units": {
        "archmagos-prime": {
            "name": "Archmagos Prime", "type": "CH",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [{"name": "Digi Weapon", "range": "(base)",
                         "firepower": "(assault) MW, EA (+1)"}],
            "notes": ["Supreme Commander.", "Invulnerable save.",
                      "Reinforced armour.", "Cortex Controller.",
                      "Upgraded unit becomes AV type."],
        },
        "magos-prime": {
            "name": "Magos Prime", "type": "CH",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [{"name": "Digi Weapon", "range": "(base)",
                         "firepower": "(assault) MW, EA (+1)"}],
            "notes": ["Commander.", "Invulnerable save.", "Cortex Controller.",
                      "Upgraded unit becomes AV type."],
        },
        "tech-priest": {
            "name": "Tech-Priest", "type": "INF",
            "speed": "15cm", "armour": "4+", "cc": "5+", "ff": "5+",
            "weapons": [
                {"name": "Graviton Gun", "range": "15cm",
                 "firepower": "AP5+/AT5+, Disrupt"},
                {"name": "Power Axe", "range": "(base)", "firepower": "Fleshbane"},
            ],
            "notes": ["Leader.", "Cortex Controller.",
                      "Counts as character for Bodyguard / Strategic Value."],
        },
        "tech-thrall": {
            "name": "Tech Thralls", "type": "INF",
            "speed": "15cm", "armour": "6+", "cc": "6+", "ff": "5+",
            "weapons": [{"name": "Las-lock", "range": "(15cm)", "firepower": "(small arms)"}],
            "notes": ["Automaton.", "Cybernetica Cortex."],
        },
        "thallax": {
            "name": "Thallax", "type": "INF",
            "speed": "30cm", "armour": "3+", "cc": "4+", "ff": "4+",
            "weapons": [{"name": "Lightning Gun + Multimelta",
                         "range": "15cm & (15cm)",
                         "firepower": "AP5+/AT5+, MW / (small arms) MW"}],
            "notes": ["Jump packs."],
        },
        "ursarax": {
            "name": "Ursarax", "type": "INF",
            "speed": "30cm", "armour": "3+", "cc": "4+", "ff": "6+",
            "weapons": [{"name": "Lightning Talons", "range": "(base)",
                         "firepower": "(assault) MW, EA (+1)"}],
            "notes": ["Jump packs."],
        },
        "myrmidon-destructor": {
            "name": "Myrmidon Destructors", "type": "INF",
            "speed": "15cm", "armour": "3+", "cc": "5+", "ff": "4+",
            "weapons": [
                {"name": "Power Fist", "range": "(base)",
                 "firepower": "(assault) MW"},
                {"name": "Volkite Culverin", "range": "45cm",
                 "firepower": "AP4+/AT6+, Disrupt"},
            ],
            "notes": ["Slow (may not take March action)."],
        },
        "myrmidon-secutor": {
            "name": "Myrmidon Secutors", "type": "INF",
            "speed": "15cm", "armour": "3+", "cc": "4+", "ff": "4+",
            "weapons": [
                {"name": "Power Axes", "range": "(base)",
                 "firepower": "(assault) Fleshbane, EA (+1)"},
                {"name": "Volkite Chargers", "range": "15cm & (15cm)",
                 "firepower": "AP4+, Disrupt / (small arms) EA (+1)"},
            ],
            "notes": ["Slow (may not take March action)."],
        },
        "scyllax": {
            "name": "Scyllax Guardian Automata", "type": "INF",
            "speed": "15cm", "armour": "4+", "cc": "4+", "ff": "4+",
            "weapons": [{"name": "Mechadendrite Array", "range": "(base)",
                         "firepower": "(assault) Singularity"}],
            "notes": ["Cybernetica Cortex.", "Fearless.", "Bodyguard."],
        },
        # Light/Armoured Vehicles
        "hyperios-platform": {
            "name": "Hyperios Platform", "type": "LV",
            "speed": "0cm", "armour": "6+", "cc": "6+", "ff": "6+",
            "weapons": [{"name": "Hyperios Missiles", "range": "60cm",
                         "firepower": "AA4+"}],
            "notes": ["Teleport.", "Scout."],
        },
        "mech-tarantula": {
            "name": "Tarantula", "type": "LV",
            "speed": "0cm", "armour": "6+", "cc": "6+", "ff": "6+ (5+)",
            "weapons": [
                {"name": "TL Lascannon OR", "range": "45cm", "firepower": "AT4+"},
                {"name": "TL Heavy Bolter", "range": "30cm", "firepower": "AP4+"},
            ],
            "notes": ["Teleport.", "Scout."],
        },
        "vorax": {
            "name": "Vorax Battle Automata", "type": "LV",
            "speed": "20cm", "armour": "4+", "cc": "4+", "ff": "4+",
            "weapons": [{"name": "TL Rotor Cannon", "range": "30cm",
                         "firepower": "AP4+"}],
            "notes": ["Fearless.", "Scout.", "Walker."],
        },
        "arletax": {
            "name": "Arletax Battle-Automata", "type": "AV",
            "speed": "15cm", "armour": "3+", "cc": "4+", "ff": "4+",
            "weapons": [
                {"name": "Lightning Blades", "range": "(base)",
                 "firepower": "(assault) Fleshbane"},
                {"name": "TL Light Autocannon", "range": "30cm",
                 "firepower": "AP5+/AT6+"},
                {"name": "Plasma Cannon", "range": "30cm",
                 "firepower": "AP5+/AT6+, Fleshbane"},
            ],
            "notes": ["Fearless.", "Invulnerable save.", "Jump packs."],
        },
        "castellax": {
            "name": "Castellax Battle-Automata", "type": "AV",
            "speed": "15cm", "armour": "3+", "cc": "4+", "ff": "4+",
            "weapons": [
                {"name": "Mauler Bolt Cannon", "range": "30cm",
                 "firepower": "AP4+/AT6+"},
                {"name": "Power Blade", "range": "(base)",
                 "firepower": "(assault) MW, EA (+1)"},
            ],
            "notes": ["Cybernetica Cortex.", "Fearless.", "Invulnerable save.",
                      "Walker."],
        },
        "domitar": {
            "name": "Domitar Battle-Automata", "type": "AV",
            "speed": "15cm", "armour": "3+", "cc": "4+", "ff": "5+",
            "weapons": [
                {"name": "Graviton Hammer", "range": "(base)",
                 "firepower": "(assault) MW, EA (+1)"},
                {"name": "Ignis Missile System", "range": "45cm",
                 "firepower": "AP5+/AT6+/AA6+, Ignore cover"},
            ],
            "notes": ["Cybernetica Cortex.", "Fearless.", "Invulnerable save.",
                      "Walker."],
        },
        "karacnos": {
            "name": "Karacnos Assault Tank", "type": "AV",
            "speed": "25cm", "armour": "4+", "cc": "5+", "ff": "5+",
            "weapons": [
                {"name": "Karacnos Mortars", "range": "45cm",
                 "firepower": "1 BP, Fleshbane, Disrupt, Ignore cover"},
                {"name": "Lightning Blaster", "range": "15cm",
                 "firepower": "AP5+, Disrupt"},
            ],
            "notes": ["Invulnerable save.", "Reinforced armour.", "Walker."],
        },
        "krios": {
            "name": "Krios Battle Tank", "type": "AV",
            "speed": "25cm", "armour": "4+", "cc": "6+", "ff": "5+",
            "weapons": [
                {"name": "Lightning Cannon OR", "range": "45cm",
                 "firepower": "AP5+/AT5+, MW"},
                {"name": "Pulse Fusil", "range": "30cm",
                 "firepower": "AP5+/AT3+"},
            ],
            "notes": [],
        },
        "minotaur": {
            "name": "Minotaur Artillery Tank", "type": "AV",
            "speed": "15cm", "armour": "4+", "cc": "6+", "ff": "6+",
            "weapons": [{"name": "Minotaur Twin Earthshakers", "range": "120cm",
                         "firepower": "2 BP, Indirect fire"}],
            "notes": ["Reinforced armour.", "Thick rear armour."],
        },
        "thanatar": {
            "name": "Thanatar Battle-Automata", "type": "AV",
            "speed": "15cm", "armour": "4+", "cc": "5+", "ff": "5+",
            "weapons": [
                {"name": "Twin Mauler Boltcannon", "range": "30cm",
                 "firepower": "AP3+/AT6+"},
                {"name": "Hellex Mortar OR", "range": "30cm",
                 "firepower": "1 BP, Ignore cover, Indirect fire"},
                {"name": "Sallex Heavy Lascannon", "range": "60cm",
                 "firepower": "AT4+"},
            ],
            "notes": ["Cybernetica Cortex.", "Fearless.", "Invulnerable save.",
                      "Reinforced armour.", "Walker."],
        },
        "triaros": {
            "name": "Triaros Armoured Conveyor", "type": "AV",
            "speed": "25cm", "armour": "4+", "cc": "5+", "ff": "5+",
            "weapons": [{"name": "Twin Mauler Boltcannon", "range": "30cm",
                         "firepower": "AP3+/AT6+"}],
            "notes": ["Invulnerable save.", "Reinforced armour.", "Walker.",
                      "Transport (2 Myrmidon/Thallax/Ursarax OR 4 Tech-Priest/Thrall/Scyllax)."],
        },
        "vulturax": {
            "name": "Vulturax Stratos-Automata", "type": "AV",
            "speed": "30cm", "armour": "4+", "cc": "6+", "ff": "4+",
            "weapons": [
                {"name": "Vulturax Arc Blaster", "range": "15cm",
                 "firepower": "AP5+/AT4+"},
                {"name": "2× Setherno Havocs", "range": "30cm",
                 "firepower": "AP4+/AT6+, Ignore cover"},
            ],
            "notes": ["Scout.", "Skimmer."],
        },
        # War Engines
        "mech-land-raider": {
            "name": "Mechanicum Land Raider", "type": "WE",
            "speed": "25cm", "armour": "4+", "cc": "6+", "ff": "4+",
            "weapons": [
                {"name": "TL Heavy Bolter", "range": "30cm", "firepower": "AP4+"},
                {"name": "2× TL Lascannons OR", "range": "45cm", "firepower": "AT4+"},
                {"name": "2× Flamestorm Cannon OR", "range": "15cm & (15cm)",
                 "firepower": "AP3+, Ignore cover / (small arms) Ignore cover"},
                {"name": "2× TL Multimelta", "range": "15cm & (15cm)",
                 "firepower": "AP4+/AT4+, MW / (small arms) MW"},
            ],
            "notes": ["DC1.", "Invulnerable save.", "Reinforced armour.",
                      "Thick rear armour.",
                      "Transport (1 Myrmidon/Thallax/Ursarax OR 2 Tech-Priest/Thrall/Scyllax)."],
        },
        "mech-falchion": {
            "name": "Mechanicum Falchion", "type": "WE",
            "speed": "20cm", "armour": "4+", "cc": "6+", "ff": "6+",
            "weapons": [
                {"name": "TL Volcano Cannon", "range": "90cm",
                 "firepower": "AP2+/AT2+, TK (D3), Ignore cover, FxF"},
                {"name": "2× Quad Lascannon", "range": "45cm", "firepower": "AT3+"},
            ],
            "notes": ["DC3.", "Reinforced armour.",
                      "Critical Hit: Destroyed; units within 5cm hit on 6+."],
        },
        "ordinatus-minoris": {
            "name": "Ordinatus Minoris", "type": "WE",
            "speed": "20cm", "armour": "5+", "cc": "5+", "ff": "5+",
            "weapons": [
                {"name": "3× Volkite Culverins", "range": "45cm",
                 "firepower": "AP4+/AT6+, Disrupt"},
                {"name": "Volcano Cannon OR", "range": "90cm",
                 "firepower": "AP2+/AT2+, TK (D3), FxF"},
                {"name": "Ulator Sonic Destroyer", "range": "75cm",
                 "firepower": "3 BP, Disrupt, Lance, FxF"},
            ],
            "notes": ["DC2.", "1 Void shield.", "Reinforced armour.",
                      "Critical Hit: Destroyed; units within 15cm hit on 5+."],
        },
        "ordinatus-majoris": {
            "name": "Ordinatus Majoris", "type": "WE",
            "speed": "15cm", "armour": "5+", "cc": "5+", "ff": "4+",
            "weapons": [
                {"name": "3× Volkite Culverins", "range": "45cm",
                 "firepower": "AP4+/AT6+, Disrupt"},
                {"name": "2× TL Lascannons", "range": "45cm", "firepower": "AT4+"},
                {"name": "Sonic Disruptor OR", "range": "100cm",
                 "firepower": "10 BP, Ignore cover, Disrupt, FxF"},
                {"name": "6× Golgothan Missiles OR", "range": "Unlimited",
                 "firepower": "2 BP, MW, Indirect fire, Single shot, FxF"},
                {"name": "Nova Cannon", "range": "100cm",
                 "firepower": "3× AP3+/AT3+, TK (D3), Singularity, FxF"},
            ],
            "notes": ["DC4.", "4 Void shields.", "Inspiring.", "Reinforced armour.",
                      "Critical Hit: Obliterated; all other units within 15cm hit on 5+; all friendly LoS formations take a Blast marker."],
        },
        # Aircraft / Spacecraft
        "mech-avenger": {
            "name": "Mechanicum Avenger Strike Fighter", "type": "AC",
            "speed": "Bomber", "armour": "5+", "cc": "-", "ff": "-",
            "weapons": [
                {"name": "Avenger Cannon", "range": "30cm",
                 "firepower": "2× AP3+/AT5+, FxF"},
                {"name": "TL Lascannon", "range": "30cm",
                 "firepower": "AT4+/AA5+, FxF"},
                {"name": "Heavy Stubber", "range": "30cm",
                 "firepower": "AA6+, Rwd"},
                {"name": "Kraken Missiles OR Unguided Bombs", "range": "30cm / 15cm",
                 "firepower": "AT4+ Single shot, FxF / 1 BP, Single shot, FxF"},
            ],
            "notes": [],
        },
        "mech-lightning": {
            "name": "Mechanicum Lightning Interceptor", "type": "AC",
            "speed": "Fighter", "armour": "6+", "cc": "-", "ff": "-",
            "weapons": [
                {"name": "TL Lascannon", "range": "30cm",
                 "firepower": "AT4+/AA5+, FxF"},
                {"name": "Autocannon", "range": "30cm",
                 "firepower": "AP5+/AT6+/AA5+, FxF"},
                {"name": "Kraken / Skystrike / Unguided Bombs", "range": "30cm/15cm",
                 "firepower": "AT4+ / AA5+ / 1 BP, Single shot"},
            ],
            "notes": [],
        },
        "ark-mechanicus": {
            "name": "Ark Mechanicus", "type": "SC",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [
                {"name": "Orbital Bombardment", "range": "-",
                 "firepower": "8 BP, MW"},
                {"name": "Heavy Lance Battery", "range": "Point",
                 "firepower": "AP2+/AT2+, TK (D3+1)"},
            ],
            "notes": ["Slow and steady (not turn 1)."],
        },
    },
}


# =====================================================================
# LEGIO CUSTODES
# =====================================================================
custodes = {
    "id": "legio-custodes",
    "name": "Legio Custodes",
    "subtitle": "The Emperor's Chosen · Companions of the Golden Throne",
    "color": "#C9A227",
    "lore": (
        "The Adeptus Custodes — golden-armoured demigods who guard the "
        "Emperor's throneroom. Each Custodian is a singular work of arcane "
        "alchemy and bonded soul-craft, their numbers small but their "
        "battle-prowess unmatched. Alongside them stand the silent Sisters "
        "of Silence, whose null-presence severs the warp from reality. As "
        "the Heresy reaches Terra, the Companions sally forth at last."
    ),
    "legionTrait": {
        "name": "The Emperor's Chosen",
        "description": (
            "Strategy Rating 6 · Initiative 1+. 3 Support per Line, max 4 "
            "Upgrades per formation, up to 1/2 of total points on Lords of "
            "War/Allies. Custodes units take 2 Blast markers to suppress; "
            "formations only break at 2 BM per unit; ignore -1 Rally if "
            "enemies within 30cm; halve hackdowns from lost assaults."
        ),
    },
    "compositionLimits": LIMITS_CUSTODES,
    "compositionRules": [
        "Strategy Rating 6, Initiative 1+.",
        "Max 3 Support per Line; max 4 Upgrades per formation; up to 1/2 of points on Lords of War/Allies.",
        "Special: It takes 2 Blast markers to suppress/kill a Custodes unit; formations break at 2 BM per unit; only half BM count in assault resolution (rounded down); broken Custodes rally with full BM (one per unit); Leader trait removes 2 BM instead of 1; ignore -1 Rally penalty for nearby enemies; halve hackdowns from lost assaults.",
        "Optional Trait: Hunters of the Throne — gain Sniper trait when shooting/Engaging Character-bearing formations.",
    ],
    "allies": {
        "cohesive": ["Knight Households", "Legio Titanicus"],
        "disruptive": ["Imperialis Militia", "Mechanicum Taghmata", "Solar Auxilia"],
    },
    "formations": [
        # ----- Line -----
        {"id": "custodian-detachment", "name": "Custodian Detachment",
         "category": "Line", "baseCost": 350,
         "composition": "6 Custodian OR 6 Sentinel units",
         "unitOptions": [
             {"label": "6 Custodian Guard",
              "units": [{"unit": "custodian-guard", "count": 6}]},
             {"label": "6 Sentinel Guard",
              "units": [{"unit": "sentinel-guard", "count": 6}]},
         ],
         "allowedUpgrades": ["cust-carrier", "cust-teleport", "cust-shield-officer",
                             "cust-tribune", "cust-vault-access", "cust-dreadnought"]},
        {"id": "agamatus-jetbike-detachment", "name": "Agamatus Jetbike Detachment",
         "category": "Line", "baseCost": 250,
         "composition": "5 Agamatus Jetbike units",
         "unitOptions": [{"label": "5 Agamatus Jetbikes",
                          "units": [{"unit": "agamatus", "count": 5}]}],
         "allowedUpgrades": ["cust-shield-officer", "cust-tribune"]},
        {"id": "sisters-detachment", "name": "Sisters of Silence Detachment",
         "category": "Line", "baseCost": 200,
         "composition": "4 Sisters of Silence (+50 each, up to 6)",
         "unitOptions": [{"label": "4 Sisters of Silence",
                          "units": [{"unit": "sisters-of-silence", "count": 4}]}],
         "extraUnit": {"unit": "sisters-of-silence", "cost": 50, "max": 2,
                       "label": "Additional Sister of Silence"},
         "allowedUpgrades": ["cust-order-transport", "cust-teleport", "cust-oblivion-knight"]},

        # ----- Support -----
        {"id": "ephotoi-detachment", "name": "Ephotoi Detachment",
         "category": "Support", "baseCost": 325,
         "composition": "4 Ephotoi units",
         "unitOptions": [{"label": "4 Ephotoi",
                          "units": [{"unit": "ephotoi", "count": 4}]}],
         "allowedUpgrades": ["cust-carrier", "cust-shield-officer", "cust-tribune"]},
        {"id": "saggitarum-detachment", "name": "Saggitarum Detachment",
         "category": "Support", "baseCost": 250,
         "composition": "4 Saggitarum units (+60 each, up to 6)",
         "unitOptions": [{"label": "4 Saggitarum",
                          "units": [{"unit": "saggitarum", "count": 4}]}],
         "extraUnit": {"unit": "saggitarum", "cost": 60, "max": 2,
                       "label": "Additional Saggitarum"},
         "allowedUpgrades": ["cust-carrier", "cust-shield-officer", "cust-tribune",
                             "cust-vault-access", "cust-dreadnought"]},
        {"id": "tharantatoi-detachment", "name": "Tharantatoi Detachment",
         "category": "Support", "baseCost": 375,
         "composition": "4 Aquilon Terminator units",
         "unitOptions": [{"label": "4 Aquilon Terminators",
                          "units": [{"unit": "aquilon-terminator", "count": 4}]}],
         "allowedUpgrades": ["cust-carrier", "cust-teleport", "cust-shield-officer",
                             "cust-tribune"]},
        {"id": "venatari-detachment", "name": "Venatari Detachment",
         "category": "Support", "baseCost": 350,
         "composition": "4 Venatari units",
         "unitOptions": [{"label": "4 Venatari",
                          "units": [{"unit": "venatari", "count": 4}]}],
         "allowedUpgrades": []},
        {"id": "morotoi-detachment", "name": "Morotoi Dreadnought Detachment",
         "category": "Support", "baseCost": 340,
         "composition": "4 Achilles OR Galatus Dreadnoughts in any combination",
         "unitOptions": [
             {"label": "4 Galatus Dreadnoughts",
              "units": [{"unit": "galatus", "count": 4}]},
             {"label": "4 Achilles Dreadnoughts",
              "units": [{"unit": "achilles", "count": 4}]},
         ],
         "allowedUpgrades": ["cust-vault-access"]},
        {"id": "erinyes-detachment", "name": "Erinyes Jetcycle Detachment",
         "category": "Support", "baseCost": 200,
         "composition": "5 Sisters Erinyes Jetcycle units",
         "unitOptions": [{"label": "5 Erinyes Jetcycles",
                          "units": [{"unit": "erinyes-jetcycle", "count": 5}]}],
         "allowedUpgrades": ["cust-oblivion-knight"]},
        {"id": "caladius-squadron", "name": "Caladius Grav-Tank Squadron",
         "category": "Support", "baseCost": 325,
         "composition": "3 Caladius Grav-Tanks",
         "unitOptions": [{"label": "3 Caladius",
                          "units": [{"unit": "caladius", "count": 3}]}],
         "allowedUpgrades": []},
        {"id": "pallas-squadron", "name": "Pallas Grav-Attack Speeder",
         "category": "Support", "baseCost": 250,
         "composition": "3 Pallas Grav-Speeders",
         "unitOptions": [{"label": "3 Pallas",
                          "units": [{"unit": "pallas", "count": 3}]}],
         "allowedUpgrades": []},

        # ----- Lords of War -----
        {"id": "orion-dropship", "name": "Orion Dropship",
         "category": "Lords of War", "baseCost": 300,
         "composition": "1 Orion Dropship (+300 for 2nd)",
         "unitOptions": [{"label": "1 Orion Dropship",
                          "units": [{"unit": "orion", "count": 1}]}],
         "extraUnit": {"unit": "orion", "cost": 300, "max": 1,
                       "label": "Additional Orion Dropship"},
         "allowedUpgrades": []},
        {"id": "ares-strike", "name": "Ares Strike Squadron",
         "category": "Lords of War", "baseCost": 275,
         "composition": "1 Ares Gunship (+275 for 2nd)",
         "unitOptions": [{"label": "1 Ares Gunship",
                          "units": [{"unit": "ares-gunship", "count": 1}]}],
         "extraUnit": {"unit": "ares-gunship", "cost": 275, "max": 1,
                       "label": "Additional Ares Gunship"},
         "allowedUpgrades": []},
        {"id": "equinox-flight", "name": "Equinox Interceptor Flight",
         "category": "Lords of War", "baseCost": 325,
         "composition": "2 Equinox Interceptors",
         "unitOptions": [{"label": "2 Equinox",
                          "units": [{"unit": "equinox", "count": 2}]}],
         "allowedUpgrades": []},
    ],
    "upgrades": [
        {"id": "cust-carrier", "name": "Carrier", "type": "multi",
         "description": "Add enough Coronus Grav-Carriers to transport the formation.",
         "variants": [{"id": "coronus", "name": "Coronus Grav-Carrier", "cost": 85}]},
        {"id": "cust-dreadnought", "name": "Dreadnought", "type": "multi", "max": 2,
         "description": "Add 1-2 Achilles or Galatus Dreadnoughts in any combination.",
         "variants": [
             {"id": "achilles", "name": "Achilles Dreadnought", "cost": 85},
             {"id": "galatus", "name": "Galatus Dreadnought", "cost": 85},
         ]},
        {"id": "cust-oblivion-knight", "name": "Oblivion Knight", "type": "flag",
         "cost": 50,
         "description": "Add 1 Oblivion Knight character.",
         "addedUnits": [{"unit": "oblivion-knight", "count": 1}]},
        {"id": "cust-order-transport", "name": "Order Transport", "type": "multi",
         "description": "Add enough Kheron Acquisitors to transport the formation.",
         "variants": [{"id": "kheron", "name": "Kheron Acquisitor", "cost": 65}]},
        {"id": "cust-shield-officer", "name": "Shield Captain", "type": "flag", "cost": 50,
         "description": "Add 1 Shield Captain character.",
         "addedUnits": [{"unit": "shield-captain", "count": 1}]},
        {"id": "cust-tribune", "name": "Tribune", "type": "flag", "cost": 50,
         "description": "Upgrade one Shield Captain to a Tribune (max 1 per force). Requires Shield Captain upgrade.",
         "addedUnits": [{"unit": "tribune", "count": 1}]},
        {"id": "cust-teleport", "name": "Teleport", "type": "flag", "cost": 0,
         "description": "Formation gains the Teleport trait (deep strike from reserves)."},
        {"id": "cust-vault-access", "name": "Vault Access", "type": "flag", "cost": 25,
         "description": "Upgrade 1-2 Galatus Dreadnoughts to Telemon Heavy Dreadnoughts."},
    ],
    "units": {
        # Characters
        "shield-captain": {
            "name": "Shield Captain", "type": "CH",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [{"name": "Paragon Blade", "range": "(base)",
                         "firepower": "(assault) Fleshbane, EA (+1)"}],
            "notes": ["Commander.", "Inspiring.", "Invulnerable save."],
        },
        "tribune": {
            "name": "Tribune", "type": "CH",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [{"name": "Solarite Gauntlet", "range": "(base)",
                         "firepower": "(assault) MW, EA (+1)"}],
            "notes": ["Supreme Commander.", "Inspiring.", "Invulnerable save."],
        },
        "oblivion-knight": {
            "name": "Oblivion Knight", "type": "CH",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [{"name": "Executioner Blade", "range": "(base)",
                         "firepower": "(assault) Fleshbane, Sniper, EA (+1)"}],
            "notes": ["Commander.", "Inspiring.", "Invulnerable save (5+)."],
        },
        # Infantry
        "aquilon-terminator": {
            "name": "Aquilon Terminator Team", "type": "INF",
            "speed": "15cm", "armour": "3+", "cc": "3+", "ff": "3+",
            "weapons": [
                {"name": "Lastrum Storm Bolter", "range": "(15cm)",
                 "firepower": "(small arms) EA (+1)"},
                {"name": "Solarite Gauntlet", "range": "(base)",
                 "firepower": "(assault) MW, EA (+1)"},
            ],
            "notes": ["Invulnerable save.", "Reinforced armour.",
                      "Thick rear armour."],
        },
        "custodian-guard": {
            "name": "Custodian Guard Team", "type": "INF",
            "speed": "15cm", "armour": "4+", "cc": "3+", "ff": "4+",
            "weapons": [{"name": "Guardian Spear", "range": "(15cm) & (base)",
                         "firepower": "(small arms) / (assault) Fleshbane, EA (+1)"}],
            "notes": ["Invulnerable save."],
        },
        "ephotoi": {
            "name": "Ephotoi Team", "type": "INF",
            "speed": "15cm", "armour": "4+", "cc": "3+", "ff": "3+",
            "weapons": [{"name": "Guardian Spear", "range": "(15cm) & (base)",
                         "firepower": "(small arms) EA (+1) / (assault) Fleshbane, EA (+1)"}],
            "notes": ["Scout.", "Infiltrate.", "Counts as Custodian for transport."],
        },
        "saggitarum": {
            "name": "Saggitarum Team", "type": "INF",
            "speed": "15cm", "armour": "3+", "cc": "4+", "ff": "3+",
            "weapons": [{"name": "Adratus Bolt Caliver",
                         "range": "30cm & (15cm)",
                         "firepower": "2× AP4+/AT6+ / (small arms) Sniper"}],
            "notes": ["Remorseless.", "Invulnerable save."],
        },
        "sentinel-guard": {
            "name": "Sentinel Team", "type": "INF",
            "speed": "15cm", "armour": "3+", "cc": "3+", "ff": "4+",
            "weapons": [{"name": "Sentinel Warblade", "range": "(base)",
                         "firepower": "(assault) Fleshbane"}],
            "notes": ["Invulnerable save (5+).",
                      "Counts as Custodian for transport."],
        },
        "sisters-of-silence": {
            "name": "Sisters of Silence", "type": "INF",
            "speed": "15cm", "armour": "5+", "cc": "4+/5+/3+", "ff": "4+/3+/6+",
            "weapons": [
                {"name": "Bolters OR", "range": "(15cm)", "firepower": "(small arms)"},
                {"name": "Flamers OR", "range": "(15cm)",
                 "firepower": "(small arms) Ignore cover"},
                {"name": "Greatblades", "range": "(base)",
                 "firepower": "(assault) Fleshbane"},
            ],
            "notes": ["Fearless.", "Counts as Custodian for transport."],
        },
        "erinyes-jetcycle": {
            "name": "Sisters Erinyes Jetcycle Team", "type": "INF",
            "speed": "35cm", "armour": "5+", "cc": "5+", "ff": "3+",
            "weapons": [{"name": "Snareguns + Neurolash",
                         "range": "15cm & (15cm)",
                         "firepower": "AP5+, Disrupt / (small arms) Ignore cover"}],
            "notes": ["Mounted.", "Fearless.",
                      "Counts as Jetbike for transport."],
        },
        "venatari": {
            "name": "Venatari Team", "type": "INF",
            "speed": "30cm", "armour": "4+", "cc": "4+", "ff": "3+",
            "weapons": [{"name": "Kinetic Destroyer", "range": "(15cm)",
                         "firepower": "(small arms) Fleshbane"}],
            "notes": ["Jump packs.", "Invulnerable save.", "Scout.",
                      "Counts as Terminator for transport."],
        },
        # Vehicles
        "achilles": {
            "name": "Achilles Dreadnought", "type": "AV",
            "speed": "15cm", "armour": "3+", "cc": "4+", "ff": "4+",
            "weapons": [{"name": "Achilles Dreadspear", "range": "(base)",
                         "firepower": "(assault) MW, EA (+2)"}],
            "notes": ["Invulnerable save.", "Walker."],
        },
        "agamatus": {
            "name": "Agamatus Jetbikes", "type": "LV",
            "speed": "35cm", "armour": "4+", "cc": "3+", "ff": "5+",
            "weapons": [{"name": "Power Lance", "range": "(base)",
                         "firepower": "(assault) MW, First Strike"}],
            "notes": ["Invulnerable save.", "Skimmer."],
        },
        "caladius": {
            "name": "Caladius Grav-Tank", "type": "AV",
            "speed": "30cm", "armour": "4+", "cc": "6+", "ff": "3+",
            "weapons": [
                {"name": "Lastrum Bolt Cannon", "range": "30cm",
                 "firepower": "2× AP4+"},
                {"name": "Illastus Accelerator", "range": "45cm",
                 "firepower": "2× AP5+/AT4+"},
            ],
            "notes": ["Invulnerable save.", "Reinforced armour.", "Skimmer."],
        },
        "coronus": {
            "name": "Coronus Grav-Carrier", "type": "AV",
            "speed": "25cm", "armour": "4+", "cc": "6+", "ff": "5+",
            "weapons": [
                {"name": "Blaze Cannon", "range": "15cm",
                 "firepower": "AP4+/AT4+, Armourbane"},
                {"name": "Illastus Accelerator", "range": "45cm",
                 "firepower": "2× AP5+/AT4+"},
            ],
            "notes": ["Invulnerable save.", "Reinforced armour.",
                      "Thick rear armour.", "Skimmer.",
                      "Transport (2 Custodian OR 1 Terminator)."],
        },
        "galatus": {
            "name": "Galatus Dreadnought", "type": "AV",
            "speed": "15cm", "armour": "3+", "cc": "4+", "ff": "4+",
            "weapons": [{"name": "Galatus Warblade",
                         "range": "(15cm) & (base)",
                         "firepower": "(small arms) EA (+1) / (assault) MW, EA (+1)"}],
            "notes": ["Invulnerable save (5+)."],
        },
        "kheron": {
            "name": "Kheron Acquisitor", "type": "AV",
            "speed": "25cm", "armour": "5+", "cc": "6+", "ff": "4+",
            "weapons": [
                {"name": "Hellion Autocannon", "range": "15cm",
                 "firepower": "2× AP5+"},
                {"name": "Missile Systems", "range": "45cm",
                 "firepower": "2× AP5+/AT6+"},
            ],
            "notes": ["Invulnerable save.", "Reinforced armour.", "Skimmer.",
                      "Transport (2 Custodian)."],
        },
        "pallas": {
            "name": "Pallas Grav-Attack Vehicle", "type": "AV",
            "speed": "35cm", "armour": "5+", "cc": "6+", "ff": "4+",
            "weapons": [
                {"name": "Blaze Cannon OR", "range": "15cm",
                 "firepower": "AP4+/AT4+, Armourbane"},
                {"name": "TL Adrathic Devastators", "range": "15cm",
                 "firepower": "2× AP4+, Fleshbane"},
            ],
            "notes": ["Invulnerable save.", "Reinforced armour.", "Skimmer."],
        },
        "telemon": {
            "name": "Telemon Heavy Dreadnought", "type": "AV",
            "speed": "15cm", "armour": "3+", "cc": "4+/5+", "ff": "5+/3+",
            "weapons": [
                {"name": "Telemon Cestus", "range": "(base)",
                 "firepower": "(assault) MW, EA (+1)"},
                {"name": "Arachnus Storm Cannon",
                 "range": "15cm & (15cm)",
                 "firepower": "2× AP3+/AT5+ / (small arms) EA (+1)"},
                {"name": "Spicules Bolt Launchers", "range": "45cm",
                 "firepower": "AP5+/AT6+, Disrupt"},
            ],
            "notes": ["Invulnerable save.", "Reinforced armour.", "Walker.",
                      "Select 2 arm weapons from Telemon Cestus / Arachnus Storm Cannon."],
        },
        # Aircraft
        "ares-gunship": {
            "name": "Ares Gunship", "type": "AC",
            "speed": "Fighter-bomber", "armour": "5+", "cc": "-", "ff": "-",
            "weapons": [
                {"name": "2× Blaze Cannons", "range": "15cm",
                 "firepower": "AP4+/AT4+, Armourbane, Fwd"},
                {"name": "Magna Blaze Cannon", "range": "30cm",
                 "firepower": "AP4+/AT3+, TK (1), FxF"},
                {"name": "Firebomb Clusters", "range": "15cm",
                 "firepower": "2 BP, Ignore cover"},
            ],
            "notes": ["DC2.", "Invulnerable save.", "Reinforced armour."],
        },
        "equinox": {
            "name": "Equinox Interceptor", "type": "AC",
            "speed": "Fighter", "armour": "5+", "cc": "-", "ff": "-",
            "weapons": [
                {"name": "Heavy Blaze Cannons", "range": "30cm",
                 "firepower": "2× AT4+/AA4+, Lance, Fwd"},
                {"name": "Arpactic Kinetic Missile", "range": "45cm",
                 "firepower": "AT4+/AA5+, MW, Singularity, One shot"},
            ],
            "notes": ["Invulnerable save.", "Reinforced armour."],
        },
        "orion": {
            "name": "Orion Dropship", "type": "AC",
            "speed": "Bomber", "armour": "4+", "cc": "6+", "ff": "5+",
            "weapons": [
                {"name": "Heavy Blaze Cannons", "range": "30cm",
                 "firepower": "2× AP4+/AT4+, Lance, Fwd"},
                {"name": "2× TL Lastrum Bolt Cannon", "range": "30cm",
                 "firepower": "2× AP4+"},
                {"name": "Spicules Bolt Launcher", "range": "30cm",
                 "firepower": "AP5+/AT6+, Disrupt"},
            ],
            "notes": ["DC2.", "Invulnerable save.", "Reinforced armour.",
                      "Transport (6 Custodian OR 4 Terminator OR 5 Jetbikes)."],
        },
    },
}


# =====================================================================
# DAEMONS OF THE RUINSTORM
# =====================================================================
# Daemon line detachments have rich composition options (multiple unit
# types in any combination). We model the BASE composition (5 + 1 Herald)
# as fixed, and surface the optional additions ("small host" / "large host"
# / "Greater Daemon") as flag upgrades with `addedUnits`. Players can
# read the PDF for full flexibility; the points totals match.
def daemon_line(uid, name, base_units, herald_unit, allowed_upgrades):
    units = [{"unit": u, "count": c} for u, c in base_units]
    units.append({"unit": herald_unit, "count": 1})
    return {
        "id": uid, "name": name, "category": "Line", "baseCost": 250,
        "composition": f"5 + 1 base unit with Herald upgrade",
        "unitOptions": [{"label": name, "units": units}],
        "allowedUpgrades": allowed_upgrades,
    }


def daemon_followers(uid, name, unit_id, cost_per, unit_label):
    """Support detachment of 6 units of a single type."""
    return {
        "id": uid, "name": name, "category": "Support",
        "baseCost": cost_per * 6,
        "composition": f"6 {unit_label} units",
        "unitOptions": [{"label": f"6 {unit_label}",
                         "units": [{"unit": unit_id, "count": 6}]}],
        "extraUnit": {"unit": unit_id, "cost": cost_per, "max": 3,
                      "label": f"Additional {unit_label}"},
        "allowedUpgrades": ["daemon-chaos-spawn", "daemon-chaos-altar"],
    }


def daemon_greater(uid, name, unit_id, label):
    """Lords of War 1-3 Greater Daemons."""
    return {
        "id": uid, "name": name, "category": "Lords of War",
        "baseCost": 200,
        "composition": f"1 {label} (+200 each, up to 3)",
        "unitOptions": [{"label": f"1 {label}",
                         "units": [{"unit": unit_id, "count": 1}]}],
        "extraUnit": {"unit": unit_id, "cost": 200, "max": 2,
                      "label": f"Additional {label}"},
        "allowedUpgrades": [],
    }


daemons = {
    "id": "daemons-ruinstorm",
    "name": "Daemons of the Ruinstorm",
    "subtitle": "Spawn of the Warp · The Four Powers Unleashed",
    "color": "#3D0B33",
    "lore": (
        "Manifest nightmares torn from the Immaterium itself. Bloodletters "
        "of Khorne, Plaguebearers of Nurgle, Daemonettes of Slaanesh and "
        "the capricious Horrors of Tzeentch march alongside renegades who "
        "made bargains too dark to name. They are unpredictable, "
        "uncontrollable, and infinitely hungry — the Warmaster harnesses "
        "their malice at terrible cost, for the gods of Chaos demand "
        "payment in souls."
    ),
    "legionTrait": {
        "name": "Echoes of the Ruinstorm",
        "description": (
            "Strategy Rating 2 · Initiative 2+. 1 Support per Line, 0-1 "
            "Lord of War per Line, any number of Upgrades per formation "
            "(each only once). Special Rules: Instability (failed Action "
            "test costs 1D3 Lesser Daemons), Chaos Gate, Daemonic Assault."
        ),
    },
    "compositionLimits": LIMITS_DAEMONS,
    "compositionRules": [
        "Strategy Rating 2, Initiative 2+.",
        "1 Support detachment per Line; 0-1 Lord of War per Line (same god affiliation).",
        "Any number of Upgrades per formation, each only once.",
        "Special: Instability — Line detachment failing an Action test loses 1D3 Lesser Daemons (no Blast markers).",
        "Special: Chaos Gate — keep up to 3 formations in the Warp; deploy via Chaos Gate objective.",
        "Special: Daemonic Assault — 1 formation per 1,000 pts may deploy by Teleport from turn 2 (max 1 Greater Daemon per teleporting formation).",
        "Optional Trait: Purposeful — single-god/Undivided force gains +2 Strategic Rating and 1 reroll/turn.",
    ],
    "allies": {
        "cohesive": ["Legiones Astartes (Traitor)", "Imperialis Militia (Traitor)",
                     "Solar Auxilia"],
        "disruptive": ["Mechanicum Taghmata", "Legio Titanicus", "Knight Households"],
    },
    "formations": [
        # ----- Line detachments (one per god) -----
        daemon_line("change-coven", "Change Coven (Tzeentch)",
                    [("horror", 5)], "herald-tzeentch",
                    ["daemon-small-host-tzeentch", "daemon-large-host-tzeentch",
                     "daemon-lord-of-change", "daemon-prince-tzeentch",
                     "daemon-chaos-spawn", "daemon-chaos-altar"]),
        daemon_line("depraved-host", "Depraved Host (Slaanesh)",
                    [("daemonette", 5)], "herald-slaanesh",
                    ["daemon-small-host-slaanesh", "daemon-large-host-slaanesh",
                     "daemon-keeper-of-secrets", "daemon-prince-slaanesh",
                     "daemon-chaos-spawn", "daemon-chaos-altar"]),
        daemon_line("murder-tide", "Murder Tide (Khorne)",
                    [("bloodletter", 5)], "herald-khorne",
                    ["daemon-small-host-khorne", "daemon-large-host-khorne",
                     "daemon-bloodthirster", "daemon-prince-khorne",
                     "daemon-chaos-spawn", "daemon-chaos-altar"]),
        daemon_line("putrid-legion", "Putrid Legion (Nurgle)",
                    [("plaguebearer", 6)], "herald-nurgle",
                    ["daemon-small-host-nurgle", "daemon-large-host-nurgle",
                     "daemon-great-unclean-one", "daemon-prince-nurgle",
                     "daemon-chaos-spawn", "daemon-chaos-altar"]),

        # ----- Support detachments (one per god, simplified to 1 unit type each)
        daemon_followers("followers-khorne-bloodcrusher", "Followers of Khorne (Bloodcrushers)",
                         "bloodcrusher", 50, "Bloodcrusher"),
        daemon_followers("followers-khorne-hounds", "Followers of Khorne (Flesh Hounds)",
                         "flesh-hound", 25, "Flesh Hound"),
        daemon_followers("followers-khorne-skull-cannons", "Followers of Khorne (Skull Cannons)",
                         "skull-cannon", 50, "Skull Cannon"),
        daemon_followers("followers-nurgle-beasts", "Followers of Nurgle (Beasts)",
                         "beast-of-nurgle", 50, "Beast of Nurgle"),
        daemon_followers("followers-nurgle-nurglings", "Followers of Nurgle (Nurglings)",
                         "nurgling", 25, "Nurgling"),
        daemon_followers("followers-nurgle-drones", "Followers of Nurgle (Plague Drones)",
                         "plague-drone", 50, "Plague Drone"),
        daemon_followers("followers-slaanesh-seekers", "Followers of Slaanesh (Seekers)",
                         "seeker", 25, "Seeker"),
        daemon_followers("followers-slaanesh-chariots", "Followers of Slaanesh (Seeker Chariots)",
                         "seeker-chariot", 50, "Seeker Chariot"),
        daemon_followers("followers-slaanesh-fiends", "Followers of Slaanesh (Fiends)",
                         "fiend", 50, "Fiend"),
        daemon_followers("followers-tzeentch-flamers", "Followers of Tzeentch (Flamers)",
                         "flamer", 50, "Flamer of Tzeentch"),
        daemon_followers("followers-tzeentch-screamers", "Followers of Tzeentch (Screamers)",
                         "screamer", 25, "Screamer"),
        daemon_followers("followers-tzeentch-chariots", "Followers of Tzeentch (Burning Chariots)",
                         "burning-chariot", 50, "Burning Chariot"),
        {"id": "undivided-furies", "name": "Undivided Furies Flight",
         "category": "Support", "baseCost": 150,
         "composition": "6 Fury units (+25 each, up to 8)",
         "unitOptions": [{"label": "6 Furies",
                          "units": [{"unit": "furies", "count": 6}]}],
         "extraUnit": {"unit": "furies", "cost": 25, "max": 2, "label": "Additional Furies"},
         "allowedUpgrades": ["daemon-chaos-spawn"]},
        {"id": "undivided-spawn-pack", "name": "Undivided Spawn Pack",
         "category": "Support", "baseCost": 200,
         "composition": "4 Chaos Spawn (+50 each, up to 6)",
         "unitOptions": [{"label": "4 Spawn",
                          "units": [{"unit": "chaos-spawn", "count": 4}]}],
         "extraUnit": {"unit": "chaos-spawn", "cost": 50, "max": 2, "label": "Additional Spawn"},
         "allowedUpgrades": []},

        # ----- Lords of War (Greater Daemons, 1-3 each) -----
        daemon_greater("greater-bloodthirster", "Greater Daemon: Bloodthirster Host",
                       "bloodthirster", "Bloodthirster"),
        daemon_greater("greater-lord-of-change", "Greater Daemon: Lord of Change Host",
                       "lord-of-change", "Lord of Change"),
        daemon_greater("greater-great-unclean", "Greater Daemon: Great Unclean One Host",
                       "great-unclean-one", "Great Unclean One"),
        daemon_greater("greater-keeper-of-secrets", "Greater Daemon: Keeper of Secrets Host",
                       "keeper-of-secrets", "Keeper of Secrets"),
    ],
    "upgrades": [
        # Per-god small host (Lesser Daemons) — adds 6 of a unit type at flat +150
        {"id": "daemon-small-host-tzeentch", "name": "Small Host (Tzeentch)",
         "type": "flag", "cost": 150,
         "description": "Add 6 Horrors, Flamers OR Screamers (any combination).",
         "addedUnits": [{"unit": "horror", "count": 6}]},
        {"id": "daemon-small-host-slaanesh", "name": "Small Host (Slaanesh)",
         "type": "flag", "cost": 150,
         "description": "Add 6 Daemonettes OR Seekers (any combination).",
         "addedUnits": [{"unit": "daemonette", "count": 6}]},
        {"id": "daemon-small-host-khorne", "name": "Small Host (Khorne)",
         "type": "flag", "cost": 150,
         "description": "Add 6 Bloodletters OR Flesh Hounds (any combination).",
         "addedUnits": [{"unit": "bloodletter", "count": 6}]},
        {"id": "daemon-small-host-nurgle", "name": "Small Host (Nurgle)",
         "type": "flag", "cost": 150,
         "description": "Add 6 Plaguebearers OR Nurglings (any combination).",
         "addedUnits": [{"unit": "plaguebearer", "count": 6}]},

        # Per-god large host (chariots / beasts / drones / fiends) — flat +300
        {"id": "daemon-large-host-tzeentch", "name": "Large Host (Tzeentch)",
         "type": "flag", "cost": 300,
         "description": "Add 6 Burning Chariots of Tzeentch.",
         "addedUnits": [{"unit": "burning-chariot", "count": 6}]},
        {"id": "daemon-large-host-slaanesh", "name": "Large Host (Slaanesh)",
         "type": "flag", "cost": 300,
         "description": "Add 6 Seeker Chariots OR Fiends of Slaanesh.",
         "addedUnits": [{"unit": "seeker-chariot", "count": 6}]},
        {"id": "daemon-large-host-khorne", "name": "Large Host (Khorne)",
         "type": "flag", "cost": 300,
         "description": "Add 6 Bloodcrushers OR Skull Cannons (any combination).",
         "addedUnits": [{"unit": "bloodcrusher", "count": 6}]},
        {"id": "daemon-large-host-nurgle", "name": "Large Host (Nurgle)",
         "type": "flag", "cost": 300,
         "description": "Add 6 Beasts of Nurgle OR Plague Drones.",
         "addedUnits": [{"unit": "beast-of-nurgle", "count": 6}]},

        # Greater Daemon attached to Line detachment (0-1 per line)
        {"id": "daemon-lord-of-change", "name": "0-1 Lord of Change",
         "type": "flag", "cost": 200,
         "description": "Add 1 Lord of Change (Greater Daemon).",
         "addedUnits": [{"unit": "lord-of-change", "count": 1}]},
        {"id": "daemon-keeper-of-secrets", "name": "0-1 Keeper of Secrets",
         "type": "flag", "cost": 200,
         "description": "Add 1 Keeper of Secrets (Greater Daemon).",
         "addedUnits": [{"unit": "keeper-of-secrets", "count": 1}]},
        {"id": "daemon-bloodthirster", "name": "0-1 Bloodthirster",
         "type": "flag", "cost": 200,
         "description": "Add 1 Bloodthirster (Greater Daemon).",
         "addedUnits": [{"unit": "bloodthirster", "count": 1}]},
        {"id": "daemon-great-unclean-one", "name": "0-1 Great Unclean One",
         "type": "flag", "cost": 200,
         "description": "Add 1 Great Unclean One (Greater Daemon).",
         "addedUnits": [{"unit": "great-unclean-one", "count": 1}]},

        # Per-god Daemon Prince upgrade (upgrade a Herald to Daemon Prince)
        {"id": "daemon-prince-tzeentch", "name": "Daemon Prince (Tzeentch)",
         "type": "flag", "cost": 50,
         "description": "Upgrade Herald to Daemon Prince (max 1 per god affiliation).",
         "addedUnits": [{"unit": "daemon-prince-tzeentch", "count": 1}]},
        {"id": "daemon-prince-slaanesh", "name": "Daemon Prince (Slaanesh)",
         "type": "flag", "cost": 50,
         "description": "Upgrade Herald to Daemon Prince (max 1 per god affiliation).",
         "addedUnits": [{"unit": "daemon-prince-slaanesh", "count": 1}]},
        {"id": "daemon-prince-khorne", "name": "Daemon Prince (Khorne)",
         "type": "flag", "cost": 50,
         "description": "Upgrade Herald to Daemon Prince (max 1 per god affiliation).",
         "addedUnits": [{"unit": "daemon-prince-khorne", "count": 1}]},
        {"id": "daemon-prince-nurgle", "name": "Daemon Prince (Nurgle)",
         "type": "flag", "cost": 50,
         "description": "Upgrade Herald to Daemon Prince (max 1 per god affiliation).",
         "addedUnits": [{"unit": "daemon-prince-nurgle", "count": 1}]},

        # Universal upgrades
        {"id": "daemon-chaos-spawn", "name": "Chaos Spawn", "type": "multi", "max": 3,
         "description": "Add 1-3 Chaos Spawn.",
         "variants": [{"id": "chaos-spawn", "name": "Chaos Spawn", "cost": 50}]},
        {"id": "daemon-chaos-altar", "name": "Chaos Altar",
         "type": "flag", "cost": 100,
         "description": "Add 1 Chaos Altar.",
         "addedUnits": [{"unit": "chaos-altar", "count": 1}]},
    ],
    "units": {
        # Undivided
        "furies": {
            "name": "Furies", "type": "INF",
            "speed": "30cm", "armour": "6+", "cc": "4+", "ff": "6+",
            "weapons": [
                {"name": "Fangs and Claws", "range": "(base)", "firepower": "(assault)"},
                {"name": "Aerial Assault", "range": "30cm", "firepower": "AA6+"},
            ],
            "notes": ["Jump pack.", "Invulnerable save.", "Scout."],
        },
        "chaos-spawn": {
            "name": "Chaos Spawn", "type": "INF",
            "speed": "15cm", "armour": "3+", "cc": "3+", "ff": "6+",
            "weapons": [{"name": "Chaos Spawn Mutations", "range": "(base)",
                         "firepower": "(assault) EA (D3)"}],
            "notes": ["Invulnerable save.", "Fearless."],
        },
        "soul-grinder": {
            "name": "Soul Grinder", "type": "AV",
            "speed": "15cm", "armour": "3+", "cc": "3+", "ff": "4+",
            "weapons": [
                {"name": "Harvester Claws", "range": "(base)",
                 "firepower": "(assault) MW, EA (+1)"},
                {"name": "Phlegm", "range": "30cm",
                 "firepower": "AP4+/AT4+/AA5+"},
                {"name": "Vomit", "range": "15cm",
                 "firepower": "AP3+, Ignore cover"},
            ],
            "notes": ["Invulnerable save.", "Berserk.", "Walker."],
        },
        "chaos-altar": {
            "name": "Chaos Altar", "type": "WE",
            "speed": "15cm", "armour": "4+", "cc": "4+", "ff": "4+",
            "weapons": [{"name": "Arcane Tech", "range": "45cm",
                         "firepower": "D3× AP4+/AT4+/AA4+"}],
            "notes": ["DC3.", "Invulnerable save.", "Reinforced armour.",
                      "Fearless.", "Inspiring.",
                      "Critical Hit: Destroyed; units within 5cm MW hit on 6+."],
        },
        "harpy": {
            "name": "Harpy", "type": "AC",
            "speed": "Fighter", "armour": "6+", "cc": "-", "ff": "-",
            "weapons": [{"name": "Wicked Talons", "range": "15cm",
                         "firepower": "AP5+/AT5+/AA5+"}],
            "notes": ["Invulnerable save."],
        },
        # Khorne
        "herald-khorne": {
            "name": "Herald of Khorne", "type": "CH",
            "speed": "-", "armour": "-", "cc": "3+", "ff": "6+",
            "weapons": [{"name": "Blade of Blood", "range": "(base)",
                         "firepower": "(assault) Fleshbane, EA (+1)"}],
            "notes": ["Commander.", "Ferocity."],
        },
        "daemon-prince-khorne": {
            "name": "Daemon Prince of Khorne", "type": "INF",
            "speed": "15cm", "armour": "3+", "cc": "3+", "ff": "-",
            "weapons": [{"name": "Skullreaver", "range": "(base)",
                         "firepower": "(assault) MW, EA (+1)"}],
            "notes": ["Commander.", "Leader.", "Brutal.", "Fearless.",
                      "Ferocity.", "Inspiring.", "Invulnerable save."],
        },
        "bloodletter": {
            "name": "Bloodletters", "type": "INF",
            "speed": "15cm", "armour": "4+", "cc": "4+", "ff": "-",
            "weapons": [{"name": "Hellblades", "range": "(base)",
                         "firepower": "(assault) EA (+1)"}],
            "notes": ["Brutal.", "Invulnerable save."],
        },
        "flesh-hound": {
            "name": "Flesh Hounds", "type": "INF",
            "speed": "20cm", "armour": "5+", "cc": "3+", "ff": "-",
            "weapons": [{"name": "Fangs and Claws", "range": "(base)",
                         "firepower": "(assault)"}],
            "notes": ["Brutal.", "Infiltrator.", "Invulnerable save."],
        },
        "bloodcrusher": {
            "name": "Bloodcrushers", "type": "INF",
            "speed": "20cm", "armour": "3+", "cc": "3+", "ff": "-",
            "weapons": [{"name": "Juggernaut Barbs", "range": "(base)",
                         "firepower": "(assault) Fleshbane, EA (+1)"}],
            "notes": ["Berserk.", "Brutal.", "Invulnerable save."],
        },
        "skull-cannon": {
            "name": "Skull Cannon", "type": "LV",
            "speed": "15cm", "armour": "5+", "cc": "5+", "ff": "4+",
            "weapons": [{"name": "Skull Cannon", "range": "30cm",
                         "firepower": "AP3/AT5+, Ignore cover"}],
            "notes": ["Brutal.", "Invulnerable save."],
        },
        "bloodthirster": {
            "name": "Bloodthirster of Unfettered Fury (Greater Daemon)", "type": "WE",
            "speed": "20cm", "armour": "4+", "cc": "3+", "ff": "4+",
            "weapons": [
                {"name": "Axe of Khorne", "range": "(base)",
                 "firepower": "(assault) TK (1), EA (+1)"},
                {"name": "Lash of Khorne", "range": "(15cm)",
                 "firepower": "(small arms) Fleshbane"},
            ],
            "notes": ["DC3.", "Jump pack.", "Commander.", "Leader.",
                      "Reinforced armour.", "Brutal.", "Berserk.", "Inspiring.",
                      "Fearless.", "Ferocity.", "Invulnerable save (5+).",
                      "Walker.",
                      "Critical Hit: hurled back into the warp; MW hit on 6+ within 5cm."],
        },
        # Nurgle
        "herald-nurgle": {
            "name": "Herald of Nurgle", "type": "CH",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [{"name": "Stream of Corruption", "range": "(15cm)",
                         "firepower": "(small arms) Fleshbane, EA (+1)"}],
            "notes": ["Commander.", "Remorseless."],
        },
        "daemon-prince-nurgle": {
            "name": "Daemon Prince of Nurgle", "type": "INF",
            "speed": "15cm", "armour": "4+", "cc": "4+", "ff": "4+",
            "weapons": [{"name": "Blighted Blade", "range": "(base)",
                         "firepower": "(assault)"}],
            "notes": ["Commander.", "Leader.", "Inspiring.", "Fearless.",
                      "Invulnerable save.", "Reinforced armour.", "Remorseless."],
        },
        "plaguebearer": {
            "name": "Plaguebearers", "type": "INF",
            "speed": "15cm", "armour": "3+", "cc": "4+", "ff": "6+",
            "weapons": [{"name": "Plaguesword", "range": "(base)",
                         "firepower": "(assault)"}],
            "notes": ["Invulnerable save."],
        },
        "nurgling": {
            "name": "Nurglings", "type": "INF",
            "speed": "15cm", "armour": "4+", "cc": "5+", "ff": "6+",
            "weapons": [{"name": "Tiny Sharp Teeth", "range": "(base)",
                         "firepower": "(assault)"}],
            "notes": ["Invulnerable save.", "Scout."],
        },
        "beast-of-nurgle": {
            "name": "Beast of Nurgle", "type": "INF",
            "speed": "15cm", "armour": "3+", "cc": "4+", "ff": "5+",
            "weapons": [
                {"name": "Acidic Slime", "range": "(base)",
                 "firepower": "(assault) Ignore cover"},
                {"name": "Cloud of Flies", "range": "(15cm)",
                 "firepower": "(small arms) Ignore cover"},
            ],
            "notes": ["Fearless.", "Invulnerable save.", "Mounted.", "Walker."],
        },
        "plague-drone": {
            "name": "Plague Drones", "type": "LV",
            "speed": "30cm", "armour": "3+", "cc": "4+", "ff": "4+",
            "weapons": [{"name": "Plague Sword", "range": "(base)",
                         "firepower": "(assault)"}],
            "notes": ["Jump pack.", "Fearless.", "Invulnerable save.", "Scout."],
        },
        "great-unclean-one": {
            "name": "Great Unclean One (Greater Daemon)", "type": "WE",
            "speed": "15cm", "armour": "4+", "cc": "4+", "ff": "4+",
            "weapons": [
                {"name": "Bilesword", "range": "(base)",
                 "firepower": "(assault) MW, EA (+1)"},
                {"name": "Gift of Bountiful Vomit",
                 "range": "30cm & (15cm)",
                 "firepower": "3 BP, Ignore cover / (small arms) Ignore cover"},
            ],
            "notes": ["DC3.", "Commander.", "Leader.", "Inspiring.",
                      "Fearless.", "Invulnerable save (5+).",
                      "Reinforced armour.", "Remorseless.", "Walker."],
        },
        # Slaanesh
        "herald-slaanesh": {
            "name": "Herald of Slaanesh", "type": "CH",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [{"name": "Daemon Blade", "range": "(base)",
                         "firepower": "(assault) MW, EA (+1)"}],
            "notes": ["Commander.", "Brutal."],
        },
        "daemon-prince-slaanesh": {
            "name": "Daemon Prince of Slaanesh", "type": "INF",
            "speed": "15cm", "armour": "3+", "cc": "3+", "ff": "3+",
            "weapons": [
                {"name": "Crushing Claws", "range": "(base)",
                 "firepower": "(assault) MW, First strike"},
                {"name": "Soporific Musk", "range": "(15cm)",
                 "firepower": "(small arms) MW, EA (+1), First strike"},
            ],
            "notes": ["Commander.", "Leader.", "Inspiring.", "Fearless.",
                      "Invulnerable save.",
                      "May take wings (Jump pack, +Speed 30cm, -1 armour to 4+)."],
        },
        "daemonette": {
            "name": "Daemonettes", "type": "INF",
            "speed": "15cm", "armour": "4+", "cc": "3+", "ff": "-",
            "weapons": [{"name": "Talons", "range": "(base)",
                         "firepower": "(assault) First strike"}],
            "notes": ["Ferocity.", "Invulnerable save."],
        },
        "fiend": {
            "name": "Fiends of Slaanesh", "type": "INF",
            "speed": "20cm", "armour": "4+", "cc": "3+", "ff": "-",
            "weapons": [{"name": "Rending Claws", "range": "(base)",
                         "firepower": "(assault) EA (+1), First strike"}],
            "notes": ["Ferocity.", "Infiltrator.", "Invulnerable save."],
        },
        "seeker": {
            "name": "Seekers of Slaanesh", "type": "INF",
            "speed": "35cm", "armour": "4+", "cc": "4+", "ff": "-",
            "weapons": [{"name": "Daemonic Talons", "range": "(base)",
                         "firepower": "(assault) EA (+1), First strike"}],
            "notes": ["Brutal.", "Invulnerable save.", "Mounted."],
        },
        "seeker-chariot": {
            "name": "Seeker Chariot", "type": "LV",
            "speed": "30cm", "armour": "5+", "cc": "3+", "ff": "6+",
            "weapons": [{"name": "Fleshshredder", "range": "(base)",
                         "firepower": "(assault) EA (+1), First strike"}],
            "notes": ["Brutal.", "Invulnerable save.", "Walker."],
        },
        "keeper-of-secrets": {
            "name": "Keeper of Secrets (Greater Daemon)", "type": "WE",
            "speed": "15cm", "armour": "5+", "cc": "3+", "ff": "4+",
            "weapons": [
                {"name": "Lash of Torment", "range": "(base)",
                 "firepower": "(assault) MW, EA (+1), First strike"},
                {"name": "Gaze of Slaanesh", "range": "(15cm)",
                 "firepower": "(small arms) MW, EA (+1), First strike"},
            ],
            "notes": ["DC3.", "Commander.", "Leader.", "Inspiring.",
                      "Fearless.", "Invulnerable save.",
                      "Reinforced armour.", "Walker."],
        },
        # Tzeentch
        "herald-tzeentch": {
            "name": "Herald of Tzeentch", "type": "CH",
            "speed": "-", "armour": "-", "cc": "-", "ff": "-",
            "weapons": [{"name": "Sorcerous Blast", "range": "(15cm)",
                         "firepower": "(small arms) MW, EA (+1), Singularity"}],
            "notes": ["Commander.", "Invulnerable save (5+)."],
        },
        "daemon-prince-tzeentch": {
            "name": "Daemon Prince of Tzeentch", "type": "INF",
            "speed": "15cm", "armour": "3+", "cc": "3+", "ff": "3+",
            "weapons": [{"name": "Warp Tempest", "range": "(15cm)",
                         "firepower": "(small arms) MW, EA (+2)"}],
            "notes": ["Commander.", "Leader.", "Fearless.", "Inspiring.",
                      "Invulnerable save.", "Reinforced armour.",
                      "May take wings (Jump pack, +Speed 30cm, -1 armour to 4+)."],
        },
        "horror": {
            "name": "Horrors", "type": "INF",
            "speed": "15cm", "armour": "4+", "cc": "5+", "ff": "4+",
            "weapons": [{"name": "Daemonic Fire", "range": "(15cm)",
                         "firepower": "(small arms)"}],
            "notes": ["Invulnerable save."],
        },
        "flamer": {
            "name": "Flamers of Tzeentch", "type": "INF",
            "speed": "15cm", "armour": "5+", "cc": "5+", "ff": "4+",
            "weapons": [{"name": "Flickering Flames",
                         "range": "15cm & (15cm)",
                         "firepower": "AP5+/AT5+ / (small arms) EA (+1)"}],
            "notes": ["Invulnerable save.", "Jump pack."],
        },
        "screamer": {
            "name": "Screamers", "type": "INF",
            "speed": "30cm", "armour": "5+", "cc": "3+", "ff": "6+",
            "weapons": [{"name": "Fangs", "range": "(base)",
                         "firepower": "(assault)"}],
            "notes": ["Invulnerable save.", "Skimmer."],
        },
        "burning-chariot": {
            "name": "Burning Chariot of Tzeentch", "type": "LV",
            "speed": "20cm", "armour": "5+", "cc": "6+", "ff": "4+",
            "weapons": [{"name": "Exalted Flamer",
                         "range": "15cm & (15cm)",
                         "firepower": "D3× AP5+/AT5+ / (small arms) EA (+1), Ignore cover"}],
            "notes": ["Invulnerable save.", "Skimmer."],
        },
        "lord-of-change": {
            "name": "Lord of Change (Greater Daemon)", "type": "WE",
            "speed": "30cm", "armour": "4+", "cc": "5+", "ff": "3+",
            "weapons": [
                {"name": "Bedlam Staff", "range": "(base)",
                 "firepower": "(assault) MW, EA (+1)"},
                {"name": "Withering Gaze",
                 "range": "45cm & (15cm)",
                 "firepower": "2× AP3+/AT3+, MW / (small arms)"},
            ],
            "notes": ["Jump packs.", "Commander.", "Leader.", "Inspiring.",
                      "Fearless.", "Invulnerable save (5+).",
                      "Reinforced armour.", "Walker."],
        },
    },
}


def main():
    doc = json.loads(DATA.read_text(encoding="utf-8"))
    factions = doc["factions"]
    new_ids = {f["id"] for f in (mechanicum, custodes, daemons)}
    factions = [f for f in factions if f["id"] not in new_ids]
    factions.extend([mechanicum, custodes, daemons])

    # Clean: remove `compositionLimits: None` (server returns it as null).
    for fac in (mechanicum, custodes, daemons):
        if fac["compositionLimits"] is None:
            fac.pop("compositionLimits", None)

    doc["factions"] = factions
    DATA.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
                     encoding="utf-8")
    print(f"OK — wrote {len(factions)} factions")
    for fac in (mechanicum, custodes, daemons):
        print(f"  {fac['id']:20s} formations={len(fac['formations'])}, "
              f"units={len(fac['units'])}, upgrades={len(fac['upgrades'])}")


if __name__ == "__main__":
    main()
