package com.anime;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class AnimeRatingApplication {

    public static void main(String[] args) {
        SpringApplication.run(AnimeRatingApplication.class, args);
        System.out.println("动漫评分系统 - Spring Boot后端启动成功!");
    }

}
