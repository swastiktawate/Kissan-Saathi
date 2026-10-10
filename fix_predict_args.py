import re

with open('frontend/src/pages/Predict.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("{t('forecast_accuracy_note', 'Predictions are most accurate for the next 7 days.')}", "{t('forecast_accuracy_note')}")

with open('frontend/src/pages/Predict.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
