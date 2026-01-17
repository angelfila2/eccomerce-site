package com.example.ecoomerce_site.controllers;

import com.example.ecoomerce_site.services.CartService;
import com.example.ecoomerce_site.users.User;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/v1/cart")
@RequiredArgsConstructor
public class CartController {

    private final CartService cartService;

    /* ================= GET CART ================= */

    @GetMapping
    public ResponseEntity<?> getCart(
            @AuthenticationPrincipal User user
    ) {
        return ResponseEntity.ok(cartService.getOrCreateCart(user));
    }

    /* ================= ADD ITEM ================= */

    @PostMapping("/items")
    public ResponseEntity<?> addCartItem(
            @AuthenticationPrincipal User user,
            @RequestParam Integer productId,
            @RequestParam Integer quantity
    ) {
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(cartService.addCartItem(user, productId, quantity));
    }

    /* ================= UPDATE ================= */

    @PutMapping("/items")
    public ResponseEntity<?> updateItemQuantity(
            @AuthenticationPrincipal User user,
            @RequestParam Integer productId,
            @RequestParam Integer quantity
    ) {
        return ResponseEntity.ok(
                cartService.updateItemQuantity(user, productId, quantity)
        );
    }

    /* ================= REMOVE ================= */

    @DeleteMapping("/items")
    public ResponseEntity<?> removeItem(
            @AuthenticationPrincipal User user,
            @RequestParam Integer productId
    ) {
        return ResponseEntity.ok(
                cartService.removeItem(user, productId)
        );
    }

    /* ================= CLEAR ================= */

    @DeleteMapping("/clear")
    public ResponseEntity<?> clearCart(
            @AuthenticationPrincipal User user
    ) {
        return ResponseEntity.ok(cartService.clearCart(user));
    }
}
