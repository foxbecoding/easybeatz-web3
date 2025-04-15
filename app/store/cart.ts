export const useCartStore = defineStore("use-cart-store", () => {
  const items = ref([])

  return {
    items
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useCartStore, import.meta.hot));
} 
