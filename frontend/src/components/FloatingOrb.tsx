import { useNavigate, useLocation } from 'react-router-dom';
import { Mic, Loader2 } from 'lucide-react';
import { useState, useEffect, useRef } from 'react';

export default function FloatingOrb() {
    const navigate = useNavigate();
    const location = useLocation();
    const [isOffline, setIsOffline] = useState(!navigator.onLine);
    const [recording, setRecording] = useState(false);
    const [processing, setProcessing] = useState(false);
    
    const mediaRecorder = useRef<MediaRecorder | null>(null);
    const audioChunks = useRef<Blob[]>([]);
    const streamRef = useRef<MediaStream | null>(null);

    useEffect(() => {
        const handleOnline = () => setIsOffline(false);
        const handleOffline = () => setIsOffline(true);
        window.addEventListener('online', handleOnline);
        window.addEventListener('offline', handleOffline);
        return () => {
            window.removeEventListener('online', handleOnline);
            window.removeEventListener('offline', handleOffline);
        };
    }, []);

    // Stop recording automatically on silence or after 5 seconds
    useEffect(() => {
        if (recording) {
            const t = setTimeout(() => {
                stopRecording();
            }, 5000);
            return () => clearTimeout(t);
        }
    }, [recording]);

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            streamRef.current = stream;
            const recorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
            
            audioChunks.current = [];
            recorder.ondataavailable = (e) => {
                if (e.data.size > 0) audioChunks.current.push(e.data);
            };
            
            recorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks.current, { type: 'audio/webm' });
                stream.getTracks().forEach(track => track.stop());
                await sendToVoiceApi(audioBlob);
            };
            
            mediaRecorder.current = recorder;
            recorder.start();
            setRecording(true);
        } catch (err) {
            console.error("Mic error:", err);
            setRecording(false);
        }
    };

    const stopRecording = () => {
        if (mediaRecorder.current && mediaRecorder.current.state === 'recording') {
            mediaRecorder.current.stop();
            setRecording(false);
            setProcessing(true);
        }
    };

    const sendToVoiceApi = async (blob: Blob) => {
        try {
            const formData = new FormData();
            formData.append('file', blob, 'audio.webm');
            formData.append('language', 'hi'); // Defaulting to hindi for demo
            
            const res = await fetch('http://localhost:8000/api/v1/voice/ask', {
                method: 'POST',
                body: formData,
            });
            
            if (res.ok) {
                const data = await res.json();
                navigate('/chat', { state: { voiceResponse: data } });
            }
        } catch (err) {
            console.error("Voice API failed", err);
        } finally {
            setProcessing(false);
        }
    };

    const handleClick = () => {
        if (recording) {
            stopRecording();
        } else {
            startRecording();
        }
    };

    // Don't show orb on chat page or if offline
    if (location.pathname === '/chat' || isOffline) return null;

    let icon = <Mic size={28} />;
    let stateClasses = "bg-green-600";
    if (recording) {
        stateClasses = "bg-red-500 animate-pulse scale-110";
    } else if (processing) {
        icon = <Loader2 size={28} className="animate-spin" />;
        stateClasses = "bg-stone-500";
    }

    return (
        <button 
            onClick={handleClick}
            disabled={processing}
            className={`fixed bottom-[72px] right-4 z-50 text-white p-4 rounded-full shadow-2xl transition-all active:scale-95 ${stateClasses}`}
        >
            {icon}
        </button>
    );
}
