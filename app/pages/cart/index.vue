<script setup lang="ts">
import CartItemList from "./components/CartItemList.vue";
import { useCartStore } from "@/store/cart";

const cartStore = useCartStore();
const subtotal = computed(() => `Subtotal: $${cartStore.cart_subtotal}`)
const isCartEmpty = computed(() => useCart().isCartEmpty);

</script>

