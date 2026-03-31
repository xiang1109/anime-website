import AnimeListPage from '../components/AnimeListPage';

const JapanesePage: React.FC = () => {
  return (
    <AnimeListPage
      title="日本动漫"
      description="日本动漫作品"
      apiEndpoint="/api/anime/japanese"
    />
  );
};

export default JapanesePage;