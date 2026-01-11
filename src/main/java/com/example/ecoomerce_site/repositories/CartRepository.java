package com.example.ecoomerce_site.repositories;

import com.example.ecoomerce_site.models.Cart;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CartRepository extends JpaRepository<Cart, Integer> {
}
