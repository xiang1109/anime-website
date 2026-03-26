package com.anime.service;

import com.anime.dto.AuthResponse;
import com.anime.dto.LoginRequest;
import com.anime.dto.RegisterRequest;
import com.anime.entity.User;
import com.anime.repository.UserRepository;
import com.anime.config.JwtUtil;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

@Service
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil;
    private final VerificationService verificationService;

    public UserService(UserRepository userRepository, PasswordEncoder passwordEncoder, JwtUtil jwtUtil, VerificationService verificationService) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtUtil = jwtUtil;
        this.verificationService = verificationService;
    }

    @Transactional
    public AuthResponse register(RegisterRequest request) {
        // 验证滑块
        if (!verificationService.verifySliderToken(request.getSliderToken())) {
            throw new RuntimeException("滑块验证失败，请重新验证");
        }

        // 验证短信验证码
        if (!verificationService.verifySmsCode(request.getPhone(), request.getVerifyCode())) {
            throw new RuntimeException("验证码错误或已过期");
        }

        if (userRepository.existsByUsername(request.getUsername())) {
            throw new RuntimeException("用户名已存在");
        }
        if (userRepository.existsByPhone(request.getPhone())) {
            throw new RuntimeException("手机号已被注册");
        }

        User user = new User();
        user.setUsername(request.getUsername());
        user.setPhone(request.getPhone());
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        // 设置默认头像
        user.setAvatar("https://picsum.photos/seed/user" + System.currentTimeMillis() + "/100/100");

        user = userRepository.save(user);

        String token = jwtUtil.generateToken(user.getId(), user.getUsername());
        AuthResponse.UserDTO userDTO = new AuthResponse.UserDTO(
                user.getId(),
                user.getUsername(),
                user.getEmail(),
                user.getAvatar()
        );

        return new AuthResponse(token, userDTO);
    }

    public AuthResponse login(LoginRequest request) {
        Optional<User> userOpt = userRepository.findByUsername(request.getUsername());
        if (!userOpt.isPresent()) {
            // 也可以尝试用手机号登录
            userOpt = userRepository.findByPhone(request.getUsername());
            if (!userOpt.isPresent()) {
                throw new RuntimeException("用户名或密码错误");
            }
        }

        User user = userOpt.get();
        if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
            throw new RuntimeException("用户名或密码错误");
        }

        String token = jwtUtil.generateToken(user.getId(), user.getUsername());
        AuthResponse.UserDTO userDTO = new AuthResponse.UserDTO(
                user.getId(),
                user.getUsername(),
                user.getEmail(),
                user.getAvatar()
        );

        return new AuthResponse(token, userDTO);
    }

    public AuthResponse.UserDTO getUserInfo(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("用户不存在"));

        return new AuthResponse.UserDTO(
                user.getId(),
                user.getUsername(),
                user.getEmail(),
                user.getAvatar()
        );
    }

    public User findById(Long userId) {
        return userRepository.findById(userId).orElse(null);
    }
}
