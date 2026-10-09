import { useEffect, useState } from 'react';
import { Megaphone, X } from 'lucide-react';

interface Alert {
    id: string;
    title: string;
    summary: string;
    category: string;
    severity: string;
    source_url: string;
    date: string;
}

export default function PolicyAlertBanner() {
    const [highAlert, setHighAlert] = useState<Alert | null>(null);
    const [dismissed, setDismissed] = useState(false);

    useEffect(() => {
        fetch('http://localhost:8000/api/v1/policy-alerts')
            .then(res => res.json())
            .then((data: Alert[]) => {
                const alert = data.find(a => a.severity === 'High');
                if (alert) setHighAlert(alert);
            })
            .catch(console.error);
    }, []);

    if (!highAlert || dismissed) return null;

    return (
        <div className="bg-amber-100 border-b border-amber-400 text-amber-900 px-4 py-2 flex items-start gap-3 shadow-sm relative z-10 pr-10">
            <Megaphone size={18} className="text-amber-600 mt-0.5 shrink-0" />
            <div>
                <p className="text-[10px] font-bold uppercase tracking-wider text-amber-700 mb-0.5">{highAlert.category} SHOCK ALERT</p>
                <p className="text-sm font-medium leading-tight">{highAlert.title}</p>
            </div>
            <button 
                onClick={() => setDismissed(true)} 
                className="absolute top-2 right-2 text-amber-700 hover:text-amber-900 p-1"
            >
                <X size={16} />
            </button>
        </div>
    );
}
