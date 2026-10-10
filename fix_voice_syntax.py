import re

with open('backend/app/api/voice.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix unterminated string literals
content = content.replace('logger.error(f"STT exception:\n{tb}")', 'logger.error(f"STT exception:\\n{tb}")')
content = content.replace('f.write(f"--- STT ERROR ---\n{tb}\n")', 'f.write(f"--- STT ERROR ---\\n{tb}\\n")')
content = content.replace('logger.error(f"Agent exception:\n{tb}")', 'logger.error(f"Agent exception:\\n{tb}")')

with open('backend/app/api/voice.py', 'w', encoding='utf-8') as f:
    f.write(content)
