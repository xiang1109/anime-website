import AnimeListPage from '../components/AnimeListPage';

const RecentPage: React.FC = () => {
  return (
    <AnimeListPage
      title="新番动漫"
      description="最近2个月上映的动漫作品"
      apiEndpoint="/api/anime/recent"
    />
  );
};

export default RecentPage;