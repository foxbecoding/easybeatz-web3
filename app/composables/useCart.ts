import { useCartStore } from "@/store/cart";
import { type CartResponse, getCart } from "@/services/models/cart";

export const useCart = () => {
  const cartStore = useCartStore();

  const fetchCart = async () => {
    const { message, data } = await getCart();
    if (!data) return;
    cartSetter(data as CartResponse);
  }

  const cartSetter = (response_data: CartResponse) => {
    if (response_data.items.length === 0) return;
    cartStore.setCartItems(response_data.items);
    cartStore.setCartCount(response_data.cart_count);
    cartStore.setCartSubtotal(response_data.cart_subtotal);
  }

  return {
    fetchCart,
    cartSetter
  }

}
