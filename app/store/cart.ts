import { type CartItem } from "@/services/models/cart";

export const useCartStore = defineStore("use-cart-store", () => {
  const items = ref<CartItem[]>([])
  const cart_count = ref(0);
  const cart_subtotal = ref(0);

  return {
    items
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useCartStore, import.meta.hot));
} 
