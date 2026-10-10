import re

with open('frontend/src/pages/Predict.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports
imports = """import { useState } from 'react';
import { useLanguage } from '../context/LanguageContext';
import PredictionChart from '../components/PredictionChart';
import { Loader2 } from 'lucide-react';
import PlantingInsightCard from '../components/PlantingInsightCard';
import { generatePlantingInsight, PlantingInsight } from '../utils/plantingInsights';"""

content = re.sub(r'import { useState }.*?from \'lucide-react\';', imports, content, flags=re.DOTALL)

# Add state
state_line = "const [forecastData, setForecastData] = useState<any[] | null>(null);\n  const [insight, setInsight] = useState<PlantingInsight | null>(null);"
content = content.replace("const [forecastData, setForecastData] = useState<any[] | null>(null);", state_line)

# Handle error reset
content = content.replace("setForecastData(null);", "setForecastData(null);\n    setInsight(null);")

# Update prediction logic
prediction_success = """      if (data.forecast && data.forecast.length > 0) {
        setForecastData(data.forecast);
        setInsight(generatePlantingInsight(data.forecast, commodity, startDate));
      }"""
content = content.replace("""      if (data.forecast && data.forecast.length > 0) {
        setForecastData(data.forecast);
      }""", prediction_success)

# Add component to render tree
render_chart = """      {forecastData && (
        <>
          <PredictionChart data={forecastData} />
          <PlantingInsightCard insight={insight} />
        </>
      )}"""
content = content.replace("""      {forecastData && (
        <PredictionChart data={forecastData} />
      )}""", render_chart)

with open('frontend/src/pages/Predict.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
