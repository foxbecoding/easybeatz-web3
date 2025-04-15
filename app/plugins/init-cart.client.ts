import { useCartStore } from "@/store/cart";
import { CartResponse, getCart } from "@/services/models/cart";

export default defineNuxtPlugin(async (nuxtApp) => {
  const cartStore = useCartStore()

  const { message, data } = await getCart();
  const response_data = data as CartResponse;
  if (!response_data.items) return;

  if (response_data.items.length === 0) return;
  cartStore.setCartItems(response_data.items);
  cartStore.setCartCount(response_data.cart_count);
  cartStore.setCartSubtotal(response_data.cart_subtotal);
})
