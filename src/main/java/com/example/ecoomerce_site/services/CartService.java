package com.example.ecoomerce_site.services;

import com.example.ecoomerce_site.models.Cart;
import com.example.ecoomerce_site.models.CartItem;
import com.example.ecoomerce_site.models.CartStatus;
import com.example.ecoomerce_site.models.Product;
import com.example.ecoomerce_site.repositories.CartRepository;
import com.example.ecoomerce_site.repositories.ProductRepository;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
public class CartService {

    private final CartRepository cartRepository;
    private final ProductRepository productRepository;

    public CartService(CartRepository cartRepository,
                       ProductRepository productRepository) {
        this.cartRepository = cartRepository;
        this.productRepository = productRepository;
    }

    /* ---------------- CART CREATION ---------------- */

    public Cart getOrCreateCart(Integer cartId) {
        if (cartId == null) {
            return createCart();
        }

        return cartRepository.findById(cartId)
                .orElseThrow(() -> new RuntimeException("Cart not found"));
    }

    public Cart createCart() {
        Cart cart = new Cart();
        cart.setStatus(CartStatus.ACTIVE);
        cart.setItems(new ArrayList<>());
        return cartRepository.save(cart);
    }

    /* ---------------- ADD ITEM ---------------- */

    public Cart addCartItem(Integer cartId, Integer productId, Integer quantity) {

        if (quantity <= 0) {
            throw new RuntimeException("Quantity must be greater than 0");
        }

        Cart cart = getOrCreateCart(cartId);

        Product product = productRepository.findById(productId)
                .orElseThrow(() -> new RuntimeException("Product does not exist"));

        Optional<CartItem> existingItem = cart.getItems()
                .stream()
                .filter(item -> item.getProduct().getProductId().equals(productId))
                .findFirst();

        if (existingItem.isPresent()) {
            CartItem item = existingItem.get();
            item.setQuantity(item.getQuantity() + quantity);
        } else {
            CartItem newItem = new CartItem(cart, product, quantity);
            cart.getItems().add(newItem);
        }

        return cartRepository.save(cart);
    }

    /* ---------------- UPDATE QUANTITY ---------------- */

    public Cart updateItemQuantity(Integer cartId, Integer productId, Integer quantity) {

        Cart cart = getOrCreateCart(cartId);

        Optional<CartItem> itemOpt = cart.getItems()
                .stream()
                .filter(item -> item.getProduct().getProductId().equals(productId))
                .findFirst();

        if (itemOpt.isEmpty()) {
            throw new RuntimeException("Product not in cart");
        }

        if (quantity <= 0) {
            cart.getItems().remove(itemOpt.get());
        } else {
            itemOpt.get().setQuantity(quantity);
        }

        return cartRepository.save(cart);
    }

    /* ---------------- REMOVE ITEM ---------------- */

    public Cart removeItem(Integer cartId, Integer productId) {

        Cart cart = getOrCreateCart(cartId);

        cart.getItems().removeIf(
                item -> item.getProduct().getProductId().equals(productId)
        );

        return cartRepository.save(cart);
    }

    /* ---------------- CLEAR CART ---------------- */

    public Cart clearCart(Integer cartId) {

        Cart cart = getOrCreateCart(cartId);
        cart.getItems().clear();
        return cartRepository.save(cart);
    }

    /* ---------------- CHECKOUT ---------------- */

    public Cart checkout(Integer cartId) {

        Cart cart = getOrCreateCart(cartId);

        if (cart.getItems().isEmpty()) {
            throw new RuntimeException("Cannot checkout empty cart");
        }

        cart.setStatus(CartStatus.CHECKED_OUT);
        return cartRepository.save(cart);
    }

    /* ================= NEW: VIEW ALL CARTS ================= */

    public List<Cart> getAllCarts() {
        return cartRepository.findAll();
    }
}
