import re

with open('frontend/src/components/ChatPanel.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the Audio playback logic from ChatPanel to stop echoing
content = re.sub(r'// Audio is natively played by useVoiceBot, but just in case:\s*if \(vr\.audio_base64 && !vr\._played\) \{.*?\n\s*\}', '', content, flags=re.DOTALL)

with open('frontend/src/components/ChatPanel.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
