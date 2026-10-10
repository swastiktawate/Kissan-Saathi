import re

with open('frontend/src/pages/Home.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the garbled characters
content = content.replace(',12,350', '\u20b92,350')
content = content.replace('+,1200', '+\u20b9200')
content = content.replace(',12,150', '\u20b92,150')
content = content.replace(',11,900', '\u20b91,900')
content = content.replace('-,1250', '-\u20b9250')

content = content.replace(',13,400', '\u20b93,400')
content = content.replace(',13,200', '\u20b93,200')
content = content.replace(',13,050', '\u20b93,050')
content = content.replace('-,1150', '-\u20b9150')

content = content.replace(',11,550', '\u20b91,550')
content = content.replace('+,1100', '+\u20b9100')
content = content.replace(',11,450', '\u20b91,450')

with open('frontend/src/pages/Home.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
