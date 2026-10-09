import { useState, useEffect } from 'react';
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
