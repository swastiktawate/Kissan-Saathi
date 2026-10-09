import { Link, useLocation } from 'react-router-dom';
import { Home, Store, MessageCircle, BarChart3 } from 'lucide-react';

export default function BottomNav() {
    const loc = useLocation().pathname;

    const navItems = [
        { to: '/', label: 'Home', icon: Home },
        { to: '/mandis', label: 'Mandis', icon: Store },
        { to: '/chat', label: 'Chat', icon: MessageCircle },
        { to: '/insights', label: 'Insights', icon: BarChart3 },
    ];

    return (
        <div className="fixed bottom-0 w-full max-w-[430px] bg-white border-t border-stone-200 flex justify-around py-2 z-50">
            {navItems.map(item => {
                const active = loc === item.to;
                const Icon = item.icon;
                return (
                    <Link key={item.to} to={item.to}
                        className={`flex flex-col items-center gap-0.5 px-3 py-1 rounded-lg transition-all ${
                            active ? 'text-green-700' : 'text-stone-400 hover:text-stone-600'
                        }`}
                    >
                        <Icon size={20} strokeWidth={active ? 2.5 : 1.5} />
                        <span className={`text-[10px] ${active ? 'font-bold' : 'font-medium'}`}>{item.label}</span>
                    </Link>
                );
            })}
        </div>
    );
}
