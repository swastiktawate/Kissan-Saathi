import os

with open('frontend/src/hooks/useOffline.ts', 'w', encoding='utf-8') as f:
    f.write('''import { useState, useEffect } from 'react';

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
''')

with open('frontend/vite.config.ts', 'w', encoding='utf-8') as f:
    f.write('''/// <reference types="vitest" />
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { VitePWA } from 'vite-plugin-pwa'
import { defineConfig } from 'vitest/config'

export default defineConfig({
  plugins: [
    react(), 
    tailwindcss(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.svg', 'icons.svg'],
      manifest: {
        name: 'Kisan Saathi',
        short_name: 'Kisan',
        theme_color: '#F7F5F0',
        icons: [
          {
            src: 'favicon.svg',
            sizes: '192x192',
            type: 'image/svg+xml'
          }
        ]
      },
      workbox: {
        runtimeCaching: [
          {
            urlPattern: /\\/api\\/v1\\/(meta|recommend)/,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              networkTimeoutSeconds: 5,
              expiration: {
                maxEntries: 10,
                maxAgeSeconds: 60 * 60 * 24
              }
            }
          }
        ]
      }
    })
  ],
  test: {
    environment: 'jsdom'
  }
})
''')

with open('frontend/src/components/OfflineBanner.tsx', 'w', encoding='utf-8') as f:
    f.write('''import { useOffline } from '../hooks/useOffline';

export default function OfflineBanner() {
    const { isOffline, lastSync } = useOffline();
    if (!isOffline) return null;
    return (
        <div className="bg-stone-900 text-white text-xs p-2 text-center fixed top-0 w-full max-w-[360px] z-50">
            Offline — showing last result {lastSync ? `from ${lastSync}` : ''}
        </div>
    );
}
''')
