package com.tradeai.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.tradeai.entity.Anime;
import com.tradeai.dto.AnimeSearchDTO;
import com.tradeai.vo.PagedResponse;

public interface AnimeService extends IService<Anime> {
    PagedResponse<Anime> searchAnime(AnimeSearchDTO searchDTO);
    PagedResponse<Anime> getAnimeList(int page, int size);
    PagedResponse<Anime> getAnimeRanking(int page, int size);
    PagedResponse<Anime> getRecentAnime(int page, int size);
    PagedResponse<Anime> getOngoingAnime(int page, int size);
    PagedResponse<Anime> getCompletedAnime(int page, int size);
    PagedResponse<Anime> getChineseAnime(int page, int size);
    PagedResponse<Anime> getJapaneseAnime(int page, int size);
    PagedResponse<Anime> getTheaterAnime(int page, int size);
    java.util.List<Anime> getDailyRecommendation();
    boolean rateAnime(Long animeId, Double rating);
}
