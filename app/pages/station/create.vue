<template>
  <AppPageContainer>
    <h1 class="text-3xl font-bold">Customize Station</h1>
    <form id="form" class="mt-8">

      <label class="form-control w-full max-w-lg">
        <div class="label flex flex-col items-start">
          <span class="label-text text-lg font-bold">Name</span>
          <span class="label-text">Choose a station name that represents your brand and content.</span>
        </div>
        <input v-model="form.name" id="name" name="name" type="text" placeholder="Enter station name"
          class="input input-ghost bg-neutral w-full max-w-lg" :class="formNameError" />
        <div class="label" :class="!formErrors.name ? 'invisible' : ''">
          <span class="label-text-alt text-error">
            {{ formErrors.name }}
          </span>
        </div>
      </label>

      <label class="form-control w-full max-w-lg">
        <div class="label flex flex-col items-start">
          <span class="label-text text-lg font-bold">Handle</span>
          <span class="label-text">Choose your unique handle by adding letters and numbers.</span>
        </div>
        <label class="input input-ghost bg-neutral flex items-center" :class="formHandleError">
          <Icon icon="streamline:sign-at-solid" />
          <input v-model="form.handle" id="handle" name="handle" type="text" placeholder="Set your handle"
            class="grow w-full max-w-lg" />
        </label>
        <div class="label" :class="!formErrors.handle ? 'invisible' : ''">
          <span class="label-text-alt text-error">
            {{ formErrors.handle }}
          </span>
        </div>
      </label>

      <label class="form-control w-full max-w-lg">
        <div class="label flex flex-col items-start">
          <span class="label-text text-lg font-bold">Email</span>
          <span class="label-text">Let people know how to contact you with business inquiries</span>
        </div>
        <input v-model="form.email" id="email" name="email" type="email" placeholder="Provide email address"
          class="input input-ghost bg-neutral w-full max-w-lg" :class="formEmailError" />
        <div class="label" :class="!formErrors.email ? 'invisible' : ''">
          <span class="label-text-alt text-error">
            {{ formErrors.email }}
          </span>
        </div>
      </label>

      <label class="form-control w-full max-w-lg">
        <div class="label">
          <span class="label-text text-lg font-bold">Description(optional)</span>
        </div>
        <textarea v-model="form.description" id="description" name="description"
          class="textarea textarea-ghost bg-neutral w-full max-w-lg h-48" :class="formDescriptionError"
          placeholder="Tell listeners about your station."></textarea>
        <div class="label">
          <span class="label-text-alt text-error" :class="!formErrors.description ? 'invisible' : ''">
            {{ formErrors.description }}
          </span>
        </div>
      </label>

    </form>
    <button @click="!isLoading ? submitHandler() : false" class="btn btn-primary text-lg">
      {{ !isLoading ? 'Submit' : 'Processing' }}
      <span v-if="isLoading" class="loading loading-dots loading-md"></span>
    </button>
  </AppPageContainer>
</template>

<script setup lang="ts">
import { type Station, createStation } from "@/services/models/station";
import { useUserStore } from "@/store/user";

definePageMeta({
  middleware: ["auth"]
})

const userStore = useUserStore();
const pubkey = userStore.pubkey as string;
const isLoading = ref(false);
const form = reactive({
  name: '',
  handle: '',
  email: '',
  description: ''
});

const formErrors = reactive<any>({
  name: '',
  handle: '',
  email: '',
  description: ''
});

const inputErrorClass = 'input-error';

const formNameError = computed(() => formErrors.name ? inputErrorClass : '')
const formHandleError = computed(() => formErrors.handle ? inputErrorClass : '')
const formEmailError = computed(() => formErrors.email ? inputErrorClass : '')
const formDescriptionError = computed(() => formErrors.description ? 'textarea-error' : '')


const toast = useToast();

const submitHandler = async () => {
  isLoading.value = true;
  const res = await createStation(form);
  if (res.error) {
    errorHandler(res);
    setTimeout(() => { isLoading.value = false }, 1000);
    return
  }
  setTimeout(() => { isLoading.value = false }, 3000);
  toast.setToast('Station created', 'SUCCESS')
}

const errorHandler = (res: any) => {
  const obj = res.error
  Object.keys(formErrors).forEach(key => {
    if (key in obj) {
      formErrors[`${key}`] = obj[key].length === 1 ? obj[key][0] : obj[key];
    } else {
      formErrors[key] = '';
    }
  });
}

</script>
