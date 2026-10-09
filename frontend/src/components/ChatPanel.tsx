import { useState, useEffect } from 'react';
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
