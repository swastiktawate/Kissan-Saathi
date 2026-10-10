import { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { Snowflake, MapPin, Navigation, Phone } from 'lucide-react';

// Fix for default Leaflet icon in React
const customIcon = new L.Icon({
    iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
    iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

// Dummy Data around Nashik/Maharashtra
const dummyStorages = [
    { id: 1, name: "Kisan Seva Cold Storage", lat: 20.0075, lng: 73.7898, capacity: "5000 MT", rate: "₹1.5/kg per month", phone: "+91 98765 43210", dist: "1.2 km" },
    { id: 2, name: "AgriSafe Nashik Unit", lat: 19.9850, lng: 73.7700, capacity: "12000 MT", rate: "₹1.2/kg per month", phone: "+91 99887 76655", dist: "3.5 km" },
    { id: 3, name: "Sahyadri Cold Chain", lat: 19.9500, lng: 73.8100, capacity: "8000 MT", rate: "₹1.4/kg per month", phone: "+91 91234 56789", dist: "5.8 km" },
    { id: 4, name: "MahaFresh Storage", lat: 20.0200, lng: 73.8300, capacity: "3000 MT", rate: "₹1.6/kg per month", phone: "+91 98989 12121", dist: "7.1 km" }
];

export default function ColdStorage() {
    const center: [number, number] = [19.9975, 73.7898]; // Nashik
    const [selectedId, setSelectedId] = useState<number | null>(null);

    return (
        <div className="flex flex-col h-[calc(100vh-60px)] bg-stone-50">
            {/* Header */}
            <div className="bg-green-700 text-white p-4 shadow-md z-10 flex items-center gap-3">
                <div className="bg-white/20 p-2 rounded-lg">
                    <Snowflake size={24} className="text-white" />
                </div>
                <div>
                    <h1 className="font-bold text-lg leading-tight">Nearby Cold Storage</h1>
                    <p className="text-xs text-green-100">Hold your crops securely</p>
                </div>
            </div>

            {/* Map Area */}
            <div className="h-[40vh] w-full z-0 relative">
                <MapContainer center={center} zoom={12} className="h-full w-full" zoomControl={false}>
                    <TileLayer
                        attribution='&copy; <a href="https://www.openstreetmap.org/">OSM</a>'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />
                    {dummyStorages.map(store => (
                        <Marker 
                            key={store.id} 
                            position={[store.lat, store.lng]} 
                            icon={customIcon}
                            eventHandlers={{
                                click: () => setSelectedId(store.id)
                            }}
                        >
                            <Popup>
                                <div className="font-bold text-green-700">{store.name}</div>
                                <div className="text-xs text-stone-600">{store.capacity} Capacity</div>
                            </Popup>
                        </Marker>
                    ))}
                </MapContainer>
                {/* Float indicator */}
                <div className="absolute top-2 right-2 bg-white px-3 py-1.5 rounded-full shadow-md z-[1000] text-xs font-bold text-stone-700 flex items-center gap-1 border border-stone-200">
                    <MapPin size={14} className="text-green-600" />
                    Nashik, MH
                </div>
            </div>

            {/* List Area */}
            <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-3">
                <h2 className="font-bold text-stone-800 flex items-center gap-2 mb-1">
                    Available Facilities <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full">{dummyStorages.length} Found</span>
                </h2>
                
                {dummyStorages.map(store => {
                    const isSelected = selectedId === store.id;
                    return (
                        <div 
                            key={store.id}
                            onClick={() => setSelectedId(store.id)}
                            className={`bg-white p-4 rounded-xl border transition-all cursor-pointer ${
                                isSelected ? 'border-green-500 shadow-md ring-1 ring-green-500' : 'border-stone-200 shadow-sm hover:border-green-300'
                            }`}
                        >
                            <div className="flex justify-between items-start mb-2">
                                <h3 className="font-bold text-stone-900 leading-tight">{store.name}</h3>
                                <div className="bg-stone-100 text-stone-600 text-[10px] font-bold px-2 py-1 rounded flex items-center gap-1">
                                    <Navigation size={10} />
                                    {store.dist}
                                </div>
                            </div>
                            
                            <div className="flex gap-4 mb-3">
                                <div className="flex flex-col">
                                    <span className="text-[10px] text-stone-400 uppercase tracking-wider font-bold">Capacity</span>
                                    <span className="text-xs font-medium text-stone-700">{store.capacity}</span>
                                </div>
                                <div className="flex flex-col">
                                    <span className="text-[10px] text-stone-400 uppercase tracking-wider font-bold">Est. Rate</span>
                                    <span className="text-xs font-medium text-green-700">{store.rate}</span>
                                </div>
                            </div>
                            
                            <div className="flex gap-2">
                                <button className="flex-1 bg-green-50 text-green-700 border border-green-200 py-1.5 rounded-lg text-xs font-bold flex items-center justify-center gap-1 hover:bg-green-100 transition-colors">
                                    <Phone size={14} />
                                    Call Now
                                </button>
                                <button className="flex-1 bg-green-600 text-white py-1.5 rounded-lg text-xs font-bold flex items-center justify-center gap-1 hover:bg-green-700 transition-colors shadow-sm">
                                    <Navigation size={14} />
                                    Directions
                                </button>
                            </div>
                        </div>
                    );
                })}
                <div className="h-6"></div> {/* Bottom padding padding for nav */}
            </div>
        </div>
    );
}
