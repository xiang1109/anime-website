import AnimeListPage from '../components/AnimeListPage';

const DailyPage: React.FC = () => {
  return (
    <AnimeListPage
      title="每日推荐"
      description="每日精选推荐动漫"
      apiEndpoint="/api/anime"
    />
  );
};

export default DailyPage;