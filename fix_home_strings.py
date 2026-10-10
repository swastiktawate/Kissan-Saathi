import re

with open('frontend/src/pages/Home.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the global mockData
content = re.sub(r'const mockData: Record<string, any> = \{.*?\n\};\n', '', content, flags=re.DOTALL)

# Insert the dynamic mockData inside Home()
new_mockData = """
    const mockData: Record<string, any> = {
        'Tamatar': {
            price: '2,150', trend: '+5.2%', action: t('action_wait_3_days'), 
            reason: t('reason_rain'),
            mandis: [
                { name: 'Kalyan', price: '₹2,350', diff: '+₹200', tag: t('best_option') },
                { name: 'Vashi', price: '₹2,150', diff: '-', tag: '' },
                { name: 'Pune', price: '₹1,900', diff: '-₹250', tag: '' }
            ]
        },
        'Pyaaz': {
            price: '3,200', trend: '-1.5%', action: t('action_sell_now'),
            reason: t('reason_export_ban'),
            mandis: [
                { name: 'Nashik', price: '₹3,400', diff: '+₹200', tag: t('best_option') },
                { name: 'Pune', price: '₹3,200', diff: '-', tag: '' },
                { name: 'Vashi', price: '₹3,050', diff: '-₹150', tag: '' }
            ]
        },
        'Aloo': {
            price: '1,450', trend: '+2.1%', action: t('action_sell_today'),
            reason: t('reason_aloo'),
            mandis: [
                { name: 'Pune', price: '₹1,550', diff: '+₹100', tag: t('best_option') },
                { name: 'Kalyan', price: '₹1,450', diff: '-', tag: '' }
            ]
        },
        'Kela': {
            price: '1,800', trend: '+0.5%', action: t('action_sell_today'),
            reason: t('reason_kela'),
            mandis: [
                { name: 'Vashi', price: '₹1,900', diff: '+₹100', tag: t('best_option') },
                { name: 'Kalyan', price: '₹1,800', diff: '-', tag: '' }
            ]
        }
    };
"""

content = content.replace("const { t } = useLanguage();", "const { t } = useLanguage();" + new_mockData)

# Translate the button text map
content = content.replace('<span className="text-xs font-medium">{crop}</span>', '<span className="text-xs font-medium">{t(crop === "Tamatar" ? "crop_tomato" : crop === "Pyaaz" ? "crop_onion" : crop === "Aloo" ? "crop_potato" : "crop_banana")}</span>')

# Translate Aaj ka Mandi Bhav
content = content.replace('>{t(\'aaj_ka_bhav\')} ({selectedCrop})<', '>{t(\'today_price_for\')} ({t(selectedCrop === "Tamatar" ? "crop_tomato" : selectedCrop === "Pyaaz" ? "crop_onion" : selectedCrop === "Aloo" ? "crop_potato" : "crop_banana")})<')

# Translate Behtar Mandi Vikalp
content = content.replace('>Behtar Mandi Vikalp<', '>{t(\'better_mandi_options\')}<')

# Translate Sab dekhein
content = content.replace('>Sab dekhein<', '>{t(\'see_all\')}<')

# Translate 35 km door
content = content.replace('35 km door', '35 {t(\'km_away\')}')

with open('frontend/src/pages/Home.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
