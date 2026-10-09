import os

with open('frontend/src/pages/Home.tsx', 'w', encoding='utf-8') as f:
    f.write('''import { Link } from 'react-router-dom';
import { Bell, Mic, Send, ArrowUpRight, TrendingUp, ChevronRight, Leaf } from 'lucide-react';

export default function Home() {
    return (
        <div className="flex flex-col bg-white min-h-[calc(100vh-60px)] font-sans">
            {/* Header */}
            <div className="flex justify-between items-center p-4">
                <div className="flex items-center gap-2">
                    <div className="bg-green-600 p-1.5 rounded-lg text-white">
                        <Leaf size={24} />
                    </div>
                    <div>
                        <h1 className="text-xl font-bold text-green-800 leading-tight">Kisan Sathi</h1>
                        <p className="text-xs text-stone-500">Sahi Samay, Behtar Daam.</p>
                    </div>
                </div>
                <button className="p-2 border border-stone-200 rounded-full">
                    <Bell size={20} className="text-stone-700" />
                </button>
            </div>

            {/* Hero Card */}
            <div className="px-4 mb-4">
                <div className="bg-gradient-to-r from-green-800 to-green-600 rounded-xl p-4 text-white shadow-md relative overflow-hidden">
                    <div className="absolute right-0 bottom-0 opacity-20 transform translate-x-4 translate-y-4">
                        <Leaf size={100} />
                    </div>
                    <h2 className="text-xl font-bold mb-1 relative z-10">Kisan Sathi</h2>
                    <p className="text-sm text-green-50 w-2/3 relative z-10">Aapke fasal ke liye behtar faisle, data ke saath.</p>
                </div>
            </div>

            {/* Quick Chat Input */}
            <div className="px-4 mb-6">
                <div className="flex items-center gap-2 bg-white border border-stone-200 rounded-full p-2 shadow-sm">
                    <button className="p-2 text-stone-500 hover:text-green-600"><Mic size={20} /></button>
                    <div className="flex-1 flex flex-col">
                        <input type="text" placeholder="Kuch poochhiye..." className="text-sm outline-none bg-transparent" />
                        <span className="text-[10px] text-stone-400 truncate">Jaise: "Kya mujhe aaj tamatar bechna chahiye?"</span>
                    </div>
                    <button className="bg-green-500 text-white p-2 rounded-full"><Send size={16} /></button>
                </div>
            </div>

            {/* My Crops */}
            <div className="px-4 mb-6">
                <div className="flex justify-between items-end mb-3">
                    <h3 className="font-bold text-stone-800">Meri Faslein</h3>
                    <button className="text-xs text-green-600 font-medium">Sab dekhein</button>
                </div>
                <div className="flex gap-4 overflow-x-auto pb-2 scrollbar-hide">
                    {[
                        {name: 'Tamatar', emoji: '🍅', active: true},
                        {name: 'Pyaaz', emoji: '🧅', active: false},
                        {name: 'Aloo', emoji: '🥔', active: false},
                        {name: 'Kela', emoji: '🍌', active: false}
                    ].map(c => (
                        <div key={c.name} className={`flex flex-col items-center min-w-[70px] p-2 rounded-xl border ${c.active ? 'border-green-500 bg-green-50' : 'border-stone-200'}`}>
                            <span className="text-2xl mb-1">{c.emoji}</span>
                            <span className={`text-xs font-medium ${c.active ? 'text-green-700' : 'text-stone-600'}`}>{c.name}</span>
                        </div>
                    ))}
                </div>
            </div>

            {/* Today's Price */}
            <div className="px-4 mb-4">
                <div className="flex justify-between items-center mb-2">
                    <h3 className="font-bold text-stone-800">Aaj ka Mandi Bhav (Tamatar)</h3>
                    <div className="flex items-center text-xs text-stone-500"><span className="text-green-600 mr-1">📍</span> Vashi Mandi <ChevronRight size={14}/></div>
                </div>
                <div className="flex justify-between items-center bg-white p-4 rounded-xl border border-stone-100 shadow-sm mb-3">
                    <div>
                        <div className="flex items-baseline gap-2">
                            <span className="text-3xl font-bold text-stone-900">₹2,150<span className="text-sm font-normal text-stone-500">/q</span></span>
                            <span className="text-xs text-green-700 bg-green-100 px-2 py-0.5 rounded font-medium">↑+18%</span>
                        </div>
                        <p className="text-xs text-stone-400 mt-1">Kal se zyada</p>
                    </div>
                    <div className="bg-stone-50 p-2 rounded-lg border border-stone-100 text-center">
                        <div className="flex justify-center mb-1"><TrendingUp size={16} className="text-green-600"/></div>
                        <p className="text-[10px] text-stone-500">Aaj ki Aamad</p>
                        <p className="text-xs font-bold text-stone-800">480 Ton</p>
                    </div>
                </div>

                {/* Recommendation Banner */}
                <Link to="/insights">
                    <div className="bg-green-100 rounded-xl p-4 flex items-center justify-between border border-green-200">
                        <div className="flex items-center gap-3">
                            <div className="bg-green-500 text-white p-2 rounded-full">
                                <ArrowUpRight size={24} />
                            </div>
                            <div>
                                <h4 className="font-bold text-green-900 text-sm">Hamari Salah</h4>
                                <p className="font-bold text-green-800">3 din rukna behtar rahega</p>
                                <p className="text-xs text-green-700">Andazan labh: +₹420 per quintal</p>
                            </div>
                        </div>
                        <ChevronRight size={20} className="text-green-700" />
                    </div>
                </Link>
            </div>

            {/* Top 3 Mandis */}
            <div className="px-4 pb-8">
                <div className="flex justify-between items-end mb-3">
                    <h3 className="font-bold text-stone-800">Top 3 Mandi Sujhav</h3>
                    <button className="text-xs text-green-600 font-medium">Sab dekhein</button>
                </div>
                <div className="flex gap-3 overflow-x-auto pb-2 scrollbar-hide">
                    {[
                        {name: 'Vashi', price: '2,150', diff: '+18%', best: true},
                        {name: 'Nerul', price: '1,980', diff: '+10%', best: false},
                        {name: 'Panvel', price: '1,750', diff: '+5%', best: false},
                    ].map(m => (
                        <div key={m.name} className="min-w-[120px] bg-white border border-stone-200 rounded-xl p-3 shadow-sm flex flex-col justify-between">
                            <div>
                                <h4 className="font-bold text-stone-800 text-sm mb-1">{m.name}</h4>
                                <p className="text-lg font-bold text-stone-900">₹{m.price}<span className="text-[10px] text-stone-500 font-normal">/q</span></p>
                                <p className="text-xs text-green-600 mb-2">{m.diff}</p>
                            </div>
                            {m.best && <span className="bg-green-500 text-white text-[10px] py-1 px-2 rounded-full text-center font-bold">Best Option</span>}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
''')

with open('frontend/src/pages/Insights.tsx', 'w', encoding='utf-8') as f:
    f.write('''import { Link } from 'react-router-dom';
import { ArrowLeft, Info, ArrowUp, ArrowDown } from 'lucide-react';

export default function Insights() {
    return (
        <div className="flex flex-col bg-stone-50 min-h-[calc(100vh-60px)] font-sans">
            {/* Header */}
            <div className="flex items-center p-4 bg-white border-b border-stone-200">
                <Link to="/" className="mr-3 text-stone-600"><ArrowLeft size={20} /></Link>
                <div className="flex items-center gap-2 flex-1">
                    <span className="text-2xl">🍅</span>
                    <div>
                        <h2 className="font-bold text-stone-900 leading-tight text-sm">Tamatar (Tomato)</h2>
                        <p className="text-xs text-stone-500">Cost-of-Waiting Analysis</p>
                    </div>
                </div>
                <div className="flex items-center text-xs font-medium text-stone-700 bg-stone-100 px-2 py-1 rounded">
                    <span className="text-green-600 mr-1">📍</span> Vashi Mandi ▾
                </div>
            </div>

            {/* Tabs */}
            <div className="flex bg-white border-b border-stone-200 px-4 text-xs font-medium">
                <button className="flex-1 py-3 text-stone-500 text-center">Price Forecast</button>
                <button className="flex-1 py-3 text-green-700 border-b-2 border-green-600 text-center">Cost of Waiting</button>
                <Link to="/mandis" className="flex-1 py-3 text-stone-500 text-center">Market Compare</Link>
            </div>

            <div className="p-4 bg-white">
                <div className="flex justify-between items-center mb-4">
                    <h3 className="font-bold text-stone-800 text-lg">Cost-of-Waiting Curve</h3>
                    <Info size={16} className="text-stone-400" />
                </div>
                <p className="text-xs text-stone-500 mb-6">Net expected gain vs waiting time (considering price gain, perishability loss, storage and transport cost)</p>
                
                {/* Chart Placeholder */}
                <div className="h-48 relative border-l border-b border-stone-300 ml-4 mb-6">
                    <div className="absolute top-0 left-[-24px] text-[10px] text-stone-400 -rotate-90 origin-left whitespace-nowrap">Net Gain (₹/quintal)</div>
                    <div className="absolute bottom-[-20px] w-full text-center text-[10px] text-stone-400">Days After Harvest</div>
                    
                    {/* Fake SVG Curve matching mockup */}
                    <svg className="w-full h-full overflow-visible" viewBox="0 0 100 100" preserveAspectRatio="none">
                        {/* Area */}
                        <path d="M0,80 Q20,30 42,10 T100,90 L100,100 L0,100 Z" fill="#dcfce7" opacity="0.5" />
                        <path d="M42,10 T100,90 L100,100 L42,100 Z" fill="#fee2e2" opacity="0.5" />
                        {/* Line */}
                        <path d="M0,80 Q20,30 42,10" fill="none" stroke="#16a34a" strokeWidth="2" />
                        <path d="M42,10 T100,90" fill="none" stroke="#ef4444" strokeWidth="2" />
                        
                        {/* Points */}
                        <circle cx="0" cy="80" r="2" fill="#16a34a" />
                        <circle cx="14" cy="45" r="2" fill="#16a34a" />
                        <circle cx="28" cy="20" r="2" fill="#16a34a" />
                        <circle cx="42" cy="10" r="3" fill="#16a34a" stroke="white" strokeWidth="1" />
                        <circle cx="56" cy="25" r="2" fill="#16a34a" />
                        <circle cx="70" cy="45" r="2" fill="#ef4444" />
                        <circle cx="85" cy="70" r="2" fill="#ef4444" />
                        <circle cx="100" cy="90" r="2" fill="#ef4444" />
                    </svg>

                    {/* Tooltip on peak */}
                    <div className="absolute top-[0%] left-[42%] transform -translate-x-1/2 -translate-y-full mb-2 bg-white border border-stone-200 shadow-lg rounded-lg p-2 text-center z-10">
                        <p className="text-[10px] font-bold text-stone-600">Optimal Day</p>
                        <p className="text-xs font-bold text-stone-900">Day 3</p>
                        <p className="text-sm font-bold text-green-600">₹640/q</p>
                        <div className="absolute bottom-[-5px] left-1/2 transform -translate-x-1/2 w-2 h-2 bg-white border-b border-r border-stone-200 rotate-45"></div>
                    </div>
                </div>

                {/* Best time banner */}
                <div className="bg-orange-50 border border-orange-100 rounded-lg p-3 flex justify-between items-center mb-6">
                    <div className="flex items-center gap-3">
                        <div className="text-orange-500">💡</div>
                        <div>
                            <p className="font-bold text-stone-800 text-sm">Best time to sell: Day 3</p>
                            <p className="text-xs text-stone-600">Expected net gain: ₹640 per quintal</p>
                        </div>
                    </div>
                    <ChevronRight size={16} className="text-stone-400" />
                </div>

                <h3 className="font-bold text-stone-800 text-sm mb-3">Factors Affecting Net Gain</h3>
                <div className="flex flex-col gap-3 border border-stone-200 rounded-xl p-3">
                    {[
                        {name: 'Expected Price Gain', desc: 'Increase in expected mandi price', val: '+₹820/q', up: true},
                        {name: 'Perishability Loss', desc: 'Quality loss over time', val: '-₹120/q', up: false},
                        {name: 'Storage Cost', desc: 'Handling and storage cost', val: '-₹40/q', up: false},
                        {name: 'Transport Cost', desc: 'Distance and fuel cost', val: '-₹60/q', up: false},
                        {name: 'Spoilage Risk', desc: 'Probability of unsellable produce', val: '-₹20/q', up: false},
                    ].map((f, i) => (
                        <div key={i} className={`flex items-center justify-between pb-3 ${i < 4 ? 'border-b border-stone-100' : ''}`}>
                            <div className="flex items-center gap-3">
                                <div className={`p-1 rounded-full ${f.up ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-500'}`}>
                                    {f.up ? <ArrowUp size={14} /> : <ArrowDown size={14} />}
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-stone-800 leading-tight">{f.name}</p>
                                    <p className="text-[10px] text-stone-400">{f.desc}</p>
                                </div>
                            </div>
                            <span className={`font-bold text-sm ${f.up ? 'text-green-600' : 'text-red-500'}`}>{f.val}</span>
                        </div>
                    ))}
                </div>

                <div className="bg-blue-50 text-blue-800 text-xs p-3 rounded-lg mt-4 flex items-start gap-2">
                    <Info size={16} className="shrink-0 mt-0.5" />
                    <p>Net gain peaks at Day 3. Waiting longer may lead to higher losses due to spoilage and falling prices.</p>
                </div>
            </div>
        </div>
    );
}
''')

with open('frontend/src/pages/Mandis.tsx', 'w', encoding='utf-8') as f:
    f.write('''import { Link } from 'react-router-dom';
import { ArrowLeft, MapPin } from 'lucide-react';

export default function Mandis() {
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
                    {name: 'Tamatar', emoji: '🍅', active: true},
                    {name: 'Pyaaz', emoji: '🧅', active: false},
                    {name: 'Aloo', emoji: '🥔', active: false},
                    {name: 'Kela', emoji: '🍌', active: false}
                ].map(c => (
                    <div key={c.name} className={`flex flex-col items-center min-w-[60px] pb-2 border-b-2 ${c.active ? 'border-green-600' : 'border-transparent'}`}>
                        <span className="text-2xl mb-1">{c.emoji}</span>
                        <span className={`text-[10px] font-medium ${c.active ? 'text-green-700' : 'text-stone-500'}`}>{c.name}</span>
                    </div>
                ))}
            </div>

            {/* Time toggle */}
            <div className="bg-white p-3 border-b border-stone-200">
                <div className="flex bg-stone-100 rounded-lg p-1">
                    <button className="flex-1 bg-white text-stone-800 font-bold text-xs py-2 rounded shadow-sm">Aaj</button>
                    <button className="flex-1 text-stone-500 font-medium text-xs py-2">3 Din Baad</button>
                    <button className="flex-1 text-stone-500 font-medium text-xs py-2">7 Din Baad</button>
                </div>
            </div>

            {/* Map Placeholder */}
            <div className="h-48 bg-blue-50 relative border-b border-stone-200 overflow-hidden">
                <div className="absolute inset-0 opacity-30 bg-[url('https://www.transparenttextures.com/patterns/cartographer.png')]"></div>
                {/* Vashi */}
                <div className="absolute top-[20%] left-[30%] flex flex-col items-center">
                    <div className="bg-white px-2 py-1 rounded shadow text-[10px] font-bold mb-1">Vashi Mandi<br/><span className="text-stone-500 font-normal">12 km</span></div>
                    <MapPin fill="#16a34a" color="white" size={24} />
                </div>
                {/* Nerul */}
                <div className="absolute top-[40%] right-[30%] flex flex-col items-center">
                    <div className="bg-white px-2 py-1 rounded shadow text-[10px] font-bold mb-1">Nerul Mandi<br/><span className="text-stone-500 font-normal">8 km</span></div>
                    <MapPin fill="#f97316" color="white" size={24} />
                </div>
                {/* Panvel */}
                <div className="absolute bottom-[20%] right-[15%] flex flex-col items-center">
                    <MapPin fill="#ef4444" color="white" size={24} />
                    <div className="bg-white px-2 py-1 rounded shadow text-[10px] font-bold mt-1">Panvel Mandi<br/><span className="text-stone-500 font-normal">28 km</span></div>
                </div>
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
                        {[
                            {name: 'Vashi Mandi', price: '2,150', diff: '+18%', trans: '230', net: '1,920', dist: '12 km', best: true},
                            {name: 'Nerul Mandi', price: '1,980', diff: '+10%', trans: '160', net: '1,820', dist: '8 km', best: false},
                            {name: 'Panvel Mandi', price: '1,750', diff: '+5%', trans: '140', net: '1,610', dist: '28 km', best: false},
                        ].map((m, i) => (
                            <tr key={i} className="border-b border-stone-100 last:border-none">
                                <td className="py-3 flex items-center gap-2">
                                    <div className="w-8 h-8 bg-stone-100 rounded overflow-hidden flex items-center justify-center text-lg">🍅</div>
                                    <span className="font-bold text-stone-800 leading-tight w-10">{m.name.replace(' ', '\\n')}</span>
                                </td>
                                <td className="py-3 font-bold text-sm">
                                    {m.price}
                                    <div className="text-[10px] text-green-600 font-medium">{m.diff}</div>
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
                        <h4 className="font-bold text-orange-900 text-sm">Key Insights</h4>
                    </div>
                    <ul className="list-disc pl-5 text-[11px] text-stone-700 space-y-1">
                        <li>Vashi Mandi offers the highest net return.</li>
                        <li>Nerul Mandi has lower transport cost but slightly lower price.</li>
                        <li>Consider quality and perishability for longer distances like Panvel.</li>
                    </ul>
                </div>
            </div>
        </div>
    );
}
''')
