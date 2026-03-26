package com.anime.repository;

import com.anime.entity.Comment;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

@Repository
public interface CommentRepository extends JpaRepository<Comment, Long> {

    @Query("SELECT c FROM Comment c WHERE c.animeId = :animeId ORDER BY c.createdAt DESC")
    Page<Comment> findByAnimeId(@Param("animeId") Long animeId, Pageable pageable);

    @Query("SELECT COUNT(c) FROM Comment c WHERE c.animeId = :animeId")
    Long countByAnimeId(@Param("animeId") Long animeId);
}
