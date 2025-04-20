<script setup lang="ts">
import CartItem from "./CartItem.vue"
import { type CartItem as CartItemType } from "@/services/models/cart"

defineProps<{ cartItems: CartItemType[] }>();

</script>

