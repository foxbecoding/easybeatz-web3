<script setup lang="ts">
import CartItemList from "./components/CartItemList.vue";
import { useCartStore } from "@/store/cart";

const cartStore = useCartStore();
const subtotal = computed(() => `Subtotal: $${cartStore.cart_subtotal}`)
const isCartEmpty = computed(() => useCart().isCartEmpty);

</script>

<template>
  <AppPageContainer>
    <div class="flex flex-col gap-4 max-w-[800px]">
      <h1 class="text-3xl font-bold">Cart</h1>
      <div v-if="isCartEmpty" class="flex flex-col w-full gap-4">
        <div class="flex flex-col gap-4 w-full">
          <CartItemList :cart-items="cartStore.items" />
        </div>
        <div class="divider"></div>
        <div class="flex flex-col gap-4">
          <p class="ml-auto text-lg">{{ subtotal }}</p>
          <button class="btn btn-secondary rounded-[1rem] text-lg">Checkout</button>
        </div>
      </div>
      <div v-else>
        <h3 class="text-lg font-semibold">Cart is empty</h3>
      </div>
    </div>
  </AppPageContainer>
</template>
