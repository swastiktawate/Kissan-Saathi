import { Link } from 'react-router-dom';
import MandiTable from '../components/MandiTable';

export default function Mandis() {
    const mockMandis = [
        { horizon: 0, name: 'Kalyan', dist: 50, price: 2100, net: 1950, isBest: true },
        { horizon: 0, name: 'Vashi', dist: 10, price: 1900, net: 1800, isBest: false },
        { horizon: 3, name: 'Kalyan', dist: 50, price: 2150, net: 1980, isBest: true },
        { horizon: 3, name: 'Vashi', dist: 10, price: 1950, net: 1820, isBest: false },
        { horizon: 7, name: 'Kalyan', dist: 50, price: 2200, net: 2000, isBest: true },
        { horizon: 7, name: 'Vashi', dist: 10, price: 1850, net: 1700, isBest: false },
    ];

    return (
        <div className="max-w-[360px] mx-auto min-h-screen flex flex-col p-4">
            <div className="flex gap-2 mb-4 text-sm font-bold items-center">
                <Link to="/" className="text-blue-600">&larr; Back</Link>
                <span>Market Compare</span>
            </div>
            
            <MandiTable data={mockMandis} />
        </div>
    );
}
