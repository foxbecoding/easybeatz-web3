<script setup lang="ts">

const { albumForm, isStep2, isStep1Completed } = useCreateProject();

const albumCoverForm = {
  label: "Project cover",
  text: "*Recommended: For best quality, provide a square image that is at least 200x200 pixels."
}

const fileInput = ref();
const previewUrl = ref<string | null>(null);

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (!file) return;

  // Revoke the previous URL to avoid memory leaks
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value);
  }

  // Create a new URL for the selected file
  previewUrl.value = URL.createObjectURL(file);
  albumForm.cover = file;
  console.log(previewUrl.value)
};

const triggerFileInput = () => {
  fileInput.value.click();
}

</script>

<template>

  <h4 class="text-2xl font-bold mb-4">Add project details</h4>
  <p class="text-lg font-bold mb-2">{{ albumCoverForm.label }}</p>
  <p class="mb-4 max-w-[400px] block md:hidden"> {{ albumCoverForm.text }} </p>
  <div class="flex">
    <button @click="triggerFileInput" class="btn btn-base-100 btn-square h-[120px] w-[120px]">
      <Icon icon="solar:camera-add-bold" class="text-4xl" />
    </button>

    <input ref="fileInput" type="file" id="fileInput" accept=".png,.jpg,.jpeg,.avif" @change="onFileChange"
      class="hidden" />
    <p class="ml-4 max-w-[300px] hidden md:block"> {{ albumCoverForm.text }} </p>
  </div>

  <form id="form">
    <label class="form-control w-full max-w-lg my-4">
      <div class="label flex flex-col items-start">
        <span class="label-text text-lg font-bold">Title</span>
        <span class="label-text">Choose a title that represents your project.</span>
      </div>
      <input v-model="albumForm.title" id="name" name="name" type="text" placeholder="Enter project title"
        class="input input-ghost bg-base-100 w-full max-w-lg" />
    </label>

    <label class="form-control w-full max-w-lg">
      <div class="label">
        <span class="label-text text-lg font-bold">Description(optional)</span>
      </div>
      <textarea v-model="albumForm.bio" id="bio" name="bio"
        class="textarea textarea-ghost bg-base-100 w-full max-w-lg h-48"
        placeholder="Tell listeners what your project is about."></textarea>
    </label>
  </form>

  <div class="w-full mt-4 flex justify-end">
    <button class="btn btn-secondary text-lg rounded-[1rem]" :disabled="!isStep1Completed">
      Next
      <Icon icon="solar:alt-arrow-right-line-duotone" class="text-2xl" />
    </button>
  </div>

</template>
