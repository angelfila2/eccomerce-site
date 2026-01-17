package com.example.ecoomerce_site.repositories;

import com.example.ecoomerce_site.models.Category;
import com.example.ecoomerce_site.models.Product;
import org.springframework.data.jpa.repository.JpaRepository;

import javax.swing.text.html.Option;
import java.util.List;

public interface ProductRepository extends JpaRepository<Product,Integer> {
     List<Product> findByCategory(Category catToFind);
    List<Product> findByNameContainingIgnoreCase(String name);
}
