package com.tradeai.service;

import com.tradeai.entity.Comment;
import java.util.List;

public interface CommentService {
    Comment createComment(Comment comment);
    Comment addComment(Comment comment);
    List<Comment> getCommentsByAnimeId(Long animeId, int page, int size);
    long getCommentCountByAnimeId(Long animeId);
    void deleteComment(Long id);
}
