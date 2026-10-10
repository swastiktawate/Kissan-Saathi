import re
with open('frontend/src/components/ChatPanel.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the entire select block
c = re.sub(
    r'<select value=\{language\}.*?</select>',
    r'''<select value={language} onChange={e => setLanguage(e.target.value as any)}
                    className="border border-stone-200 rounded-lg p-1.5 text-xs bg-white shadow-sm">
                    <option value="en">English</option>
                    <option value="hi">हिन्दी</option>
                    <option value="mr">मराठी</option>
                    <option value="pa">ਪੰਜਾਬੀ</option>
                    <option value="hr">हरियाणवी</option>
                </select>''',
    c,
    flags=re.DOTALL
)

with open('frontend/src/components/ChatPanel.tsx', 'w', encoding='utf-8') as f:
    f.write(c)
