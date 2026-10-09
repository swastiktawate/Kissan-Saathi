import { useState, useRef, useEffect } from 'react';

export function useVoice(lang: string = 'en') {
    const [isListening, setIsListening] = useState(false);
    const [transcript, setTranscript] = useState('');
    const [supported, setSupported] = useState(true);
    
    const mediaRecorder = useRef<MediaRecorder | null>(null);
    const audioChunks = useRef<Blob[]>([]);

    useEffect(() => {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            setSupported(false);
        }
    }, []);

    const startListening = async () => {
        if (!supported) return;
        setTranscript('');
        
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const recorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
            
            audioChunks.current = [];
            recorder.ondataavailable = (e) => {
                if (e.data.size > 0) audioChunks.current.push(e.data);
            };
            
            recorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks.current, { type: 'audio/webm' });
                
                // Stop all tracks to release microphone
                stream.getTracks().forEach(track => track.stop());
                
                await transcribeAudio(audioBlob);
            };
            
            mediaRecorder.current = recorder;
            recorder.start();
            setIsListening(true);
            
        } catch (err) {
            console.error("Mic error:", err);
            setIsListening(false);
        }
    };

    const stopListening = () => {
        if (mediaRecorder.current && mediaRecorder.current.state === 'recording') {
            mediaRecorder.current.stop();
            setIsListening(false);
        }
    };
    
    const transcribeAudio = async (blob: Blob) => {
        try {
            const formData = new FormData();
            formData.append('file', blob, 'audio.webm');
            formData.append('language', lang);
            
            const res = await fetch('http://localhost:8000/api/v1/transcribe', {
                method: 'POST',
                body: formData,
            });
            
            if (res.ok) {
                const data = await res.json();
                if (data.transcript) {
                    setTranscript(data.transcript);
                }
            }
        } catch (err) {
            console.error("Transcription failed", err);
        }
    };

    return { isListening, transcript, startListening, stopListening, supported, setTranscript };
}
