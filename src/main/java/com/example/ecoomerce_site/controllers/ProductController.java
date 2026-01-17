package com.example.ecoomerce_site.controllers;


import com.example.ecoomerce_site.models.Category;
import com.example.ecoomerce_site.models.Product;
import com.example.ecoomerce_site.services.ProductService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.List;

@RestController
@RequestMapping("/v1/products")
public class ProductController {

    private final ProductService productService;

    public ProductController(ProductService productService){
        this.productService = productService;
    }

    // POST /v1/products
    @PostMapping
    public ResponseEntity<?> createProduct(
            @RequestParam String name,
            @RequestParam BigDecimal price,
            @RequestParam Integer quantity,
            @RequestParam Integer categoryId
    ) {
        try {
            return ResponseEntity
                    .status(HttpStatus.CREATED)
                    .body(productService.createProduct(name, price, quantity, categoryId));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    // GET /v1/products
    @GetMapping
    public ResponseEntity<?> getAllProducts() {
        return ResponseEntity.ok(productService.getAllProducts());
    }

    // GET /v1/products/{id}
    @GetMapping("/{id}")
    public ResponseEntity<?> getProductById(@PathVariable Integer id) {
        try {
            return ResponseEntity.ok(productService.getProductById(id));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    // GET /v1/products/category/{id}
    @GetMapping("/category/{id}")
    public ResponseEntity<?> getProductsByCategory(@PathVariable Integer id) {
        try {
            return ResponseEntity.ok(productService.getProductsByCategory(id));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    // PUT /v1/products/{id}
    @PutMapping("/{id}")
    public ResponseEntity<?> updateProduct(
            @PathVariable Integer id,
            @RequestParam String name,
            @RequestParam BigDecimal price,
            @RequestParam Integer quantity,
            @RequestParam Integer categoryId
    ) {
        try {
            return ResponseEntity.ok(
                    productService.updateProduct(id, name, price, quantity, categoryId)
            );
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    // DELETE /v1/products/{id}
    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteProduct(@PathVariable Integer id) {
        try {
            productService.deleteProduct(id);
            return ResponseEntity.noContent().build();
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    @GetMapping("/search")
    public ResponseEntity<List<Product>> searchProducts(
            @RequestParam String q
    ) {
        return ResponseEntity.ok(
                productService.getProductByName(q)
        );
    }


}
