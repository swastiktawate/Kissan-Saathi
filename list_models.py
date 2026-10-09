import google.generativeai as genai
from backend.app.config import settings
genai.configure(api_key=settings.GEMINI_API_KEY)
print([m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods])
