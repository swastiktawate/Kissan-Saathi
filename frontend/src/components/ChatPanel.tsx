import { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useVoiceBot } from '../hooks/useVoiceBot';
import { Mic, Send, Bot, User, Sparkles, Loader2 } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import ReactMarkdown from 'react-markdown';

export default function ChatPanel() {
    const [messages, setMessages] = useState<any[]>([]);
    const [input, setInput] = useState('');
    const { language, setLanguage } = useLanguage();
    const [loading, setLoading] = useState(false);
    
    const { isRecording, isProcessing, toggleRecording } = useVoiceBot(language);
    const scrollRef = useRef<HTMLDivElement>(null);

    const [isOffline, setIsOffline] = useState(!navigator.onLine);
    const location = useLocation();
    const navigate = useNavigate();

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
        if (location.state?.initialMsg && messages.length === 0) {
            sendMsg(location.state.initialMsg);
            navigate(location.pathname, { replace: true, state: {} });
        } else if (location.state?.autoStartMic) {
            if (!isRecording) {
                // Short delay to allow UI to mount before triggering mic prompt
                setTimeout(() => toggleRecording(), 100);
            }
            navigate(location.pathname, { replace: true, state: {} });
        } else if (location.state?.voiceResponse) {
            const vr = location.state.voiceResponse;
            const userText = vr.user_text || vr.transcript || '🎤 Voice message';
            const replyText = vr.reply || vr.reply_text || '';
            
            setMessages(prev => {
                // Prevent duplicate appending if the state didn't actually clear due to React strict mode
                const last = prev[prev.length - 1];
                if (last && last.content === replyText) return prev;
                return [
                    ...prev,
                    { role: 'user', content: userText },
                    { role: 'assistant', content: replyText }
                ];
            });
            
            
            
            // Clear the state so it doesn't trigger again on re-renders
            navigate(location.pathname, { replace: true, state: {} });
        }
    }, [location.state, navigate, location.pathname]);

    useEffect(() => {
        scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const suggestedPrompts = [
        "Kya mujhe aaj tamatar bechna chahiye?",
        "Should I wait 3 days?",
        "Which mandi is best for onion?",
        "What's the price trend?"
    ];

    const sendMsg = async (text: string) => {
        if (!text.trim() || isOffline || loading) return;

        const newMsgs = [...messages, { role: 'user', content: text }];
        setMessages(newMsgs);
        setInput('');
        setLoading(true);

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
        } catch {
            setMessages([...newMsgs, { role: 'assistant', content: 'Network error. Could not reach assistant.' }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-[calc(100vh-60px)] bg-stone-50">
            {/* Header */}
            <div className="flex justify-between items-center p-4 bg-white border-b border-stone-200">
                <div className="flex items-center gap-2">
                    <div className="bg-green-600 p-1.5 rounded-lg text-white">
                        <Bot size={20} />
                    </div>
                    <div>
                        <h2 className="font-bold text-stone-900 text-sm">Kisan Sathi Assistant</h2>
                        <p className="text-[10px] text-stone-500">Crop prices, recommendations & more</p>
                    </div>
                </div>
                <select value={language} onChange={e => setLanguage(e.target.value as any)}
                    className="border border-stone-200 rounded-lg p-1.5 text-xs bg-white shadow-sm">
                    <option value="en">English</option>
                    <option value="hi">हिन्दी</option>
                    <option value="mr">मराठी</option>
                    <option value="pa">ਪੰਜਾਬੀ</option>
                    <option value="hr">हरियाणवी</option>
                </select>
            </div>

            {/* Messages area */}
            <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-3">
                {messages.length === 0 && (
                    <div className="flex flex-col items-center justify-center flex-1 gap-4 py-8">
                        <div className="bg-green-100 p-4 rounded-full">
                            <Sparkles size={32} className="text-green-600" />
                        </div>
                        <p className="text-stone-500 text-sm text-center">Ask about crop prices, when to sell, or market scenarios!</p>
                        <div className="flex flex-wrap gap-2 justify-center mt-2">
                            {suggestedPrompts.map((p, i) => (
                                <button key={i} onClick={() => sendMsg(p)}
                                    className="text-xs bg-white border border-green-200 text-green-700 px-3 py-1.5 rounded-full hover:bg-green-50 shadow-sm transition-all">
                                    {p}
                                </button>
                            ))}
                        </div>
                    </div>
                )}
                {messages.map((m, i) => (
                    <div key={i} className={`flex gap-2 ${m.role === 'user' ? 'flex-row-reverse' : ''}`}>
                        <div className={`w-7 h-7 rounded-full flex items-center justify-center shrink-0 ${
                            m.role === 'user' ? 'bg-green-600 text-white' : 'bg-stone-200 text-stone-600'
                        }`}>
                            {m.role === 'user' ? <User size={14} /> : <Bot size={14} />}
                        </div>
                        <div className={`p-3 rounded-2xl text-sm max-w-[80%] ${
                            m.role === 'user'
                                ? 'bg-green-600 text-white rounded-tr-sm'
                                : 'bg-white border border-stone-200 shadow-sm rounded-tl-sm text-stone-700'
                        }`}>
                            <ReactMarkdown
                                components={{
                                    p: ({node, ...props}) => <p className="mb-2 last:mb-0 leading-relaxed" {...props} />,
                                    strong: ({node, ...props}) => <strong className="font-bold" {...props} />,
                                    ul: ({node, ...props}) => <ul className="list-disc pl-4 mb-2" {...props} />,
                                    ol: ({node, ...props}) => <ol className="list-decimal pl-4 mb-2" {...props} />,
                                    li: ({node, ...props}) => <li className="mb-1" {...props} />,
                                }}
                            >
                                {m.content}
                            </ReactMarkdown>

                            {m.mode === 'rule_based' && (
                                <div className={`mt-2 text-[10px] pt-1 border-t ${
                                    m.role === 'user' ? 'border-green-500 text-green-200' : 'border-stone-200 text-stone-400'
                                }`}>
                                    ⚡ Basic answers — AI assistant unavailable
                                </div>
                            )}
                            {m.mode === 'gemini' && (
                                <div className="mt-2 text-[10px] pt-1 border-t border-stone-200 text-green-600">
                                    ✨ Powered by Gemini AI
                                </div>
                            )}
                            {m.tools && m.tools.length > 0 && (
                                <div className="mt-2 flex gap-1 flex-wrap">
                                    {m.tools.map((t: string, j: number) => (
                                        <span key={j} className="text-[10px] bg-green-100 text-green-700 px-1.5 py-0.5 rounded-full font-medium">
                                            🔧 {t}
                                        </span>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                ))}
                {(loading || isProcessing) && (
                    <div className="flex gap-2">
                        <div className="w-7 h-7 rounded-full flex items-center justify-center bg-stone-200 text-stone-600 shrink-0">
                            <Bot size={14} />
                        </div>
                        <div className="p-3 rounded-2xl rounded-tl-sm bg-white border border-stone-200 shadow-sm">
                            <div className="flex gap-1">
                                <div className="w-2 h-2 bg-green-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                <div className="w-2 h-2 bg-green-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                <div className="w-2 h-2 bg-green-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                            </div>
                        </div>
                    </div>
                )}
                <div ref={scrollRef} />
            </div>

            {isOffline && (
                <div className="bg-red-50 text-red-700 text-xs p-2 text-center border-t border-red-200 font-medium">
                    📡 Offline mode — Chat is disabled
                </div>
            )}

            {/* Input bar */}
            <div className="p-3 bg-white border-t border-stone-200">
                <div className="flex items-center gap-2 bg-stone-50 border border-stone-200 rounded-full px-3 py-1.5">
                    <button
                        onClick={toggleRecording}
                        disabled={isOffline || isProcessing}
                        className={`p-1.5 rounded-full transition-all disabled:opacity-50 ${
                            isRecording ? 'bg-red-500 text-white animate-pulse' : 'text-stone-500 hover:text-green-600'
                        }`}
                    >
                        {isProcessing ? (
                            <Loader2 size={18} className="animate-spin text-green-600" />
                        ) : isRecording ? (
                            <Mic size={18} />
                        ) : (
                            <Mic size={18} />
                        )}
                    </button>
                    
                    <input
                        type="text"
                        value={input}
                        onChange={e => setInput(e.target.value)}
                        onKeyDown={e => e.key === 'Enter' && sendMsg(input)}
                        disabled={isOffline || isProcessing}
                        placeholder={isOffline ? "Offline..." : isProcessing ? "Processing voice..." : "Kuch poochhiye..."}
                        className="flex-1 text-sm outline-none bg-transparent disabled:text-stone-400"
                    />
                    <button
                        onClick={() => sendMsg(input)}
                        disabled={isOffline || !input.trim() || loading || isProcessing}
                        className="bg-green-500 text-white p-2 rounded-full disabled:opacity-40 hover:bg-green-600 transition-all"
                    >
                        <Send size={16} />
                    </button>
                </div>
            </div>
        </div>
    );
}
