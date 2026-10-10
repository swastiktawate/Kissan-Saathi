import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeft, Leaf, Package, MapPin, Truck, Users, FileText, Send, ChevronRight } from 'lucide-react';

export default function PoolingCreate() {
    const navigate = useNavigate();
    
    const [crop, setCrop] = useState('Tomato');
    const [quantity, setQuantity] = useState('100');
    const [unit, setUnit] = useState('Quintals');
    const [mandi, setMandi] = useState('Vashi Mandi');
    const [transport, setTransport] = useState('I will arrange');
    const [details, setDetails] = useState('');

    const handlePost = () => {
        const newPool = { crop, quantity: `${quantity} ${unit.charAt(0).toLowerCase()}`, mandi, transport, details };
        
        // Save to localStorage for demo persistence
        const existing = localStorage.getItem('kisan_my_pools');
        const pools = existing ? JSON.parse(existing) : [];
        pools.push(newPool);
        localStorage.setItem('kisan_my_pools', JSON.stringify(pools));
        
        // Go back to list
        navigate('/pooling');
    };

    const crops = ['Tomato', 'Onion', 'Potato', 'Banana'];
    const mandis = ['Vashi Mandi', 'Pune Mandi', 'Nashik Mandi'];

    return (
        <div className="flex flex-col bg-white min-h-screen font-sans pb-[240px]">
            {/* Header */}
            <div className="flex items-center gap-3 p-4 bg-green-50 border-b border-green-100">
                <button onClick={() => navigate(-1)} className="p-1 -ml-1 text-green-900">
                    <ChevronLeft size={24} strokeWidth={2.5} />
                </button>
                <div className="flex-1">
                    <h1 className="text-xl font-bold text-green-900 leading-tight">Create Your Own Pool</h1>
                    <p className="text-[10px] text-green-800 opacity-80">Bring together nearby farmers, pool your produce and get better prices.</p>
                </div>
                {/* Small illustration placeholder */}
                <div className="w-16 h-12 bg-green-200 rounded-lg flex items-center justify-center shrink-0">
                    <Users size={24} className="text-green-700 opacity-50" />
                </div>
            </div>

            <div className="p-4 flex flex-col gap-6">
                
                {/* Crop */}
                <div className="flex gap-3">
                    <div className="mt-1 text-green-600"><Leaf size={20} /></div>
                    <div className="flex-1">
                        <label className="block font-bold text-stone-900 text-sm mb-1">Select Crop</label>
                        <p className="text-[10px] text-stone-500 mb-2">Choose the crop you want to pool.</p>
                        <div className="relative">
                            <select 
                                value={crop} onChange={e => setCrop(e.target.value)}
                                className="w-full appearance-none bg-white border border-stone-200 rounded-xl pl-10 pr-4 py-3 text-sm font-bold text-stone-900 outline-none focus:border-green-500 shadow-sm"
                            >
                                {crops.map(c => <option key={c} value={c}>{c}</option>)}
                            </select>
                            <ChevronRight size={16} className="absolute right-4 top-3.5 text-stone-400 pointer-events-none" />
                            {/* Dummy icon for the crop */}
                            <div className="absolute left-3 top-2.5 text-xl pointer-events-none">
                                {crop === 'Tomato' ? '🍅' : crop === 'Onion' ? '🧅' : crop === 'Potato' ? '🥔' : '🍌'}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Quantity */}
                <div className="flex gap-3">
                    <div className="mt-1 text-green-600"><Package size={20} /></div>
                    <div className="flex-1">
                        <label className="block font-bold text-stone-900 text-sm mb-1">Quantity</label>
                        <p className="text-[10px] text-stone-500 mb-2">Enter the total quantity you want to pool.</p>
                        <div className="flex gap-2">
                            <div className="relative flex-1">
                                <input 
                                    type="number" 
                                    value={quantity} onChange={e => setQuantity(e.target.value)}
                                    className="w-full bg-white border border-stone-200 rounded-xl pl-10 pr-4 py-3 text-sm font-bold text-stone-900 outline-none focus:border-green-500 shadow-sm"
                                />
                                <Package size={16} className="absolute left-4 top-3.5 text-stone-400" />
                            </div>
                            <select 
                                value={unit} onChange={e => setUnit(e.target.value)}
                                className="w-28 bg-stone-50 border border-stone-200 rounded-xl px-3 py-3 text-sm font-bold text-stone-700 outline-none focus:border-green-500"
                            >
                                <option>Quintals</option>
                                <option>Tonnes</option>
                                <option>KG</option>
                            </select>
                        </div>
                        <div className="bg-green-50 text-green-700 text-[10px] p-2 rounded-lg mt-2 flex items-center gap-2 font-medium">
                            <span className="w-4 h-4 bg-green-200 text-green-800 rounded-full flex items-center justify-center font-bold">i</span>
                            You can add more details (variety, grade, etc.) in the next step.
                        </div>
                    </div>
                </div>

                {/* Mandi */}
                <div className="flex gap-3">
                    <div className="mt-1 text-green-600"><MapPin size={20} /></div>
                    <div className="flex-1">
                        <label className="block font-bold text-stone-900 text-sm mb-1">Preferred Mandi / Destination</label>
                        <p className="text-[10px] text-stone-500 mb-2">Choose a mandi or let us suggest the best nearby options.</p>
                        <div className="relative">
                            <select 
                                value={mandi} onChange={e => setMandi(e.target.value)}
                                className="w-full appearance-none bg-white border border-stone-200 rounded-xl px-10 py-3 text-sm font-bold text-stone-900 outline-none focus:border-green-500 shadow-sm"
                            >
                                {mandis.map(m => <option key={m} value={m}>{m}</option>)}
                            </select>
                            <MapPin size={16} className="absolute left-4 top-3.5 text-stone-400 pointer-events-none" />
                        </div>
                    </div>
                </div>

                {/* Transport */}
                <div className="flex gap-3">
                    <div className="mt-1 text-green-600"><Truck size={20} /></div>
                    <div className="flex-1">
                        <label className="block font-bold text-stone-900 text-sm mb-1">Transport Arrangement</label>
                        <p className="text-[10px] text-stone-500 mb-2">How do you want to handle transport?</p>
                        
                        <div className="flex gap-2">
                            {['I will arrange', 'Group transport', 'No preference'].map(opt => {
                                const active = transport === opt;
                                return (
                                    <button 
                                        key={opt}
                                        onClick={() => setTransport(opt)}
                                        className={`flex-1 flex flex-col items-center justify-center gap-1 p-2 rounded-xl border text-[10px] font-bold transition-all ${
                                            active ? 'border-green-600 bg-green-50 text-green-800' : 'border-stone-200 bg-white text-stone-600 hover:border-green-300'
                                        }`}
                                    >
                                        {opt === 'I will arrange' && <Truck size={16} className={active ? 'text-green-600' : 'text-stone-400'}/>}
                                        {opt === 'Group transport' && <Users size={16} className={active ? 'text-green-600' : 'text-stone-400'}/>}
                                        {opt === 'No preference' && <FileText size={16} className={active ? 'text-green-600' : 'text-stone-400'}/>}
                                        <span className="text-center">{opt}</span>
                                    </button>
                                );
                            })}
                        </div>
                    </div>
                </div>

                {/* Details */}
                <div className="flex gap-3">
                    <div className="mt-1 text-green-600"><FileText size={20} /></div>
                    <div className="flex-1">
                        <label className="block font-bold text-stone-900 text-sm mb-1">Additional Details <span className="text-stone-400 font-normal">(Optional)</span></label>
                        <p className="text-[10px] text-stone-500 mb-2">Add any extra information (e.g. preferred date, special notes).</p>
                        <textarea 
                            value={details} onChange={e => setDetails(e.target.value)}
                            maxLength={200}
                            placeholder="e.g. Need to sell within 3 days, prefer 8-10 quintals per farmer..."
                            className="w-full bg-stone-50 border border-stone-200 rounded-xl px-4 py-3 text-xs text-stone-900 outline-none focus:border-green-500 min-h-[80px] resize-none"
                        />
                        <div className="text-right text-[10px] text-stone-400 mt-1">{details.length}/200</div>
                    </div>
                </div>

            </div>

            {/* Bottom Sticky Section */}
            <div className="fixed bottom-[56px] left-1/2 -translate-x-1/2 w-full max-w-[430px] bg-white border-t border-stone-200 p-4 shadow-[0_-10px_20px_-10px_rgba(0,0,0,0.1)] z-40">
                {/* Summary Card */}
                <div className="bg-green-50 border border-green-100 rounded-xl p-3 mb-4">
                    <div className="flex items-center gap-2 mb-2">
                        <Users size={16} className="text-green-700" />
                        <h4 className="font-bold text-green-900 text-xs">Your Pool Summary</h4>
                    </div>
                    <div className="flex justify-between items-center bg-white p-2 rounded-lg shadow-sm border border-green-100">
                        <div className="flex flex-col items-center">
                            <span className="text-[14px]">{crop === 'Tomato' ? '🍅' : crop === 'Onion' ? '🧅' : crop === 'Potato' ? '🥔' : '🍌'}</span>
                            <span className="text-[9px] text-stone-500">Crop</span>
                        </div>
                        <div className="h-6 w-px bg-stone-200"></div>
                        <div className="flex flex-col items-center">
                            <span className="font-bold text-stone-800 text-[10px]">{quantity} {unit.charAt(0).toLowerCase()}</span>
                            <span className="text-[9px] text-stone-500">Quantity</span>
                        </div>
                        <div className="h-6 w-px bg-stone-200"></div>
                        <div className="flex flex-col items-center">
                            <span className="font-bold text-stone-800 text-[10px] truncate max-w-[60px]">{mandi}</span>
                            <span className="text-[9px] text-stone-500">Mandi</span>
                        </div>
                        <div className="h-6 w-px bg-stone-200"></div>
                        <div className="flex flex-col items-center">
                            <span className="font-bold text-stone-800 text-[10px] truncate max-w-[60px]">{transport}</span>
                            <span className="text-[9px] text-stone-500">Transport</span>
                        </div>
                    </div>
                </div>

                <button 
                    onClick={handlePost}
                    className="w-full bg-green-700 text-white font-bold py-3.5 rounded-xl shadow-lg hover:bg-green-800 transition-colors flex items-center justify-center gap-2"
                >
                    <Send size={18} />
                    Post Pool Request
                </button>
                <p className="text-center text-[10px] text-stone-500 mt-2">Other farmers in your area will be notified.</p>
            </div>
        </div>
    );
}
