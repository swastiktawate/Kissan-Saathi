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
    { id: 1, name: "Supreme Fresh", lat: 19.090152, lng: 73.03137, capacity: "5000 MT", rate: "₹1.5/kg per month", phone: "Not Available", dist: "Navi Mumbai", mapsLink: "https://maps.app.goo.gl/82nXibFw6xYhTLBn6" },
    { id: 2, name: "Rishi Ice and Cold Storage", lat: 19.063241, lng: 73.028541, capacity: "8000 MT", rate: "₹1.2/kg per month", phone: "09821787878", dist: "Navi Mumbai", mapsLink: "https://maps.app.goo.gl/thvNT6EanwM74Xsu8" },
    { id: 3, name: "Prabhu Hira Ice and Cold Storage", lat: 19.069167, lng: 73.008386, capacity: "4500 MT", rate: "₹1.4/kg per month", phone: "09511110080", dist: "Navi Mumbai", mapsLink: "https://maps.app.goo.gl/b4HGXsTUwyaXusXm9" },
    { id: 4, name: "Snowman Logistics", lat: 19.087648, lng: 73.139770, capacity: "12000 MT", rate: "₹1.8/kg per month", phone: "09821383252", dist: "Navi Mumbai", mapsLink: "https://maps.app.goo.gl/ZoVkubUfVXNPRXvK7" },
    { id: 5, name: "JWL Cold Storage", lat: 18.961725, lng: 73.046260, capacity: "10000 MT", rate: "₹1.6/kg per month", phone: "Not Available", dist: "Navi Mumbai", mapsLink: "https://maps.app.goo.gl/sVgMS9uHkiauu9oV7" },
    { id: 6, name: "Bhalerao Cold Storage", lat: 20.125854, lng: 73.964295, capacity: "3000 MT", rate: "₹1.1/kg per month", phone: "Not Available", dist: "Nashik", mapsLink: "https://maps.google.com/?q=20.125854,73.964295" },
    { id: 7, name: "Sangale Cold Storage", lat: 20.098164, lng: 74.115558, capacity: "6500 MT", rate: "₹1.3/kg per month", phone: "Not Available", dist: "Nashik", mapsLink: "https://maps.google.com/?q=20.098164,74.115558" },
    { id: 8, name: "Arya Cold Storage", lat: 20.127155, lng: 73.968179, capacity: "5500 MT", rate: "₹1.2/kg per month", phone: "Not Available", dist: "Nashik", mapsLink: "https://maps.google.com/?q=20.127155,73.968179" },
    { id: 9, name: "Vakratunda Cold Storage", lat: 20.138261, lng: 73.966165, capacity: "4000 MT", rate: "₹1.4/kg per month", phone: "Not Available", dist: "Nashik", mapsLink: "https://maps.google.com/?q=20.138261,73.966165" }
];

export default function ColdStorage() {
    const center: [number, number] = [19.6, 73.5]; // Maharashtra Center
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
                <MapContainer center={center} zoom={8} className="h-full w-full" zoomControl={false}>
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
                    Maharashtra
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
                                <button 
                                    onClick={() => {
                                        if(store.phone !== 'Not Available') window.open('tel:' + store.phone);
                                        else alert('Contact number not available for this storage.');
                                    }}
                                    className={`flex-1 border py-1.5 rounded-lg text-xs font-bold flex items-center justify-center gap-1 transition-colors ${store.phone !== 'Not Available' ? 'bg-green-50 text-green-700 border-green-200 hover:bg-green-100' : 'bg-stone-50 text-stone-400 border-stone-200 cursor-not-allowed'}`}>
                                    <Phone size={14} />
                                    {store.phone !== 'Not Available' ? 'Call Now' : 'No Number'}
                                </button>
                                <button 
                                    onClick={() => window.open(store.mapsLink, '_blank')}
                                    className="flex-1 bg-green-600 text-white py-1.5 rounded-lg text-xs font-bold flex items-center justify-center gap-1 hover:bg-green-700 transition-colors shadow-sm">
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
