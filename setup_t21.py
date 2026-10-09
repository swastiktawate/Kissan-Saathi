import json
import os

hi_dict = {
  "greeting": "नमस्ते, किसान",
  "home_mandi": "आपकी मंडी",
  "my_crops": "मेरी फसलें",
  "today_price": "आज का भाव",
  "top_mandis": "शीर्ष सुझाव",
  "INSUFFICIENT_DATA": "अपर्याप्त डेटा",
  "SELL_NOW": "अभी बेचें",
  "ANOTHER_MANDI": "दूसरी मंडी में बेचें",
  "WAIT_N_DAYS": "प्रतीक्षा करें",
  "SPLIT_SALE": "विभाजित बिक्री",
  "action": "कार्रवाई",
  "expected_gain": "संभावित लाभ (Rs/q)",
  "confidence": "विश्वास",
  "trust": "विश्वास स्कोर",
  "clear": "स्पष्ट",
  "moderate": "मध्यम",
  "low": "कम",
  "high": "उच्च",
  "medium": "मध्यम",
  "caution": "सावधानी: डेटा विश्वास मध्यम है। अनुमानों में अधिक अनिश्चितता हो सकती है।",
  "insufficient_reasons": "विश्वास स्कोर अपर्याप्त है। हम विश्वास के साथ कार्रवाई की सिफारिश नहीं कर सकते।",
  "settings": "सेटिंग्स",
  "quantity": "मात्रा (क्विंटल)",
  "horizon": "क्षितिज (दिन)",
  "risk_setting": "जोखिम सेटिंग",
  "cautious": "सतर्क",
  "balanced": "संतुलित",
  "aggressive": "आक्रामक",
  "save": "सहेजें"
}

mr_dict = {
  "greeting": "नमस्कार, शेतकरी",
  "home_mandi": "तुमची मंडी",
  "my_crops": "माझी पिके",
  "today_price": "आजचा भाव",
  "top_mandis": "शीर्ष शिफारसी",
  "INSUFFICIENT_DATA": "अपुरा डेटा",
  "SELL_NOW": "आता विका",
  "ANOTHER_MANDI": "दुसऱ्या मंडीत विका",
  "WAIT_N_DAYS": "वाट पाहा",
  "SPLIT_SALE": "विभाजित विक्री",
  "action": "कृती",
  "expected_gain": "अपेक्षित लाभ (Rs/q)",
  "confidence": "आत्मविश्वास",
  "trust": "विश्वास स्कोर",
  "clear": "स्पष्ट",
  "moderate": "मध्यम",
  "low": "कमी",
  "high": "उच्च",
  "medium": "मध्यम",
  "caution": "सावधानता: डेटा विश्वास मध्यम आहे. अंदाजांमध्ये जास्त अनिश्चितता असू शकते.",
  "insufficient_reasons": "विश्वास स्कोर अपुरा आहे. आम्ही आत्मविश्वासाने कृतीची शिफारस करू शकत नाही.",
  "settings": "सेटिंग्ज",
  "quantity": "प्रमाण (क्विंटल)",
  "horizon": "क्षितिज (दिवस)",
  "risk_setting": "जोखीम सेटिंग",
  "cautious": "सावध",
  "balanced": "संतुलित",
  "aggressive": "आक्रमक",
  "save": "जतन करा"
}

with open('frontend/src/i18n/hi.json', 'w', encoding='utf-8') as f:
    json.dump(hi_dict, f, ensure_ascii=False, indent=2)

with open('frontend/src/i18n/mr.json', 'w', encoding='utf-8') as f:
    json.dump(mr_dict, f, ensure_ascii=False, indent=2)

with open('frontend/scripts/check_i18n.ts', 'w', encoding='utf-8') as f:
    f.write('''import fs from 'fs';
import path from 'path';

const en = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'src/i18n/en.json'), 'utf8'));
const hi = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'src/i18n/hi.json'), 'utf8'));
const mr = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'src/i18n/mr.json'), 'utf8'));

const enKeys = Object.keys(en).sort();
const hiKeys = Object.keys(hi).sort();
const mrKeys = Object.keys(mr).sort();

let failed = false;
if (JSON.stringify(enKeys) !== JSON.stringify(hiKeys)) {
    console.error("Hindi keys do not match English keys");
    failed = true;
}
if (JSON.stringify(enKeys) !== JSON.stringify(mrKeys)) {
    console.error("Marathi keys do not match English keys");
    failed = true;
}

if (failed) process.exit(1);
console.log("i18n check passed");
''')

# Update package.json to include the script
import json as js
with open('frontend/package.json', 'r') as f:
    pkg = js.load(f)
pkg['scripts']['check:i18n'] = "npx tsx scripts/check_i18n.ts"
with open('frontend/package.json', 'w') as f:
    js.dump(pkg, f, indent=2)

with open('frontend/src/hooks/useVoice.ts', 'w', encoding='utf-8') as f:
    f.write('''import { useState, useEffect, useRef } from 'react';

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
''')

with open('frontend/src/components/ChatPanel.tsx', 'w', encoding='utf-8') as f:
    f.write('''import { useState, useEffect } from 'react';
import { useVoice } from '../hooks/useVoice';

export default function ChatPanel() {
    const [messages, setMessages] = useState<any[]>([]);
    const [input, setInput] = useState('');
    const [language, setLanguage] = useState('en');
    const { isListening, transcript, startListening, stopListening, supported, setTranscript } = useVoice(language);
    
    // Check offline status
    const [isOffline, setIsOffline] = useState(!navigator.onLine);
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

    useEffect(() => {
        if (transcript) setInput(transcript);
    }, [transcript]);

    const sendMsg = async (text: string) => {
        if (!text.trim() || isOffline) return;
        
        const newMsgs = [...messages, { role: 'user', content: text }];
        setMessages(newMsgs);
        setInput('');
        setTranscript('');
        
        setMessages([...newMsgs, { role: 'assistant', loading: true }]);
        
        try {
            const res = await fetch('http://localhost:8000/api/v1/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text, language })
            });
            const data = await res.json();
            
            setMessages([...newMsgs, { 
                role: 'assistant', 
                content: data.reply,
                tools: data.tools_used,
                mode: data.meta?.llm_mode
            }]);
        } catch (e) {
            setMessages([...newMsgs, { role: 'assistant', content: 'Network error. Could not reach assistant.' }]);
        }
    };

    return (
        <div className="flex flex-col h-[calc(100vh-60px)] p-4 max-w-[360px] mx-auto bg-canvas">
            <div className="flex justify-between items-center mb-4">
                <h2 className="font-bold">Kisan Saathi</h2>
                <select value={language} onChange={e => setLanguage(e.target.value)} className="border p-1 text-sm bg-white">
                    <option value="en">English</option>
                    <option value="hi">हिंदी</option>
                    <option value="mr">मराठी</option>
                </select>
            </div>
            
            <div className="flex-1 overflow-y-auto mb-4 flex flex-col gap-3">
                {messages.length === 0 && (
                    <div className="text-center text-stone-500 mt-10 text-sm">
                        Ask about crop prices, when to sell, or scenarios!
                    </div>
                )}
                {messages.map((m, i) => (
                    <div key={i} className={`p-3 rounded-sm text-sm max-w-[85%] ${m.role === 'user' ? 'bg-stone-900 text-white self-end' : 'bg-white border border-stone-200 self-start shadow-sm'}`}>
                        {m.loading ? 'Thinking...' : m.content}
                        
                        {m.mode === 'rule_based' && (
                            <div className="mt-2 text-[10px] text-stone-400 border-t border-stone-200 pt-1">
                                Basic answers — AI assistant unavailable
                            </div>
                        )}
                        {m.tools && m.tools.length > 0 && (
                            <div className="mt-2 flex gap-1 flex-wrap">
                                {m.tools.map((t: string, j: number) => (
                                    <span key={j} className="text-[10px] bg-accent text-stone-900 px-1 py-0.5 rounded-sm">Used: {t}</span>
                                ))}
                            </div>
                        )}
                    </div>
                ))}
            </div>
            
            {isOffline && (
                <div className="bg-red-100 text-red-800 text-xs p-2 mb-2 text-center rounded-sm">
                    Offline mode. Chat is disabled.
                </div>
            )}
            
            <div className="flex gap-2">
                <input 
                    type="text" 
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    onKeyPress={e => e.key === 'Enter' && sendMsg(input)}
                    disabled={isOffline}
                    placeholder={isOffline ? "Offline" : "Ask something..."}
                    className="flex-1 border p-2 text-sm bg-white disabled:bg-stone-100"
                />
                {supported && (
                    <button 
                        onClick={isListening ? stopListening : startListening}
                        disabled={isOffline}
                        className={`p-2 border rounded-sm disabled:opacity-50 ${isListening ? 'bg-red-500 text-white' : 'bg-white'}`}
                    >
                        🎤
                    </button>
                )}
                <button onClick={() => sendMsg(input)} disabled={isOffline} className="bg-stone-900 text-white px-3 rounded-sm disabled:opacity-50">➤</button>
            </div>
        </div>
    );
}
''')
