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

<template>
  <dialog :id="modalID" class="modal modal-bottom sm:modal-middle">
    <div class="modal-box">
      <h2 class="text-2xl font-bold">Remove track from cart?</h2>
      <p>{{ cartItem.track.title }}</p>
      <div class="modal-action">
        <button @click="closeModal()" class="btn btn-neutral">Close</button>
        <button @click="submit()" class="btn btn-error">
          Remove
        </button>
      </div>
    </div>
  </dialog>
</template>
