package com.example.ecoomerce_site.services;

import com.example.ecoomerce_site.models.Category;
import com.example.ecoomerce_site.models.Product;
import com.example.ecoomerce_site.repositories.CategoryRepository;
import com.example.ecoomerce_site.repositories.ProductRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.List;

@Service
public class ProductService {

    private final ProductRepository productRepository;
    private final CategoryRepository categoryRepository;

    public ProductService(ProductRepository productRepository,CategoryRepository categoryRepository){
        this.productRepository=productRepository;
        this.categoryRepository=categoryRepository;
    }

//    createProduct(name, price, quantity, categoryId)
     public Product createProduct(String name, BigDecimal price, Integer quantity, Integer categoryId){

        Category category = categoryRepository.findById(categoryId).orElseThrow(()->new RuntimeException("Not valid category id" +
                ""));

        Product newProduct = new Product(name,price,quantity,category);
        return productRepository.save(newProduct);

     }
//    getAllProducts()
     public List<Product> getAllProducts(){
        return productRepository.findAll();
     }
//    getProductById(id)
     public Product getProductById(Integer id){
        return productRepository.findById(id).orElseThrow(()->new RuntimeException("No such product. Invalid product id"));
     }
//    getProductsByCategory(categoryId)
    public List<Product> getProductsByCategory(Integer categoryId){
        Category catToFind = categoryRepository.findById(categoryId).orElseThrow(()->new RuntimeException("Invalid categoryId"));
        return productRepository.findByCategory(catToFind);
    }
//    updateProduct(id, name, price, quantity, categoryId)
    public Product updateProduct(Integer id, String name,BigDecimal price, Integer quantity,Integer categoryId){
       Product productToUpdate = productRepository.findById(id).orElseThrow(()->new RuntimeException("No product with id. fail update"));
        Category catToFind = categoryRepository.findById(categoryId).orElseThrow(()->new RuntimeException("Invalid categoryId"));

        productToUpdate.setCategory(catToFind);
        productToUpdate.setName(name);
        productToUpdate.setPrice(price);
        productToUpdate.setQuantity(quantity);
        return productRepository.save(productToUpdate);


    }
//    deleteProduct(id)
public void deleteProduct(Integer id) {
    Product product = productRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("Product not found"));
    productRepository.delete(product);
}

//    decreaseStock(productId, quantity) (used during checkout)

    public Product decreaseStock(Integer productId,Integer quantity){
        Product productToDecrease = productRepository.findById(productId).orElseThrow(()->new RuntimeException("No such product id to decrease quantity"));
        Integer oldQuantity = productToDecrease.getQuantity();
        if (productToDecrease.getQuantity() < quantity) {
            throw new RuntimeException("Insufficient stock");
        }
        productToDecrease.setQuantity(oldQuantity-quantity);
        return productRepository.save(productToDecrease);
    }

    public List<Product> getProductByName(String name){
        return productRepository.findByNameContainingIgnoreCase(name);
    }
}
