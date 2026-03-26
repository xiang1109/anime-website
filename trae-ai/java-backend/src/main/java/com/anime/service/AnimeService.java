package com.anime.service;

import com.anime.entity.Anime;
import com.anime.repository.AnimeRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class AnimeService {

    private final AnimeRepository animeRepository;

    public AnimeService(AnimeRepository animeRepository) {
        this.animeRepository = animeRepository;
    }

    public Map<String, Object> getAnimeList(int page, int limit, String sort) {
        Pageable pageable = PageRequest.of(page - 1, limit);
        Page<Anime> animePage;

        if ("year".equals(sort)) {
            animePage = animeRepository.findAll(pageable);
        } else if ("name".equals(sort)) {
            animePage = animeRepository.findAll(pageable);
        } else {
            animePage = animeRepository.findAllByOrderByAverageRatingDescRatingCountDesc(pageable);
        }

        Map<String, Object> result = new HashMap<>();
        result.put("animes", animePage.getContent());
        Map<String, Object> pagination = new HashMap<>();
        pagination.put("total", animePage.getTotalElements());
        pagination.put("page", page);
        pagination.put("limit", limit);
        pagination.put("totalPages", animePage.getTotalPages());
        result.put("pagination", pagination);

        return result;
    }

    public Anime getAnimeDetail(Long id) {
        return animeRepository.findById(id).orElseThrow(() -> new RuntimeException("动漫不存在"));
    }

    public Map<String, Object> searchAnime(String keyword, Integer year, String status, String studio, int page, int limit) {
        Pageable pageable = PageRequest.of(page - 1, limit);
        Page<Anime> animePage = animeRepository.searchAnime(keyword, year, status, studio, pageable);

        Map<String, Object> result = new HashMap<>();
        result.put("animes", animePage.getContent());
        Map<String, Object> pagination = new HashMap<>();
        pagination.put("total", animePage.getTotalElements());
        pagination.put("page", page);
        pagination.put("limit", limit);
        pagination.put("totalPages", animePage.getTotalPages());
        result.put("pagination", pagination);

        return result;
    }

    public Map<String, List<?>> getFilterOptions() {
        Map<String, List<?>> options = new HashMap<>();
        options.put("years", animeRepository.findDistinctYears());
        options.put("statuses", animeRepository.findDistinctStatuses());
        options.put("studios", animeRepository.findDistinctStudios());
        return options;
    }

    public void updateAnimeRating(Long animeId, double avgRating, long count) {
        Anime anime = animeRepository.findById(animeId).orElse(null);
        if (anime != null) {
            java.math.BigDecimal bd = java.math.BigDecimal.valueOf(avgRating);
            anime.setAverageRating(bd);
            anime.setRatingCount((int) count);
            animeRepository.save(anime);
        }
    }
}
