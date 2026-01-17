package com.example.ecoomerce_site.orders;


import com.example.ecoomerce_site.models.Cart;
import com.example.ecoomerce_site.models.CartItem;
import com.example.ecoomerce_site.models.CartStatus;
import com.example.ecoomerce_site.models.Product;
import com.example.ecoomerce_site.orders.exceptions.CartEmptyException;
import com.example.ecoomerce_site.orders.exceptions.InsufficientStockException;
import com.example.ecoomerce_site.repositories.CartRepository;
import com.example.ecoomerce_site.repositories.ProductRepository;
import com.example.ecoomerce_site.users.User;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepository;
    private final CartRepository cartRepository;
    private final ProductRepository productRepository;

    /**
     * Convert ACTIVE cart into an Order
     */
    @Transactional
    public Order checkout(User user) {

        Cart cart = cartRepository.findByUserAndStatus(user, CartStatus.ACTIVE)
                .orElseThrow(() -> new RuntimeException("Cart not found"));

        if (cart.getItems().isEmpty()) {
            throw new CartEmptyException("Cart is empty");
        }

        // 1. Validate stock
        for (CartItem item : cart.getItems()) {
            Product product = item.getProduct();
            if (product.getQuantity() < item.getQuantity()) {
                throw new InsufficientStockException(
                        "Product " + product.getName()
                                + ": requested " + item.getQuantity()
                                + ", available " + product.getQuantity()
                );

            }



        }

        // 2. Create Order
        Order order = Order.builder()
                .user(user)
                .status(OrderStatus.CREATED)
                .createdAt(LocalDateTime.now())
                .build();

        // 3. Create OrderItems + deduct stock
        List<OrderItem> orderItems = cart.getItems().stream().map(cartItem -> {

            Product product = cartItem.getProduct();

            // Deduct stock
            product.setQuantity(product.getQuantity() - cartItem.getQuantity());
            productRepository.save(product);

            return OrderItem.builder()
                    .order(order)
                    .product(product)
                    .quantity(cartItem.getQuantity())
                    .priceAtPurchase(product.getPrice())
                    .build();
        }).toList();

        order.setItems(orderItems);

        // 4. Calculate total
        BigDecimal total = orderItems.stream()
                .map(i -> i.getPriceAtPurchase()
                        .multiply(BigDecimal.valueOf(i.getQuantity())))
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        order.setTotalAmount(total);

        // 5. Save order
        Order savedOrder = orderRepository.save(order);

        // 6. Clear cart
        cart.getItems().clear();
        cartRepository.save(cart);

        return savedOrder;
    }

    public List<Order> getOrdersForUser(User user) {
        return orderRepository.findByUserOrderByCreatedAtDesc(user);
    }

    public Order getOrderByIdForUser(Long orderId, User user) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new RuntimeException("Order not found"));

        if (!order.getUser().getId().equals(user.getId())) {
            throw new RuntimeException("Access denied");
        }

        System.out.println(order);

        return order;
    }
}
