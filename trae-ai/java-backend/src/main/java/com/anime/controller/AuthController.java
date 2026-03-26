package com.anime.controller;

import com.anime.dto.*;
import com.anime.service.UserService;
import com.anime.service.VerificationService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class AuthController {

    private final UserService userService;
    private final VerificationService verificationService;

    public AuthController(UserService userService, VerificationService verificationService) {
        this.userService = userService;
        this.verificationService = verificationService;
    }

    @GetMapping("/health")
    public ResponseEntity<ApiResponse<String>> health() {
        return ResponseEntity.ok(ApiResponse.success("服务运行正常", null));
    }

    // 获取滑块验证令牌
    @GetMapping("/slider-token")
    public ResponseEntity<ApiResponse<Map<String, String>>> getSliderToken() {
        String token = verificationService.generateSliderToken();
        Map<String, String> result = new HashMap<>();
        result.put("sliderToken", token);
        return ResponseEntity.ok(ApiResponse.success("获取成功", result));
    }

    // 发送短信验证码
    @PostMapping("/send-code")
    public ResponseEntity<ApiResponse<Map<String, String>>> sendCode(@Valid @RequestBody SendCodeRequest request) {
        try {
            // 验证滑块
            if (!verificationService.verifySliderToken(request.getSliderToken())) {
                return ResponseEntity.badRequest().body(ApiResponse.error("滑块验证失败，请重新验证"));
            }

            // 检查手机号是否已注册
            // 这里可以添加手机号是否已注册的检查，根据业务需求决定

            // 发送验证码(模拟)
            String code = verificationService.sendSmsCode(request.getPhone());

            // 生成新的滑块令牌供下一步使用
            String newSliderToken = verificationService.generateSliderToken();

            Map<String, String> result = new HashMap<>();
            result.put("message", "验证码发送成功");
            result.put("sliderToken", newSliderToken);
            // 注意：真实环境中不要返回验证码，这里只是为了测试方便
            result.put("testCode", code);

            return ResponseEntity.ok(ApiResponse.success("验证码已发送", result));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(ApiResponse.error(e.getMessage()));
        }
    }

    @PostMapping("/register")
    public ResponseEntity<ApiResponse<AuthResponse>> register(@Valid @RequestBody RegisterRequest request) {
        try {
            AuthResponse response = userService.register(request);
            return ResponseEntity.ok(ApiResponse.success("注册成功", response));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(ApiResponse.error(e.getMessage()));
        }
    }

    @PostMapping("/login")
    public ResponseEntity<ApiResponse<AuthResponse>> login(@Valid @RequestBody LoginRequest request) {
        try {
            AuthResponse response = userService.login(request);
            return ResponseEntity.ok(ApiResponse.success("登录成功", response));
        } catch (RuntimeException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(ApiResponse.error(e.getMessage()));
        }
    }

    @GetMapping("/user/info")
    public ResponseEntity<ApiResponse<AuthResponse.UserDTO>> getUserInfo(@RequestAttribute("userId") Long userId) {
        try {
            AuthResponse.UserDTO userInfo = userService.getUserInfo(userId);
            return ResponseEntity.ok(ApiResponse.success(userInfo));
        } catch (RuntimeException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(ApiResponse.error(e.getMessage()));
        }
    }

    // 管理员登录特殊接口（可选）
    @PostMapping("/admin/login")
    public ResponseEntity<ApiResponse<AuthResponse>> adminLogin(@Valid @RequestBody LoginRequest request) {
        try {
            AuthResponse response = userService.login(request);
            // 这里可以添加管理员角色验证逻辑
            // 简单验证：如果用户名是admin则认为是管理员
            if (response.getUser().getUsername().equals("admin")) {
                return ResponseEntity.ok(ApiResponse.success("管理员登录成功", response));
            } else {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(ApiResponse.error("非管理员账号"));
            }
        } catch (RuntimeException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(ApiResponse.error(e.getMessage()));
        }
    }
}
