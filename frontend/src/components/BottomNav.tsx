import { Link, useLocation } from 'react-router-dom';

export default function BottomNav() {
    const loc = useLocation().pathname;
    
    return (
        <div className="fixed bottom-0 w-full max-w-[360px] bg-white border-t border-stone-200 flex justify-between px-4 py-2 text-xs text-stone-500">
            <Link to="/" className={`flex flex-col items-center ${loc === '/' ? 'text-stone-900 font-bold' : ''}`}>
                <span>Home</span>
            </Link>
            <Link to="/mandis" className={`flex flex-col items-center ${loc === '/mandis' ? 'text-stone-900 font-bold' : ''}`}>
                <span>Mandis</span>
            </Link>
            <Link to="/chat" className={`flex flex-col items-center ${loc === '/chat' ? 'text-stone-900 font-bold' : ''}`}>
                <span>Chat</span>
            </Link>
            <Link to="/detail" className={`flex flex-col items-center ${loc === '/detail' ? 'text-stone-900 font-bold' : ''}`}>
                <span>Insights</span>
            </Link>
        </div>
    );
}
