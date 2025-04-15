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

    if (response_data.items.length === 0) return;
    cartStore.setCartItems(response_data.items);
    cartStore.setCartCount(response_data.cart_count);
    cartStore.setCartSubtotal(response_data.cart_subtotal);

  }

  //const addCartItemHandler = async () => {
  //  try {
  //    const res = await submitTrackFavorite(tid);
  //    userStore.favoriteTracks.push(res.data);
  //    useToast().setToast(res.message, "SUCCESS");
  //  } catch (error: any) {
  //    if (error.status === 401) {
  //      useToast().setToast("Please login", "INFO");
  //      return;
  //    }
  //    useToast().setToast(error.data.message, "ERROR");
  //  }
  //}
  //
  //const removeCartItemHandler = async () => {
  //  try {
  //    const res = await removeTrackFavorite(tid);
  //    userStore.favoriteTracks = userStore.favoriteTracks.filter(x => x !== res.data);
  //    useToast().setToast(res.message, "SUCCESS");
  //  } catch (error: any) {
  //    if (error.status === 401) {
  //      useToast().setToast("Please login", "INFO");
  //      return;
  //    }
  //    useToast().setToast(error.data.message, "ERROR");
  //  }
  //}

  return {
    fetchCart,
  }

}
