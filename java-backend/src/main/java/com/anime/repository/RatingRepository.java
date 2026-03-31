package com.anime.repository;

import com.anime.entity.Rating;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface RatingRepository extends JpaRepository<Rating, Long> {

    Optional<Rating> findByUserIdAndAnimeId(Long userId, Long animeId);

    @Query("SELECT AVG(r.rating) FROM Rating r WHERE r.animeId = :animeId")
    Double calculateAverageRating(@Param("animeId") Long animeId);

    @Query("SELECT COUNT(r) FROM Rating r WHERE r.animeId = :animeId")
    Long countByAnimeId(@Param("animeId") Long animeId);

    boolean existsByUserIdAndAnimeId(Long userId, Long animeId);
}
