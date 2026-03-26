package com.anime.service;

import com.anime.entity.Comment;
import com.anime.entity.User;
import com.anime.repository.CommentRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.Map;

@Service
public class CommentService {

    private final CommentRepository commentRepository;
    private final UserService userService;

    public CommentService(CommentRepository commentRepository, UserService userService) {
        this.commentRepository = commentRepository;
        this.userService = userService;
    }

    public Map<String, Object> getComments(Long animeId, int page, int limit) {
        Pageable pageable = PageRequest.of(page - 1, limit);
        Page<Comment> commentPage = commentRepository.findByAnimeId(animeId, pageable);

        commentPage.getContent().forEach(comment -> {
            User user = userService.findById(comment.getUserId());
            if (user != null) {
                comment.setUsername(user.getUsername());
                comment.setAvatar(user.getAvatar());
            }
        });

        Map<String, Object> result = new HashMap<>();
        result.put("comments", commentPage.getContent());
        Map<String, Object> pagination = new HashMap<>();
        pagination.put("total", commentPage.getTotalElements());
        pagination.put("page", page);
        pagination.put("limit", limit);
        pagination.put("totalPages", commentPage.getTotalPages());
        result.put("pagination", pagination);

        return result;
    }

    @Transactional
    public Comment addComment(Long userId, Long animeId, String content) {
        Comment comment = new Comment();
        comment.setUserId(userId);
        comment.setAnimeId(animeId);
        comment.setContent(content);

        comment = commentRepository.save(comment);

        User user = userService.findById(userId);
        if (user != null) {
            comment.setUsername(user.getUsername());
            comment.setAvatar(user.getAvatar());
        }

        return comment;
    }
}
