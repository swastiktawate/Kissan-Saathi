import { useState } from 'react';
import { Calendar, Search, TrendingDown, TrendingUp } from 'lucide-react';

interface RegretData {
    difference: number;
    result: string;
    message: string;
    sold_price: number;
    today_price: number;
    error?: string;
}

export default function RegretView({ crop = 'tomato', mandi = 'vashi' }: { crop?: string, mandi?: string }) {
    const [date, setDate] = useState('2024-05-01');
    const [quantity, setQuantity] = useState(50);
    const [data, setData] = useState<RegretData | null>(null);
    const [loading, setLoading] = useState(false);

    const handleAnalyze = async () => {
        setLoading(true);
        setData(null);
        try {
            const res = await fetch(`http://localhost:8000/api/v1/regret-analysis?crop=${crop}&mandi=${mandi}&quantity=${quantity}&sold_date=${date}`);
            const d = await res.json();
            setData(d);
        } catch (e) {
            setData({ error: "Network error", difference: 0, result: "", message: "", sold_price: 0, today_price: 0 });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-white rounded-xl shadow-md border border-stone-200 p-4 mb-4">
            <h3 className="font-bold text-stone-800 text-lg mb-1">Pichla Faisla (Looking Back)</h3>
            <p className="text-xs text-stone-500 mb-4">Evaluate a past sale decision against today's market.</p>
            
            <div className="flex gap-2 mb-4">
                <div className="flex-1 bg-stone-50 border border-stone-200 rounded-lg p-2 flex items-center">
                    <Calendar size={16} className="text-stone-400 mr-2" />
                    <input 
                        type="date" 
                        value={date} 
                        onChange={e => setDate(e.target.value)}
                        className="bg-transparent text-sm outline-none w-full text-stone-700"
                    />
                </div>
                <div className="w-24 bg-stone-50 border border-stone-200 rounded-lg p-2 flex items-center">
                    <input 
                        type="number" 
                        value={quantity} 
                        onChange={e => setQuantity(Number(e.target.value))}
                        className="bg-transparent text-sm outline-none w-full text-stone-700"
                        placeholder="Qty (q)"
                    />
                </div>
                <button 
                    onClick={handleAnalyze}
                    className="bg-green-600 hover:bg-green-700 text-white p-2 rounded-lg transition-colors flex items-center justify-center min-w-[40px]"
                >
                    <Search size={18} />
                </button>
            </div>

            {loading && <div className="text-xs text-stone-500 animate-pulse py-2">Analyzing past data...</div>}
            
            {data && data.error && (
                <div className="text-xs text-red-500 bg-red-50 p-2 rounded border border-red-100">
                    {data.error}
                </div>
            )}

            {data && !data.error && (
                <div className={`p-4 rounded-xl border ${data.result === 'loss' ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200'}`}>
                    <div className="flex items-start gap-3">
                        <div className={`p-2 rounded-full ${data.result === 'loss' ? 'bg-red-100 text-red-600' : 'bg-green-100 text-green-600'}`}>
                            {data.result === 'loss' ? <TrendingDown size={20} /> : <TrendingUp size={20} />}
                        </div>
                        <div>
                            <h4 className={`font-bold text-sm mb-1 ${data.result === 'loss' ? 'text-red-800' : 'text-green-800'}`}>
                                {data.result === 'loss' ? 'Sold Too Early' : 'Great Decision!'}
                            </h4>
                            <p className={`text-xs ${data.result === 'loss' ? 'text-red-700' : 'text-green-700'}`}>
                                {data.message}
                            </p>
                            <div className="mt-3 grid grid-cols-2 gap-4 text-xs">
                                <div>
                                    <span className="text-stone-500 block mb-1">Sold Price</span>
                                    <span className="font-bold text-stone-700">₹{data.sold_price}/q</span>
                                </div>
                                <div>
                                    <span className="text-stone-500 block mb-1">Today's Price</span>
                                    <span className="font-bold text-stone-700">₹{data.today_price}/q</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
