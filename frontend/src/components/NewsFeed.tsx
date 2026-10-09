import { useEffect, useState } from 'react';
import { ExternalLink } from 'lucide-react';

interface Alert {
    id: string;
    title: string;
    summary: string;
    category: string;
    severity: string;
    source_url: string;
    date: string;
}

export default function NewsFeed() {
    const [alerts, setAlerts] = useState<Alert[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('http://localhost:8000/api/v1/policy-alerts')
            .then(res => res.json())
            .then(data => {
                setAlerts(data);
                setLoading(false);
            })
            .catch(() => setLoading(false));
    }, []);

    if (loading) return <div className="p-4 text-xs text-stone-500 animate-pulse">Loading policy news...</div>;

    return (
        <div className="flex flex-col gap-4">
            <h3 className="font-bold text-stone-800 text-lg">Policy & News Radar</h3>
            <p className="text-xs text-stone-500 -mt-2 mb-2">Macro events affecting agricultural supply chains.</p>
            
            {alerts.map(alert => (
                <div key={alert.id} className="bg-white rounded-xl shadow-sm border border-green-200 p-4 transition-all hover:shadow-md relative overflow-hidden">
                    {alert.severity === 'High' && <div className="absolute top-0 left-0 w-1 h-full bg-red-500"></div>}
                    {alert.severity === 'Medium' && <div className="absolute top-0 left-0 w-1 h-full bg-orange-500"></div>}
                    {alert.severity === 'Low' && <div className="absolute top-0 left-0 w-1 h-full bg-green-500"></div>}
                    
                    <div className="flex justify-between items-start mb-2 ml-1">
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                            alert.severity === 'High' ? 'bg-red-100 text-red-700 border border-red-200' :
                            alert.severity === 'Medium' ? 'bg-orange-100 text-orange-700 border border-orange-200' :
                            'bg-green-100 text-green-700 border border-green-200'
                        }`}>
                            {alert.severity} • {alert.category}
                        </span>
                        <span className="text-[10px] text-stone-400 font-medium">{alert.date}</span>
                    </div>
                    
                    <div className="ml-1">
                        <h4 className="font-bold text-stone-800 text-sm mb-1">{alert.title}</h4>
                        <p className="text-xs text-stone-600 leading-relaxed mb-3">{alert.summary}</p>
                        <a 
                            href={alert.source_url} 
                            target="_blank" 
                            rel="noreferrer" 
                            className="inline-flex items-center text-xs font-bold text-green-600 hover:text-green-700"
                        >
                            Read full story <ExternalLink size={12} className="ml-1" />
                        </a>
                    </div>
                </div>
            ))}
        </div>
    );
}
