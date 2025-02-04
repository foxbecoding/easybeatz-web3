<script setup lang="ts">
import { useCreateProjectStore } from "@/store/createProject";

const createProjectStore = useCreateProjectStore();

const backStepHandler = async () => {
  createProjectStore.back();
}
</script>

<template>
  <h1 class="text-2xl">Review</h1>
  <div class="flex justify-between">
    <button @click="backStepHandler()" class="btn text-lg rounded-[1rem]">
      <Icon icon="solar:alt-arrow-left-line-duotone" class="text-2xl" />
      Back
    </button>
    <button class="btn btn-primary text-lg rounded-[1rem]">
      Submit
    </button>
  </div>
</template>
