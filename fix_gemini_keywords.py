import re

with open('backend/app/assistant/providers/gemini.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the hardcoded string matching with one that includes native languages

new_trigger_logic = """
            needs_forecast = is_user and any(kw in last_msg for kw in [
                "forecast", "predict", "future", "agla", "mahina", "next", "month", "bhavishya",
                "भविष्य", "भविष्यवाणी", "महिना", "आगे", "अंदाज", "भावी"
            ])
            
            needs_recommend = is_user and any(kw in last_msg for kw in [
                "sell", "price", "mandi", "wait", "tomato", "onion",
                "tamatar", "pyaaz", "bechna", "kab", "kaha", "recommend",
                "बेचना", "बेचूँ", "बेच", "मंडी", "भाव", "दाम", "कहाँ", "कधी", "कुठे", "विकायचं", "विकू"
            ])

            if needs_forecast or needs_recommend:
                crop = "tomato"
                if any(k in last_msg for k in ["onion", "pyaaz", "pyaj", "प्याज़", "कांदा"]):
                    crop = "onion"
                elif any(k in last_msg for k in ["potato", "aloo", "alu", "आलू", "बटाटा"]):
                    crop = "potato"
                elif any(k in last_msg for k in ["banana", "kela", "केला", "केळी"]):
                    crop = "banana"
"""

content = re.sub(
    r'needs_forecast = is_user and any\(kw in last_msg for kw in \[\n.*?elif any\(k in last_msg for k in \["banana", "kela"\]\):\n.*?crop = "banana"',
    new_trigger_logic.strip(),
    content,
    flags=re.DOTALL
)

with open('backend/app/assistant/providers/gemini.py', 'w', encoding='utf-8') as f:
    f.write(content)
