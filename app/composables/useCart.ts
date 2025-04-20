import { useCartStore } from "@/store/cart";
import { type CartResponse, getCart } from "@/services/models/cart";

export const useCart = () => {
  const cartStore = useCartStore();

  const isCartEmpty = computed(() => cartStore.cart_count);

  const fetchCart = async () => {
    const { message, data } = await getCart();
    if (!data) return;
    cartSetter(data as CartResponse);
  }

  const cartSetter = (response_data: CartResponse) => {
    cartStore.setCartItems(response_data.items);
    cartStore.setCartCount(response_data.cart_count);
    cartStore.setCartSubtotal(response_data.cart_subtotal);
  }

  return {
    fetchCart,
    cartSetter,
    isCartEmpty,
  }

}
