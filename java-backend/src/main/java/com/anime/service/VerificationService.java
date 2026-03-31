package com.anime.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.TimeUnit;

@Service
public class VerificationService {

    @Autowired
    private JavaMailSender mailSender;
    
    // 存储验证码: email -> (code, timestamp)
    private final Map<String, VerificationCode> codeCache = new ConcurrentHashMap<>();
    
    // 存储滑块验证令牌: token -> isValid
    private final Map<String, Boolean> sliderCache = new ConcurrentHashMap<>();
    
    // 验证码过期时间: 5分钟
    private static final long CODE_EXPIRE_TIME = TimeUnit.MINUTES.toMillis(5);
    
    // 滑块验证过期时间: 10分钟
    private static final long SLIDER_EXPIRE_TIME = TimeUnit.MINUTES.toMillis(10);

    // 发送邮箱验证码
    public String sendEmailCode(String email) {
        // 生成6位随机验证码
        String code = generateRandomCode();
        
        // 存储验证码
        codeCache.put(email, new VerificationCode(code, System.currentTimeMillis()));
        
        // 发送邮箱
        try {
            SimpleMailMessage message = new SimpleMailMessage();
            message.setFrom("your-email@qq.com");
            message.setTo(email);
            message.setSubject("【动漫评分】注册验证码");
            message.setText("您的注册验证码为: " + code + "，有效期5分钟，请及时使用。");
            mailSender.send(message);
            System.out.println("【邮箱发送】邮箱: " + email + ", 验证码: " + code);
        } catch (Exception e) {
            System.err.println("邮箱发送失败: " + e.getMessage());
            throw new RuntimeException("发送验证码失败，请检查邮箱地址是否正确");
        }
        
        return code;
    }

    // 验证邮箱验证码
    public boolean verifyEmailCode(String email, String code) {
        VerificationCode storedCode = codeCache.get(email);
        if (storedCode == null) {
            return false;
        }
        
        // 检查是否过期
        if (System.currentTimeMillis() - storedCode.timestamp > CODE_EXPIRE_TIME) {
            codeCache.remove(email);
            return false;
        }
        
        boolean isValid = storedCode.code.equals(code);
        if (isValid) {
            // 验证成功后删除验证码
            codeCache.remove(email);
        }
        return isValid;
    }

    // 生成滑块验证令牌
    public String generateSliderToken() {
        String token = UUID.randomUUID().toString();
        sliderCache.put(token, true);
        return token;
    }

    // 验证滑块令牌
    public boolean verifySliderToken(String token) {
        Boolean isValid = sliderCache.get(token);
        if (isValid == null || !isValid) {
            return false;
        }
        // 验证成功后删除，防止重复使用
        sliderCache.remove(token);
        return true;
    }

    // 清理过期数据
    public void cleanExpiredData() {
        long now = System.currentTimeMillis();
        // 清理过期验证码
        codeCache.entrySet().removeIf(entry -> 
            now - entry.getValue().timestamp > CODE_EXPIRE_TIME
        );
        // 这里简化滑块过期处理，实际可定时清理
    }

    private String generateRandomCode() {
        Random random = new Random();
        StringBuilder code = new StringBuilder();
        for (int i = 0; i < 6; i++) {
            code.append(random.nextInt(10));
        }
        return code.toString();
    }

    // 内部类存储验证码和时间戳
    private static class VerificationCode {
        String code;
        long timestamp;

        VerificationCode(String code, long timestamp) {
            this.code = code;
            this.timestamp = timestamp;
        }
    }
}
