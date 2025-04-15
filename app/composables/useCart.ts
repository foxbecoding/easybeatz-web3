import { useCartStore } from "@/store/cart";
import { type CartResponse, type CartItem, getCart, addCartItem } from "@/services/models/cart";
import { TrackPriceEnum } from "@/services/enums/track-price-enums";

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
