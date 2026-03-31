package com.tradeai.dto;

import lombok.Data;

@Data
public class AnimeSearchDTO {
    private String keyword;
    private Integer year;
    private String status;
    private String studio;
    private String nationality;
    private String animeType;
    private int page = 1;
    private int size = 12;
    private Boolean orderByRating = false;
    private Boolean orderByCreated = false;
}
