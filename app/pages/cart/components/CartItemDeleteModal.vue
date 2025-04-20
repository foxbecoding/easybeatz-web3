<script setup lang="ts">
import { type CartItem } from "@/services/models/cart";

const props = defineProps<{
  cartItem: CartItem;
}>();

// Modal control logic
const model = defineModel({ default: false, required: true });
const modalID = computed(() => `cart_item_${props.cartItem.track.tid}_modal`);
const closeModal = () => model.value = false;
watch(model, (newVal: any) => {
  if (newVal) {
    document.getElementById(modalID.value)?.showModal();
  } else {
    document.getElementById(modalID.value)?.close();
  }
});

// Submit logic
const emit = defineEmits(["submit"]);
const submit = async () => {
  emit("submit");
  closeModal();
}

</script>

