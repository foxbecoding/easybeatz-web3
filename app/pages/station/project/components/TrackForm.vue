<script setup lang="ts">
import { useCreateProjectStore } from "@/store/createProject";

const createProjectStore = useCreateProjectStore();

const nextStepHandler = async () => {
  createProjectStore.next();
}

const backStepHandler = async () => {
  createProjectStore.back();
}
</script>

<template>
  <h1 class="text-2xl">Track Form</h1>
  <div class="flex justify-between">
    <button @click="backStepHandler()" class="btn text-lg rounded-[1rem]">
      <Icon icon="solar:alt-arrow-left-line-duotone" class="text-2xl" />
      Back
    </button>
    <button @click="nextStepHandler()" class="btn btn-secondary text-lg rounded-[1rem]">
      Next
      <Icon icon="solar:alt-arrow-right-line-duotone" class="text-2xl" />
    </button>
  </div>
</template>
