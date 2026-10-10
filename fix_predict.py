import re

with open('frontend/src/pages/Predict.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Add useLanguage import if not present
if "from '../context/LanguageContext'" not in content:
    content = content.replace("import { useState } from 'react';", "import { useState } from 'react';\nimport { useLanguage } from '../context/LanguageContext';")

# Add the t hook
if "const { t } = useLanguage();" not in content:
    content = content.replace("export default function Predict() {", "export default function Predict() {\n  const { t } = useLanguage();")

# Add the small disclaimer line
# Original: <p className="text-sm text-gray-500 mt-1">AI-powered market predictions based on historical data.</p>
disclaimer_html = """<p className="text-sm text-gray-500 mt-1">AI-powered market predictions based on historical data.</p>
          <div className="mt-2 inline-block bg-amber-50 border border-amber-200 text-amber-700 text-xs px-2 py-1 rounded">
            <strong>Note:</strong> {t('forecast_accuracy_note', 'Predictions are most accurate for the next 7 days.')}
          </div>"""

content = content.replace('<p className="text-sm text-gray-500 mt-1">AI-powered market predictions based on historical data.</p>', disclaimer_html)

with open('frontend/src/pages/Predict.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
