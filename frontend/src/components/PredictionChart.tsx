import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from 'recharts';

interface DataPoint {
  date: string;
  predicted_price: number;
}

interface PredictionChartProps {
  data: DataPoint[];
}

export default function PredictionChart({ data }: PredictionChartProps) {
  // Format dates for X-Axis (e.g., '2026-10-10' -> 'Oct 26')
  const formatXAxis = (tickItem: string) => {
    const d = new Date(tickItem);
    return d.toLocaleDateString('en-US', { month: 'short', year: '2-digit' });
  };

  // Format price for Tooltip and Y-Axis
  const formatPrice = (value: number) => `₹${value.toLocaleString('en-IN')}`;

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const d = new Date(label);
      const formattedDate = d.toLocaleDateString('en-US', { day: 'numeric', month: 'long', year: 'numeric' });
      return (
        <div className="bg-white p-3 border border-green-100 shadow-lg rounded-lg text-sm">
          <p className="font-semibold text-gray-800">{formattedDate}</p>
          <p className="text-green-600 font-bold mt-1">
            Predicted: {formatPrice(payload[0].value)}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full mt-6 bg-white shadow-md rounded-xl p-4 border border-green-100">
      <h3 className="text-lg font-bold text-gray-800 mb-4">Price Trend</h3>
      <div className="h-[300px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
            <XAxis 
              dataKey="date" 
              tickFormatter={formatXAxis} 
              tick={{ fill: '#6b7280', fontSize: 12 }} 
              tickMargin={10}
              minTickGap={30}
              axisLine={false}
              tickLine={false}
            />
            <YAxis 
              tickFormatter={formatPrice} 
              tick={{ fill: '#6b7280', fontSize: 12 }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip content={<CustomTooltip />} />
            <Line 
              type="monotone" 
              dataKey="predicted_price" 
              stroke="#16a34a" 
              strokeWidth={3} 
              dot={false} 
              activeDot={{ r: 6, fill: '#16a34a', stroke: '#fff', strokeWidth: 2 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
