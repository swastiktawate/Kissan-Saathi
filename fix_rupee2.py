import re

with open('frontend/src/pages/Home.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace any occurrence of the garbled ₹ symbol
# Since the character might be unprintable, we can just replace anything that looks like "price: ',12,350'" using regex.
content = re.sub(r"['\"](?:[^\x00-\x7F]*,)?12,350['\"]", "'\u20b92,350'", content)
content = re.sub(r"['\"](?:[^\x00-\x7F]*,)?1200['\"]", "'\u20b9200'", content)
content = re.sub(r"['\"](?:[^\x00-\x7F]*,)?12,150['\"]", "'\u20b92,150'", content)
content = re.sub(r"['\"](?:[^\x00-\x7F]*,)?11,900['\"]", "'\u20b91,900'", content)
content = re.sub(r"['\"]-(?:[^\x00-\x7F]*,)?1250['\"]", "'-\u20b9250'", content)
content = re.sub(r"['\"]\+(?:[^\x00-\x7F]*,)?1200['\"]", "'+\u20b9200'", content)

content = re.sub(r"['\"](?:[^\x00-\x7F]*,)?13,400['\"]", "'\u20b93,400'", content)
content = re.sub(r"['\"](?:[^\x00-\x7F]*,)?13,200['\"]", "'\u20b93,200'", content)
content = re.sub(r"['\"](?:[^\x00-\x7F]*,)?13,050['\"]", "'\u20b93,050'", content)
content = re.sub(r"['\"]-(?:[^\x00-\x7F]*,)?1150['\"]", "'-\u20b9150'", content)

content = re.sub(r"['\"](?:[^\x00-\x7F]*,)?11,550['\"]", "'\u20b91,550'", content)
content = re.sub(r"['\"]\+(?:[^\x00-\x7F]*,)?1100['\"]", "'+\u20b9100'", content)
content = re.sub(r"['\"](?:[^\x00-\x7F]*,)?11,450['\"]", "'\u20b91,450'", content)

with open('frontend/src/pages/Home.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
