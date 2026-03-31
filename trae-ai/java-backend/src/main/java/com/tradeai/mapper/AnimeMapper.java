package com.tradeai.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.tradeai.entity.Anime;
import org.apache.ibatis.annotations.Param;
import java.util.List;

public interface AnimeMapper extends BaseMapper<Anime> {
    List<Anime> selectByKeyword(
        @Param("keyword") String keyword,
        @Param("year") Integer year,
        @Param("status") String status,
        @Param("studio") String studio,
        @Param("nationality") String nationality,
        @Param("animeType") String animeType,
        @Param("orderByRating") Boolean orderByRating,
        @Param("orderByCreated") Boolean orderByCreated,
        @Param("offset") Integer offset,
        @Param("limit") Integer limit
    );
    
    Long countByKeyword(
        @Param("keyword") String keyword,
        @Param("year") Integer year,
        @Param("status") String status,
        @Param("studio") String studio,
        @Param("nationality") String nationality,
        @Param("animeType") String animeType
    );
    
    List<Anime> selectRandom(@Param("limit") Integer limit);
    
    List<Anime> selectByRecentMonth(@Param("offset") Integer offset, @Param("limit") Integer limit);
    
    int updateRating(@Param("animeId") Long animeId, @Param("averageRating") Double averageRating);
}
