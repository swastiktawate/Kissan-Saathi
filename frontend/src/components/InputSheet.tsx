import { useState, useEffect } from 'react';
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
