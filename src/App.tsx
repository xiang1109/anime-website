import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import SearchPage from './pages/SearchPage';
import AdminPage from './pages/AdminPage';
import AnimeManagerPage from './pages/AnimeManagerPage';
import RecentPage from './pages/RecentPage';
import OngoingPage from './pages/OngoingPage';
import CompletedPage from './pages/CompletedPage';
import TheaterPage from './pages/TheaterPage';
import DailyPage from './pages/DailyPage';
import HiddenGemsPage from './pages/HiddenGemsPage';
import ProfilePage from './pages/ProfilePage';
import AnimeDetailPage from './pages/AnimeDetailPage';
import AnimeListPage from './components/AnimeListPage';
import { AuthProvider, useAuth } from './context/AuthContext';

const HomePage: React.FC = () => {
  return (
    <AnimeListPage
      title="全部动漫"
      description="按评分排序的所有动漫作品"
      apiEndpoint="/api/anime"
    />
  );
};

const AppContent: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-background relative">
      <Header />

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/recent" element={<RecentPage />} />
        <Route path="/ongoing" element={<OngoingPage />} />
        <Route path="/completed" element={<CompletedPage />} />
        <Route path="/theater" element={<TheaterPage />} />
        <Route path="/daily" element={<DailyPage />} />
        <Route path="/hidden-gems" element={<HiddenGemsPage />} />
        <Route path="/anime/:id" element={<AnimeDetailPage />} />
        <Route path="/profile" element={user ? <ProfilePage /> : <Navigate to="/" replace />} />
        <Route path="/admin" element={user?.username === 'admin' ? <AdminPage /> : <Navigate to="/" replace />} />
        <Route path="/anime-manager" element={user?.username === 'admin' ? <AnimeManagerPage /> : <Navigate to="/" replace />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>

      <footer className="bg-surface border-t border-border py-8 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-text-muted">
          <p>动漫评分网站 - 帮助你找到喜欢的动漫作品</p>
          <p className="text-sm mt-2">数据来源：网络收集整理，仅供学习交流使用</p>
        </div>
      </footer>
    </div>
  );
};

const App: React.FC = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
