import { useState, useEffect } from 'react';

export function useOffline() {
    const [isOffline, setIsOffline] = useState(!navigator.onLine);
    const [lastSync, setLastSync] = useState<string | null>(null);

    useEffect(() => {
        const handleOnline = () => setIsOffline(false);
        const handleOffline = () => setIsOffline(true);
        window.addEventListener('online', handleOnline);
        window.addEventListener('offline', handleOffline);
        
        const syncTime = localStorage.getItem('lastSyncTime');
        if (syncTime) setLastSync(new Date(syncTime).toLocaleString());

        return () => {
            window.removeEventListener('online', handleOnline);
            window.removeEventListener('offline', handleOffline);
        };
    }, []);

    return { isOffline, lastSync };
}
