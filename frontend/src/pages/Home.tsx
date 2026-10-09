import { useState, useEffect } from 'react';
import en from '../i18n/en.json';
import RecommendationCard from '../components/RecommendationCard';
import InputSheet from '../components/InputSheet';
import { fetchRecommendation } from '../api/client';

export default function Home() {
    const [recData, setRecData] = useState<any>(null);

    const loadData = async (params: any) => {
        const data = await fetchRecommendation(params);
        setRecData(data);
    };

    useEffect(() => {
        const saved = localStorage.getItem('kisan_settings');
        if (saved) loadData(JSON.parse(saved));
        else loadData({ crop: 'tomato', home_mandi: 'vashi', quantity_q: 50, horizon_days: 7, risk_setting: 'balanced' });
    }, []);

    return (
        <div className="max-w-[360px] mx-auto min-h-screen flex flex-col">
            <div className="flex-1 p-4">
                <h1 className="text-2xl font-bold mb-4">{en.greeting}</h1>
                <div className="flex gap-2 mb-4">
                    <span className="bg-stone-200 px-3 py-1 rounded-full text-sm">Tomato</span>
                    <span className="bg-stone-200 px-3 py-1 rounded-full text-sm">Onion</span>
                </div>
                
                <h2 className="font-bold mb-2">{en.top_mandis}</h2>
                <RecommendationCard data={recData} />
            </div>
            
            <InputSheet onSave={loadData} />
        </div>
    );
}
