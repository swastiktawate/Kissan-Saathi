import { useLocation, useNavigate } from 'react-router-dom';
import { Mic } from 'lucide-react';

export default function FloatingVoiceOrb() {
    const location = useLocation();
    const navigate = useNavigate();

    // Hide when offline or on chat page
    if (!navigator.onLine || location.pathname === '/chat') return null;

    return (
        <div className="fixed bottom-[80px] left-1/2 -translate-x-1/2 w-full max-w-[430px] pointer-events-none flex justify-end pr-6 z-[9999]">
            <button
                onClick={() => navigate('/chat', { state: { autoStartMic: true } })}
                className="pointer-events-auto w-14 h-14 rounded-full text-white shadow-2xl flex items-center justify-center bg-green-600 hover:bg-green-700 transition-all focus:outline-none focus:ring-4 focus:ring-green-300"
            >
                <Mic size={24} />
            </button>
        </div>
    );
}
