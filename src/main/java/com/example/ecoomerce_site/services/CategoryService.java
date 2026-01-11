package com.example.ecoomerce_site.services;


import com.example.ecoomerce_site.models.Category;
import com.example.ecoomerce_site.repositories.CategoryRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CategoryService {
    private final CategoryRepository categoryRepository;

    public CategoryService(CategoryRepository categoryRepository){
        this.categoryRepository=categoryRepository;
    }

    public Category createCategory(String name){
        Category newCat = new Category(name);
        return categoryRepository.save(newCat);

    }
//    createCategory(name)
//
//    getAllCategories()
    public List<Category> getAllCategories(){
        return categoryRepository.findAll();
    }
//
//    getCategoryById(id)
    public Category getCategoryById(Integer id){
        return categoryRepository.getById(id);
    }
//
//    updateCategory(id, name)
    public Category updateCategory(Integer id, String name){
        Category exists = categoryRepository.findById(id).orElseThrow(()->new RuntimeException ("Category does not exist"
        ));

        exists.setCategoryName(name);
        return categoryRepository.save(exists);
    }
//
//    deleteCategory(id)

    public void deleteCategory(Integer id) {
        if (!categoryRepository.existsById(id)) {
            throw new RuntimeException("Category not found");
        }
        categoryRepository.deleteById(id);
    }

}
