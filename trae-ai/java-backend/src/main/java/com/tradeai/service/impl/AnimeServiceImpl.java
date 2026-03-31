package com.tradeai.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.tradeai.entity.Anime;
import com.tradeai.mapper.AnimeMapper;
import com.tradeai.service.AnimeService;
import com.tradeai.dto.AnimeSearchDTO;
import com.tradeai.vo.PagedResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class AnimeServiceImpl extends ServiceImpl<AnimeMapper, Anime> implements AnimeService {
    
    @Autowired
    private AnimeMapper animeMapper;
    
    @Override
    public PagedResponse<Anime> searchAnime(AnimeSearchDTO searchDTO) {
        int offset = (searchDTO.getPage() - 1) * searchDTO.getSize();
        
        List<Anime> animes = animeMapper.selectByKeyword(
            searchDTO.getKeyword(),
            searchDTO.getYear(),
            searchDTO.getStatus(),
            searchDTO.getStudio(),
            searchDTO.getNationality(),
            searchDTO.getAnimeType(),
            searchDTO.getOrderByRating(),
            searchDTO.getOrderByCreated(),
            offset,
            searchDTO.getSize()
        );
        
        Long total = animeMapper.countByKeyword(
            searchDTO.getKeyword(),
            searchDTO.getYear(),
            searchDTO.getStatus(),
            searchDTO.getStudio(),
            searchDTO.getNationality(),
            searchDTO.getAnimeType()
        );
        
        int totalPages = (int) Math.ceil((double) total / searchDTO.getSize());
        
        Map<String, Object> pagination = new HashMap<>();
        pagination.put("currentPage", searchDTO.getPage());
        pagination.put("totalPages", totalPages);
        pagination.put("total", total);
        pagination.put("size", searchDTO.getSize());
        
        PagedResponse<Anime> response = new PagedResponse<>();
        response.setData(animes);
        response.setPagination(pagination);
        
        return response;
    }
    
    @Override
    public PagedResponse<Anime> getAnimeList(int page, int size) {
        AnimeSearchDTO searchDTO = new AnimeSearchDTO();
        searchDTO.setPage(page);
        searchDTO.setSize(size);
        return searchAnime(searchDTO);
    }
    
    @Override
    public PagedResponse<Anime> getAnimeRanking(int page, int size) {
        AnimeSearchDTO searchDTO = new AnimeSearchDTO();
        searchDTO.setPage(page);
        searchDTO.setSize(size);
        searchDTO.setOrderByRating(true);
        return searchAnime(searchDTO);
    }
    
    @Override
    public PagedResponse<Anime> getRecentAnime(int page, int size) {
        int offset = (page - 1) * size;
        List<Anime> animes = animeMapper.selectByRecentMonth(offset, size);
        
        Long total = animeMapper.countByKeyword(null, null, null, null, null, null);
        int totalPages = (int) Math.ceil((double) total / size);
        
        Map<String, Object> pagination = new HashMap<>();
        pagination.put("currentPage", page);
        pagination.put("totalPages", totalPages);
        pagination.put("total", total);
        pagination.put("size", size);
        
        PagedResponse<Anime> response = new PagedResponse<>();
        response.setData(animes);
        response.setPagination(pagination);
        
        return response;
    }
    
    @Override
    public PagedResponse<Anime> getOngoingAnime(int page, int size) {
        AnimeSearchDTO searchDTO = new AnimeSearchDTO();
        searchDTO.setPage(page);
        searchDTO.setSize(size);
        searchDTO.setStatus("连载中");
        searchDTO.setOrderByRating(true);
        return searchAnime(searchDTO);
    }
    
    @Override
    public PagedResponse<Anime> getCompletedAnime(int page, int size) {
        AnimeSearchDTO searchDTO = new AnimeSearchDTO();
        searchDTO.setPage(page);
        searchDTO.setSize(size);
        searchDTO.setStatus("已完结");
        searchDTO.setOrderByRating(true);
        return searchAnime(searchDTO);
    }
    
    @Override
    public PagedResponse<Anime> getChineseAnime(int page, int size) {
        AnimeSearchDTO searchDTO = new AnimeSearchDTO();
        searchDTO.setPage(page);
        searchDTO.setSize(size);
        searchDTO.setNationality("国产");
        searchDTO.setOrderByRating(true);
        return searchAnime(searchDTO);
    }
    
    @Override
    public PagedResponse<Anime> getJapaneseAnime(int page, int size) {
        AnimeSearchDTO searchDTO = new AnimeSearchDTO();
        searchDTO.setPage(page);
        searchDTO.setSize(size);
        searchDTO.setNationality("日本");
        searchDTO.setOrderByRating(true);
        return searchAnime(searchDTO);
    }
    
    @Override
    public PagedResponse<Anime> getTheaterAnime(int page, int size) {
        AnimeSearchDTO searchDTO = new AnimeSearchDTO();
        searchDTO.setPage(page);
        searchDTO.setSize(size);
        searchDTO.setAnimeType("剧场版");
        searchDTO.setOrderByRating(true);
        return searchAnime(searchDTO);
    }
    
    @Override
    public List<Anime> getDailyRecommendation() {
        return animeMapper.selectRandom(5);
    }
    
    @Override
    @Transactional
    public boolean rateAnime(Long animeId, Double rating) {
        Anime anime = getById(animeId);
        if (anime == null) {
            return false;
        }
        
        double currentTotal = (anime.getAverageRating() != null ? anime.getAverageRating() : 0) * 
                            (anime.getRatingCount() != null ? anime.getRatingCount() : 0);
        int newCount = (anime.getRatingCount() != null ? anime.getRatingCount() : 0) + 1;
        double newAverage = (currentTotal + rating) / newCount;
        
        return animeMapper.updateRating(animeId, newAverage) > 0;
    }
}
