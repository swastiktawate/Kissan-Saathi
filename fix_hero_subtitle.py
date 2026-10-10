import json
with open('frontend/src/i18n/translations.ts', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('best_option: "Best Option",', 'best_option: "Best Option",\n        hero_subtitle: "Better decisions for your crops, with data.",')
text = text.replace('best_option: "सबसे अच्छा विकल्प",', 'best_option: "सबसे अच्छा विकल्प",\n        hero_subtitle: "आपकी फसल के लिए बेहतर फैसले, डेटा के साथ।",')
text = text.replace('best_option: "उत्तम पर्याय",', 'best_option: "उत्तम पर्याय",\n        hero_subtitle: "तुमच्या पिकांसाठी उत्तम निर्णय, डेटा सोबत.",')
text = text.replace('best_option: "कसूता विकल्प",', 'best_option: "कसूता विकल्प",\n        hero_subtitle: "आपकी फसल खातिर बढ़िया फैसले, डेटा गैल।",')
text = text.replace('best_option: "ਸਭ ਤੋਂ ਵਧੀਆ ਵਿਕਲਪ",', 'best_option: "ਸਭ ਤੋਂ ਵਧੀਆ ਵਿਕਲਪ",\n        hero_subtitle: "ਤੁਹਾਡੀਆਂ ਫਸਲਾਂ ਲਈ ਬਿਹਤਰ ਫੈਸਲੇ, ਡੇਟਾ ਦੇ ਨਾਲ।",')

with open('frontend/src/i18n/translations.ts', 'w', encoding='utf-8') as f:
    f.write(text)
