package com.anime.service;

import com.anime.entity.Rating;
import com.anime.repository.RatingRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

@Service
public class RatingService {

    private final RatingRepository ratingRepository;
    private final AnimeService animeService;

    public RatingService(RatingRepository ratingRepository, AnimeService animeService) {
        this.ratingRepository = ratingRepository;
        this.animeService = animeService;
    }

    @Transactional
    public Map<String, Object> rateAnime(Long userId, Long animeId, int ratingValue) {
        Optional<Rating> existingRating = ratingRepository.findByUserIdAndAnimeId(userId, animeId);

        Rating rating;
        if (existingRating.isPresent()) {
            rating = existingRating.get();
            rating.setRating(ratingValue);
        } else {
            rating = new Rating();
            rating.setUserId(userId);
            rating.setAnimeId(animeId);
            rating.setRating(ratingValue);
        }

        ratingRepository.save(rating);

        Double avgRating = ratingRepository.calculateAverageRating(animeId);
        if (avgRating == null) {
            avgRating = 0.0;
        }
        long count = ratingRepository.countByAnimeId(animeId);

        animeService.updateAnimeRating(animeId, avgRating, count);

        Map<String, Object> result = new HashMap<>();
        result.put("message", "评分成功");
        result.put("average_rating", avgRating);
        result.put("rating_count", count);
        result.put("user_rating", ratingValue);

        return result;
    }

    public Integer getUserRating(Long userId, Long animeId) {
        Optional<Rating> rating = ratingRepository.findByUserIdAndAnimeId(userId, animeId);
        return rating.map(Rating::getRating).orElse(null);
    }
}
