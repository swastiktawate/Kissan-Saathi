import re

with open('backend/app/api/voice.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the dangerous print statements causing the UnicodeEncodeError on Windows
content = re.sub(r'print\(f\'PRINT: "Transcribed: \{transcript\}"\'\)', 'pass # removed print to avoid UnicodeEncodeError', content)
content = re.sub(r'print\(f\'PRINT: "Gemini replied.*?\]: \{gemini_text.*?\}\.\.\."\'\)', 'pass', content)
content = re.sub(r'print\(f\'PRINT: "Gemini replied: \{gemini_text.*?\}\.\.\."\'\)', 'pass', content)

# I should also ensure that no logger calls are causing it, though usually logger is slightly safer, it still might crash the console stream handler.
# The error trace specifically points to line 48 `print(f'PRINT: "Transcribed: {transcript}"')`.

with open('backend/app/api/voice.py', 'w', encoding='utf-8') as f:
    f.write(content)
