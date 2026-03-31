import AnimeListPage from '../components/AnimeListPage';

const RecentPage: React.FC = () => {
  return (
    <AnimeListPage
      title="新番动漫"
      description="最新更新的动漫作品"
      apiEndpoint="/api/anime"
    />
  );
};

export default RecentPage;