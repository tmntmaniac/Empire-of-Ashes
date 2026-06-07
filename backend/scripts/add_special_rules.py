"""Inject `specialRules: [{name, description}]` for the 7 non-Astartes factions.

Source: /app/pdf_work/eoa.txt pages 32 (SA), 35 (IM), 37 (KH), 39 (LT),
41 (Mech), 43 (Custodes), 45 (Daemons). Idempotent — re-running overwrites.
"""
import json
from pathlib import Path

PATH = Path("/app/backend/data/factions.json")
data = json.loads(PATH.read_text())

RULES = {
    "solar-auxilia": [
        {
            "name": "Legate Commanders",
            "description": (
                "A Solar Auxilia army may include one Legate Commander character per 750 points, "
                "or part thereof, in the army. Legate Commanders cost no points. They are added at the "
                "start of the battle before either side sets up. If the army includes a Lord Marshall, "
                "the first Legate Commander must be attached to that formation. Otherwise the first "
                "must be attached to the most expensive Line Detachment. No more than one Legate "
                "Commander per formation, and none may be attached to Imperial Navy or allied formations. "
                "Excess Legate Commanders are lost."
            ),
        },
        {
            "name": "Armoured Spearhead",
            "description": (
                "An army with the Armoured Spearhead special rule may garrison one formation that has "
                "more than 2 AV units per full 2,000 points, regardless of the normal restrictions for "
                "unit/formation types able to garrison. These formations may be placed on Overwatch but "
                "still count toward the maximum number of garrisoned units that may Overwatch (normally two)."
            ),
        },
    ],
    "imperialis-militia": [
        {
            "name": "Discipline Masters / Rogue Psykers",
            "description": (
                "An Imperialis Militia army may include one free Discipline Master character for every "
                "full 750 points, assigned prior to the start of the battle. If the army includes a Force "
                "Commander, the first Discipline Master must be attached to the formation containing the "
                "Force Commander. Otherwise the first must be placed in the most expensive Imperialis "
                "Militia Line Detachment. Further Discipline Masters may be attached to any other "
                "Imperialis Militia formation. No more than one Discipline Master per formation, and "
                "none may be attached to an allied formation. A Rogue Psyker may be exchanged for a "
                "Discipline Master in a formation that has taken the Traitors Provenance upgrade."
            ),
        },
        {
            "name": "Provenance",
            "description": (
                "Before the start of the game, select up to two of the Provenances from the list below. "
                "You may then select one of these two provenances per formation and modify the attributes "
                "of all Infantry (INF) units in the formation as indicated.\n"
                "• Determined: +1 Firefight (FF) value when defending in an assault or using supporting fire.\n"
                "• Feral Warriors: +1 Close Combat (CC) value.\n"
                "• Survivors of the Dark Age: +1 Armour save (Armour) value.\n"
                "• Traitors: gain the Berserk trait. Ogryn Brute Squad units chosen in a formation with "
                "the Traitors Provenance must choose the Chaos Spawn Mutations option. Units with the "
                "Mounted trait gain Ferocity instead of Berserk.\n"
                "• Void Fighters: Grenadier units gain Jump packs and increase their movement to 30cm "
                "but may not take Standard or Heavy Transport options except the Arvus Lighter.\n"
                "• Warrior Elite: +1 Firefight (FF) value when taking an Engage action."
            ),
        },
    ],
    "knight-household": [
        {
            "name": "Ion Gauntlet",
            "description": (
                "Grants a 4+ save vs Normal, Macro-Weapon & Titan Killer shooting, as well as hits from "
                "Firefight, and a 5+ save against Normal, Macro-Weapon, and Titan Killer Close Combat "
                "hits. Each point of Titan Killer damage must be saved individually. Failed saves may use "
                "Reinforced armour rerolls against the Knight's armour if not negated by Titan Killer, "
                "Macro-Weapons, or Lance special rules. Ion Gauntlets may not be used in a Crossfire."
            ),
        },
        {
            "name": "Ion Shield",
            "description": (
                "Grants a 4+ save vs Normal, Macro-Weapon & Titan Killer shooting, as well as hits from "
                "Firefight. Each point of Titan Killer damage must be saved individually. Failed saves "
                "may use Reinforced armour rerolls against the Knight's armour if not negated by Titan "
                "Killer, Macro-Weapon, or Lance special rules. Ion Shields may not be used in a Crossfire."
            ),
        },
    ],
    "legio-titanicus": [
        {
            "name": "Void Shields",
            "description": (
                "Some units are protected by void shield generators. Each void shield will stop one "
                "point of damage and then go down. Do not make armour saves for damage stopped by void "
                "shields, or allocate Blast markers. Once all of the shields have been knocked down, the "
                "unit may be damaged normally and you may make saving throws against any hits that are "
                "allocated and suffer Blast markers as normal.\n\n"
                "Hits from close combat ignore void shields, but units using their firefight value must "
                "first knock down any shields before they can damage the unit. Void shields that have "
                "been knocked down can be repaired: a unit automatically repairs one downed void shield "
                "in the end phase of each turn. In addition, if a unit regroups it can use the dice roll "
                "to either repair a void shield or remove Blast markers (e.g. if you rolled a 2 you "
                "could repair 2 shields, remove 2 Blast markers, or repair 1 shield and remove 1 Blast marker)."
            ),
        },
    ],
    "mechanicum-taghmata": [
        {
            "name": "Automaton",
            "description": (
                "A formation does not receive a Blast marker when a unit with Automaton is destroyed. "
                "However, Automaton units hit by a weapon with Disrupt do take a Blast marker. If a hit "
                "is inflicted on an Automaton unit because it is in a broken formation which is receiving "
                "a Blast marker (see Blast Markers and Broken Formations) then it may attempt to save "
                "normally."
            ),
        },
        {
            "name": "Cortex Controller and Cybernetica Cortex",
            "description": (
                "Formations that include units with the Cybernetica Cortex trait suffer a -1 penalty on "
                "all Action tests and may not take March or Overwatch actions unless at least 1 unit in "
                "the formation is within 15cm of a unit with the Cortex Controller trait."
            ),
        },
    ],
    "legio-custodes": [
        {
            "name": "The Emperor's Chosen",
            "description": (
                "The Legio Custodes are famed as the Emperor's elite guard, forged by his hand by arcane "
                "alchemical means. This is represented by the following changes to the standard rules, "
                "which apply to all Legio Custodes units:\n"
                "• It takes 2 Blast markers to suppress a Legio Custodes unit or kill a unit in a broken "
                "formation (ignoring any leftover Blast markers).\n"
                "• Legio Custodes formations are only considered broken if they have 2 Blast markers per "
                "unit in the formation (as opposed to the standard one Blast marker per unit).\n"
                "• Legio Custodes formations only count half the number of Blast markers in assault "
                "resolution, rounding down. (Note: for assault resolution, enemy formations will not "
                "receive a +1 for having no Blast markers if the Custodes formation only has 1 Blast "
                "marker before rounding down.)\n"
                "• When a broken Legio Custodes formation rallies, it receives a number of Blast markers "
                "equal to the number of units, rather than half their number rounding down. Legio "
                "Custodes with the Leader trait remove 2 Blast markers instead of 1.\n"
                "• Legio Custodes formations halve the number of hackdowns suffered when a formation "
                "loses an assault.\n"
                "• Legio Custodes units ignore the -1 penalty to Rally tests if enemies are within 30cm."
            ),
        },
    ],
    "daemons-ruinstorm": [
        {
            "name": "Instability",
            "description": (
                "Any Line detachment that fails an Action test, for any reason, immediately loses 1D3 "
                "Lesser Daemons (INF). These losses do not cause any additional Blast markers."
            ),
        },
        {
            "name": "Chaos Gate",
            "description": (
                "Chaos Gates are breaches in the walls of reality that allow the forces of Chaos direct "
                "access from their foul realms. A Chaos Gate included in the army allows the Chaos "
                "player to pick up to three other formations and keep them within the Warp instead of "
                "deploying them normally. Any formations kept within the Warp may enter play via the "
                "Chaos Gate by taking an action that allows them to make a move, then measuring their "
                "first move from the centre of the Chaos Gate objective marker. No more than one "
                "formation may deploy from a Chaos Gate each turn."
            ),
        },
        {
            "name": "Daemonic Assault",
            "description": (
                "Before deployment, the Daemon player may nominate one formation in their army per "
                "1,000 points of this Army List to deploy by Teleport. These formations may only enter "
                "play from the second turn on, and may contain any units, with the restriction that the "
                "formation may only include a single Greater Daemon unit."
            ),
        },
    ],
}

changed = 0
for fac in data["factions"]:
    if fac["id"] not in RULES:
        continue
    fac["specialRules"] = RULES[fac["id"]]
    changed += 1
    print(f"  set specialRules ({len(RULES[fac['id']])} entries) on {fac['id']}")

PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
print(f"Done. {changed} factions updated.")
