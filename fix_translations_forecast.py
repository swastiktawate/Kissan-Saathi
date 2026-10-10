import json
with open('frontend/src/i18n/translations.ts', 'r', encoding='utf-8') as f:
    text = f.read()

# English
text = text.replace('hero_subtitle: "Better decisions for your crops, with data.",', 'hero_subtitle: "Better decisions for your crops, with data.",\n        forecast_accuracy_note: "Predictions are most accurate for the next 7 days.",')

# Hindi
text = text.replace('hero_subtitle: "आपकी फसल के लिए बेहतर फैसले, डेटा के साथ।",', 'hero_subtitle: "आपकी फसल के लिए बेहतर फैसले, डेटा के साथ।",\n        forecast_accuracy_note: "अगले 7 दिनों के लिए भविष्यवाणियाँ सबसे सटीक हैं।",')

# Marathi
text = text.replace('hero_subtitle: "तुमच्या पिकांसाठी उत्तम निर्णय, डेटा सोबत.",', 'hero_subtitle: "तुमच्या पिकांसाठी उत्तम निर्णय, डेटा सोबत.",\n        forecast_accuracy_note: "पुढील ७ दिवसांचे अंदाज सर्वात अचूक असतात.",')

# Haryanvi
text = text.replace('hero_subtitle: "आपकी फसल खातिर बढ़िया फैसले, डेटा गैल।",', 'hero_subtitle: "आपकी फसल खातिर बढ़िया फैसले, डेटा गैल।",\n        forecast_accuracy_note: "अगले 7 दिनां की भविष्यवाणी सबतै बढ़िया अर सही होवै सै।",')

# Punjabi
text = text.replace('hero_subtitle: "ਤੁਹਾਡੀਆਂ ਫਸਲਾਂ ਲਈ ਬਿਹਤਰ ਫੈਸਲੇ, ਡੇਟਾ ਦੇ ਨਾਲ।",', 'hero_subtitle: "ਤੁਹਾਡੀਆਂ ਫਸਲਾਂ ਲਈ ਬਿਹਤਰ ਫੈਸਲੇ, ਡੇਟਾ ਦੇ ਨਾਲ।",\n        forecast_accuracy_note: "ਅਗਲੇ 7 ਦਿਨਾਂ ਦੀਆਂ ਭਵਿੱਖਬਾਣੀਆਂ ਸਭ ਤੋਂ ਸਹੀ ਹੁੰਦੀਆਂ ਹਨ।",')

with open('frontend/src/i18n/translations.ts', 'w', encoding='utf-8') as f:
    f.write(text)
