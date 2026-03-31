package com.tradeai.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.tradeai.entity.Comment;
import org.apache.ibatis.annotations.Param;
import java.util.List;

public interface CommentMapper extends BaseMapper<Comment> {
    List<Comment> selectByAnimeId(@Param("animeId") Long animeId, @Param("offset") Integer offset, @Param("limit") Integer limit);
    long countByAnimeId(@Param("animeId") Long animeId);
}
