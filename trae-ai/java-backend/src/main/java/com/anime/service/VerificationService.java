package com.anime.service;

import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.TimeUnit;

@Service
public class VerificationService {

    // 存储验证码: phone -> (code, timestamp)
    private final Map<String, VerificationCode> codeCache = new ConcurrentHashMap<>();
    
    // 存储滑块验证令牌: token -> isValid
    private final Map<String, Boolean> sliderCache = new ConcurrentHashMap<>();
    
    // 验证码过期时间: 5分钟
    private static final long CODE_EXPIRE_TIME = TimeUnit.MINUTES.toMillis(5);
    
    // 滑块验证过期时间: 10分钟
    private static final long SLIDER_EXPIRE_TIME = TimeUnit.MINUTES.toMillis(10);

    // 发送短信验证码
    public String sendSmsCode(String phone) {
        // 生成6位随机验证码
        String code = generateRandomCode();
        System.out.println("【模拟短信发送】手机号: " + phone + ", 验证码: " + code);
        
        // 存储验证码
        codeCache.put(phone, new VerificationCode(code, System.currentTimeMillis()));
        
        // 在真实环境中，这里需要调用第三方短信服务API
        // 如阿里云短信、腾讯云短信等
        
        return code;
    }

    // 验证短信验证码
    public boolean verifySmsCode(String phone, String code) {
        VerificationCode storedCode = codeCache.get(phone);
        if (storedCode == null) {
            return false;
        }
        
        // 检查是否过期
        if (System.currentTimeMillis() - storedCode.timestamp > CODE_EXPIRE_TIME) {
            codeCache.remove(phone);
            return false;
        }
        
        boolean isValid = storedCode.code.equals(code);
        if (isValid) {
            // 验证成功后删除验证码
            codeCache.remove(phone);
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
