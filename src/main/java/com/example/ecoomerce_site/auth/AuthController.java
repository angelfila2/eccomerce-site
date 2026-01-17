package com.example.ecoomerce_site.auth;

import com.example.ecoomerce_site.dto.AuthResponse;
import com.example.ecoomerce_site.dto.LoginRequest;
import com.example.ecoomerce_site.users.User;
import com.example.ecoomerce_site.users.UserRepository;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseCookie;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.Arrays;

@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthenticationManager authenticationManager;
    private final JwtService jwtService;
    private final RefreshTokenService refreshTokenService;
    private final UserRepository userRepository;

    /* ========= LOGIN ========= */
    @PostMapping("/login")
    public AuthResponse login(
            @RequestBody LoginRequest request,
            HttpServletResponse response
    ) {
        Authentication authentication =
                authenticationManager.authenticate(
                        new UsernamePasswordAuthenticationToken(
                                request.getEmail(),
                                request.getPassword()
                        )
                );

        User user = (User) authentication.getPrincipal();

        RefreshToken refreshToken = refreshTokenService.create(user);

        ResponseCookie cookie = ResponseCookie.from("refreshToken", refreshToken.getToken())
                .httpOnly(true)
                .path("/")
                .maxAge(30L * 24 * 60 * 60)
                .sameSite("Lax")
                .build();

        response.addHeader("Set-Cookie", cookie.toString());

        return new AuthResponse(
                jwtService.generateAccessToken(user),
                null
        );
    }

    /* ========= REFRESH ========= */
    @PostMapping("/refresh")
    public ResponseEntity<AuthResponse> refresh(HttpServletRequest request) {

        Cookie[] cookies = request.getCookies();
        if (cookies == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }

        String tokenValue = Arrays.stream(cookies)
                .filter(c -> c.getName().equals("refreshToken"))
                .findFirst()
                .map(Cookie::getValue)
                .orElse(null);

        if (tokenValue == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }

        try {
            RefreshToken token = refreshTokenService.verify(tokenValue);
            User user = token.getUser();

            return ResponseEntity.ok(
                    new AuthResponse(
                            jwtService.generateAccessToken(user),
                            null
                    )
            );

        } catch (RuntimeException e) {
            // ❌ DO NOT revoke here
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
    }

    /* ========= LOGOUT ========= */
    @PostMapping("/logout")
    public ResponseEntity<Void> logout(HttpServletRequest request) {

        Cookie[] cookies = request.getCookies();
        if (cookies != null) {
            Arrays.stream(cookies)
                    .filter(c -> c.getName().equals("refreshToken"))
                    .findFirst()
                    .ifPresent(c -> {
                        try {
                            RefreshToken token =
                                    refreshTokenService.verify(c.getValue());
                            refreshTokenService.revoke(token);
                        } catch (RuntimeException ignored) {
                            // token invalid / expired / already revoked
                        }
                    });
        }

        return ResponseEntity.noContent().build();
    }


    /* ========= CURRENT USER ========= */
    @GetMapping("/me")
    public UserResponse me() {

        Authentication authentication =
                SecurityContextHolder.getContext().getAuthentication();

        UserDetails userDetails =
                (UserDetails) authentication.getPrincipal();

        User user = userRepository
                .findByEmail(userDetails.getUsername())
                .orElseThrow(() ->
                        new RuntimeException("User not found")
                );

        return new UserResponse(
                user.getId(),
                user.getFirstname(),
                user.getEmail()
        );
    }
}
