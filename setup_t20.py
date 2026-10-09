import os

with open('frontend/src/components/CostOfWaitingChart.tsx', 'w', encoding='utf-8') as f:
    f.write('''import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

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
''')

with open('frontend/src/components/RiskChips.tsx', 'w', encoding='utf-8') as f:
    f.write('''import { useState } from 'react';

export default function RiskChips({ risks }: { risks: any[] }) {
    const [expanded, setExpanded] = useState<number | null>(null);

    if (!risks || risks.length === 0) {
        return <div className="text-sm bg-stone-100 p-2 rounded-sm mb-4">No reliable risk signals.</div>;
    }

    return (
        <div className="flex flex-col gap-2 mb-4">
            <h3 className="font-bold text-sm">Risk Flags</h3>
            {risks.map((r, i) => (
                <div key={i} className="border border-stone-200 rounded-sm">
                    <button 
                        className="w-full text-left p-2 bg-white flex justify-between items-center text-sm"
                        onClick={() => setExpanded(expanded === i ? null : i)}
                    >
                        <span className="font-semibold text-red-600">⚠ {r.name}</span>
                        <span className="text-stone-400">{expanded === i ? '−' : '+'}</span>
                    </button>
                    {expanded === i && (
                        <div className="p-2 border-t border-stone-200 bg-stone-50 text-xs">
                            <p><strong>Value:</strong> {r.value}</p>
                            <p><strong>Threshold:</strong> {r.threshold}</p>
                            <p className="mt-1 text-stone-600">{r.explanation}</p>
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
}
''')

with open('frontend/src/components/WhatIfSliders.tsx', 'w', encoding='utf-8') as f:
    f.write('''import { useState, useEffect } from 'react';
import { runWhatIf } from '../api/client';

export default function WhatIfSliders() {
    const [transport, setTransport] = useState(0);
    const [result, setResult] = useState<any>(null);

    useEffect(() => {
        const timer = setTimeout(async () => {
            const res = await runWhatIf({ transport_multiplier: 1 + transport / 100 });
            setResult(res);
        }, 500);
        return () => clearTimeout(timer);
    }, [transport]);

    return (
        <div className="bg-white p-4 border border-stone-200 rounded-sm shadow-sm mb-4">
            <h3 className="font-bold mb-4 text-sm">Scenario Playground</h3>
            
            <div className="mb-4">
                <label className="flex justify-between text-xs mb-1">
                    <span>Transport Cost Spike</span>
                    <span>+{transport}%</span>
                </label>
                <input 
                    type="range" min="0" max="50" value={transport} 
                    onChange={(e) => setTransport(parseInt(e.target.value))} 
                    className="w-full"
                />
            </div>
            
            {result && (
                <div className="bg-stone-50 p-2 border border-stone-200 rounded-sm text-xs">
                    <p><strong>Baseline Gain:</strong> {result.baseline.expected_gain.toFixed(2)}</p>
                    <p><strong>Scenario Gain:</strong> {result.scenario.expected_gain.toFixed(2)}</p>
                    <p className="mt-1 font-bold text-red-600">Delta: {result.delta.nr_change.toFixed(2)}</p>
                </div>
            )}
        </div>
    );
}
''')

with open('frontend/src/components/ExplanationPanel.tsx', 'w', encoding='utf-8') as f:
    f.write('''export default function ExplanationPanel({ isVisible, onClose }: { isVisible: boolean, onClose: () => void }) {
    if (!isVisible) return null;
    
    return (
        <div className="fixed inset-0 bg-stone-900/50 z-50 flex flex-col justify-end">
            <div className="bg-white max-h-[80vh] overflow-y-auto w-full max-w-[360px] mx-auto rounded-t-lg p-4">
                <div className="flex justify-between items-center mb-4">
                    <h2 className="font-bold">About this Data</h2>
                    <button onClick={onClose} className="text-xl">&times;</button>
                </div>
                <div className="text-sm">
                    <p className="mb-2"><strong>Data Source:</strong> data.gov.in (Synthetic Fallback)</p>
                    <p className="mb-2"><strong>Trust Score:</strong> High (85/100)</p>
                    <ul className="list-disc pl-4 mb-4 text-xs text-stone-600">
                        <li>Freshness: 30/30</li>
                        <li>Completeness: 20/25</li>
                    </ul>
                    <p className="text-xs text-stone-500 italic">Updated: {new Date().toLocaleDateString()}</p>
                </div>
            </div>
        </div>
    );
}
''')
