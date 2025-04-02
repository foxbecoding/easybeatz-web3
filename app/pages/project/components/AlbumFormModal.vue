<script setup lang="ts">
import { updateAlbum } from "@/services/models/album";

const props = defineProps<{
  title: String;
  bio: String;
}>();

const aid = useRoute().params.aid

const model = defineModel({ default: false, required: true });
const closeModal = () => model.value = false;
const isLoading = ref(false);

const emit = defineEmits(["submit"]);
const submit = async () => {
  if (isLoading.value) return;
  isLoading.value = true;
  try {
    const { message, data } = await updateAlbum(aid.toString(), formFields);
    if (message) {
      useToast().setToast(message, "INFO");
      emit("submit");
      closeModal();
      clearFormErrors();
    }
  }
  catch (error: any) {
    const { message, data } = error.data;
    setFormErrors(data);
  }
  finally {
    setTimeout(() => {
      isLoading.value = false;
    }, 2000);
  }
}

const formFields = reactive({
  title: props.title,
  bio: props.bio.toString()
})

const formErrors = reactive<any>({
  title: '',
  bio: ''
});

const formTitleError = computed(() => formErrors.title ? 'input-error' : '')
const formBioError = computed(() => formErrors.bio ? 'textarea-error' : '')

const setFormErrors = (res: any) => {
  const obj = res;
  Object.keys(formErrors).forEach(key => {
    if (key in obj) {
      formErrors[`${key}`] = obj[key].length === 1 ? obj[key][0] : obj[key];
    } else {
      formErrors[key] = '';
    }
  });
}

const clearFormErrors = () => {
  Object.keys(formErrors).forEach(key => {
    formErrors[key] = '';
  });
}

watch(model, (newVal) => {
  if (newVal) {
    document.getElementById('album_form_modal')?.showModal();
  } else {
    document.getElementById('album_form_modal')?.close();
  }
});

</script>

<template>
  <dialog id="album_form_modal" class="modal modal-bottom sm:modal-middle">
    <div class="modal-box">
      <h2 class="text-2xl font-bold">Edit project details</h2>
      <form id="album-form" ref="albumForm" class="flex flex-col gap-4" @keydown.enter.prevent>
        <label class="form-control w-full">
          <div class="label flex flex-col items-start">
            <span class="label-text text-lg font-semibold">Title</span>
          </div>
          <input v-model="formFields.title" id="title" name="title" type="text" placeholder="Enter album title"
            class="input input-ghost bg-neutral w-full" :class="formTitleError" />
          <div class="label" :class="!formErrors.title ? 'invisible' : ''">
            <span class="label-text-alt text-error">
              {{ formErrors.title }}
            </span>
          </div>
        </label>

        <label class="form-control w-full">
          <div class="label flex flex-col items-start">
            <span class="label-text text-lg font-semibold">Description</span>
          </div>
          <textarea v-model="formFields.bio" rows="6" id="bio" name="bio" type="text" placeholder="Enter album bio"
            class="textarea textarea-ghost bg-neutral w-full" :class="formBioError"></textarea>
          <div class="label" :class="!formErrors.bio ? 'invisible' : ''">
            <span class="label-text-alt text-error">
              {{ formErrors.bio }}
            </span>
          </div>
        </label>
      </form>

      <div class="modal-action">
        <button @click="closeModal()" class="btn btn-neutral">Close</button>
        <button @click="submit()" class="btn btn-primary">
          Submit
          <span v-if="isLoading" class="loading loading-dots loading-md"></span>
        </button>
      </div>
    </div>
  </dialog>
</template>
