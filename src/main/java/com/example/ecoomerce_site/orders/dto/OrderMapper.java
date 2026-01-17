package com.example.ecoomerce_site.orders.dto;

import com.example.ecoomerce_site.orders.Order;
import com.example.ecoomerce_site.orders.OrderItem;
import com.example.ecoomerce_site.orders.dto.OrderItemResponseDTO;
import com.example.ecoomerce_site.orders.dto.OrderResponseDTO;

import java.util.List;

public class OrderMapper {

    public static OrderResponseDTO toResponse(Order order) {
        return new OrderResponseDTO(
                order.getId(),
                order.getStatus().name(),
                order.getTotalAmount(),
                order.getCreatedAt(),
                toItemResponses(order.getItems())
        );
    }

    private static List<OrderItemResponseDTO> toItemResponses(List<OrderItem> items) {
        return items.stream()
                .map(item -> new OrderItemResponseDTO(
                        item.getProduct().getProductId(),
                        item.getProduct().getName(),
                        item.getPriceAtPurchase(),
                        item.getQuantity()
                ))
                .toList();
    }
}
