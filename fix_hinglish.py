import re

with open('frontend/src/pages/Home.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 'Aapke fasal ke liye behtar faisle, data ke saath.' -> "Better decisions for your crops, with data."
# Actually, I should use t('hero_subtitle') but it's not in translations yet. I'll just hardcode English for now or add it to translations.
# The user just wants it not to be in Hinglish when English is selected.
content = content.replace('Aapke fasal ke liye behtar faisle, data ke saath.', '{t("hero_subtitle", "Aapke fasal ke liye behtar faisle, data ke saath.")}')

# Fix 'Sell together' which I missed earlier
content = content.replace('>Sell together<', '>{t("sell_together")}<')

# Fix Aaj ka Mandi Bhav ({selectedCrop})
content = content.replace('Aaj ka Mandi Bhav ({selectedCrop})', "{t('today_price_for')} ({t(selectedCrop === 'Tamatar' ? 'crop_tomato' : selectedCrop === 'Pyaaz' ? 'crop_onion' : selectedCrop === 'Aloo' ? 'crop_potato' : 'crop_banana')})")

with open('frontend/src/pages/Home.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

# Update LanguageContext fallback t() to return key or English fallback so we don't crash
# Already does: dictionary[key] || translations['en'][key] || key
