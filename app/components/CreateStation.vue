<template>
  <dialog class="modal modal-bottom sm:modal-middle" open>
    <div class="modal-box">
      <h3 class="text-lg font-bold">Hello!</h3>
      <p class="py-4">Press ESC key or click the button below to close</p>
      <div class="modal-action">
        <form method="dialog">
          <!-- if there is a button in form, it will close the modal -->
          <button class="btn">Close</button>
        </form>
      </div>
    </div>
  </dialog>
</template>

<script setup lang="ts"></script>

<style scoped>
.modal {
  width: calc(100% + 320px) !important;
}
</style>
