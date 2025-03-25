<script setup lang="ts">

</script>

<template>
  <dialog id="track_form_modal" class="modal modal-bottom sm:modal-middle">
    <div class="modal-box">
      <h2 class="text-2xl font-bold">Edit track</h2>
      <form id="track-form" ref="trackForm">
      </form>
    </div>
    <div class="modal-action">
      <form id="dialog-form" method="dialog" class="flex justify-end gap-2">
        <button class="btn btn-neutral">Close</button>
        <button class="btn btn-primary">
          Submit
        </button>
      </form>
    </div>
  </dialog>
</template>
