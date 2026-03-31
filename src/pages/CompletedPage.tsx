import AnimeListPage from '../components/AnimeListPage';

const CompletedPage: React.FC = () => {
  return (
    <AnimeListPage
      title="完结动漫"
      description="已经完结的动漫作品"
      apiEndpoint="/api/anime/completed"
    />
  );
};

export default CompletedPage;