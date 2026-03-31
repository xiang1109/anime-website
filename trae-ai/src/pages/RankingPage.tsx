import AnimeListPage from '../components/AnimeListPage';

const RankingPage: React.FC = () => {
  return (
    <AnimeListPage
      title="动漫排行"
      description="根据评分和评论数量排序的动漫排行榜"
      apiEndpoint="/api/anime"
    />
  );
};

export default RankingPage;
