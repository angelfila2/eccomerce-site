package com.example.ecoomerce_site.services;

import com.example.ecoomerce_site.repositories.UserRepository;
import org.springframework.stereotype.Service;


@Service
public class UserService {

    private  final UserRepository userRepository;
//}
    public UserService (UserRepository userRepository){
        this.userRepository = userRepository;
    }
}



