import AnimeListPage from '../components/AnimeListPage';

const HiddenGemsPage: React.FC = () => {
  return (
    <AnimeListPage
      title="Table冷门佳作"
      description="来自B站的高分冷门动漫，不容错过的宝藏作品"
      apiEndpoint="/api/anime/hidden-gems"
    />
  );
};

export default HiddenGemsPage;
