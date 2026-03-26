package com.anime.repository;

import com.anime.entity.Anime;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AnimeRepository extends JpaRepository<Anime, Long> {

    Page<Anime> findAllByOrderByAverageRatingDescRatingCountDesc(Pageable pageable);

    @Query("SELECT a FROM Anime a WHERE " +
           "(:keyword IS NULL OR :keyword = '' OR " +
           "a.title LIKE %:keyword% OR a.description LIKE %:keyword% OR a.studio LIKE %:keyword%) " +
           "AND (:year IS NULL OR a.releaseYear = :year) " +
           "AND (:status IS NULL OR :status = '' OR a.status = :status) " +
           "AND (:studio IS NULL OR :studio = '' OR a.studio LIKE %:studio%) " +
           "ORDER BY a.averageRating DESC, a.ratingCount DESC")
    Page<Anime> searchAnime(
            @Param("keyword") String keyword,
            @Param("year") Integer year,
            @Param("status") String status,
            @Param("studio") String studio,
            Pageable pageable
    );

    @Query("SELECT DISTINCT a.releaseYear FROM Anime a WHERE a.releaseYear IS NOT NULL ORDER BY a.releaseYear DESC")
    List<Integer> findDistinctYears();

    @Query("SELECT DISTINCT a.status FROM Anime a WHERE a.status IS NOT NULL")
    List<String> findDistinctStatuses();

    @Query("SELECT DISTINCT a.studio FROM Anime a WHERE a.studio IS NOT NULL ORDER BY a.studio")
    List<String> findDistinctStudios();
}
