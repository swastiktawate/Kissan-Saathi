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
import ColdStorage from './pages/ColdStorage';
import PoolingList from './pages/PoolingList';
import PoolingCreate from './pages/PoolingCreate';
import Profile from './pages/Profile';

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
          <Route path="/cold-storage" element={<ColdStorage />} />
          <Route path="/pooling" element={<PoolingList />} />
          <Route path="/pooling/create" element={<PoolingCreate />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
        <BottomNav />
      </div>
    </BrowserRouter>
  );
}

export default App;
