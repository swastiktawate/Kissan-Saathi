import { ComposedChart, Line, Area, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

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
