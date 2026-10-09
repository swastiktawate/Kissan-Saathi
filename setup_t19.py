import os

os.makedirs('frontend/src/components', exist_ok=True)
os.makedirs('frontend/src/pages', exist_ok=True)

with open('frontend/src/components/ForecastChart.tsx', 'w', encoding='utf-8') as f:
    f.write('''import { ComposedChart, Line, Area, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function ForecastChart({ data }: { data: any[] }) {
    if (!data || data.length === 0) return <div>No forecast data</div>;

    return (
        <div className="bg-white p-2 border border-stone-200 rounded-sm mb-4 shadow-sm">
            <h3 className="font-bold mb-1 text-sm">Price Forecast (Rs/q)</h3>
            <div className="text-xs text-stone-500 mb-2">Estimated range, not guaranteed</div>
            <div className="h-48 w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <ComposedChart data={data} margin={{ top: 5, right: 0, left: -20, bottom: 5 }}>
                        <XAxis dataKey="day" fontSize={10} />
                        <YAxis fontSize={10} domain={['auto', 'auto']} />
                        <Tooltip contentStyle={{ fontSize: '12px' }} />
                        <Legend wrapperStyle={{ fontSize: '10px' }} />
                        <Area type="monotone" dataKey="band" stroke="none" fill="#bfdbfe" fillOpacity={0.4} name="P10 - P90" />
                        <Line type="monotone" dataKey="observed" stroke="#1c1917" strokeWidth={2} dot={false} name="Observed" />
                        <Line type="monotone" dataKey="forecast" stroke="#60a5fa" strokeDasharray="5 5" strokeWidth={2} dot={false} name="Forecast P50" />
                    </ComposedChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
''')

with open('frontend/src/components/MandiTable.tsx', 'w', encoding='utf-8') as f:
    f.write('''import { useState } from 'react';

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
''')

with open('frontend/src/pages/Detail.tsx', 'w', encoding='utf-8') as f:
    f.write('''import { Link } from 'react-router-dom';
import ForecastChart from '../components/ForecastChart';

export default function Detail() {
    const mockForecast = [
        { day: 'Mon', observed: 2100, band: [2100, 2100] },
        { day: 'Tue', observed: 2050, band: [2050, 2050] },
        { day: 'Wed', observed: 2150, band: [2150, 2150] },
        { day: 'Thu', forecast: 2200, band: [2100, 2300] },
        { day: 'Fri', forecast: 2250, band: [2120, 2400] },
        { day: 'Sat', forecast: 2180, band: [2000, 2350] },
    ];

    return (
        <div className="max-w-[360px] mx-auto min-h-screen flex flex-col p-4">
            <div className="flex gap-2 mb-4 text-sm font-bold items-center">
                <Link to="/" className="text-blue-600">&larr; Back</Link>
                <span>Insight Details</span>
            </div>
            
            <h2 className="text-xl font-bold mb-4">Tomato in Vashi</h2>
            <ForecastChart data={mockForecast} />
            
            <div className="bg-white p-4 border border-stone-200 rounded-sm shadow-sm text-sm">
                <h3 className="font-bold mb-2">Cost of Waiting</h3>
                <p>Chart coming in T20</p>
            </div>
        </div>
    );
}
''')

with open('frontend/src/pages/Mandis.tsx', 'w', encoding='utf-8') as f:
    f.write('''import { Link } from 'react-router-dom';
import MandiTable from '../components/MandiTable';

export default function Mandis() {
    const mockMandis = [
        { horizon: 0, name: 'Kalyan', dist: 50, price: 2100, net: 1950, isBest: true },
        { horizon: 0, name: 'Vashi', dist: 10, price: 1900, net: 1800, isBest: false },
        { horizon: 3, name: 'Kalyan', dist: 50, price: 2150, net: 1980, isBest: true },
        { horizon: 3, name: 'Vashi', dist: 10, price: 1950, net: 1820, isBest: false },
        { horizon: 7, name: 'Kalyan', dist: 50, price: 2200, net: 2000, isBest: true },
        { horizon: 7, name: 'Vashi', dist: 10, price: 1850, net: 1700, isBest: false },
    ];

    return (
        <div className="max-w-[360px] mx-auto min-h-screen flex flex-col p-4">
            <div className="flex gap-2 mb-4 text-sm font-bold items-center">
                <Link to="/" className="text-blue-600">&larr; Back</Link>
                <span>Market Compare</span>
            </div>
            
            <MandiTable data={mockMandis} />
        </div>
    );
}
''')
