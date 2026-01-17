package com.example.ecoomerce_site.orders.exceptions;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(InsufficientStockException.class)
    public ResponseEntity<?> handleInsufficientStock(
            InsufficientStockException ex
    ) {
        return ResponseEntity
                .status(HttpStatus.CONFLICT) // ✅ 409
                .body(Map.of(
                        "error", "INSUFFICIENT_STOCK",
                        "message", ex.getMessage()
                ));
    }

    @ExceptionHandler(CartEmptyException.class)
    public ResponseEntity<?> handleCartEmpty(
            CartEmptyException ex
    ) {
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(Map.of(
                        "error", "CART_EMPTY",
                        "message", ex.getMessage()
                ));
    }
}
