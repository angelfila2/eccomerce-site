package com.example.ecoomerce_site.controllers;


import com.example.ecoomerce_site.models.Category;
import com.example.ecoomerce_site.services.CategoryService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/v1/category")
public class CategoryController {
    private final CategoryService categoryService;

    public CategoryController(CategoryService categoryService) {
        this.categoryService = categoryService;
    }

    @GetMapping
    public ResponseEntity<List<Category>> getCategories() {
        List<Category> categoryList = categoryService.getAllCategories();
        return ResponseEntity.ok(categoryList);
    }


    //for error catching
    @PostMapping
    public ResponseEntity<?> createCategory(@RequestParam String name) {
        try {
            Category created = categoryService.createCategory(name);
            return ResponseEntity.status(HttpStatus.CREATED).body(created);
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

//    POST   /categories          → createCategory
//    GET    /categories          → getAllCategories
//    GET    /categories/{id}     → getCategoryById

    @GetMapping("/{id}")
    public ResponseEntity<?> getCategoryById(@PathVariable Integer id){
        try{
            return ResponseEntity.status(HttpStatus.CREATED).body(categoryService.getCategoryById(id));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
//    PUT    /categories/{id}     → updateCategory

    @PutMapping("/{id}")
    public ResponseEntity<?> updateCategory(@PathVariable Integer id,@RequestParam String name){
        try{
            return ResponseEntity.status(HttpStatus.CREATED).body(categoryService.updateCategory(id,name));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
//    DELETE /categories/{id}     → deleteCategory
    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteCategory(@PathVariable Integer id) {
        try {
            categoryService.deleteCategory(id);
            return ResponseEntity.noContent().build();
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
}