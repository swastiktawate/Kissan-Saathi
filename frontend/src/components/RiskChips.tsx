import { useState } from 'react';

export default function RiskChips({ risks }: { risks: any[] }) {
    const [expanded, setExpanded] = useState<number | null>(null);

    if (!risks || risks.length === 0) {
        return <div className="text-sm bg-stone-100 p-2 rounded-sm mb-4">No reliable risk signals.</div>;
    }

    return (
        <div className="flex flex-col gap-2 mb-4">
            <h3 className="font-bold text-sm">Risk Flags</h3>
            {risks.map((r, i) => (
                <div key={i} className="border border-stone-200 rounded-sm">
                    <button 
                        className="w-full text-left p-2 bg-white flex justify-between items-center text-sm"
                        onClick={() => setExpanded(expanded === i ? null : i)}
                    >
                        <span className="font-semibold text-red-600">⚠ {r.name}</span>
                        <span className="text-stone-400">{expanded === i ? '−' : '+'}</span>
                    </button>
                    {expanded === i && (
                        <div className="p-2 border-t border-stone-200 bg-stone-50 text-xs">
                            <p><strong>Value:</strong> {r.value}</p>
                            <p><strong>Threshold:</strong> {r.threshold}</p>
                            <p className="mt-1 text-stone-600">{r.explanation}</p>
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
}
