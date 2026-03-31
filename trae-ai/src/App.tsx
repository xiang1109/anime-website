import { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import LoginModal from './components/LoginModal';
import RegisterModal from './components/RegisterModal';
import SearchPage from './pages/SearchPage';
import AdminPage from './pages/AdminPage';
import RankingPage from './pages/RankingPage';
import RecentPage from './pages/RecentPage';
import OngoingPage from './pages/OngoingPage';
import CompletedPage from './pages/CompletedPage';
import ChinesePage from './pages/ChinesePage';
import JapanesePage from './pages/JapanesePage';
import TheaterPage from './pages/TheaterPage';
import DailyPage from './pages/DailyPage';
import { useAuth } from './context/AuthContext';

const HomePage: React.FC = () => {
  return <Navigate to="/ranking" replace />;
};

const App: React.FC = () => {
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const { user } = useAuth();

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-background relative">
        <Navbar
          onLoginClick={() => setShowLogin(true)}
          onRegisterClick={() => setShowRegister(true)}
        />

        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/ranking" element={<RankingPage />} />
          <Route path="/search" element={<SearchPage />} />
          <Route path="/recent" element={<RecentPage />} />
          <Route path="/ongoing" element={<OngoingPage />} />
          <Route path="/completed" element={<CompletedPage />} />
          <Route path="/chinese" element={<ChinesePage />} />
          <Route path="/japanese" element={<JapanesePage />} />
          <Route path="/theater" element={<TheaterPage />} />
          <Route path="/daily" element={<DailyPage />} />
          <Route path="/admin" element={user?.isAdmin ? <AdminPage /> : <Navigate to="/" replace />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>

        <footer className="bg-surface border-t border-border py-8 mt-12">
          <div className="container mx-auto px-4 text-center text-text-secondary">
            <p>动漫搜索系统 - 帮助你找到喜欢的动漫作品</p>
            <p className="text-sm mt-2">数据来源：网络收集整理，仅供学习交流使用</p>
          </div>
        </footer>

        <LoginModal
          isOpen={showLogin}
          onClose={() => setShowLogin(false)}
          onSwitchToRegister={() => {
            setShowLogin(false);
            setShowRegister(true);
          }}
        />

        <RegisterModal
          isOpen={showRegister}
          onClose={() => setShowRegister(false)}
          onSwitchToLogin={() => {
            setShowRegister(false);
            setShowLogin(true);
          }}
        />
      </div>
    </BrowserRouter>
  );
};

export default App;