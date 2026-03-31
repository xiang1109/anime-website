package com.anime.controller;

import com.anime.dto.ApiResponse;
import com.anime.entity.Anime;
import com.anime.service.AnimeService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/admin")
public class AdminController {

    private final AnimeService animeService;

    public AdminController(AnimeService animeService) {
        this.animeService = animeService;
    }

    @PutMapping("/anime/{id}")
    public ResponseEntity<ApiResponse<Anime>> updateAnime(
            @PathVariable Long id,
            @RequestBody Anime animeRequest
    ) {
        try {
            Anime anime = animeService.getAnimeDetail(id);
            if (anime == null) {
                return ResponseEntity.status(404).body(ApiResponse.error("动漫不存在"));
            }

            if (animeRequest.getTitle() != null) {
                anime.setTitle(animeRequest.getTitle());
            }
            if (animeRequest.getTitleJp() != null) {
                anime.setTitleJp(animeRequest.getTitleJp());
            }
            if (animeRequest.getDescription() != null) {
                anime.setDescription(animeRequest.getDescription());
            }
            if (animeRequest.getCoverImage() != null) {
                anime.setCoverImage(animeRequest.getCoverImage());
            }
            if (animeRequest.getEpisodes() != null) {
                anime.setEpisodes(animeRequest.getEpisodes());
            }
            if (animeRequest.getStatus() != null) {
                anime.setStatus(animeRequest.getStatus());
            }
            if (animeRequest.getReleaseYear() != null) {
                anime.setReleaseYear(animeRequest.getReleaseYear());
            }
            if (animeRequest.getStudio() != null) {
                anime.setStudio(animeRequest.getStudio());
            }
            if (animeRequest.getNationality() != null) {
                anime.setNationality(animeRequest.getNationality());
            }
            if (animeRequest.getAnimeType() != null) {
                anime.setAnimeType(animeRequest.getAnimeType());
            }
            if (animeRequest.getIsMovie() != null) {
                anime.setIsMovie(animeRequest.getIsMovie());
            }
            if (animeRequest.getAverageRating() != null) {
                anime.setAverageRating(animeRequest.getAverageRating());
            }
            if (animeRequest.getRatingCount() != null) {
                anime.setRatingCount(animeRequest.getRatingCount());
            }

            Anime updatedAnime = animeService.updateAnime(anime);
            return ResponseEntity.ok(ApiResponse.success("更新成功", updatedAnime));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(ApiResponse.error(e.getMessage()));
        }
    }

    @PostMapping("/anime/batch-insert")
    public ResponseEntity<ApiResponse<String>> batchInsertAnime(
            @RequestBody List<Anime> animeList
    ) {
        try {
            int insertCount = 0;
            for (Anime anime : animeList) {
                animeService.createAnime(anime);
                insertCount++;
            }
            return ResponseEntity.ok(ApiResponse.success("批量插入成功", "共插入 " + insertCount + " 条记录"));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(ApiResponse.error(e.getMessage()));
        }
    }

    @DeleteMapping("/anime/clear")
    public ResponseEntity<ApiResponse<String>> clearAllAnime() {
        try {
            animeService.clearAllAnime();
            return ResponseEntity.ok(ApiResponse.success("清空成功", "所有动漫数据已清空"));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(ApiResponse.error(e.getMessage()));
        }
    }
}
