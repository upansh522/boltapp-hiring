export interface CheckoutFormValues {
  email: string;
  phone: string;
  shipping_address: string;
}

export interface CheckoutSuccessResponse {
  success: boolean;
  message: string;
  checkout_id: number;
  user_id: number | null;
}