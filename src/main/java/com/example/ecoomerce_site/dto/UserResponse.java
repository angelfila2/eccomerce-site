package com.example.ecoomerce_site.dto;

import com.example.ecoomerce_site.users.Role;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class UserResponse {
    private Integer id;
    private String firstname;
    private String lastname;
    private String email;
    private Role role;

    public UserResponse(Integer id, String firstname, String email) {
    }
}
