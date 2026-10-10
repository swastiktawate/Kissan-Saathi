import re

with open('frontend/src/pages/Home.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('{t("hero_subtitle", "Aapke fasal ke liye behtar faisle, data ke saath.")}', '{t("hero_subtitle")}')

with open('frontend/src/pages/Home.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
