import { useState } from 'react';
import PredictionChart from '../components/PredictionChart';
import { Loader2 } from 'lucide-react';

export default function Predict() {
  const [commodity, setCommodity] = useState('Tomato');
  const [market, setMarket] = useState('APMC Mumbai');
  const [variety, setVariety] = useState('Other');
  
  // Default to today in YYYY-MM-DD
  const today = new Date().toISOString().split('T')[0];
  const [startDate, setStartDate] = useState(today);

  const [forecastData, setForecastData] = useState<any[] | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setForecastData(null);

    const payload = {
      commodity,
      market,
      variety,
      district: 'Mumbai', // defaulting to Mumbai as requested or inferred from market
      start_date: startDate
    };

    try {
      const res = await fetch('http://localhost:8000/api/v1/forecast/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        throw new Error('Failed to connect to the prediction engine. Is the backend running?');
      }

      const data = await res.json();
      if (data.forecast && data.forecast.length > 0) {
        setForecastData(data.forecast);
      } else {
        setError('No forecast data returned.');
      }
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-gray-50 min-h-screen p-4 pb-24">
      <div className="mb-6 mt-2">
        <h1 className="text-2xl font-bold text-gray-900">1-Year Price Forecast</h1>
        <p className="text-sm text-gray-500 mt-1">AI-powered market predictions based on historical data.</p>
      </div>

      <div className="bg-white shadow-md rounded-xl p-5 border border-green-100">
        <form onSubmit={handlePredict} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Commodity</label>
            <select 
              className="w-full border border-gray-300 rounded-lg p-2.5 bg-white focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none transition-all"
              value={commodity}
              onChange={(e) => setCommodity(e.target.value)}
            >
              <option value="Tomato">Tomato</option>
              <option value="Onion">Onion</option>
              <option value="Potato">Potato</option>
              <option value="Banana">Banana</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Market</label>
            <select 
              className="w-full border border-gray-300 rounded-lg p-2.5 bg-white focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none transition-all"
              value={market}
              onChange={(e) => setMarket(e.target.value)}
            >
              <option value="APMC Mumbai">APMC Mumbai</option>
              <option value="Mumbai-Onion & Potato Market">Mumbai-Onion & Potato Market</option>
              <option value="Pune">Pune</option>
              <option value="Vashi">Vashi</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Variety</label>
            <select 
              className="w-full border border-gray-300 rounded-lg p-2.5 bg-white focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none transition-all"
              value={variety}
              onChange={(e) => setVariety(e.target.value)}
            >
              <option value="Other">Other</option>
              <option value="Local">Local</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
            <input 
              type="date"
              className="w-full border border-gray-300 rounded-lg p-2.5 bg-white focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none transition-all"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              required
            />
          </div>

          <button 
            type="submit" 
            disabled={isLoading}
            className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-4 rounded-lg shadow-md hover:shadow-lg transition-all flex justify-center items-center mt-2 disabled:opacity-70 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <>
                <Loader2 size={20} className="animate-spin mr-2" />
                Generating...
              </>
            ) : (
              'Generate 1-Year Forecast'
            )}
          </button>
        </form>
      </div>

      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-600 text-sm">
          {error}
        </div>
      )}

      {forecastData && (
        <PredictionChart data={forecastData} />
      )}
    </div>
  );
}
