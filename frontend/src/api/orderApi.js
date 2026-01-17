import api from "./api";

export const createOrder = () => api.post("/v1/orders");

export const getOrderById = (id) => api.get(`/v1/orders/${id}`);
