export default defineNuxtPlugin(async (nuxtApp) => {
  useCart().fetchCart()
});
