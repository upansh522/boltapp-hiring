import api from "./api";

// Checkout Service
export async function createCheckout(checkoutData: {
  email: string;
  phone: string;
  shipping_address: string;
}) {
  const response = await api.post("/api/checkout/create", checkoutData);
  return response.data;
}
