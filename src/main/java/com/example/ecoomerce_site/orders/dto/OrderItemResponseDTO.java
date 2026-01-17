package com.example.ecoomerce_site.orders.dto;

import java.math.BigDecimal;

public record OrderItemResponseDTO(
        Integer productId,
        String productName,
        BigDecimal price,
        Integer quantity
) {}
