<script setup lang="ts">
import { useCreateProjectStore } from "@/store/createProject";

const createProjectStore = useCreateProjectStore();

const albumCoverForm = {
  label: "Project cover",
  text: "*Recommended: For best quality, provide a square image that is at least 200x200 pixels."
}

const fileInput = ref();
const previewUrl = computed(() => createProjectStore.coverPreviewUrl);

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (!file) return;

  // Revoke the previous URL to avoid memory leaks
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value);
  }

  // Create a new URL for the selected file
  createProjectStore.coverPreviewUrl = URL.createObjectURL(file);
  createProjectStore.albumForm.cover = file;
};

const triggerFileInput = () => {
  fileInput.value.click();
}

const img = useImage()
const coverImgStyles = computed(() => {
  const imgUrl = img(createProjectStore.coverPreviewUrl, { width: 100 })
  return { backgroundImage: `url('${imgUrl}')`, backgroundSize: 'cover' }
})

//< NuxtImg v-else class="rounded-[1rem]" : src = "previewUrl" width = "120px" height = "120px" alt = "project cover" />
</script>

<template>
  <h2 class="text-2xl font-bold mb-4">Add project details</h2>
  <p class="text-lg font-bold mb-2">{{ albumCoverForm.label }}</p>
  <p class="mb-4 max-w-[400px] block md:hidden"> {{ albumCoverForm.text }} </p>

  <div class="flex">
    <div class="group bg-neutral rounded-[1rem] relative w-[120px] h-[120px]">
      <button v-if="!previewUrl" @click="triggerFileInput"
        class="btn btn-neutral btn-square rounded-[1rem] h-full w-full">
        <Icon icon="solar:camera-add-bold" class="text-4xl" />
      </button>
      <div :style="coverImgStyles" v-else class="aspect-sqaure w-[120px] h-[120px] rounded-[1rem]"></div>
      <button v-if="previewUrl" @click="triggerFileInput" class="btn glass mask mask-squircle upload-button opacity-80">
        <Icon icon="solar:camera-add-bold" class="text-xl" />
      </button>
      <input ref="fileInput" type="file" id="fileInput" accept=".png,.jpg,.jpeg,.avif,.bmp,.webp" @change="onFileChange"
        class="hidden" />
    </div>
    <p class="ml-4 max-w-[300px] hidden md:block"> {{ albumCoverForm.text }} </p>
  </div>

  <form id="form" @keydown.enter.prevent>
    <label class="form-control w-full my-4">
      <div class="label flex flex-col items-start">
        <span class="label-text text-lg font-bold">Title</span>
        <span class="label-text">Choose a title that represents your project.</span>
      </div>
      <input v-model="createProjectStore.albumForm.title" id="name" name="name" type="text"
        placeholder="Enter project title" class="input input-ghost bg-neutral w-full" />
    </label>

    <label class="form-control w-full">
      <div class="label">
        <span class="label-text text-lg font-bold">Description(optional)</span>
      </div>
      <textarea v-model="createProjectStore.albumForm.bio" id="bio" name="bio"
        class="textarea textarea-ghost bg-neutral w-full h-48"
        placeholder="Tell listeners what your project is about."></textarea>
    </label>
  </form>
</template>

<style scoped>
.upload-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) !important;
}
</style>
