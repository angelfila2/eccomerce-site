package com.example.ecoomerce_site.auth;

import com.example.ecoomerce_site.users.User;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class RefreshTokenService {

    private final RefreshTokenRepository refreshTokenRepository;

    // 30 days (Shopee-style long-lived session)
    private static final long REFRESH_TOKEN_DAYS = 30;

    public RefreshToken create(User user) {
        RefreshToken token = RefreshToken.builder()
                .token(UUID.randomUUID().toString())
                .user(user)
                .expiryDate(
                        Instant.now().plus(
                                REFRESH_TOKEN_DAYS, ChronoUnit.DAYS
                        )
                )
                .revoked(false)
                .build();

        return refreshTokenRepository.save(token);
    }

    public RefreshToken verify(String tokenValue) {
        RefreshToken token = refreshTokenRepository
                .findByToken(tokenValue)
                .orElseThrow(() ->
                        new RuntimeException("Invalid refresh token"));

        if (token.isRevoked()) {
            throw new RuntimeException("Refresh token revoked");
        }

        if (token.getExpiryDate().isBefore(Instant.now())) {
            throw new RuntimeException("Refresh token expired");
        }

        return token;
    }

    public void revoke(RefreshToken token) {
        token.setRevoked(true);
        refreshTokenRepository.save(token);
    }
}
