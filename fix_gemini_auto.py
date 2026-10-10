import re

with open('backend/app/assistant/providers/gemini.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Update system prompt to handle auto language
new_sys_prompt = """            lang_instruction = f"CRITICAL: You MUST respond in the language code '{language}'."
            if language == "auto":
                lang_instruction = "CRITICAL: You MUST detect the language of the user's message. Reply in the EXACT SAME language. YOU MUST start your response with a language tag in square brackets: [en], [hi], [mr], [pa], or [hr], followed by your actual response."

            system_prompt = (
                "You are Kisan Sathi, a helpful agricultural assistant for Indian farmers. "
                "You help farmers decide when and where to sell their crops. "
                f"{lang_instruction} "
                "Keep answers brief, highly actionable, and avoid markdown if possible. Do not use asterisks or bold text."
            )"""

content = re.sub(r'            system_prompt = \(\n.*?            \)', new_sys_prompt, content, flags=re.DOTALL)

with open('backend/app/assistant/providers/gemini.py', 'w', encoding='utf-8') as f:
    f.write(content)
