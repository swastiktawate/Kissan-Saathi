
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
