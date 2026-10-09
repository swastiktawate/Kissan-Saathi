import { useState } from 'react';
import { Plus, Trash2, Users, Truck } from 'lucide-react';

export default function FarmerPooling() {
    const [farmers, setFarmers] = useState([{ name: 'Me', qty: 10 }]);
    const [mandi, setMandi] = useState('vashi');
    const [vehicle, setVehicle] = useState('Auto');
    const [result, setResult] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const addNeighbour = () => {
        setFarmers([...farmers, { name: '', qty: 10 }]);
    };

    const updateFarmer = (index: number, field: string, value: any) => {
        const newFarmers = [...farmers];
        newFarmers[index] = { ...newFarmers[index], [field]: value };
        setFarmers(newFarmers);
    };

    const removeFarmer = (index: number) => {
        const newFarmers = farmers.filter((_, i) => i !== index);
        setFarmers(newFarmers);
    };

    const calculatePool = async () => {
        setLoading(true);
        try {
            const res = await fetch('http://localhost:8000/api/v1/pool', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ farmers, mandi, vehicle_type: vehicle, crop: 'tomato' })
            });
            const data = await res.json();
            setResult(data);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-white rounded-xl shadow-md border border-stone-200 p-4 mb-4">
            <div className="flex items-center gap-2 mb-2">
                <Users className="text-green-600" size={20} />
                <h3 className="font-bold text-stone-800 text-lg">Farmer Pooling</h3>
            </div>
            <p className="text-xs text-stone-500 mb-4">Group produce to share transport costs.</p>

            <div className="grid grid-cols-2 gap-3 mb-4 text-sm">
                <div>
                    <label className="block text-[10px] font-bold text-stone-500 uppercase mb-1">Target Mandi</label>
                    <select 
                        value={mandi} 
                        onChange={(e) => setMandi(e.target.value)}
                        className="w-full bg-stone-50 border border-stone-200 rounded p-2 text-stone-700 outline-none"
                    >
                        <option value="vashi">Vashi Mandi</option>
                        <option value="kalyan">Kalyan Mandi</option>
                        <option value="pune">Pune Mandi</option>
                    </select>
                </div>
                <div>
                    <label className="block text-[10px] font-bold text-stone-500 uppercase mb-1">Vehicle Size</label>
                    <select 
                        value={vehicle} 
                        onChange={(e) => setVehicle(e.target.value)}
                        className="w-full bg-stone-50 border border-stone-200 rounded p-2 text-stone-700 outline-none"
                    >
                        <option value="Auto">Auto (Smart Select)</option>
                        <option value="Tempo">Tempo (10q)</option>
                        <option value="Pickup">Pickup (30q)</option>
                        <option value="Truck">Truck (90q)</option>
                    </select>
                </div>
            </div>

            <div className="space-y-2 mb-4">
                <label className="block text-[10px] font-bold text-stone-500 uppercase">Pool Members</label>
                {farmers.map((farmer, idx) => (
                    <div key={idx} className="flex items-center gap-2">
                        <input 
                            type="text" 
                            placeholder={idx === 0 ? "Your Name" : "Neighbour Name"}
                            value={farmer.name}
                            onChange={(e) => updateFarmer(idx, 'name', e.target.value)}
                            className="flex-1 bg-stone-50 border border-stone-200 rounded p-2 text-sm text-stone-700 outline-none"
                            disabled={idx === 0 && farmer.name === 'Me'}
                        />
                        <div className="flex items-center bg-stone-50 border border-stone-200 rounded w-24">
                            <input 
                                type="number" 
                                value={farmer.qty}
                                onChange={(e) => updateFarmer(idx, 'qty', Number(e.target.value))}
                                className="w-full bg-transparent p-2 text-sm text-stone-700 outline-none text-right"
                            />
                            <span className="text-xs text-stone-400 pr-2">q</span>
                        </div>
                        {idx > 0 && (
                            <button onClick={() => removeFarmer(idx)} className="p-2 text-red-400 hover:text-red-600 transition-colors">
                                <Trash2 size={16} />
                            </button>
                        )}
                    </div>
                ))}
            </div>

            <div className="flex gap-2 mb-6">
                <button 
                    onClick={addNeighbour}
                    className="flex-1 bg-stone-100 hover:bg-stone-200 text-stone-700 text-xs font-bold py-2 rounded-lg transition-colors flex items-center justify-center gap-1 border border-stone-200"
                >
                    <Plus size={14} /> Add Neighbour
                </button>
                <button 
                    onClick={calculatePool}
                    className="flex-1 bg-green-600 hover:bg-green-700 text-white text-xs font-bold py-2 rounded-lg transition-colors flex items-center justify-center gap-1"
                >
                    <Truck size={14} /> Calculate Savings
                </button>
            </div>

            {loading && <div className="text-xs text-stone-500 animate-pulse text-center">Crunching transport data...</div>}

            {result && !result.error && (
                <div className="bg-green-50 border border-green-200 p-4 rounded-xl">
                    <h4 className="text-green-800 font-bold text-lg leading-tight mb-1">
                        You save ₹{Math.round(result.primary_savings_per_q)} per quintal by travelling together!
                    </h4>
                    <p className="text-xs text-green-700 mb-4">
                        Total {result.total_qty}q loaded into a {result.optimal_vehicle}.
                    </p>
                    
                    <div className="space-y-2">
                        {result.breakdown.map((b: any, i: number) => (
                            <div key={i} className="flex justify-between items-center bg-white p-2 rounded border border-green-100 shadow-sm text-sm">
                                <div className="flex flex-col">
                                    <span className="font-bold text-stone-700">{b.name} <span className="font-normal text-stone-400 text-xs">({b.qty}q)</span></span>
                                    <span className="text-[10px] text-stone-500 line-through">Alone: ₹{Math.round(b.alone_cost)}</span>
                                </div>
                                <div className="flex flex-col items-end">
                                    <span className="font-bold text-green-700">Pays ₹{Math.round(b.shared_cost)}</span>
                                    <span className="text-[10px] text-green-600 font-medium">Saved ₹{Math.round(b.savings)}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
            
            {result && result.error && (
                <div className="text-xs text-red-500 bg-red-50 p-2 rounded border border-red-100">
                    {result.error}
                </div>
            )}
        </div>
    );
}
