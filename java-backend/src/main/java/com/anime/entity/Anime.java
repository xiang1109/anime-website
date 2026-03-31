package com.anime.entity;

import lombok.Data;
import javax.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "animes")
public class Anime {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 255)
    private String title;

    @Column(name = "title_jp", length = 255)
    private String titleJp;

    @Column(columnDefinition = "TEXT")
    private String description;

    @Column(name = "cover_image", length = 255)
    private String coverImage;

    private Integer episodes;

    @Column(length = 50)
    private String status;

    @Column(name = "release_year")
    private Integer releaseYear;

    @Column(length = 100)
    private String studio;

    @Column(length = 50)
    private String nationality;

    @Column(name = "anime_type", length = 50)
    private String animeType;

    @Column(name = "is_movie")
    private Boolean isMovie;

    @Column(name = "average_rating", precision = 3, scale = 2)
    private BigDecimal averageRating;

    @Column(name = "rating_count")
    private Integer ratingCount;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
}
