import httpx
import logging
import traceback

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from backend.app.config import settings
from backend.app.assistant.agent import run_agent

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/chat")
async def voice_chat(
    file: UploadFile = File(...),
    language: str = Form("hi"),
):
    """Unified Voice Pipeline: STT -> Gemini Agent -> TTS -> Response"""

    if not settings.SARVAM_API_KEY:
        raise HTTPException(status_code=500, detail="Sarvam API key not configured")

    # --- STEP 1: Sarvam STT (Saaras) ---
    # We use 'Unknown' to auto-detect whatever the user speaks, ignoring UI language
    sarvam_lang = "Unknown"

    stt_url = "https://api.sarvam.ai/speech-to-text"
    stt_headers = {"api-subscription-key": settings.SARVAM_API_KEY}

    try:
        content = await file.read()
        stt_files = {
            "file": (file.filename or "audio.webm", content, file.content_type or "audio/webm"),
        }
        stt_data = {"language_code": sarvam_lang, "model": "saaras:v3"}

        async with httpx.AsyncClient() as client:
            stt_resp = await client.post(
                stt_url, headers=stt_headers, files=stt_files, data=stt_data, timeout=30.0
            )

        if stt_resp.status_code != 200:
            logger.error(f"Sarvam STT error {stt_resp.status_code}: {stt_resp.text}")
            raise HTTPException(status_code=stt_resp.status_code, detail="STT failed")

        transcript = stt_resp.json().get("transcript", "")
        pass # removed print to avoid UnicodeEncodeError

    except HTTPException:
        raise
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"STT exception:\n{tb}")
        with open("voice_error.log", "a") as f:
            f.write(f"--- STT ERROR ---\n{tb}\n")
        raise HTTPException(status_code=500, detail=f"STT error: {e}")

    if not transcript.strip():
        return {"reply_text": "I could not hear anything. Please speak again.", "audio_base64": "", "user_transcript": ""}

    # --- STEP 2: Gemini Agent ---
    detected_lang_code = "hi"
    try:
        # Run agent in 'auto' mode so it detects speech and returns [lang] tag
        agent_result = await run_agent(transcript, language="auto")
        gemini_text = agent_result.get("reply", "Maaf kijiye, main samajh nahi paaya.")
        
        # Extract the language tag (e.g., [en], [hi], [mr], [hr], [pa])
        import re
        match = re.match(r'^\[(en|hi|mr|pa|hr|ha)\](.*)', gemini_text.strip(), re.IGNORECASE | re.DOTALL)
        if match:
            detected_lang_code = match.group(1).lower()
            gemini_text = match.group(2).strip()
            
        pass
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"Agent exception:\n{tb}")
        gemini_text = "System is experiencing an issue. Please try again later."
        detected_lang_code = "en"

    # --- STEP 3: Sarvam TTS (Bulbul) ---
    tts_url = "https://api.sarvam.ai/text-to-speech"
    tts_headers = {
        "api-subscription-key": settings.SARVAM_API_KEY,
        "Content-Type": "application/json",
    }
    
    # Map back to sarvam language code
    if detected_lang_code == 'ha': detected_lang_code = 'hi' # fallback Haryanvi to Hindi TTS
    if detected_lang_code == 'hr': detected_lang_code = 'hi'
    
    lang_map_out = {"hi": "hi-IN", "mr": "mr-IN", "pa": "pa-IN", "en": "en-IN"}
    final_sarvam_lang = lang_map_out.get(detected_lang_code, "hi-IN")

    speaker_map = {
        "hi-IN": "ritu",
        "mr-IN": "roopa",
        "pa-IN": "ritu", # Sarvam doesn't strictly have a Punjabi bulbul speaker sometimes, but fallback is fine
        "en-IN": "kavya",
    }

    tts_payload = {
        "inputs": [gemini_text[:500]],
        "target_language_code": final_sarvam_lang,
        "speaker": speaker_map.get(final_sarvam_lang, "ritu"),
        "pitch": 0,
        "pace": 1.0,
        "loudness": 1.5,
        "speech_sample_rate": 8000,
        "enable_preprocessing": True,
        "model": "bulbul:v3",
    }

    audio_base64 = ""
    try:
        async with httpx.AsyncClient() as client:
            tts_resp = await client.post(
                tts_url, headers=tts_headers, json=tts_payload, timeout=30.0
            )

        if tts_resp.status_code == 200:
            audios = tts_resp.json().get("audios", [])
            if audios:
                audio_base64 = audios[0]
                print(f'PRINT: "TTS audio generated, length={len(audio_base64)}"')
        else:
            logger.warning(f"TTS error {tts_resp.status_code}: {tts_resp.text}")
    except Exception as e:
        logger.error(f"TTS exception: {e}")

    return {
        "reply_text": gemini_text,
        "audio_base64": audio_base64,
        "user_transcript": transcript,
    }
