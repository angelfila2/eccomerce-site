package com.example.ecoomerce_site.controllers;

import com.example.ecoomerce_site.services.CartService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/v1/cart")
public class CartController {

    private final CartService cartService;

    public CartController(CartService cartService) {
        this.cartService = cartService;
    }

    // POST /v1/cart
    @PostMapping
    public ResponseEntity<?> createCart() {
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(cartService.createCart());
    }

    // GET /v1/cart?cartId=1
    @GetMapping
    public ResponseEntity<?> getOrCreateCart(
            @RequestParam(required = false) Integer cartId
    ) {
        return ResponseEntity.ok(cartService.getOrCreateCart(cartId));
    }

    // POST /v1/cart/items
    @PostMapping("/items")
    public ResponseEntity<?> addCartItem(
            @RequestParam Integer cartId,
            @RequestParam Integer productId,
            @RequestParam Integer quantity
    ) {
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(cartService.addCartItem(cartId, productId, quantity));
    }

    // PUT /v1/cart/items
    @PutMapping("/items")
    public ResponseEntity<?> updateItemQuantity(
            @RequestParam Integer cartId,
            @RequestParam Integer productId,
            @RequestParam Integer quantity
    ) {
        return ResponseEntity.ok(
                cartService.updateItemQuantity(cartId, productId, quantity)
        );
    }

    // DELETE /v1/cart/{cartId}/items
    @DeleteMapping("/{cartId}/items")
    public ResponseEntity<?> removeItem(
            @PathVariable Integer cartId,
            @RequestParam Integer productId
    ) {
        cartService.removeItem(cartId, productId);
        return ResponseEntity.noContent().build();
    }

    // DELETE /v1/cart/{cartId}/clear
    @DeleteMapping("/{cartId}/clear")
    public ResponseEntity<?> clearCart(@PathVariable Integer cartId) {
        cartService.clearCart(cartId);
        return ResponseEntity.noContent().build();
    }

    // POST /v1/cart/{cartId}/checkout
    @PostMapping("/{cartId}/checkout")
    public ResponseEntity<?> checkout(@PathVariable Integer cartId) {
        return ResponseEntity.ok(cartService.checkout(cartId));
    }

    /* ================= NEW ================= */

    // GET /v1/cart/all
    @GetMapping("/all")
    public ResponseEntity<?> getAllCarts() {
        return ResponseEntity.ok(cartService.getAllCarts());
    }
}
