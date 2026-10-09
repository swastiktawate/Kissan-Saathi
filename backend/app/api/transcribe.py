import httpx
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
import logging

from backend.app.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = Form("hi")
):
    if not settings.SARVAM_API_KEY:
        raise HTTPException(status_code=500, detail="Sarvam API key not configured")

    # Map our UI languages to Sarvam language codes
    lang_map = {
        "hi": "hi-IN",
        "mr": "mr-IN",
        "pa": "pa-IN",
        "en": "en-IN",
    }
    sarvam_lang = lang_map.get(language, "hi-IN")
    
    url = "https://api.sarvam.ai/speech-to-text"
    headers = {
        "api-subscription-key": settings.SARVAM_API_KEY
    }
    
    try:
        content = await file.read()
        files = {
            "file": (file.filename or "audio.webm", content, file.content_type or "audio/webm")
        }
        data = {
            "language_code": sarvam_lang,
            "model": "saaras:v3"
        }
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers=headers, files=files, data=data, timeout=30.0)
            
        if resp.status_code != 200:
            logger.error(f"Sarvam STT failed: {resp.status_code} {resp.text}")
            raise HTTPException(status_code=resp.status_code, detail="Speech-to-text failed")
            
        result = resp.json()
        transcript = result.get("transcript", "")
        return {"transcript": transcript}
        
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail="Transcription error")

from pydantic import BaseModel

class SynthesizeRequest(BaseModel):
    text: str
    language: str = "hi"

@router.post("/synthesize")
async def synthesize_speech(req: SynthesizeRequest):
    if not settings.SARVAM_API_KEY:
        raise HTTPException(status_code=500, detail="Sarvam API key not configured")

    lang_map = {
        "hi": "hi-IN",
        "mr": "mr-IN",
        "pa": "pa-IN",
        "en": "en-IN",
    }
    sarvam_lang = lang_map.get(req.language, "hi-IN")
    
    url = "https://api.sarvam.ai/text-to-speech"
    headers = {
        "api-subscription-key": settings.SARVAM_API_KEY,
        "Content-Type": "application/json"
    }
    
    speaker_map = {
        "hi-IN": "ritu",
        "mr-IN": "roopa",
        "pa-IN": "ritu",
        "en-IN": "kavya"
    }
    
    payload = {
        "inputs": [req.text[:500]], # limit text length for safety
        "target_language_code": sarvam_lang,
        "speaker": speaker_map.get(sarvam_lang, "ritu"),
        "pitch": 0,
        "pace": 1.0,
        "loudness": 1.5,
        "speech_sample_rate": 8000,
        "enable_preprocessing": True,
        "model": "bulbul:v3"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers=headers, json=payload, timeout=30.0)
            
        if resp.status_code != 200:
            logger.error(f"Sarvam TTS failed: {resp.status_code} {resp.text}")
            raise HTTPException(status_code=resp.status_code, detail="Text-to-speech failed")
            
        result = resp.json()
        audios = result.get("audios", [])
        if not audios:
            raise HTTPException(status_code=500, detail="No audio returned")
            
        return {"audio_base64": audios[0]}
        
    except Exception as e:
        logger.error(f"Synthesis error: {e}")
        raise HTTPException(status_code=500, detail="Synthesis error")
