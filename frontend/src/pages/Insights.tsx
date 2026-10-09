import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Info, ChevronRight } from 'lucide-react';
import WhatIfSliders from '../components/WhatIfSliders';
import FairPriceMeter from '../components/FairPriceMeter';
import RegretView from '../components/RegretView';
import FarmerPooling from '../components/FarmerPooling';
import NewsFeed from '../components/NewsFeed';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const costOfWaitingData = [
  { day: 0, gain: 0 },
  { day: 1, gain: 400 },
  { day: 2, gain: 1100 },
  { day: 3, gain: 1640 },
  { day: 4, gain: 1200 },
  { day: 5, gain: 500 },
  { day: 6, gain: -200 },
  { day: 7, gain: -500 }
];

const priceForecastData = [
  { date: '10 Oct', median: 2150, band: [2050, 2250] },
  { date: '11 Oct', median: 2200, band: [2080, 2320] },
  { date: '12 Oct', median: 2450, band: [2250, 2650] },
  { date: '13 Oct', median: 2600, band: [2300, 2900] },
  { date: '14 Oct', median: 2800, band: [2400, 3200] },
  { date: '15 Oct', median: 2750, band: [2350, 3150] },
  { date: '16 Oct', median: 2700, band: [2200, 3200] }
];

export default function Insights() {
    const [activeTab, setActiveTab] = useState('Cost of Waiting');

    return (
        <div className="flex flex-col bg-stone-50 min-h-[calc(100vh-60px)] font-sans pb-8">
            {/* Header */}
            <div className="flex items-center p-4 bg-white border-b border-stone-200">
                <Link to="/" className="mr-3 text-stone-600"><ArrowLeft size={20} /></Link>
                <div className="flex items-center gap-2 flex-1">
                    <span className="text-2xl">🍅</span>
                    <div>
                        <h2 className="font-bold text-stone-900 leading-tight text-sm">Tamatar (Tomato)</h2>
                        <p className="text-xs text-stone-500">Analytics & Forecasts</p>
                    </div>
                </div>
                <div className="flex items-center text-xs font-medium text-stone-700 bg-stone-100 px-2 py-1 rounded">
                    <span className="text-green-600 mr-1">📍</span> Vashi Mandi ▾
                </div>
            </div>

            {/* Tabs */}
            <div className="flex bg-white border-b border-stone-200 px-2 text-xs font-medium overflow-x-auto scrollbar-hide">
                <button 
                    onClick={() => setActiveTab('Price Forecast')}
                    className={`shrink-0 px-3 py-3 text-center transition-colors ${activeTab === 'Price Forecast' ? 'text-green-700 border-b-2 border-green-600' : 'text-stone-500'}`}
                >
                    Price Forecast
                </button>
                <button 
                    onClick={() => setActiveTab('Cost of Waiting')}
                    className={`shrink-0 px-3 py-3 text-center transition-colors ${activeTab === 'Cost of Waiting' ? 'text-green-700 border-b-2 border-green-600' : 'text-stone-500'}`}
                >
                    Cost of Waiting
                </button>
                <button 
                    onClick={() => setActiveTab('News')}
                    className={`shrink-0 px-3 py-3 text-center transition-colors ${activeTab === 'News' ? 'text-green-700 border-b-2 border-green-600' : 'text-stone-500'}`}
                >
                    News & Policy
                </button>
                <Link to="/mandis" className="shrink-0 px-3 py-3 text-stone-500 text-center">Compare</Link>
            </div>

            {activeTab === 'Cost of Waiting' && (
                <div className="p-4 bg-white">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="font-bold text-stone-800 text-lg">Cost-of-Waiting Curve</h3>
                        <Info size={16} className="text-stone-400" />
                    </div>
                    <p className="text-xs text-stone-500 mb-6">Net expected gain vs waiting time (considering price gain, perishability loss, storage and transport cost)</p>
                    
                <div className="h-56 ml-[-15px] mb-6">
                    <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={costOfWaitingData} margin={{ top: 20, right: 20, left: 0, bottom: 0 }}>
                            <defs>
                                <linearGradient id="colorGain" x1="0" y1="0" x2="1" y2="0">
                                    <stop offset="42%" stopColor="#16a34a" stopOpacity={0.8}/>
                                    <stop offset="42%" stopColor="#ef4444" stopOpacity={0.8}/>
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
                            <XAxis 
                                dataKey="day" 
                                tickFormatter={(val) => `Day ${val}`} 
                                axisLine={false} 
                                tickLine={false} 
                                tick={{ fontSize: 10, fill: '#78716c' }} 
                            />
                            <YAxis 
                                axisLine={false} 
                                tickLine={false} 
                                tick={{ fontSize: 10, fill: '#78716c' }} 
                                tickFormatter={(val) => `₹${val}`}
                            />
                            <Tooltip 
                                contentStyle={{ borderRadius: '8px', border: '1px solid #e7e5e4', fontSize: '12px', fontWeight: 'bold' }}
                                formatter={(value: any) => [`₹${value}/q`, 'Net Gain']}
                                labelFormatter={(label) => `Day ${label}`}
                            />
                            <Area 
                                type="monotone" 
                                dataKey="gain" 
                                stroke="url(#colorGain)" 
                                fill="url(#colorGain)" 
                                strokeWidth={3} 
                                activeDot={{ r: 6, fill: '#16a34a', stroke: 'white', strokeWidth: 2 }}
                            />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>

                    {/* Best time banner */}
                    <div className="bg-orange-50 border border-orange-100 rounded-lg p-3 flex justify-between items-center mb-6">
                        <div className="flex items-center gap-3">
                            <div className="text-orange-500">💡</div>
                            <div>
                                <p className="font-bold text-stone-800 text-sm">Best time to sell: Day 3</p>
                                <p className="text-xs text-stone-600">Expected net gain: ₹1,640 per quintal</p>
                            </div>
                        </div>
                        <ChevronRight size={16} className="text-stone-400" />
                    </div>

                    {/* Sliders */}
                    <WhatIfSliders />
                    
                    <div className="mt-8">
                        <FairPriceMeter crop="tomato" mandi="vashi" />
                        <RegretView crop="tomato" mandi="vashi" />
                        <FarmerPooling />
                    </div>
                </div>
            )}

            {activeTab === 'Price Forecast' && (
                <div className="p-4 bg-white">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="font-bold text-stone-800 text-lg">Price Forecast</h3>
                        <Info size={16} className="text-stone-400" />
                    </div>
                    <p className="text-xs text-stone-500 mb-6">Conformal AI predictions for Tamatar at Vashi Mandi</p>
                    
                    <div className="h-56 ml-[-15px] mb-6">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={priceForecastData} margin={{ top: 20, right: 20, left: 0, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
                                <XAxis 
                                    dataKey="date" 
                                    axisLine={false} 
                                    tickLine={false} 
                                    tick={{ fontSize: 10, fill: '#78716c' }} 
                                />
                                <YAxis 
                                    domain={['dataMin - 100', 'dataMax + 100']}
                                    axisLine={false} 
                                    tickLine={false} 
                                    tick={{ fontSize: 10, fill: '#78716c' }} 
                                    tickFormatter={(val) => `₹${val}`}
                                />
                                <Tooltip 
                                    contentStyle={{ borderRadius: '8px', border: '1px solid #e7e5e4', fontSize: '12px', fontWeight: 'bold' }}
                                    formatter={(value: any, name: any) => [`₹${value}/q`, name]}
                                    labelFormatter={(label) => `${label}`}
                                />
                                <Area 
                                    type="monotone" 
                                    dataKey="band" 
                                    stroke="none" 
                                    fill="#dcfce7" 
                                    opacity={0.6}
                                />
                                <Area 
                                    type="monotone" 
                                    dataKey="median" 
                                    stroke="#16a34a" 
                                    fill="none" 
                                    strokeWidth={3} 
                                    strokeDasharray="4 2"
                                    activeDot={{ r: 6, fill: '#16a34a', stroke: 'white', strokeWidth: 2 }}
                                />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>

                    <div className="bg-stone-50 rounded-lg p-4 mb-4">
                        <div className="flex justify-between items-center mb-2">
                            <span className="text-sm font-bold text-stone-700">Trend Signal</span>
                            <span className="bg-green-100 text-green-700 text-xs px-2 py-1 rounded-full font-bold">Strong Buy</span>
                        </div>
                        <p className="text-xs text-stone-600">Prices are expected to rise significantly over the next week due to delayed monsoon arrivals in the northern supply zones.</p>
                    </div>
                </div>
            )}

            {activeTab === 'News' && (
                <div className="p-4 bg-stone-50">
                    <NewsFeed />
                </div>
            )}
        </div>
    );
}
