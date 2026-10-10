import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import type { LanguageCode } from '../i18n/translations';
import { ChevronLeft, CheckCircle2, MapPin, Warehouse, Sprout, Globe, Volume2, Bell, Database, Info } from 'lucide-react';

export default function Profile() {
    const navigate = useNavigate();
    const { t, language, setLanguage } = useLanguage();

    const languages: { code: LanguageCode, label: string }[] = [
        { code: 'en', label: 'English' },
        { code: 'hi', label: 'हिन्दी (Hindi)' },
        { code: 'mr', label: 'मराठी (Marathi)' },
        { code: 'hr', label: 'हरियाणवी (Haryanvi)' },
        { code: 'pa', label: 'ਪੰਜਾਬੀ (Punjabi)' }
    ];

    return (
        <div className="flex flex-col bg-stone-50 min-h-screen font-sans pb-24">
            {/* Header */}
            <div className="flex items-center gap-3 p-4 bg-white sticky top-0 z-10 border-b border-stone-100 shadow-sm">
                <button onClick={() => navigate(-1)} className="p-1 -ml-1 text-green-900">
                    <ChevronLeft size={24} strokeWidth={2.5} />
                </button>
                <h1 className="text-xl font-bold text-green-900 leading-tight">{t('profile_title')}</h1>
            </div>

            <div className="p-4 flex flex-col gap-4">
                {/* User Card */}
                <div className="bg-white rounded-2xl p-5 shadow-sm border border-stone-100 flex flex-col gap-4">
                    <div className="flex items-center gap-4">
                        <div className="w-16 h-16 rounded-full bg-green-100 border-2 border-green-400 text-green-800 flex items-center justify-center font-bold text-2xl shrink-0">
                            VS
                        </div>
                        <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                                <h2 className="text-lg font-bold text-stone-900">Vedant Saruk</h2>
                            </div>
                            <div className="inline-flex items-center gap-1 bg-green-50 text-green-700 px-2 py-0.5 rounded text-xs font-bold border border-green-100">
                                <CheckCircle2 size={12} /> {t('verified_kisan')}
                            </div>
                        </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-3 mt-2 border-t border-stone-100 pt-4">
                        <div className="flex flex-col">
                            <span className="text-[10px] text-stone-400 uppercase font-bold flex items-center gap-1"><MapPin size={12}/> {t('location')}</span>
                            <span className="text-sm font-bold text-stone-700">Navi Mumbai, MH</span>
                        </div>
                        <div className="flex flex-col">
                            <span className="text-[10px] text-stone-400 uppercase font-bold flex items-center gap-1"><Warehouse size={12}/> {t('primary_mandi')}</span>
                            <span className="text-sm font-bold text-stone-700">Vashi APMC</span>
                        </div>
                        <div className="flex flex-col col-span-2">
                            <span className="text-[10px] text-stone-400 uppercase font-bold flex items-center gap-1"><Sprout size={12}/> {t('holding')}</span>
                            <span className="text-sm font-bold text-stone-700">50 Quintals (Tomato / Onion)</span>
                        </div>
                    </div>
                </div>

                <h3 className="font-bold text-stone-800 text-sm mt-2 ml-1">{t('settings')}</h3>

                {/* Settings Block: Language */}
                <div className="bg-white rounded-2xl p-4 shadow-sm border border-stone-100 flex flex-col gap-3">
                    <div className="flex items-center gap-2 text-stone-900 font-bold">
                        <Globe size={18} className="text-green-600" /> {t('app_language')}
                    </div>
                    <div className="grid grid-cols-2 gap-2 mt-1">
                        {languages.map(lang => {
                            const active = language === lang.code;
                            return (
                                <button 
                                    key={lang.code}
                                    onClick={() => setLanguage(lang.code)}
                                    className={`py-2 px-3 rounded-lg text-sm font-bold border transition-colors ${
                                        active ? 'bg-green-700 text-white border-green-700' : 'bg-stone-50 text-stone-600 border-stone-200 hover:border-green-300'
                                    }`}
                                >
                                    {lang.label}
                                </button>
                            )
                        })}
                    </div>
                </div>

                {/* Settings Block: Voice */}
                <div className="bg-white rounded-2xl p-4 shadow-sm border border-stone-100 flex flex-col gap-3">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2 text-stone-900 font-bold">
                            <Volume2 size={18} className="text-green-600" /> {t('voice_assistant')}
                        </div>
                    </div>
                    <div className="flex gap-2 text-xs">
                        {['Auto', 'Hindi', 'Marathi'].map(opt => (
                            <button key={opt} className={`px-3 py-1.5 rounded-full border font-bold ${opt === 'Auto' ? 'bg-green-50 text-green-700 border-green-200' : 'bg-stone-50 text-stone-500 border-stone-200'}`}>
                                {opt}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Settings Block: Alerts */}
                <div className="bg-white rounded-2xl p-4 shadow-sm border border-stone-100 flex flex-col gap-4">
                    <div className="flex items-center gap-2 text-stone-900 font-bold mb-1">
                        <Bell size={18} className="text-green-600" /> {t('alerts')}
                    </div>
                    {[
                        "Daily Mandi Price Alerts",
                        "Extreme Weather & Spoilage Warnings",
                        "Trade & Export Ban Shocks"
                    ].map((alert, i) => (
                        <div key={i} className="flex items-center justify-between">
                            <span className="text-sm text-stone-700 font-medium">{alert}</span>
                            <div className="w-10 h-6 bg-green-500 rounded-full relative cursor-pointer shadow-inner">
                                <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full shadow-sm"></div>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Settings Block: Offline Storage */}
                <div className="bg-white rounded-2xl p-4 shadow-sm border border-stone-100 flex flex-col gap-3">
                    <div className="flex items-center gap-2 text-stone-900 font-bold">
                        <Database size={18} className="text-green-600" /> {t('offline')}
                    </div>
                    <div className="bg-green-50 text-green-800 text-xs font-bold p-3 rounded-lg border border-green-100 flex items-center justify-between">
                        <span>{t('pwa_offline')}</span>
                        <CheckCircle2 size={16} className="text-green-600" />
                    </div>
                    <button className="text-sm font-bold text-red-600 bg-red-50 py-2.5 rounded-lg border border-red-100 hover:bg-red-100 transition-colors">
                        {t('clear_cache')}
                    </button>
                </div>

                {/* Settings Block: About */}
                <div className="bg-white rounded-2xl p-4 shadow-sm border border-stone-100 flex flex-col gap-2">
                    <div className="flex items-center gap-2 text-stone-900 font-bold mb-1">
                        <Info size={18} className="text-green-600" /> {t('about')}
                    </div>
                    <p className="text-xs text-stone-500 font-medium">Data sources: data.gov.in, Open-Meteo, OSRM</p>
                    <p className="text-xs text-stone-400">{t('version')}</p>
                </div>
            </div>
        </div>
    );
}
