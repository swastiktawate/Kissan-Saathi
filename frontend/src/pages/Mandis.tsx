import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import MandiMap from '../components/MandiMap';

const mandisData: Record<string, Record<string, any>> = {
    'Tamatar': {
        'Aaj': [
            {name: 'Kalyan Mandi', price: '2,350', diff: '+18%', trans: '60', net: '2,290', dist: '12 km', best: true},
            {name: 'Vashi Mandi', price: '2,150', diff: '+10%', trans: '100', net: '2,050', dist: '8 km', best: false},
            {name: 'Pune Mandi', price: '1,900', diff: '+5%', trans: '140', net: '1,760', dist: '28 km', best: false},
        ],
        '3 Din Baad': [
            {name: 'Kalyan Mandi', price: '2,450', diff: '+22%', trans: '60', net: '2,390', dist: '12 km', best: true},
            {name: 'Vashi Mandi', price: '2,200', diff: '+12%', trans: '100', net: '2,100', dist: '8 km', best: false},
            {name: 'Pune Mandi', price: '1,950', diff: '+7%', trans: '140', net: '1,810', dist: '28 km', best: false},
        ],
        '7 Din Baad': [
            {name: 'Vashi Mandi', price: '2,800', diff: '+35%', trans: '100', net: '2,700', dist: '8 km', best: true},
            {name: 'Kalyan Mandi', price: '2,650', diff: '+30%', trans: '60', net: '2,590', dist: '12 km', best: false},
            {name: 'Pune Mandi', price: '2,100', diff: '+15%', trans: '140', net: '1,960', dist: '28 km', best: false},
        ]
    },
    'Pyaaz': {
        'Aaj': [
            {name: 'Nashik Mandi', price: '3,400', diff: '+8%', trans: '200', net: '3,200', dist: '85 km', best: true},
            {name: 'Pune Mandi', price: '3,200', diff: '+5%', trans: '150', net: '3,050', dist: '40 km', best: false},
            {name: 'Vashi Mandi', price: '3,050', diff: '+2%', trans: '100', net: '2,950', dist: '8 km', best: false},
        ],
        '3 Din Baad': [
            {name: 'Nashik Mandi', price: '3,200', diff: '-2%', trans: '200', net: '3,000', dist: '85 km', best: true},
            {name: 'Pune Mandi', price: '3,100', diff: '-4%', trans: '150', net: '2,950', dist: '40 km', best: false},
            {name: 'Vashi Mandi', price: '2,900', diff: '-5%', trans: '100', net: '2,800', dist: '8 km', best: false},
        ],
        '7 Din Baad': [
            {name: 'Nashik Mandi', price: '2,900', diff: '-12%', trans: '200', net: '2,700', dist: '85 km', best: true},
            {name: 'Pune Mandi', price: '2,850', diff: '-10%', trans: '150', net: '2,700', dist: '40 km', best: false},
            {name: 'Vashi Mandi', price: '2,700', diff: '-12%', trans: '100', net: '2,600', dist: '8 km', best: false},
        ]
    },
    'Aloo': {
        'Aaj': [
            {name: 'Pune Mandi', price: '1,550', diff: '+4%', trans: '150', net: '1,400', dist: '40 km', best: true},
            {name: 'Vashi Mandi', price: '1,450', diff: '+2%', trans: '100', net: '1,350', dist: '8 km', best: false},
            {name: 'Kalyan Mandi', price: '1,400', diff: '+1%', trans: '60', net: '1,340', dist: '12 km', best: false},
        ],
        '3 Din Baad': [
            {name: 'Pune Mandi', price: '1,550', diff: '+4%', trans: '150', net: '1,400', dist: '40 km', best: true},
            {name: 'Vashi Mandi', price: '1,460', diff: '+2%', trans: '100', net: '1,360', dist: '8 km', best: false},
            {name: 'Kalyan Mandi', price: '1,420', diff: '+1%', trans: '60', net: '1,360', dist: '12 km', best: false},
        ],
        '7 Din Baad': [
            {name: 'Pune Mandi', price: '1,600', diff: '+6%', trans: '150', net: '1,450', dist: '40 km', best: true},
            {name: 'Vashi Mandi', price: '1,500', diff: '+4%', trans: '100', net: '1,400', dist: '8 km', best: false},
            {name: 'Kalyan Mandi', price: '1,480', diff: '+3%', trans: '60', net: '1,420', dist: '12 km', best: false},
        ]
    },
    'Kela': {
        'Aaj': [
            {name: 'Jalgaon Mandi', price: '1,250', diff: '+10%', trans: '180', net: '1,070', dist: '120 km', best: true},
            {name: 'Vashi Mandi', price: '1,100', diff: '+5%', trans: '100', net: '1,000', dist: '8 km', best: false},
            {name: 'Nashik Mandi', price: '1,050', diff: '+2%', trans: '200', net: '850', dist: '85 km', best: false},
        ],
        '3 Din Baad': [
            {name: 'Jalgaon Mandi', price: '1,300', diff: '+12%', trans: '180', net: '1,120', dist: '120 km', best: true},
            {name: 'Vashi Mandi', price: '1,150', diff: '+8%', trans: '100', net: '1,050', dist: '8 km', best: false},
            {name: 'Nashik Mandi', price: '1,100', diff: '+5%', trans: '200', net: '900', dist: '85 km', best: false},
        ],
        '7 Din Baad': [
            {name: 'Jalgaon Mandi', price: '1,400', diff: '+15%', trans: '180', net: '1,220', dist: '120 km', best: true},
            {name: 'Vashi Mandi', price: '1,200', diff: '+10%', trans: '100', net: '1,100', dist: '8 km', best: false},
            {name: 'Nashik Mandi', price: '1,150', diff: '+8%', trans: '200', net: '950', dist: '85 km', best: false},
        ]
    }
};

export default function Mandis() {
    const [activeCrop, setActiveCrop] = useState('Tamatar');
    const [activeTime, setActiveTime] = useState('Aaj');
    
    const cropEmoji = activeCrop === 'Tamatar' ? '🍅' : activeCrop === 'Pyaaz' ? '🧅' : activeCrop === 'Aloo' ? '🥔' : '🍌';
    const data = mandisData[activeCrop]?.[activeTime] || mandisData['Tamatar']['Aaj'];
    
    return (
        <div className="flex flex-col bg-stone-50 min-h-[calc(100vh-60px)] font-sans pb-4">
            {/* Header */}
            <div className="flex items-center p-4 bg-white border-b border-stone-200">
                <Link to="/" className="mr-3 text-stone-600"><ArrowLeft size={20} /></Link>
                <div>
                    <h2 className="font-bold text-stone-900 leading-tight text-lg">Mandi Comparison</h2>
                    <p className="text-xs text-stone-500">Compare prices, costs and net returns</p>
                </div>
            </div>

            {/* Crop Selector */}
            <div className="bg-white px-4 py-3 flex gap-4 overflow-x-auto border-b border-stone-200 scrollbar-hide">
                {[
                    {name: 'Tamatar', emoji: '🍅'},
                    {name: 'Pyaaz', emoji: '🧅'},
                    {name: 'Aloo', emoji: '🥔'},
                    {name: 'Kela', emoji: '🍌'}
                ].map(c => {
                    const isActive = activeCrop === c.name;
                    return (
                    <button key={c.name} onClick={() => setActiveCrop(c.name)} className={`flex flex-col items-center min-w-[60px] pb-2 border-b-2 transition-all ${isActive ? 'border-green-600' : 'border-transparent opacity-60 hover:opacity-100'}`}>
                        <span className="text-2xl mb-1">{c.emoji}</span>
                        <span className={`text-[10px] font-medium ${isActive ? 'text-green-700' : 'text-stone-500'}`}>{c.name}</span>
                    </button>
                    );
                })}
            </div>

            {/* Time toggle */}
            <div className="bg-white p-3 border-b border-stone-200">
                <div className="flex bg-stone-100 rounded-lg p-1">
                    {['Aaj', '3 Din Baad', '7 Din Baad'].map(t => (
                        <button key={t} onClick={() => setActiveTime(t)} className={`flex-1 font-medium text-xs py-2 rounded transition-all ${activeTime === t ? 'bg-white text-stone-800 font-bold shadow-sm' : 'text-stone-500 hover:text-stone-700'}`}>{t}</button>
                    ))}
                </div>
            </div>

            {/* Map Area */}
            <div className="h-64 bg-stone-200 relative border-b border-stone-200 z-0">
                <MandiMap data={data} />
            </div>

            <div className="bg-white p-4">
                <h3 className="font-bold text-stone-800 text-lg mb-3">Mandi Comparison</h3>
                
                <table className="w-full text-left text-xs">
                    <thead>
                        <tr className="border-b border-stone-200 text-stone-500">
                            <th className="pb-2 font-medium">Mandi</th>
                            <th className="pb-2 font-medium">Price<br/>(₹/q)</th>
                            <th className="pb-2 font-medium">Transport<br/>Cost (₹/q)</th>
                            <th className="pb-2 font-medium">Net Return<br/>(₹/q)</th>
                            <th className="pb-2 font-medium text-right">Distance</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.map((m: any, i: number) => (
                            <tr key={i} className="border-b border-stone-100 last:border-none">
                                <td className="py-3 flex items-center gap-2">
                                    <div className="w-8 h-8 bg-stone-100 rounded overflow-hidden flex items-center justify-center text-lg">{cropEmoji}</div>
                                    <span className="font-bold text-stone-800 leading-tight w-12">{m.name.replace(' ', '\n')}</span>
                                </td>
                                <td className="py-3 font-bold text-sm">
                                    {m.price}
                                    <div className={`text-[10px] font-medium ${m.diff.startsWith('+') ? 'text-green-600' : 'text-red-500'}`}>{m.diff}</div>
                                </td>
                                <td className="py-3 text-stone-600">{m.trans}</td>
                                <td className="py-3 font-bold text-sm text-stone-900">{m.net}</td>
                                <td className="py-3 text-right">
                                    <div className="text-stone-600">{m.dist}</div>
                                    {m.best && <div className="text-[9px] bg-green-500 text-white font-bold px-1.5 py-0.5 rounded-full inline-block mt-1">Best Option</div>}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                
                <div className="bg-orange-50 border border-orange-100 rounded-lg p-3 mt-4">
                    <div className="flex items-center gap-2 mb-2">
                        <div className="bg-orange-500 text-white w-5 h-5 rounded-full flex justify-center items-center font-bold text-xs">!</div>
                        <h4 className="font-bold text-orange-900 text-sm">Key Insights ({activeTime})</h4>
                    </div>
                    <ul className="list-disc pl-5 text-[11px] text-stone-700 space-y-1">
                        <li>{data.find((d: any) => d.best)?.name} offers the highest net return {activeTime === 'Aaj' ? 'today' : 'at this time'}.</li>
                        <li>Consider transport cost and spoilage risk before selecting distant mandis.</li>
                        <li>AI confidence is high for this recommendation based on seasonal trends.</li>
                    </ul>
                </div>
            </div>
        </div>
    );
}
