package com.tradeai.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("animes")
public class Anime {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private String title;
    
    private String titleJp;
    
    private String description;
    
    private String coverImage;
    
    private Integer episodes;
    
    private String status;
    
    private Integer releaseYear;
    
    private String studio;
    
    private String genre;
    
    @TableField("average_rating")
    private Double averageRating;
    
    @TableField("rating_count")
    private Integer ratingCount;
    
    private String nationality;
    
    private String animeType;
    
    @TableField(value = "created_at", fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
    
    @TableField(value = "updated_at", fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updatedAt;
    
    @TableLogic
    private Integer deleted;
}
