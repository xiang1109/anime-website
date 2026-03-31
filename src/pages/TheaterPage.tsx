import AnimeListPage from '../components/AnimeListPage';

const TheaterPage: React.FC = () => {
  return (
    <AnimeListPage
      title="剧场版"
      description="动漫剧场版作品"
      apiEndpoint="/api/anime/theater"
    />
  );
};

export default TheaterPage;