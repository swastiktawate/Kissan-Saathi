export const USE_MOCKS = import.meta.env?.VITE_USE_MOCKS === 'true' || import.meta.env?.MODE === 'test';

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

export async function runWhatIf(scenario: any) {
    if (USE_MOCKS) {
        return {
            baseline: { action: 'SELL_NOW', expected_gain: 100 },
            scenario: { action: 'ANOTHER_MANDI', expected_gain: 100 - (scenario.transport_multiplier - 1)*100 },
            delta: { action_change: true, nr_change: -((scenario.transport_multiplier - 1)*100) }
        };
    }
    const res = await fetch('http://localhost:8000/api/v1/whatif', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ base: {}, scenario })
    });
    return res.json();
}
