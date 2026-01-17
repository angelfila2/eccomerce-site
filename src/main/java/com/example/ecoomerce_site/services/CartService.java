package com.example.ecoomerce_site.services;

import com.example.ecoomerce_site.models.*;
import com.example.ecoomerce_site.repositories.CartRepository;
import com.example.ecoomerce_site.repositories.ProductRepository;
import com.example.ecoomerce_site.users.User;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Optional;

@Service
public class CartService {

    private final CartRepository cartRepository;
    private final ProductRepository productRepository;

    public CartService(
            CartRepository cartRepository,
            ProductRepository productRepository
    ) {
        this.cartRepository = cartRepository;
        this.productRepository = productRepository;
    }

    /* ================= CART ================= */

    public Cart getOrCreateCart(User user) {
        if (user == null) {
            throw new RuntimeException("User not authenticated");
        }

        return cartRepository
                .findByUserAndStatus(user, CartStatus.ACTIVE)
                .orElseGet(() -> {
                    Cart cart = new Cart();
                    cart.setUser(user);
                    cart.setStatus(CartStatus.ACTIVE);
                    cart.setItems(new ArrayList<>());
                    return cartRepository.save(cart);
                });
    }

    /* ================= ADD ITEM ================= */

    public Cart addCartItem(User user, Integer productId, Integer quantity) {

        if (quantity == null || quantity <= 0) {
            throw new RuntimeException("Quantity must be greater than 0");
        }

        Cart cart = getOrCreateCart(user);

        Product product = productRepository.findById(productId)
                .orElseThrow(() -> new RuntimeException("Product not found"));

        Optional<CartItem> existingItem = cart.getItems()
                .stream()
                .filter(i -> i.getProduct().getProductId().equals(productId))
                .findFirst();

        if (existingItem.isPresent()) {
            CartItem item = existingItem.get();
            item.setQuantity(item.getQuantity() + quantity);
        } else {
            cart.getItems().add(new CartItem(cart, product, quantity));
        }

        return cartRepository.save(cart);
    }

    /* ================= UPDATE QUANTITY ================= */

    public Cart updateItemQuantity(User user, Integer productId, Integer quantity) {

        Cart cart = getOrCreateCart(user);

        CartItem item = cart.getItems()
                .stream()
                .filter(i -> i.getProduct().getProductId().equals(productId))
                .findFirst()
                .orElseThrow(() -> new RuntimeException("Product not in cart"));

        if (quantity == null || quantity <= 0) {
            cart.getItems().remove(item);
        } else {
            item.setQuantity(quantity);
        }

        return cartRepository.save(cart);
    }

    /* ================= REMOVE ITEM ================= */

    public Cart removeItem(User user, Integer productId) {

        Cart cart = getOrCreateCart(user);

        cart.getItems().removeIf(
                i -> i.getProduct().getProductId().equals(productId)
        );

        return cartRepository.save(cart);
    }

    /* ================= CLEAR CART ================= */

    public Cart clearCart(User user) {

        Cart cart = getOrCreateCart(user);
        cart.getItems().clear();
        return cartRepository.save(cart);
    }
}
