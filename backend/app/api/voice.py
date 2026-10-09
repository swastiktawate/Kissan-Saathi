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
    lang_map = {"hi": "hi-IN", "mr": "mr-IN", "pa": "pa-IN", "en": "en-IN"}
    sarvam_lang = lang_map.get(language, "hi-IN")

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
        print(f'PRINT: "Transcribed: {transcript}"')

    except HTTPException:
        raise
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"STT exception:\n{tb}")
        with open("voice_error.log", "a") as f:
            f.write(f"--- STT ERROR ---\n{tb}\n")
        raise HTTPException(status_code=500, detail=f"STT error: {e}")

    if not transcript.strip():
        return {"reply_text": "Mujhe kuch sunaai nahi diya. Kripya phir se bolein.", "audio_base64": "", "user_transcript": ""}

    # --- STEP 2: Gemini Agent ---
    try:
        agent_result = await run_agent(transcript, language=language)
        gemini_text = agent_result.get("reply", "Maaf kijiye, main samajh nahi paaya.")
        print(f'PRINT: "Gemini replied: {gemini_text[:100]}..."')
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"Agent exception:\n{tb}")
        with open("voice_error.log", "a") as f:
            f.write(f"--- AGENT ERROR ---\n{tb}\n")
        gemini_text = "System mein kuch gadbad hai. Kripya baad mein try karein."

    # --- STEP 3: Sarvam TTS (Bulbul) ---
    tts_url = "https://api.sarvam.ai/text-to-speech"
    tts_headers = {
        "api-subscription-key": settings.SARVAM_API_KEY,
        "Content-Type": "application/json",
    }

    speaker_map = {
        "hi-IN": "ritu",
        "mr-IN": "roopa",
        "pa-IN": "ritu",
        "en-IN": "kavya",
    }

    tts_payload = {
        "inputs": [gemini_text[:500]],
        "target_language_code": sarvam_lang,
        "speaker": speaker_map.get(sarvam_lang, "ritu"),
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
            with open("voice_error.log", "a") as f:
                f.write(f"--- TTS ERROR {tts_resp.status_code} ---\n{tts_resp.text}\n")
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"TTS exception:\n{tb}")
        with open("voice_error.log", "a") as f:
            f.write(f"--- TTS EXCEPTION ---\n{tb}\n")

    return {
        "reply_text": gemini_text,
        "audio_base64": audio_base64,
        "user_transcript": transcript,
    }
