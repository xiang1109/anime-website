package com.tradeai.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.tradeai.entity.Comment;
import com.tradeai.mapper.CommentMapper;
import com.tradeai.service.CommentService;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class CommentServiceImpl extends ServiceImpl<CommentMapper, Comment> implements CommentService {
    @Override
    public Comment createComment(Comment comment) {
        save(comment);
        return comment;
    }

    @Override
    public Comment addComment(Comment comment) {
        return createComment(comment);
    }

    @Override
    public List<Comment> getCommentsByAnimeId(Long animeId, int page, int size) {
        return baseMapper.selectByAnimeId(animeId, (page - 1) * size, size);
    }

    @Override
    public long getCommentCountByAnimeId(Long animeId) {
        return baseMapper.countByAnimeId(animeId);
    }

    @Override
    public void deleteComment(Long id) {
        removeById(id);
    }
}
