import re

with open('frontend/src/components/PlantingInsightCard.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("t('smart_insight_title', '💡 Smart Planting Insight')", "t('smart_insight_title')")

with open('frontend/src/components/PlantingInsightCard.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

with open('frontend/src/i18n/translations.ts', 'r', encoding='utf-8') as f:
    text = f.read()

# Add smart_insight_title to translations.ts
text = text.replace('forecast_accuracy_note: "Predictions are most accurate for the next 7 days.",', 'forecast_accuracy_note: "Predictions are most accurate for the next 7 days.",\n        smart_insight_title: "💡 Smart Planting Insight",')
text = text.replace('forecast_accuracy_note: "अगले 7 दिनों के लिए भविष्यवाणियाँ सबसे सटीक हैं।",', 'forecast_accuracy_note: "अगले 7 दिनों के लिए भविष्यवाणियाँ सबसे सटीक हैं।",\n        smart_insight_title: "💡 स्मार्ट रोपण सलाह",')
text = text.replace('forecast_accuracy_note: "पुढील ७ दिवसांचे अंदाज सर्वात अचूक असतात.",', 'forecast_accuracy_note: "पुढील ७ दिवसांचे अंदाज सर्वात अचूक असतात.",\n        smart_insight_title: "💡 स्मार्ट लागवड सल्ला",')
text = text.replace('forecast_accuracy_note: "अगले 7 दिनां की भविष्यवाणी सबतै बढ़िया अर सही होवै सै।",', 'forecast_accuracy_note: "अगले 7 दिनां की भविष्यवाणी सबतै बढ़िया अर सही होवै सै।",\n        smart_insight_title: "💡 समझदार बिजाई सलाह",')
text = text.replace('forecast_accuracy_note: "ਅਗਲੇ 7 ਦਿਨਾਂ ਦੀਆਂ ਭਵਿੱਖਬਾਣੀਆਂ ਸਭ ਤੋਂ ਸਹੀ ਹੁੰਦੀਆਂ ਹਨ।",', 'forecast_accuracy_note: "ਅਗਲੇ 7 ਦਿਨਾਂ ਦੀਆਂ ਭਵਿੱਖਬਾਣੀਆਂ ਸਭ ਤੋਂ ਸਹੀ ਹੁੰਦੀਆਂ ਹਨ।",\n        smart_insight_title: "💡 ਸਮਾਰਟ ਬਿਜਾਈ ਸਲਾਹ",')

with open('frontend/src/i18n/translations.ts', 'w', encoding='utf-8') as f:
    f.write(text)
