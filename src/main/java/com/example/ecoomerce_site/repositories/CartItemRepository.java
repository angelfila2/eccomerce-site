package com.example.ecoomerce_site.repositories;

import com.example.ecoomerce_site.models.CartItem;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CartItemRepository extends JpaRepository<CartItem,Integer> {
}
