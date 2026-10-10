import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Bell, ArrowUpRight, TrendingUp, ChevronRight, Leaf, MapPin, Warehouse, Users } from 'lucide-react';


import PolicyAlertBanner from '../components/PolicyAlertBanner';

import { useLanguage } from '../context/LanguageContext';

export default function Home() {
    const { t } = useLanguage();

    const mockData: Record<string, any> = {
        'Tamatar': {
            price: '2,150', trend: '+5.2%', action: t('action_wait_3_days'), 
            reason: t('reason_rain'),
            mandis: [
                { name: 'Kalyan', price: '₹2,350', diff: '+₹200', tag: t('best_option') },
                { name: 'Vashi', price: '₹2,150', diff: '-', tag: '' },
                { name: 'Pune', price: '₹1,900', diff: '-₹250', tag: '' }
            ]
        },
        'Pyaaz': {
            price: '3,200', trend: '-1.5%', action: t('action_sell_now'),
            reason: t('reason_export_ban'),
            mandis: [
                { name: 'Nashik', price: '₹3,400', diff: '+₹200', tag: t('best_option') },
                { name: 'Pune', price: '₹3,200', diff: '-', tag: '' },
                { name: 'Vashi', price: '₹3,050', diff: '-₹150', tag: '' }
            ]
        },
        'Aloo': {
            price: '1,450', trend: '+2.1%', action: t('action_sell_today'),
            reason: t('reason_aloo'),
            mandis: [
                { name: 'Pune', price: '₹1,550', diff: '+₹100', tag: t('best_option') },
                { name: 'Kalyan', price: '₹1,450', diff: '-', tag: '' }
            ]
        },
        'Kela': {
            price: '1,800', trend: '+0.5%', action: t('action_sell_today'),
            reason: t('reason_kela'),
            mandis: [
                { name: 'Vashi', price: '₹1,900', diff: '+₹100', tag: t('best_option') },
                { name: 'Kalyan', price: '₹1,800', diff: '-', tag: '' }
            ]
        }
    };

    
    const [selectedCrop, setSelectedCrop] = useState('Tamatar');
    const [selectedHomeMandi, setSelectedHomeMandi] = useState('Vashi Mandi');
    const navigate = useNavigate();
    
    const data = mockData[selectedCrop] || mockData['Tamatar'];

    return (
        <div className="flex flex-col bg-white min-h-[calc(100vh-60px)] font-sans pb-6">
            <PolicyAlertBanner />
            {/* Header */}
            <div className="flex justify-between items-center p-4">
                <div className="flex items-center gap-2">
                    <div className="bg-green-600 p-1.5 rounded-lg text-white">
                        <Leaf size={24} />
                    </div>
                    <div>
                        <h1 className="text-xl font-bold text-green-800 leading-tight">{t('app_title')}</h1>
                        <p className="text-xs text-stone-500">{t('app_subtitle')}</p>
                    </div>
                </div>
                <div className="flex items-center gap-2.5">
                    <button className="p-2 border border-stone-200 rounded-full">
                        <Bell size={20} className="text-stone-700" />
                    </button>
                    <button 
                        onClick={() => navigate('/profile')}
                        className="w-9 h-9 rounded-full bg-green-100 border border-green-300 text-green-800 flex items-center justify-center font-bold text-sm hover:ring-2 hover:ring-green-400 transition-all cursor-pointer"
                    >
                        VS
                    </button>
                </div>
            </div>

            {/* Hero Banner */}
            <div className="mx-4 mt-2 rounded-2xl bg-stone-900 overflow-hidden relative shadow-md">
                <img src="/placeholder-farm.jpg" alt="Farm" className="w-full h-32 object-cover opacity-60" 
                     onError={(e) => { e.currentTarget.style.display = 'none'; }} />
                <div className="absolute inset-0 bg-gradient-to-t from-stone-900 to-transparent flex flex-col justify-end p-4">
                    <h2 className="text-white font-bold text-lg leading-tight">{t("hero_subtitle")}</h2>
                </div>
            </div>

            {/* QUICK ACCESS */}
            <div className="px-4 mt-4">
                <h2 className="text-[10px] font-bold text-stone-400 uppercase tracking-wider mb-2">
                    {t('quick_access')}
                </h2>
                <div className="grid grid-cols-2 gap-3">
                    {/* Cold Storage Card */}
                    <div 
                        onClick={() => navigate('/cold-storage')}
                        className="bg-green-50 border border-green-100 rounded-xl p-3 flex items-center justify-between cursor-pointer hover:bg-green-100 transition-colors shadow-sm"
                    >
                        <div className="flex items-center gap-2">
                            <Warehouse size={24} className="text-green-700" />
                            <div className="flex flex-col">
                                <span className="text-sm font-bold text-green-900 leading-tight">{t('cold_storage')}</span>
                                <span className="text-[10px] text-green-700">{t('find_nearby')}</span>
                            </div>
                        </div>
                        <ChevronRight size={16} className="text-green-700 opacity-50" />
                    </div>

                    {/* Farmer Pooling Card */}
                    <div 
                        onClick={() => navigate('/pooling')}
                        className="bg-green-50 border border-green-100 rounded-xl p-3 flex items-center justify-between cursor-pointer hover:bg-green-100 transition-colors shadow-sm"
                    >
                        <div className="flex items-center gap-2">
                            <Users size={24} className="text-green-700" />
                            <div className="flex flex-col">
                                <span className="text-sm font-bold text-green-900 leading-tight">{t('farmer_pooling')}</span>
                                <span className="text-[10px] text-green-700">{t("sell_together")}</span>
                            </div>
                        </div>
                        <ChevronRight size={16} className="text-green-700 opacity-50" />
                    </div>
                </div>
            </div>

            {/* Meri Faslein */}
            <div className="mt-8 px-4">
                <h3 className="font-bold text-stone-800 mb-3 text-sm">{t('meri_faslein')}</h3>
                <div className="flex gap-3 overflow-x-auto pb-2 scrollbar-hide">
                    {['Tamatar', 'Pyaaz', 'Aloo', 'Kela'].map(crop => (
                        <button 
                            key={crop}
                            onClick={() => setSelectedCrop(crop)}
                            className={`flex flex-col items-center justify-center p-3 rounded-2xl border min-w-[80px] shadow-sm transition-all ${
                                selectedCrop === crop 
                                ? 'border-green-600 bg-green-50 text-green-800' 
                                : 'border-stone-100 bg-white text-stone-600'
                            }`}
                        >
                            <span className="text-2xl mb-1">
                                {crop === 'Tamatar' ? '🍅' : crop === 'Pyaaz' ? '🧅' : crop === 'Aloo' ? '🥔' : '🍌'}
                            </span>
                            <span className="text-xs font-medium">{t(crop === "Tamatar" ? "crop_tomato" : crop === "Pyaaz" ? "crop_onion" : crop === "Aloo" ? "crop_potato" : "crop_banana")}</span>
                        </button>
                    ))}
                </div>
            </div>

            {/* Price Card */}
            <div className="px-4 mt-6">
                <div className="flex justify-between items-center mb-3">
                    <h3 className="font-bold text-stone-800 text-sm">{t('today_price_for')} ({t(selectedCrop === 'Tamatar' ? 'crop_tomato' : selectedCrop === 'Pyaaz' ? 'crop_onion' : selectedCrop === 'Aloo' ? 'crop_potato' : 'crop_banana')})</h3>
                    <div 
                        className="flex items-center text-xs text-stone-500 gap-1 bg-stone-100 px-2 py-1 rounded-full cursor-pointer hover:bg-stone-200 transition-colors"
                        onClick={() => setSelectedHomeMandi(selectedHomeMandi === 'Vashi Mandi' ? 'Pune Mandi' : 'Vashi Mandi')}
                    >
                        <MapPin size={12} />
                        <span>{selectedHomeMandi}</span>
                        <ChevronRight size={12} />
                    </div>
                </div>
                <div className="flex items-end gap-3 mb-4">
                    <h2 className="text-3xl font-black text-stone-800 tracking-tight">₹{data.price}<span className="text-sm font-medium text-stone-500 font-sans">/q</span></h2>
                    <div className={`flex items-center text-xs font-bold px-2 py-1 rounded mb-1 ${data.trend.startsWith('+') ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                        <TrendingUp size={12} className="mr-1" /> {data.trend}
                    </div>
                </div>
                
                {/* Hamari Salah */}
                <div className="bg-green-50 border border-green-200 rounded-xl p-4 flex gap-3 shadow-sm">
                    <div className="bg-green-100 p-2 rounded-lg h-fit text-green-700 mt-1">
                        <ArrowUpRight size={20} />
                    </div>
                    <div>
                        <h4 className="font-bold text-green-800 text-sm mb-1">{data.action}</h4>
                        <p className="text-xs text-green-700 leading-relaxed">{data.reason}</p>
                    </div>
                </div>
            </div>

            {/* Top 3 Mandis */}
            <div className="mt-8 px-4">
                <div className="flex justify-between items-center mb-3">
                    <h3 className="font-bold text-stone-800 text-sm">{t('better_mandi_options')}</h3>
                    <Link to="/mandis" className="text-xs text-green-600 font-medium hover:underline">{t('see_all')}</Link>
                </div>
                <div className="flex gap-3 overflow-x-auto pb-4 scrollbar-hide">
                    {data.mandis.map((m: any, i: number) => (
                        <div key={i} className="min-w-[140px] border border-stone-200 rounded-xl p-3 shadow-sm bg-white shrink-0">
                            <h4 className="font-bold text-stone-800 text-sm">{m.name}</h4>
                            <p className="text-stone-500 text-xs mb-2">35 {t('km_away')}</p>
                            <div className="flex justify-between items-end">
                                <span className="font-bold text-stone-800">{m.price}</span>
                                <span className={`text-xs font-bold ${m.diff.startsWith('+') ? 'text-green-600' : 'text-stone-400'}`}>{m.diff}</span>
                            </div>
                            {m.tag && (
                                <div className="mt-2 bg-green-100 text-green-700 text-[10px] font-bold px-2 py-1 rounded inline-block">
                                    {m.tag}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
