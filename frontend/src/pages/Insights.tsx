import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';

export default function Insights() {
    const [backtest, setBacktest] = useState<any>(null);

    useEffect(() => {
        fetch('http://localhost:8000/api/v1/backtest?crop=tomato&mandi=vashi')
            .then(res => res.json())
            .then(data => setBacktest(data))
            .catch(e => console.log(e));
    }, []);

    return (
        <div className="flex flex-col p-4 bg-canvas min-h-[calc(100vh-60px)]">
            <div className="flex gap-2 mb-4 text-sm font-bold items-center">
                <Link to="/" className="text-blue-600">&larr; Back</Link>
                <span>Backtest & Insights</span>
            </div>
            
            <h2 className="text-xl font-bold mb-4">Strategy Performance</h2>
            
            {backtest ? (
                <div className="bg-white p-4 border border-stone-200 rounded-sm shadow-sm text-sm">
                    <p className="text-xs text-stone-500 mb-2 uppercase tracking-wide">{backtest.data_origin_summary}</p>
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <p className="text-stone-500 text-xs">Mean Gain</p>
                            <p className="text-lg font-bold text-green-600">+{backtest.metrics.mean_gain} Rs/q</p>
                        </div>
                        <div>
                            <p className="text-stone-500 text-xs">Win Rate</p>
                            <p className="text-lg font-bold">{backtest.metrics.positive_dates_pct}%</p>
                        </div>
                        <div>
                            <p className="text-stone-500 text-xs">Worst Loss</p>
                            <p className="text-lg font-bold text-red-600">{backtest.metrics.worst_case_loss} Rs/q</p>
                        </div>
                        <div>
                            <p className="text-stone-500 text-xs">Days Tested</p>
                            <p className="text-lg font-bold">{backtest.days_tested}</p>
                        </div>
                    </div>
                </div>
            ) : (
                <div className="text-sm">Loading backtest...</div>
            )}
            
            <div className="bg-white p-4 border border-stone-200 rounded-sm shadow-sm text-sm mt-4">
                <h3 className="font-bold mb-2">Policy</h3>
                <p className="text-xs text-stone-600">
                    Recommendations simulate transport, spoilage, and holding costs based on PRD formulas. 
                    Accuracy figures are strictly bound to historical evaluations.
                </p>
            </div>
        </div>
    );
}
