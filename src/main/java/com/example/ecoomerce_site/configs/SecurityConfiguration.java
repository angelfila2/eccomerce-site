package com.example.ecoomerce_site.configs;

import com.example.ecoomerce_site.auth.JwtAuthenticationFilter;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
@RequiredArgsConstructor
public class SecurityConfiguration {

    private final JwtAuthenticationFilter jwtAuthenticationFilter;
    private final AuthenticationProvider authenticationProvider;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http)
            throws Exception {

        http
                .cors(Customizer.withDefaults())
                .csrf(AbstractHttpConfigurer::disable)

                // ✅ Stateless JWT
                .sessionManagement(session ->
                        session.sessionCreationPolicy(SessionCreationPolicy.STATELESS)
                )

                // ✅ IMPORTANT: return 401 (not 403) when unauthenticated
                .exceptionHandling(ex -> ex
                        .authenticationEntryPoint((request, response, authException) ->
                                response.sendError(
                                        HttpServletResponse.SC_UNAUTHORIZED,
                                        "Unauthorized"
                                )
                        )
                )

                .authorizeHttpRequests(auth -> auth
                        // Preflight
                        .requestMatchers(HttpMethod.OPTIONS, "/**").permitAll()

                        // Auth (public)
                        .requestMatchers(HttpMethod.POST, "/auth/login").permitAll()
                        .requestMatchers(HttpMethod.POST, "/auth/refresh").permitAll()

                        // Auth (protected)
                        .requestMatchers(HttpMethod.GET, "/auth/me").authenticated()
                        .requestMatchers(HttpMethod.POST, "/auth/logout").authenticated()

                        // ===== Public catalogue browsing =====
                        // Products
                        .requestMatchers(HttpMethod.GET, "/v1/products/**").permitAll()

                        // Categories
                        .requestMatchers(HttpMethod.GET, "/v1/category/**").permitAll()

                        // ===== Protected management =====
                        // Products (create/update/delete)
                        .requestMatchers(HttpMethod.POST, "/v1/products/**").authenticated()
                        .requestMatchers(HttpMethod.PUT, "/v1/products/**").authenticated()
                        .requestMatchers(HttpMethod.DELETE, "/v1/products/**").authenticated()

                        // Categories (create/update/delete)
                        .requestMatchers(HttpMethod.POST, "/v1/category/**").authenticated()
                        .requestMatchers(HttpMethod.PUT, "/v1/category/**").authenticated()
                        .requestMatchers(HttpMethod.DELETE, "/v1/category/**").authenticated()

                        // Cart (protected)
                        .requestMatchers("/v1/cart/**").authenticated()

                        // Orders (protected)
                        .requestMatchers("/v1/orders/**").authenticated()

                        // Everything else sealed
                        .anyRequest().authenticated()
                )


                .authenticationProvider(authenticationProvider)

                // ✅ JWT filter
                .addFilterBefore(
                        jwtAuthenticationFilter,
                        UsernamePasswordAuthenticationFilter.class
                );

        return http.build();
    }
}
