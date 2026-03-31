import AnimeListPage from '../components/AnimeListPage';

const OngoingPage: React.FC = () => {
  return (
    <AnimeListPage
      title="连载动漫"
      description="正在连载中的动漫作品"
      apiEndpoint="/api/anime/ongoing"
    />
  );
};

export default OngoingPage;