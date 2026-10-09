import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Detail from './pages/Detail';
import Mandis from './pages/Mandis';
import Insights from './pages/Insights';
import BottomNav from './components/BottomNav';
import ChatPanel from './components/ChatPanel';
import OfflineBanner from './components/OfflineBanner';
import FloatingVoiceOrb from './components/FloatingVoiceOrb';
import Predict from './pages/Predict';

function App() {
  return (
    <BrowserRouter>
      <OfflineBanner />
      <div className="max-w-[430px] mx-auto bg-white min-h-screen relative pb-16 shadow-xl">
        <FloatingVoiceOrb />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/predict" element={<Predict />} />
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
