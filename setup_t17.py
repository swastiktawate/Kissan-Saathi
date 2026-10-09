import os
import json

os.makedirs('frontend/src/api', exist_ok=True)
os.makedirs('frontend/src/i18n', exist_ok=True)

with open('frontend/src/i18n/en.json', 'w') as f:
    json.dump({
        "greeting": "Hello, Farmer",
        "home_mandi": "Your Home Mandi",
        "my_crops": "My crops",
        "today_price": "Today's Price",
        "top_mandis": "Top Recommendations",
        "INSUFFICIENT_DATA": "Insufficient Data",
        "SELL_NOW": "Sell Now",
        "ANOTHER_MANDI": "Sell at another Mandi",
        "WAIT_N_DAYS": "Wait",
        "SPLIT_SALE": "Split Sale",
        "action": "Action",
        "expected_gain": "Expected Gain (Rs/q)",
        "confidence": "Confidence",
        "trust": "Trust Score",
        "clear": "Clear",
        "moderate": "Moderate",
        "low": "Low",
        "high": "High",
        "medium": "Medium",
        "caution": "Caution: Data trust is Medium. Estimates may have higher uncertainty.",
        "insufficient_reasons": "Trust score is Insufficient. We cannot confidently recommend an action.",
        "settings": "Settings",
        "quantity": "Quantity (Quintals)",
        "horizon": "Horizon (Days)",
        "risk_setting": "Risk Setting",
        "cautious": "Cautious",
        "balanced": "Balanced",
        "aggressive": "Aggressive",
        "save": "Save"
    }, f, indent=2)

with open('frontend/src/api/client.ts', 'w') as f:
    f.write('''export const USE_MOCKS = import.meta.env.VITE_USE_MOCKS === 'true';

export async function fetchRecommendation(params: any) {
    if (USE_MOCKS) {
        return {
            meta: { data_mode: "auto", trust: "High" },
            action: "ANOTHER_MANDI",
            expected_gain_per_q: 75.0,
            reasons: ["Selling today at Kalyan yields higher return."],
            drivers: { base_price: 2100, spoilage_cost: -15, transport: -100 }
        };
    }
    const res = await fetch('http://localhost:8000/api/v1/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params)
    });
    return res.json();
}
''')

with open('frontend/tailwind.config.js', 'w') as f:
    f.write('''/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        canvas: '#F7F5F0',
        textMain: 'rgb(28 25 23)', // stone-900
        accent: 'rgb(191 219 254)', // blue-200
      }
    },
  },
  plugins: [],
}
''')

with open('frontend/src/index.css', 'w') as f:
    f.write('''@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  background-color: theme('colors.canvas');
  color: theme('colors.textMain');
  margin: 0;
  font-family: sans-serif;
}
''')
