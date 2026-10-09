import { useState, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';

export function useVoiceBot(language: string = 'hi') {
    const [isRecording, setIsRecording] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const chunksRef = useRef<Blob[]>([]);
    const streamRef = useRef<MediaStream | null>(null);
    const navigate = useNavigate();

    const startRecording = useCallback(async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            streamRef.current = stream;

            const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
            mediaRecorderRef.current = mediaRecorder;
            chunksRef.current = [];

            mediaRecorder.ondataavailable = (e) => {
                if (e.data.size > 0) chunksRef.current.push(e.data);
            };

            mediaRecorder.onstop = async () => {
                // Release mic immediately
                stream.getTracks().forEach(track => track.stop());

                const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
                setIsProcessing(true);

                try {
                    const formData = new FormData();
                    formData.append('file', audioBlob, 'audio.webm');
                    formData.append('language', language);

                    const res = await fetch('http://localhost:8000/api/v1/voice/chat', {
                        method: 'POST',
                        body: formData,
                    });

                    if (!res.ok) {
                        console.error('Voice API error:', res.status, await res.text());
                        setIsProcessing(false);
                        return;
                    }

                    const response = await res.json();

                    // CRITICAL PLAYBACK FIX: Play audio from base64
                    if (response.audio_base64) {
                        const audioData = `data:audio/wav;base64,${response.audio_base64}`;
                        const audio = new Audio(audioData);
                        audio.play().catch(e => console.error("Audio playback failed:", e));
                    }

                    // Navigate to chat with the response for UI rendering
                    navigate('/chat', {
                        state: {
                            voiceResponse: {
                                transcript: response.reply_text ? undefined : '',
                                user_text: response.user_transcript || '',
                                reply: response.reply_text || '',
                                audio_base64: response.audio_base64 || '',
                            }
                        }
                    });

                } catch (err) {
                    console.error('Voice fetch failed:', err);
                } finally {
                    setIsProcessing(false);
                }
            };

            mediaRecorder.start();
            setIsRecording(true);
        } catch (err) {
            console.error('Mic permission error:', err);
            setIsRecording(false);
        }
    }, [navigate, language]);

    const stopRecording = useCallback(() => {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
            mediaRecorderRef.current.stop();
            setIsRecording(false);
        }
    }, []);

    const toggleRecording = useCallback(() => {
        if (isRecording) {
            stopRecording();
        } else if (!isProcessing) {
            startRecording();
        }
    }, [isRecording, isProcessing, startRecording, stopRecording]);

    return { isRecording, isProcessing, toggleRecording };
}
