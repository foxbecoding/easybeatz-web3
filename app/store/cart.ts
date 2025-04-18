import { type CartItem } from "@/services/models/cart";

export const useCartStore = defineStore("use-cart-store", () => {
  const items = ref<CartItem[]>([])
  const cart_count = ref(0);
  const cart_subtotal = ref(0);

  const setCartItems = (_items: CartItem[]) => items.value = _items;
  const setCartCount = (_count: number) => cart_count.value = _count;
  const setCartSubtotal = (_subtotal: number) => cart_subtotal.value = _subtotal;

  return {
    items,
    cart_count,
    setCartCount,
    setCartItems,
    setCartSubtotal
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useCartStore, import.meta.hot));
} 
