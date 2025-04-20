<script setup lang="ts">
import CartItem from "./CartItem.vue"
import { type CartItem as CartItemType } from "@/services/models/cart"

defineProps<{ cartItems: CartItemType[] }>();

</script>

<template>
  <div id="cart-items" class="flex flex-col gap-4 w-full">
    <div v-for="(item, i) in cartItems" class="flex flex-col ">
      <CartItem :cart-item="item" />
      <div v-if="false" class="divider"></div>
    </div>
  </div>
</template>
