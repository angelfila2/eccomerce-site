package com.example.ecoomerce_site.repositories;

import com.example.ecoomerce_site.models.Cart;
import com.example.ecoomerce_site.models.CartStatus;
import com.example.ecoomerce_site.users.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface CartRepository extends JpaRepository<Cart, Integer> {

    Optional<Cart> findByUserAndStatus(User user, CartStatus status);
}
