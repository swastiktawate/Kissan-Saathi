import re

with open('frontend/src/pages/Home.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Strip out the current mockData entirely.
content = re.sub(r'const mockData: Record<string, any> = \{.*?\n    \};\n', '', content, flags=re.DOTALL)

# Re-inject it properly.
new_mockData = """
    const mockData: Record<string, any> = {
        'Tamatar': {
            price: '2,150', trend: '+5.2%', action: t('action_wait_3_days'), 
            reason: t('reason_rain'),
            mandis: [
                { name: 'Kalyan', price: '\u20b92,350', diff: '+\u20b9200', tag: t('best_option') },
                { name: 'Vashi', price: '\u20b92,150', diff: '-', tag: '' },
                { name: 'Pune', price: '\u20b91,900', diff: '-\u20b9250', tag: '' }
            ]
        },
        'Pyaaz': {
            price: '3,200', trend: '-1.5%', action: t('action_sell_now'),
            reason: t('reason_export_ban'),
            mandis: [
                { name: 'Nashik', price: '\u20b93,400', diff: '+\u20b9200', tag: t('best_option') },
                { name: 'Pune', price: '\u20b93,200', diff: '-', tag: '' },
                { name: 'Vashi', price: '\u20b93,050', diff: '-\u20b9150', tag: '' }
            ]
        },
        'Aloo': {
            price: '1,450', trend: '+2.1%', action: t('action_sell_today'),
            reason: t('reason_aloo'),
            mandis: [
                { name: 'Pune', price: '\u20b91,550', diff: '+\u20b9100', tag: t('best_option') },
                { name: 'Kalyan', price: '\u20b91,450', diff: '-', tag: '' }
            ]
        },
        'Kela': {
            price: '1,800', trend: '+0.5%', action: t('action_sell_today'),
            reason: t('reason_kela'),
            mandis: [
                { name: 'Vashi', price: '\u20b91,900', diff: '+\u20b9100', tag: t('best_option') },
                { name: 'Kalyan', price: '\u20b91,800', diff: '-', tag: '' }
            ]
        }
    };
"""

content = content.replace("const { t } = useLanguage();", "const { t } = useLanguage();\n" + new_mockData)

with open('frontend/src/pages/Home.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
