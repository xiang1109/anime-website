import AnimeListPage from '../components/AnimeListPage';

const ChinesePage: React.FC = () => {
  return (
    <AnimeListPage
      title="国产动漫"
      description="国产原创动漫作品"
      apiEndpoint="/api/anime/chinese"
    />
  );
};

export default ChinesePage;