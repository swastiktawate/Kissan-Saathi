import re

with open('frontend/src/pages/Home.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace any line containing "crop === 'Tamatar' ?" inside span with the right emojis
content = re.sub(
    r"<span className=\"text-2xl mb-1\">.*?</span>",
    "<span className=\"text-2xl mb-1\">\n                                {crop === 'Tamatar' ? '🍅' : crop === 'Pyaaz' ? '🧅' : crop === 'Aloo' ? '🥔' : '🍌'}\n                            </span>",
    content,
    flags=re.DOTALL
)

with open('frontend/src/pages/Home.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
