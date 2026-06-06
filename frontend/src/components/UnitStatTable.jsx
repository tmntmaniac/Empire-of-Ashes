export default function UnitStatTable({ units, faction }) {
    if (!units || units.length === 0) return null;
    return (
        <div className="overflow-x-auto">
            <table className="stat-table" data-testid="unit-stat-table">
                <thead>
                    <tr>
                        <th>Unit</th>
                        <th>Type</th>
                        <th>Speed</th>
                        <th>Armour</th>
                        <th>CC</th>
                        <th>FF</th>
                        <th>Weapons / Notes</th>
                    </tr>
                </thead>
                <tbody>
                    {units.map(({ unitId, count }) => {
                        const u = faction.units?.[unitId];
                        if (!u) return null;
                        return (
                            <tr key={unitId}>
                                <td className="text-[#E0E0E0]">{count}× {u.name}</td>
                                <td><span className="tag tag-green">{u.type}</span></td>
                                <td>{u.speed}</td>
                                <td>{u.armour}</td>
                                <td>{u.cc}</td>
                                <td>{u.ff}</td>
                                <td className="text-[#B8B8B8]">
                                    {(u.weapons || []).map((w, i) => (
                                        <div key={i}>
                                            <span className="text-[#C2A165]">{w.name}</span> <span className="text-[#888]">{w.range}</span> {w.firepower}
                                        </div>
                                    ))}
                                    {u.notes && u.notes.length > 0 && (
                                        <div className="text-[10px] text-[#888] mt-1">{u.notes.join(" · ")}</div>
                                    )}
                                </td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    );
}
