export default function ExplanationPanel({ isVisible, onClose }: { isVisible: boolean, onClose: () => void }) {
    if (!isVisible) return null;
    
    return (
        <div className="fixed inset-0 bg-stone-900/50 z-50 flex flex-col justify-end">
            <div className="bg-white max-h-[80vh] overflow-y-auto w-full max-w-[360px] mx-auto rounded-t-lg p-4">
                <div className="flex justify-between items-center mb-4">
                    <h2 className="font-bold">About this Data</h2>
                    <button onClick={onClose} className="text-xl">&times;</button>
                </div>
                <div className="text-sm">
                    <p className="mb-2"><strong>Data Source:</strong> data.gov.in (Synthetic Fallback)</p>
                    <p className="mb-2"><strong>Trust Score:</strong> High (85/100)</p>
                    <ul className="list-disc pl-4 mb-4 text-xs text-stone-600">
                        <li>Freshness: 30/30</li>
                        <li>Completeness: 20/25</li>
                    </ul>
                    <p className="text-xs text-stone-500 italic">Updated: {new Date().toLocaleDateString()}</p>
                </div>
            </div>
        </div>
    );
}
