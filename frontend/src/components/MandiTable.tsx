import { useState } from 'react';

export default function MandiTable({ data }: { data: any[] }) {
    const [horizon, setHorizon] = useState(0);
    
    if (!data || data.length === 0) return <div>No mandi data</div>;
    
    const filtered = data.filter(d => d.horizon === horizon);

    return (
        <div className="bg-white border border-stone-200 rounded-sm mb-4 shadow-sm overflow-hidden">
            <div className="flex gap-2 p-2 border-b border-stone-200 text-sm">
                <button className={`px-2 py-1 rounded-sm ${horizon === 0 ? 'bg-stone-900 text-white' : 'bg-stone-200 text-textMain'}`} onClick={() => setHorizon(0)}>Today</button>
                <button className={`px-2 py-1 rounded-sm ${horizon === 3 ? 'bg-stone-900 text-white' : 'bg-stone-200 text-textMain'}`} onClick={() => setHorizon(3)}>+3 Days</button>
                <button className={`px-2 py-1 rounded-sm ${horizon === 7 ? 'bg-stone-900 text-white' : 'bg-stone-200 text-textMain'}`} onClick={() => setHorizon(7)}>+7 Days</button>
            </div>
            <div className="overflow-x-auto">
                <table className="w-full text-left text-xs whitespace-nowrap">
                    <thead>
                        <tr className="bg-stone-100 text-stone-600">
                            <th className="p-2 font-medium">Mandi</th>
                            <th className="p-2 font-medium">Dist (km)</th>
                            <th className="p-2 font-medium">Price</th>
                            <th className="p-2 font-medium">Net Return</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filtered.map((m, i) => (
                            <tr key={i} className={`border-b border-stone-100 ${m.isBest ? 'bg-blue-50' : ''}`}>
                                <td className="p-2 font-semibold">{m.name} {m.isBest && '★'}</td>
                                <td className="p-2">{m.dist}</td>
                                <td className="p-2">{m.price}</td>
                                <td className="p-2 font-bold">{m.net}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
