package com.example.ecoomerce_site.orders;

import com.example.ecoomerce_site.orders.dto.OrderMapper;
import com.example.ecoomerce_site.orders.dto.OrderResponseDTO;
import com.example.ecoomerce_site.users.User;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/v1/orders")
@RequiredArgsConstructor
public class OrderController {

    private final OrderService orderService;

    /**
     * Checkout current user's ACTIVE cart
     */
    @PostMapping("/checkout")
    @ResponseStatus(HttpStatus.CREATED)
    public OrderResponseDTO checkout(
            @AuthenticationPrincipal User user
    ) {
        Order order = orderService.checkout(user);
        return OrderMapper.toResponse(order);
    }

    /**
     * Get all orders for current user
     */
    @GetMapping
    public List<OrderResponseDTO> getMyOrders(
            @AuthenticationPrincipal User user
    ) {
        return orderService.getOrdersForUser(user)
                .stream()
                .map(OrderMapper::toResponse)
                .toList();
    }

    /**
     * Get single order by ID (ownership enforced)
     */
    @GetMapping("/{id}")
    public OrderResponseDTO getOrderById(
            @PathVariable Long id,
            @AuthenticationPrincipal User user
    ) {
        Order order = orderService.getOrderByIdForUser(id, user);
        return OrderMapper.toResponse(order);
    }
}
