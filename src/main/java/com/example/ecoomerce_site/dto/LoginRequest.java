package com.example.ecoomerce_site.dto;

import lombok.Data;

@Data
public class LoginRequest {
    private String email;
    private String password;
}
