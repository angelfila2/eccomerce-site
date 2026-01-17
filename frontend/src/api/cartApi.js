import api from "./api";

export function getCart() {
  return api.get("/v1/cart");
}

export function addToCart(productId, quantity) {
  return api.post("/v1/cart/items", null, {
    params: {
      productId,
      quantity,
    },
  });
}

export function updateCartItem(productId, quantity) {
  return api.put("/v1/cart/items", null, {
    params: {
      productId,
      quantity,
    },
  });
}

export function removeCartItem(productId) {
  return api.delete("/v1/cart/items", {
    params: { productId },
  });
}

export function clearCart() {
  return api.delete("/v1/cart/clear");
}

export function checkout() {
  return api.post("/v1/orders/checkout");
}
