import { Link } from 'react-router-dom';
import ForecastChart from '../components/ForecastChart';

export default function Detail() {
    const mockForecast = [
        { day: 'Mon', observed: 2100, band: [2100, 2100] },
        { day: 'Tue', observed: 2050, band: [2050, 2050] },
        { day: 'Wed', observed: 2150, band: [2150, 2150] },
        { day: 'Thu', forecast: 2200, band: [2100, 2300] },
        { day: 'Fri', forecast: 2250, band: [2120, 2400] },
        { day: 'Sat', forecast: 2180, band: [2000, 2350] },
    ];

    return (
        <div className="max-w-[360px] mx-auto min-h-screen flex flex-col p-4">
            <div className="flex gap-2 mb-4 text-sm font-bold items-center">
                <Link to="/" className="text-blue-600">&larr; Back</Link>
                <span>Insight Details</span>
            </div>
            
            <h2 className="text-xl font-bold mb-4">Tomato in Vashi</h2>
            <ForecastChart data={mockForecast} />
            
            <div className="bg-white p-4 border border-stone-200 rounded-sm shadow-sm text-sm">
                <h3 className="font-bold mb-2">Cost of Waiting</h3>
                <p>Chart coming in T20</p>
            </div>
        </div>
    );
}
