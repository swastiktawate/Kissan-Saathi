import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeft, Users, CheckCircle2, MapPin, Plus, ChevronRight, Sprout, Trash2 } from 'lucide-react';

const STATIC_GROUPS = [
    {
        id: 1,
        name: 'Vashi Tomato Growers',
        farmers: 8,
        mandi: 'Vashi Mandi',
        dist: '4 km',
        cropStr: 'Tomatoes • 25 quintals',
        price: '₹2,250',
        crop: 'Tomato',
        image: 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80'
    },
    {
        id: 2,
        name: 'Nerul Onion Collective',
        farmers: 12,
        mandi: 'Nerul',
        dist: '7 km',
        cropStr: 'Onions • 40 quintals',
        price: '₹1,980',
        crop: 'Onion',
        image: 'https://images.unsplash.com/photo-1620574387735-3624d75b2dbc?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80'
    },
    {
        id: 3,
        name: 'Turbhe Potato Pool',
        farmers: 6,
        mandi: 'Turbhe',
        dist: '8 km',
        cropStr: 'Potatoes • 30 quintals',
        price: '₹1,750',
        crop: 'Potato',
        image: 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80'
    }
];

export default function PoolingList() {
    const navigate = useNavigate();
    const [filter, setFilter] = useState('All');
    const [myPools, setMyPools] = useState<any[]>([]);

    useEffect(() => {
        const saved = localStorage.getItem('kisan_my_pools');
        if (saved) {
            try {
                setMyPools(JSON.parse(saved));
            } catch (e) {
                console.error(e);
            }
        }
    }, []);

    const handleDelete = (indexToDelete: number) => {
        const updatedPools = myPools.filter((_, idx) => idx !== indexToDelete);
        setMyPools(updatedPools);
        localStorage.setItem('kisan_my_pools', JSON.stringify(updatedPools));
    };

    const filters = ['All', 'Tomato', 'Onion', 'Potato', 'Banana', 'Other'];

    const filteredGroups = STATIC_GROUPS.filter(g => filter === 'All' || g.crop === filter);

    return (
        <div className="flex flex-col bg-white min-h-screen font-sans pb-10">
            {/* Header */}
            <div className="flex items-center justify-between p-4 bg-white sticky top-0 z-10 border-b border-stone-100">
                <div className="flex items-center gap-3">
                    <button onClick={() => navigate(-1)} className="p-1 -ml-1 text-green-900">
                        <ChevronLeft size={24} strokeWidth={2.5} />
                    </button>
                    <div>
                        <h1 className="text-xl font-bold text-green-900 leading-tight">Farmer Pooling</h1>
                        <p className="text-xs text-stone-500">Join or create a group. Sell together. Get better prices.</p>
                    </div>
                </div>
                <div className="bg-green-50 p-2 rounded-full">
                    <Users size={20} className="text-green-700" />
                </div>
            </div>

            <div className="px-4 mt-4">
                {/* Hero section */}
                <div className="bg-green-50 rounded-2xl p-4 flex gap-4 items-center mb-6">
                    <div className="flex-1">
                        <h2 className="font-bold text-green-900 text-sm mb-2">Why Pool Your Produce?</h2>
                        <ul className="flex flex-col gap-1.5">
                            {['Get better mandi prices', 'Share transport costs', 'Reduce middlemen', 'Sell in larger quantities'].map((text, i) => (
                                <li key={i} className="flex items-center gap-2 text-xs text-green-800 font-medium">
                                    <CheckCircle2 size={14} className="text-green-600 shrink-0" />
                                    {text}
                                </li>
                            ))}
                        </ul>
                    </div>
                    {/* Placeholder illustration */}
                    <div className="w-24 h-24 bg-green-200 rounded-xl overflow-hidden flex items-center justify-center shrink-0">
                        <Users size={40} className="text-green-600 opacity-50" />
                    </div>
                </div>

                {/* Find a Group Header */}
                <div className="flex justify-between items-end mb-3">
                    <div>
                        <h2 className="font-bold text-stone-900 text-lg leading-tight">Find a Group</h2>
                        <p className="text-xs text-stone-500">Join existing farmer groups near you</p>
                    </div>
                    <button className="flex items-center gap-1 bg-stone-50 border border-stone-200 px-3 py-1.5 rounded-full text-xs font-bold text-stone-700 hover:bg-stone-100">
                        <MapPin size={12} className="text-stone-500" /> Vashi Mandi <ChevronRight size={12} className="text-stone-400" />
                    </button>
                </div>

                {/* Filters */}
                <div className="flex gap-2 overflow-x-auto pb-4 scrollbar-hide">
                    {filters.map(f => (
                        <button 
                            key={f}
                            onClick={() => setFilter(f)}
                            className={`px-4 py-1.5 rounded-full text-sm font-bold whitespace-nowrap transition-all border ${
                                filter === f 
                                ? 'bg-green-700 text-white border-green-700' 
                                : 'bg-white text-stone-600 border-stone-200 hover:border-stone-300'
                            }`}
                        >
                            {f}
                        </button>
                    ))}
                </div>

                {/* Group List */}
                <div className="flex flex-col gap-3 mb-6">
                    {filteredGroups.map(group => (
                        <div key={group.id} className="border border-stone-200 rounded-2xl p-3 flex gap-3 items-center hover:border-green-300 transition-colors bg-white">
                            <img src={group.image} alt={group.name} className="w-16 h-16 rounded-xl object-cover shrink-0" />
                            <div className="flex-1 min-w-0">
                                <h3 className="font-bold text-stone-900 text-sm truncate">{group.name}</h3>
                                <div className="flex items-center gap-2 mt-1 mb-1">
                                    <span className="flex items-center gap-1 bg-green-100 text-green-800 text-[10px] font-bold px-1.5 py-0.5 rounded">
                                        <Users size={10} /> {group.farmers} farmers
                                    </span>
                                </div>
                                <div className="text-[10px] text-stone-500 flex items-center gap-1">
                                    <MapPin size={10} /> {group.mandi} • {group.dist}
                                </div>
                                <div className="text-[10px] text-stone-500 mt-0.5">{group.cropStr}</div>
                            </div>
                            <div className="flex flex-col items-end shrink-0">
                                <div className="bg-green-50 px-2 py-1.5 rounded-lg border border-green-100 text-right mb-2">
                                    <div className="text-[9px] text-green-700 font-bold uppercase">Expected price</div>
                                    <div className="text-sm font-black text-green-900">{group.price}<span className="text-[10px] font-medium text-green-700">/q</span></div>
                                    <div className="text-[9px] text-stone-500">(est.)</div>
                                </div>
                                <button className="bg-green-700 text-white w-full py-1.5 rounded-lg text-xs font-bold flex justify-center items-center gap-1 hover:bg-green-800 transition-colors">
                                    Join <ChevronRight size={14} />
                                </button>
                            </div>
                        </div>
                    ))}
                    {filteredGroups.length === 0 && (
                        <div className="text-center py-6 text-stone-500 text-sm">No groups found for {filter}.</div>
                    )}
                </div>

                {/* Create Pool Banner */}
                <div 
                    onClick={() => navigate('/pooling/create')}
                    className="bg-green-50 border border-green-200 rounded-2xl p-4 flex items-center justify-between cursor-pointer hover:bg-green-100 transition-colors mb-8"
                >
                    <div className="flex items-center gap-4">
                        <div className="w-12 h-12 bg-green-200 rounded-full flex items-center justify-center text-green-700 shrink-0">
                            <Plus size={24} />
                        </div>
                        <div>
                            <h3 className="font-bold text-green-900 text-sm">Create Your Own Pool</h3>
                            <p className="text-[10px] text-green-700">Looking for specific quantity, mandi or transport?</p>
                        </div>
                    </div>
                    <div className="bg-white border border-green-200 px-3 py-1.5 rounded-full text-xs font-bold text-green-800 flex items-center gap-1 shadow-sm shrink-0">
                        Post a Request <ChevronRight size={14} />
                    </div>
                </div>

                {/* My Requests */}
                {myPools.length > 0 && (
                    <div className="mb-8">
                        <div className="flex justify-between items-center mb-3">
                            <h2 className="font-bold text-stone-900 text-sm">My Pooling Requests</h2>
                            <ChevronRight size={16} className="text-stone-400" />
                        </div>
                        <div className="flex flex-col gap-2">
                            {myPools.map((pool, idx) => (
                                <div key={idx} className="border border-stone-200 rounded-xl p-3 flex items-center gap-3 bg-white hover:bg-stone-50 transition-colors group cursor-pointer">
                                    <div className="bg-green-50 p-2 rounded-lg text-green-700">
                                        <Sprout size={20} />
                                    </div>
                                    <div className="flex-1">
                                        <div className="flex gap-2 items-center mb-0.5">
                                            <span className="bg-green-100 text-green-800 text-[10px] font-bold px-2 py-0.5 rounded">Active</span>
                                            <h4 className="font-bold text-stone-900 text-sm">{pool.crop} • {pool.quantity}</h4>
                                        </div>
                                        <p className="text-[10px] text-stone-500">Looking for more farmers • {pool.mandi}</p>
                                    </div>
                                    <div className="text-right border-l border-stone-100 pl-3">
                                        <p className="text-[9px] text-stone-400 uppercase font-bold">Ends in</p>
                                        <p className="text-xs font-medium text-stone-700 flex items-center gap-1"><CheckCircle2 size={10} className="text-green-600"/> 2 days</p>
                                    </div>
                                    <button 
                                        onClick={(e) => { e.stopPropagation(); handleDelete(idx); }}
                                        className="p-2 ml-1 text-stone-300 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                                    >
                                        <Trash2 size={16} />
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
