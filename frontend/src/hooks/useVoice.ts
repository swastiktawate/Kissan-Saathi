import { useState, useEffect, useRef } from 'react';

export function useVoice(lang: string = 'en-US') {
    const [isListening, setIsListening] = useState(false);
    const [transcript, setTranscript] = useState('');
    const [supported, setSupported] = useState(true);
    const recognition = useRef<any>(null);

    useEffect(() => {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            setSupported(false);
            return;
        }
        
        const SpeechRec = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
        recognition.current = new SpeechRec();
        recognition.current.continuous = false;
        recognition.current.interimResults = false;
        
        recognition.current.onresult = (event: any) => {
            const current = event.resultIndex;
            const res = event.results[current][0].transcript;
            setTranscript(res);
            setIsListening(false);
        };
        
        recognition.current.onend = () => {
            setIsListening(false);
        };
        
        recognition.current.onerror = () => {
            setIsListening(false);
        };
    }, []);

    useEffect(() => {
        if (recognition.current) {
            recognition.current.lang = lang === 'hi' ? 'hi-IN' : lang === 'mr' ? 'mr-IN' : 'en-US';
        }
    }, [lang]);

    const startListening = () => {
        if (supported && recognition.current) {
            setTranscript('');
            setIsListening(true);
            recognition.current.start();
        }
    };

    const stopListening = () => {
        if (supported && recognition.current) {
            setIsListening(false);
            recognition.current.stop();
        }
    };

    return { isListening, transcript, startListening, stopListening, supported, setTranscript };
}
