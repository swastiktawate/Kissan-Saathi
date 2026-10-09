# Kisan Saathi (किसान साथी)

An autonomous AI agent and decision intelligence platform for Indian farmers, evaluating multiple Mandis (markets) to compute true net-return gains by factoring in dynamic transport costs, transit spoilage, holding risks, and weather forecasts.

Built for the Google DeepMind Advanced Agentic Coding Hackathon (v0.1-hackathon).

## Prerequisites
- Node.js (v18+)
- Python (3.11 explicitly required by PRD)
- DuckDB
- A `.env` file in the root directory. 

### `.env` Setup
Create a `.env` file at the root:
```env
GEMINI_API_KEY=your_gemini_key
DATAGOV_API_KEY=your_datagov_key
LLM_PROVIDER=gemini # or "rule_based" for offline/fallback
DATA_MODE=auto # "auto", "sample", or "synthetic"
```

## Running the Application

1. **Setup Environment**:
```bash
make setup
```
*(On Windows without Make, run: `py -3.11 -m venv venv`, `venv/Scripts/pip install -r backend/requirements.txt`, and `cd frontend && npm install`)*

2. **Seed the Database**:
```bash
make seed
```
*(On Windows: `venv/Scripts/python backend/scripts/init_db.py` and `venv/Scripts/python backend/scripts/ingest.py`)*

3. **Run the Backend API**:
```bash
make run-api
```
*(On Windows: `venv/Scripts/uvicorn backend.app.main:app --reload`)*

4. **Run the Frontend App**:
```bash
make run-web
```
*(On Windows: `cd frontend && npm run dev`)*

## Status Matrix (PRD §10.1)

| Subsystem | Target API / Logic | Current MVP Status |
| :--- | :--- | :--- |
| **Market Data** | Data.gov.in / CEDA | 🟡 Mocked / Synthetic Fallback (Data.gov schemas mapped) |
| **Transport / Routing** | OSRM | 🟢 Integrated (Live HTTP calls via `httpx` with haversine fallback) |
| **Weather** | Open-Meteo | 🟡 Mocked (Rain multipliers built into Net-Return logic) |
| **Language Translation** | Bhashini / Sarvam | 🟡 Mocked (Offline i18n JSON packs via React Context) |
| **Generative AI** | Gemini 1.5 Flash | 🟢 Integrated (LangChain/LLM abstractions with strict Numeric Guardrails) |
| **Pricing Forecasts** | Prophet / AutoARIMA | 🟡 Baseline (EWMA + Damped trend implemented) |

## Data Attributions
- **Market Prices**: Ministry of Agriculture and Farmers Welfare (data.gov.in)
- **Routing**: Open Source Routing Machine (OSRM) 
- **Weather**: Open-Meteo API (Fallback)

## 4-Minute Demo Script
**0:00 - 0:30 | The Farmer's Dilemma**
* "Hello judges! I'm a farmer in Maharashtra. I just harvested 50 quintals of tomatoes. Should I sell today at my local Vashi mandi, or wait 3 days and drive to Kalyan?"

**0:30 - 1:30 | The Recommendation Engine**
* Open the app. The UI immediately runs the net-return scenario.
* Point out the "Top Recommendation" card. It recommends "Sell at another Mandi" (Kalyan).
* Highlight the "Expected Gain": This isn't just a higher price. It deducts OSRM transport costs and transit spoilage!

**1:30 - 2:30 | Transparency & Risk**
* Click "About Data". Show the "Trust Score" (mapped to freshness and completeness).
* Navigate to the "Insights" tab. 
* Show the interactive What-If sliders. "What if transport costs spike by 30%?" (Slide the bar, watch the delta drop). 
* Expand the "Risk Flags" chip to show the Rain Spoilage warning.

**2:30 - 3:30 | The AI Assistant Guardrails**
* Navigate to the Chat tab. Speak or type: "Should I wait 7 days?"
* Show the `tools_used` chips. The LLM isn't guessing; it's invoking our exact calculation modules.
* **Adversarial Test**: Explain our Numeric Consistency Guardrail. If the LLM hallucinates a price of "99999", our strict regex checker blocks the payload and overwrites it.

**3:30 - 4:00 | Offline Mode & Backtest**
* Turn off Wi-Fi. Refresh the PWA. 
* The offline banner appears! We can still read our last recommendation.
* Conclude with the Backtest Engine tab showing the strategy's mean gain over the last 180 days. 

## Truthfulness Caveats
> **NOTE:** The current system utilizes *Synthetic Data* generated for demonstration. Recommendations, while mathematically correct based on PRD formulas, are using uncalibrated baselines and should be treated as illustrative until live data.gov.in pipelines are fully seeded. Live policy alerts are simulated.
