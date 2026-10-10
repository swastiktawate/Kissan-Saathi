import re

with open('frontend/src/components/PlantingInsightCard.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("import React from 'react';\n", "")
content = content.replace("import { PlantingInsight } from '../utils/plantingInsights';", "import type { PlantingInsight } from '../utils/plantingInsights';")

with open('frontend/src/components/PlantingInsightCard.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

with open('frontend/src/pages/Predict.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("import { generatePlantingInsight, PlantingInsight } from '../utils/plantingInsights';", "import { generatePlantingInsight } from '../utils/plantingInsights';\nimport type { PlantingInsight } from '../utils/plantingInsights';")

with open('frontend/src/pages/Predict.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
