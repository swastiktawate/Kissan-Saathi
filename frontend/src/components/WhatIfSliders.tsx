import { useState, useEffect } from 'react';
import { runWhatIf } from '../api/client';
import { Settings2 } from 'lucide-react';

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
        <div className="bg-white p-4 border border-stone-200 rounded-xl shadow-sm mb-6">
            <div className="flex justify-between items-center mb-4">
                <h3 className="font-bold text-stone-800 text-sm">Scenario Playground</h3>
                <Settings2 size={16} className="text-stone-400" />
            </div>
            
            <div className="mb-4">
                <label className="flex justify-between text-xs mb-2">
                    <span className="font-medium text-stone-700">Transport Cost Spike</span>
                    <span className="text-green-700 font-bold">+{transport}%</span>
                </label>
                <input 
                    type="range" min="0" max="50" value={transport} 
                    onChange={(e) => setTransport(parseInt(e.target.value))} 
                    className="w-full accent-green-600 h-1.5 bg-stone-200 rounded-lg appearance-none cursor-pointer"
                />
            </div>
            
            {result && (
                <div className="bg-green-50 p-3 border border-green-100 rounded-lg text-xs flex justify-between items-center">
                    <div>
                        <p className="text-stone-500 mb-1">Scenario Gain:</p>
                        <p className="font-bold text-stone-800 text-sm">₹{result.scenario.expected_gain.toFixed(2)}/q</p>
                    </div>
                    <div className="text-right">
                        <p className="text-stone-500 mb-1">Impact:</p>
                        <p className={`font-bold text-sm ${result.delta.nr_change < 0 ? 'text-red-500' : 'text-green-600'}`}>
                            {result.delta.nr_change > 0 ? '+' : ''}{result.delta.nr_change.toFixed(2)}
                        </p>
                    </div>
                </div>
            )}
        </div>
    );
}
