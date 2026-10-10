import re

with open('frontend/src/pages/ColdStorage.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the dummyStorages array completely
new_data = """const dummyStorages = [
    { id: 1, name: "Supreme Fresh", lat: 19.090152, lng: 73.03137, capacity: "5000 MT", rate: "₹1.5/kg per month", phone: "Not Available", dist: "Navi Mumbai", mapsLink: "https://maps.app.goo.gl/82nXibFw6xYhTLBn6" },
    { id: 2, name: "Rishi Ice and Cold Storage", lat: 19.063241, lng: 73.028541, capacity: "8000 MT", rate: "₹1.2/kg per month", phone: "09821787878", dist: "Navi Mumbai", mapsLink: "https://maps.app.goo.gl/thvNT6EanwM74Xsu8" },
    { id: 3, name: "Prabhu Hira Ice and Cold Storage", lat: 19.069167, lng: 73.008386, capacity: "4500 MT", rate: "₹1.4/kg per month", phone: "09511110080", dist: "Navi Mumbai", mapsLink: "https://maps.app.goo.gl/b4HGXsTUwyaXusXm9" },
    { id: 4, name: "Snowman Logistics", lat: 19.087648, lng: 73.139770, capacity: "12000 MT", rate: "₹1.8/kg per month", phone: "09821383252", dist: "Navi Mumbai", mapsLink: "https://maps.app.goo.gl/ZoVkubUfVXNPRXvK7" },
    { id: 5, name: "JWL Cold Storage", lat: 18.961725, lng: 73.046260, capacity: "10000 MT", rate: "₹1.6/kg per month", phone: "Not Available", dist: "Navi Mumbai", mapsLink: "https://maps.app.goo.gl/sVgMS9uHkiauu9oV7" },
    { id: 6, name: "Bhalerao Cold Storage", lat: 20.125854, lng: 73.964295, capacity: "3000 MT", rate: "₹1.1/kg per month", phone: "Not Available", dist: "Nashik", mapsLink: "https://maps.google.com/?q=20.125854,73.964295" },
    { id: 7, name: "Sangale Cold Storage", lat: 20.098164, lng: 74.115558, capacity: "6500 MT", rate: "₹1.3/kg per month", phone: "Not Available", dist: "Nashik", mapsLink: "https://maps.google.com/?q=20.098164,74.115558" },
    { id: 8, name: "Arya Cold Storage", lat: 20.127155, lng: 73.968179, capacity: "5500 MT", rate: "₹1.2/kg per month", phone: "Not Available", dist: "Nashik", mapsLink: "https://maps.google.com/?q=20.127155,73.968179" },
    { id: 9, name: "Vakratunda Cold Storage", lat: 20.138261, lng: 73.966165, capacity: "4000 MT", rate: "₹1.4/kg per month", phone: "Not Available", dist: "Nashik", mapsLink: "https://maps.google.com/?q=20.138261,73.966165" }
];"""

content = re.sub(r'const dummyStorages = \[.*?\];', new_data, content, flags=re.DOTALL)

# Adjust center to between Nashik and Navi Mumbai [19.5, 73.5] and zoom to 8
content = content.replace('const center: [number, number] = [19.9975, 73.7898]; // Nashik', 'const center: [number, number] = [19.6, 73.5]; // Maharashtra Center')
content = content.replace('zoom={12}', 'zoom={8}')

# Change indicator from Nashik, MH to Maharashtra
content = content.replace('Nashik, MH', 'Maharashtra')

# Adjust Call Now button
call_btn_old = """<button className="flex-1 bg-green-50 text-green-700 border border-green-200 py-1.5 rounded-lg text-xs font-bold flex items-center justify-center gap-1 hover:bg-green-100 transition-colors">
                                    <Phone size={14} />
                                    Call Now
                                </button>"""

call_btn_new = """<button 
                                    onClick={() => {
                                        if(store.phone !== 'Not Available') window.open('tel:' + store.phone);
                                        else alert('Contact number not available for this storage.');
                                    }}
                                    className={`flex-1 border py-1.5 rounded-lg text-xs font-bold flex items-center justify-center gap-1 transition-colors ${store.phone !== 'Not Available' ? 'bg-green-50 text-green-700 border-green-200 hover:bg-green-100' : 'bg-stone-50 text-stone-400 border-stone-200 cursor-not-allowed'}`}>
                                    <Phone size={14} />
                                    {store.phone !== 'Not Available' ? 'Call Now' : 'No Number'}
                                </button>"""

content = content.replace(call_btn_old, call_btn_new)

# Adjust Directions button
dir_btn_old = """<button className="flex-1 bg-green-600 text-white py-1.5 rounded-lg text-xs font-bold flex items-center justify-center gap-1 hover:bg-green-700 transition-colors shadow-sm">
                                    <Navigation size={14} />
                                    Directions
                                </button>"""

dir_btn_new = """<button 
                                    onClick={() => window.open(store.mapsLink, '_blank')}
                                    className="flex-1 bg-green-600 text-white py-1.5 rounded-lg text-xs font-bold flex items-center justify-center gap-1 hover:bg-green-700 transition-colors shadow-sm">
                                    <Navigation size={14} />
                                    Directions
                                </button>"""

content = content.replace(dir_btn_old, dir_btn_new)

with open('frontend/src/pages/ColdStorage.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
