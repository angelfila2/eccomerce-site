import api from "./api";

/**
 * GET /v1/category
 * Returns: List<Category>
 */
export function getCategories() {
  return api.get("/v1/category");
}

/**
 * POST /v1/category?name=CategoryName
 * Uses @RequestParam on backend
 */
export function createCategory(name) {
  return api.post("/v1/category", null, {
    params: { name },
  });
}

/**
 * DELETE /v1/category/{id}
 */
export function deleteCategory(id) {
  return api.delete(`/v1/category/${id}`);
}

/**
 * GET /v1/category/{id}
 */
export function getCategoryById(id) {
  return api.get(`/v1/category/${id}`);
}

/**
 * PUT /v1/category/{id}?name=NewName
 */
export function updateCategory(id, name) {
  return api.put(`/v1/category/${id}`, null, {
    params: { name },
  });
}
