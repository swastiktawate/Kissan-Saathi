import { MapContainer, TileLayer, Marker, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { useEffect } from 'react';

const mandiCoords: Record<string, [number, number]> = {
    'Vashi Mandi': [19.076, 73.008],
    'Kalyan Mandi': [19.243, 73.136],
    'Pune Mandi': [18.520, 73.856],
    'Nashik Mandi': [19.997, 73.789],
    'Jalgaon Mandi': [21.007, 75.562],
};

const createIcon = (name: string, dist: string, isBest: boolean) => {
    const color = isBest ? '#16a34a' : '#f97316';
    return L.divIcon({
        className: 'bg-transparent border-none',
        html: `
            <div style="display: flex; flex-direction: column; align-items: center; width: max-content; transform: translate(-50%, -100%);">
                <div style="background: white; padding: 4px 8px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; margin-bottom: 2px;">
                    <div style="font-size: 11px; font-weight: bold; color: #1c1917;">${name}</div>
                    <div style="font-size: 10px; color: #78716c;">${dist}</div>
                </div>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="${color}" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                    <circle cx="12" cy="10" r="3" fill="white"></circle>
                </svg>
            </div>
        `,
        iconSize: [0, 0], // The HTML transform centers it
    });
};

function ChangeView({ bounds }: { bounds: L.LatLngBounds }) {
    const map = useMap();
    useEffect(() => {
        if (bounds.isValid()) {
            map.fitBounds(bounds, { padding: [30, 30] });
        }
    }, [bounds, map]);
    return null;
}

export default function MandiMap({ data }: { data: any[] }) {
    const bounds = L.latLngBounds(data.map(m => mandiCoords[m.name] || [19.0, 73.0]));
    
    return (
        <MapContainer 
            bounds={bounds} 
            style={{ height: '100%', width: '100%', zIndex: 0 }}
            zoomControl={false}
            attributionControl={false} // Removes the OSM footer overlay to keep UI clean
        >
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {data.map((m, i) => {
                const coord = mandiCoords[m.name];
                if (!coord) return null;
                return (
                    <Marker 
                        key={i} 
                        position={coord} 
                        icon={createIcon(m.name, m.dist, m.best)}
                    />
                );
            })}
            <ChangeView bounds={bounds} />
        </MapContainer>
    );
}
