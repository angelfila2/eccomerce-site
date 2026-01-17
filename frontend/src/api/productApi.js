import api from "./api";

/**
 * POST /v1/products
 * @RequestParam: name, price, quantity, categoryId
 */
export function createProduct({ name, price, quantity, categoryId }) {
  return api.post("/v1/products", null, {
    params: {
      name,
      price,
      quantity,
      categoryId,
    },
  });
}

/**
 * GET /v1/products
 */
export function getProducts() {
  return api.get("/v1/products");
}

/**
 * GET /v1/products/{id}
 */
export function getProductById(id) {
  return api.get(`/v1/products/${id}`);
}

/**
 * GET /v1/products/category/{id}
 */
export function getProductsByCategory(categoryId) {
  return api.get(`/v1/products/category/${categoryId}`);
}

/**
 * PUT /v1/products/{id}
 * @RequestParam: name, price, quantity, categoryId
 */
export function updateProduct(id, { name, price, quantity, categoryId }) {
  return api.put(`/v1/products/${id}`, null, {
    params: {
      name,
      price,
      quantity,
      categoryId,
    },
  });
}

/**
 * DELETE /v1/products/{id}
 */
export function deleteProduct(id) {
  return api.delete(`/v1/products/${id}`);
}

export function searchProducts(query) {
  return api.get(`/v1/products/search?q=${query}`);
}
