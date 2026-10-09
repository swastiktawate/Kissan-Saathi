import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Detail from './pages/Detail';
import Mandis from './pages/Mandis';
import Insights from './pages/Insights';
import BottomNav from './components/BottomNav';
import ChatPanel from './components/ChatPanel';
import OfflineBanner from './components/OfflineBanner';

function App() {
  return (
    <BrowserRouter>
      <OfflineBanner />
      <div className="max-w-[360px] mx-auto bg-canvas min-h-screen relative pb-16 pt-6 shadow-lg">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/detail" element={<Detail />} />
          <Route path="/mandis" element={<Mandis />} />
          <Route path="/insights" element={<Insights />} />
          <Route path="/chat" element={<ChatPanel />} />
        </Routes>
        <BottomNav />
      </div>
    </BrowserRouter>
  );
}

export default App;
