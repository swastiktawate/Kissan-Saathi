import { useOffline } from '../hooks/useOffline';

export default function OfflineBanner() {
    const { isOffline, lastSync } = useOffline();
    if (!isOffline) return null;
    return (
        <div className="bg-stone-900 text-white text-xs p-2 text-center fixed top-0 w-full max-w-[360px] z-50">
            Offline — showing last result {lastSync ? `from ${lastSync}` : ''}
        </div>
    );
}
