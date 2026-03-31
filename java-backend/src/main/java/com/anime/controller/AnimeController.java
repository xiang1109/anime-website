package com.anime.controller;

import com.anime.dto.ApiResponse;
import com.anime.dto.CommentRequest;
import com.anime.dto.RatingRequest;
import com.anime.entity.Anime;
import com.anime.entity.Comment;
import com.anime.service.AnimeService;
import com.anime.service.CommentService;
import com.anime.service.RatingService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/anime")
public class AnimeController {

    private final AnimeService animeService;
    private final RatingService ratingService;
    private final CommentService commentService;

    public AnimeController(AnimeService animeService, RatingService ratingService, CommentService commentService) {
        this.animeService = animeService;
        this.ratingService = ratingService;
        this.commentService = commentService;
    }

    @GetMapping
    public ResponseEntity<ApiResponse<Map<String, Object>>> getAnimeList(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int limit,
            @RequestParam(defaultValue = "") String sort
    ) {
        Map<String, Object> result = animeService.getAnimeList(page, limit, sort);
        return ResponseEntity.ok(ApiResponse.success(result));
    }

    @GetMapping("/search")
    public ResponseEntity<ApiResponse<Map<String, Object>>> searchAnime(
            @RequestParam(defaultValue = "") String keyword,
            @RequestParam(required = false) Integer year,
            @RequestParam(defaultValue = "") String status,
            @RequestParam(defaultValue = "") String studio,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int limit
    ) {
        Map<String, Object> result = animeService.searchAnime(keyword, year, status, studio, page, limit);
        return ResponseEntity.ok(ApiResponse.success(result));
    }

    @GetMapping("/filter-options")
    public ResponseEntity<ApiResponse<Map<String, List<?>>>> getFilterOptions() {
        Map<String, List<?>> options = animeService.getFilterOptions();
        return ResponseEntity.ok(ApiResponse.success(options));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<Anime>> getAnimeDetail(@PathVariable Long id) {
        try {
            Anime anime = animeService.getAnimeDetail(id);
            return ResponseEntity.ok(ApiResponse.success(anime));
        } catch (RuntimeException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(ApiResponse.error(e.getMessage()));
        }
    }

    @GetMapping("/{id}/user-rating")
    public ResponseEntity<ApiResponse<Map<String, Integer>>> getUserRating(
            @PathVariable Long id,
            @RequestAttribute("userId") Long userId
    ) {
        Integer rating = ratingService.getUserRating(userId, id);
        Map<String, Integer> result = new HashMap<>();
        result.put("rating", rating);
        return ResponseEntity.ok(ApiResponse.success(result));
    }

    @PostMapping("/{id}/rate")
    public ResponseEntity<ApiResponse<Map<String, Object>>> rateAnime(
            @PathVariable Long id,
            @Valid @RequestBody RatingRequest request,
            @RequestAttribute("userId") Long userId
    ) {
        try {
            Map<String, Object> result = ratingService.rateAnime(userId, id, request.getRating());
            return ResponseEntity.ok(ApiResponse.success("评分成功", result));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(ApiResponse.error(e.getMessage()));
        }
    }

    @GetMapping("/{id}/comments")
    public ResponseEntity<ApiResponse<Map<String, Object>>> getComments(
            @PathVariable Long id,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int limit
    ) {
        Map<String, Object> result = commentService.getComments(id, page, limit);
        return ResponseEntity.ok(ApiResponse.success(result));
    }

    @PostMapping("/{id}/comments")
    public ResponseEntity<ApiResponse<Comment>> addComment(
            @PathVariable Long id,
            @Valid @RequestBody CommentRequest request,
            @RequestAttribute("userId") Long userId
    ) {
        Comment comment = commentService.addComment(userId, id, request.getContent());
        return ResponseEntity.ok(ApiResponse.success("评论发表成功", comment));
    }
}
