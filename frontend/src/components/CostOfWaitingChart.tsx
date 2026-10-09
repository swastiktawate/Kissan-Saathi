import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function CostOfWaitingChart({ data, drivers }: { data: any[], drivers: any }) {
    if (!data || data.length === 0) return null;

    return (
        <div className="bg-white p-2 border border-stone-200 rounded-sm mb-4 shadow-sm">
            <h3 className="font-bold mb-1 text-sm">Cost of Waiting</h3>
            <div className="h-32 w-full mb-4">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data} margin={{ top: 5, right: 0, left: -20, bottom: 5 }}>
                        <XAxis dataKey="day" fontSize={10} />
                        <YAxis fontSize={10} />
                        <Tooltip contentStyle={{ fontSize: '12px' }} />
                        <Line type="monotone" dataKey="gain" stroke="#1c1917" strokeWidth={2} dot={{r: 3}} name="Gain" />
                    </LineChart>
                </ResponsiveContainer>
            </div>
            
            <div className="text-xs">
                <h4 className="font-bold mb-1">Factors affecting gain:</h4>
                <ul className="list-disc pl-4">
                    <li>Price movement: <span className={drivers.base_price > 0 ? "text-green-600" : "text-red-600"}>{drivers.base_price > 0 ? '+' : ''}{drivers.base_price}</span></li>
                    <li>Spoilage loss: <span className="text-red-600">{drivers.spoilage_cost}</span></li>
                    <li>Transport cost: <span>{drivers.transport}</span></li>
                </ul>
            </div>
        </div>
    );
}
