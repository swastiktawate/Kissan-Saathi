import { useState, useEffect } from 'react';

interface FairPriceData {
    min_price: number;
    modal_price: number;
    max_price: number;
    target_fair_price: number;
}

export default function FairPriceMeter({ crop = 'tomato', mandi = 'vashi' }: { crop?: string, mandi?: string }) {
    const [data, setData] = useState<FairPriceData | null>(null);
    const [loading, setLoading] = useState(true);
    const [userTarget, setUserTarget] = useState<number | null>(null);

    useEffect(() => {
        setLoading(true);
        fetch(`http://localhost:8000/api/v1/fair-price?crop=${crop}&mandi=${mandi}`)
            .then(res => res.json())
            .then(d => {
                if(!d.error) {
                    setData(d);
                    setUserTarget(d.target_fair_price);
                }
                setLoading(false);
            })
            .catch(() => setLoading(false));
    }, [crop, mandi]);

    if (loading) return <div className="p-4 text-xs text-stone-500 animate-pulse">Loading Fair Price...</div>;
    if (!data) return null;

    const min = data.min_price;
    const max = data.max_price;
    const range = max - min || 1;
    
    // Calculate positions (0 to 100%)
    const getPos = (val: number) => {
        const p = ((val - min) / range) * 100;
        return Math.max(0, Math.min(100, p));
    };

    const currentTarget = userTarget !== null ? userTarget : data.target_fair_price;
    const modalPos = getPos(data.modal_price);
    const targetPos = getPos(currentTarget);

    return (
        <div className="bg-white rounded-xl shadow-md border border-stone-200 p-4 mb-4">
            <h3 className="font-bold text-stone-800 text-lg mb-1">Fair-Price Meter</h3>
            <p className="text-xs text-stone-500">Show this to the trader during negotiation. Drag the target to adjust.</p>
            
            <div className="relative h-2 bg-stone-200 rounded-full mt-12 mb-10">
                {/* Interactive Slider Overlay */}
                <input 
                    type="range"
                    min={min}
                    max={max}
                    value={currentTarget}
                    onChange={(e) => setUserTarget(Number(e.target.value))}
                    className="absolute top-[-8px] left-0 w-full h-4 opacity-0 cursor-pointer z-30"
                />

                {/* Gauge Background */}
                <div 
                    className="absolute h-full bg-green-200 rounded-full" 
                    style={{ left: `${Math.min(modalPos, targetPos)}%`, width: `${Math.abs(targetPos - modalPos)}%` }} 
                ></div>

                {/* Min Marker */}
                <div className="absolute top-[-4px] w-0.5 h-4 bg-stone-400" style={{ left: '0%' }}></div>
                <div className="absolute top-4 text-[10px] text-stone-500 -translate-x-1/2" style={{ left: '0%' }}>₹{Math.round(min)}<br/>(Min)</div>

                {/* Max Marker */}
                <div className="absolute top-[-4px] w-0.5 h-4 bg-stone-400" style={{ left: '100%' }}></div>
                <div className="absolute top-4 text-[10px] text-stone-500 -translate-x-1/2" style={{ left: '100%' }}>₹{Math.round(max)}<br/>(Max)</div>

                {/* Modal Marker */}
                <div className="absolute top-[-8px] flex flex-col items-center -translate-x-1/2" style={{ left: `${modalPos}%` }}>
                    <div className="w-3 h-3 bg-stone-500 rounded-full border-2 border-white shadow"></div>
                    <div className="absolute bottom-4 text-[10px] font-bold text-stone-700 whitespace-nowrap mb-1 bg-white/80 px-1 rounded">₹{Math.round(data.modal_price)} (Avg)</div>
                </div>

                {/* Target Fair Price Marker */}
                <div className="absolute top-[-8px] flex flex-col items-center -translate-x-1/2 z-20 pointer-events-none" style={{ left: `${targetPos}%` }}>
                    <div className="w-4 h-4 bg-green-600 rounded-full border-2 border-white shadow"></div>
                    <div className="absolute top-5 bg-green-100 text-green-800 text-[10px] font-bold px-2 py-1 rounded shadow-sm whitespace-nowrap mt-1 border border-green-200 transition-all">
                        Target: ₹{Math.round(currentTarget)}
                    </div>
                </div>
            </div>
            
            <div className="mt-8 bg-green-50 p-3 rounded-lg border border-green-100">
                <p className="text-xs text-green-800 leading-relaxed">
                    <strong>AI Recommendation:</strong> Aim for <span className="font-bold">₹{Math.round(data.target_fair_price)}/q</span> based on tomorrow's expected supply. Do not accept below ₹{Math.round(data.modal_price)}/q.
                </p>
            </div>
        </div>
    );
}
