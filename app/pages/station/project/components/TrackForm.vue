<script setup lang="ts">
import { useCreateProjectStore } from "@/store/createProject";

const createProjectStore = useCreateProjectStore();

const nextStepHandler = async () => {
  createProjectStore.next();
}

const backStepHandler = async () => {
  createProjectStore.back();
}

const sanitizeInput = (index: any, event: any) => {
  let value = event.target.value;

  // Remove non-digit characters
  value = value.replace(/\D/g, '');

  // Remove leading zeros
  value = value.replace(/^0+/, '');

  // Update the corresponding item in the array
  createProjectStore.trackFormFields[index]['price'] = value;
};

</script>

<template>
  <h1 class="text-2xl font-bold">Add project tracks</h1>
  {{ createProjectStore.trackFormFields }}
  <form id="form" class="mt-4">
    <div v-for="(track, t) in createProjectStore.trackFormFields" :key="t">
      <p class="text-xl font-bold">Track {{ t + 1 }}</p>
      <div class="mb-4">
        <label class="form-control w-full max-w-lg">
          <div class="label flex flex-col items-start">
            <span class="label-text text-lg font-bold">Title</span>
            <span class="label-text">Choose a title for your track.</span>
          </div>
          <input v-model="track.title" id="title" name="title" type="text" placeholder="Enter track title"
            class="input input-ghost bg-base-100 w-full max-w-lg" />
        </label>
      </div>
      <div class="mb-4">
        <label class="form-control w-full max-w-lg">
          <div class="label flex flex-col items-start">
            <span class="label-text text-lg font-bold">Price</span>
          </div>
          <input v-model="track.price" @input="sanitizeInput(t, $event)" id="price" name="price"
            placeholder="Enter track price" class="input input-ghost bg-base-100 w-full max-w-lg" />
        </label>
      </div>
    </div>
  </form>
  <button class="btn btn-secondary text-lg">
    <Icon icon="material-symbols:music-note-add-rounded" class="text-2xl" />
    Add new track
  </button>

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
