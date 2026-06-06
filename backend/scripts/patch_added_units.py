"""
Patch flag-type upgrades that ADD units so the FormationEditor roster
surfaces them in the stat table.

Adds `addedUnits: [{unit, count}]` to:
  - solar-auxilia/sa-ogryn-charonite      (2 ogryn-charonite)
  - solar-auxilia/sa-rapier-battery       (4 sa-rapier-platform)
  - imperialis-militia/im-fire-support    (4 fire-support-team)
  - imperialis-militia/im-ogryn-brute-squad (4 ogryn-brute-squad)
  - imperialis-militia/im-sniper          (4 recon-team)

Converts solar-auxilia/sa-support (was flag) → multi (max 4), variants:
  - sa-close-support-section (+18.75)  [75 / 4]
  - veletaris-storm           (+18.75)
NOTE: Solar Auxilia book lists sa-support as +75 for 4 in any combo,
so we keep the flat 75 price and let users pick the split.  Modeled as
type:"multi" with `bundleCost: 75, max: 4` so the formation pays the
bundle once and the user splits the 4 picks across the two unit types.

The FormationEditor.jsx merge logic is updated separately to
(a) read flag.addedUnits, and (b) honour upgrade.bundleCost.
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "factions.json"

ADDED = {
    "solar-auxilia": {
        "sa-ogryn-charonite": [{"unit": "ogryn-charonite", "count": 2}],
        "sa-rapier-battery":  [{"unit": "sa-rapier-platform", "count": 4}],
    },
    "imperialis-militia": {
        "im-fire-support":     [{"unit": "fire-support-team", "count": 4}],
        "im-ogryn-brute-squad": [{"unit": "ogryn-brute-squad", "count": 4}],
        "im-sniper":            [{"unit": "recon-team", "count": 4}],
    },
}


def patch():
    doc = json.loads(DATA.read_text(encoding="utf-8"))
    for fac in doc["factions"]:
        rules = ADDED.get(fac["id"])
        if not rules:
            continue
        for up in fac["upgrades"]:
            if up["id"] in rules:
                up["addedUnits"] = rules[up["id"]]

        # Convert sa-support → multi with bundle pricing.
        if fac["id"] == "solar-auxilia":
            for up in fac["upgrades"]:
                if up["id"] == "sa-support":
                    up["type"] = "multi"
                    up["max"] = 4
                    up["bundleCost"] = 75
                    up.pop("cost", None)
                    up["variants"] = [
                        {"id": "sa-close-support-section",
                         "name": "Auxilia Close Support (Flamer) Section",
                         "cost": 0},
                        {"id": "veletaris-storm",
                         "name": "Veletaris Storm Section",
                         "cost": 0},
                    ]
                    up["description"] = (
                        "Add 4 units in any combination of Auxilia Close Support "
                        "(Flamer) Sections and/or Veletaris Storm Sections (75 pts total)."
                    )

    DATA.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
                     encoding="utf-8")
    print(f"OK — patched {DATA}")


if __name__ == "__main__":
    patch()
