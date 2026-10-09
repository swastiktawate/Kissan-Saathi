import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Detail from './pages/Detail';
import Mandis from './pages/Mandis';
import BottomNav from './components/BottomNav';

function App() {
  return (
    <BrowserRouter>
      <div className="max-w-[360px] mx-auto bg-canvas min-h-screen relative pb-16 shadow-lg">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/detail" element={<Detail />} />
          <Route path="/mandis" element={<Mandis />} />
          <Route path="/chat" element={<div className="p-4">Chat Placeholder</div>} />
        </Routes>
        <BottomNav />
      </div>
    </BrowserRouter>
  );
}

export default App;
