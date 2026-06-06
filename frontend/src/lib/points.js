// Pure helpers to calculate formation and army point totals.
export const formationCost = (formation, formationDef) => {
    if (!formationDef) return 0;
    let cost = formationDef.baseCost || 0;
    const extras = formation.extraUnits || 0;
    if (formationDef.extraUnit && extras > 0) {
        cost += extras * (formationDef.extraUnit.cost || 0);
    }
    (formation.upgrades || []).forEach((u) => {
        (u.selections || []).forEach((sel) => {
            cost += (sel.count || 0) * (sel.cost || 0);
        });
        if (u.flagCost) cost += u.flagCost;
    });
    return cost;
};

export const armyTotal = (army, faction) => {
    if (!army || !faction) return 0;
    const formMap = Object.fromEntries((faction.formations || []).map((f) => [f.id, f]));
    return (army.formations || []).reduce((sum, f) => sum + formationCost(f, formMap[f.formationId]), 0);
};
