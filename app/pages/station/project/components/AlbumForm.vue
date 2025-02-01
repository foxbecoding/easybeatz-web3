<script setup lang="ts">

const albumCoverForm = {
  label: "Add project cover",
  text: "*Recommended: For best quality, provide a square image that is at least 200x200 pixels."
}

</script>

<template>

  <h4 class="text-2xl font-bold md:mb-4">{{ albumCoverForm.label }}</h4>
  <p class="mb-4 max-w-[400px] block md:hidden"> {{ albumCoverForm.text }} </p>
  <div class="flex">
    <button class="btn btn-base-100 btn-square h-[120px] w-[120px]">
      <Icon icon="solar:camera-add-bold" class="text-4xl" />
    </button>
    <p class="ml-4 max-w-[300px] hidden md:block"> {{ albumCoverForm.text }} </p>
  </div>
</template>
