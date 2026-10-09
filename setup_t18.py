import os

os.makedirs('frontend/src/pages', exist_ok=True)
os.makedirs('frontend/src/components', exist_ok=True)

with open('frontend/src/components/RecommendationCard.tsx', 'w') as f:
    f.write('''import React from 'react';
import en from '../i18n/en.json';

export default function RecommendationCard({ data }: { data: any }) {
    if (!data) return <div>Loading...</div>;

    const { action, expected_gain_per_q, meta, reasons } = data;
    const isInsufficient = meta?.trust === 'Insufficient';

    return (
        <div className="bg-white p-4 rounded border border-stone-200 mb-4">
            <div className="flex justify-between items-center mb-2">
                <h3 className="font-bold">{en.action}: {!isInsufficient && en[action as keyof typeof en]}</h3>
                <span className={`px-2 py-1 text-xs rounded ${meta?.trust === 'High' ? 'bg-accent' : 'bg-stone-200'}`}>
                    {en.trust}: {en[meta?.trust?.toLowerCase() as keyof typeof en] || meta?.trust}
                </span>
            </div>
            
            {!isInsufficient && (
                <div className="mb-2">
                    <span className="text-sm font-semibold">{en.expected_gain}: {expected_gain_per_q?.toFixed(2)}</span>
                </div>
            )}
            
            {meta?.trust === 'Medium' && (
                <div className="bg-yellow-100 p-2 text-xs mb-2 rounded">{en.caution}</div>
            )}
            
            <ul className="list-disc pl-4 text-sm">
                {reasons?.map((r: string, i: number) => (
                    <li key={i}>{r}</li>
                ))}
            </ul>
        </div>
    );
}
''')

with open('frontend/src/components/InputSheet.tsx', 'w') as f:
    f.write('''import React, { useState, useEffect } from 'react';
import en from '../i18n/en.json';

export default function InputSheet({ onSave }: { onSave: (p: any) => void }) {
    const [params, setParams] = useState({
        crop: 'tomato',
        home_mandi: 'vashi',
        quantity_q: 50,
        horizon_days: 7,
        risk_setting: 'balanced'
    });

    useEffect(() => {
        const saved = localStorage.getItem('kisan_settings');
        if (saved) setParams(JSON.parse(saved));
    }, []);

    const handleChange = (e: any) => {
        setParams({ ...params, [e.target.name]: e.target.value });
    };

    const handleSave = () => {
        localStorage.setItem('kisan_settings', JSON.stringify(params));
        onSave(params);
    };

    return (
        <div className="p-4 bg-white border-t border-stone-200">
            <h3 className="font-bold mb-2">{en.settings}</h3>
            <div className="flex flex-col gap-2">
                <input name="quantity_q" type="number" value={params.quantity_q} onChange={handleChange} className="border p-1" placeholder={en.quantity} />
                <select name="risk_setting" value={params.risk_setting} onChange={handleChange} className="border p-1">
                    <option value="cautious">{en.cautious}</option>
                    <option value="balanced">{en.balanced}</option>
                    <option value="aggressive">{en.aggressive}</option>
                </select>
                <button onClick={handleSave} className="bg-accent text-textMain px-4 py-2 rounded">{en.save}</button>
            </div>
        </div>
    );
}
''')

with open('frontend/src/pages/Home.tsx', 'w') as f:
    f.write('''import React, { useState, useEffect } from 'react';
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
''')

with open('frontend/src/App.tsx', 'w') as f:
    f.write('''import React from 'react';
import Home from './pages/Home';

function App() {
  return <Home />;
}

export default App;
''')
