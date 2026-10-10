import re
with open('frontend/src/components/ChatPanel.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

if 'useLanguage' not in c:
    c = c.replace("from 'lucide-react';", "from 'lucide-react';\nimport { useLanguage } from '../context/LanguageContext';")

c = re.sub(r'const \[language, setLanguage\] = useState\(.*?\'\);', 'const { language, setLanguage } = useLanguage();', c)

# Replace the native hardcoded <select> with a functional one matching LanguageCode
# Actually wait, the user will change it via Profile/Settings or the local one. The local one can remain, it just needs to update global state.
# But let's check what the local select does.
# <option value="en">English</option>
# <option value="hi">हिंदी</option>
# <option value="mr">मराठी</option>
# <option value="pa">ਪੰਜਾਬੀ</option>
# <option value="hr">हरियाणवी</option>

c = c.replace('<option value="hi"> 1  , ݅?</option>', '<option value="hi">हिन्दी</option>')
c = c.replace('<option value="mr">   1</option>', '<option value="mr">मराठी</option>')
c = c.replace('<option value="pa">     ݅?</option>', '<option value="pa">ਪੰਜਾਬੀ</option>')
c = c.replace('<option value="hr">  1  ݅?</option>', '<option value="hr">हरियाणवी</option>')

with open('frontend/src/components/ChatPanel.tsx', 'w', encoding='utf-8') as f:
    f.write(c)
