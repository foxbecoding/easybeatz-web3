<script setup lang="ts">
import { type Station, createStation, updateStation } from "@/services/models/station";

const props = defineProps<{
  title: string;
  type: "CREATE" | "EDIT";
  pubkey?: string;
  station?: Station | null;
}>();

const emit = defineEmits(['submit'])
const isLoading = ref(false);

const form = reactive<any>({
  name: props.station ? props.station.name : '',
  handle: props.station ? props.station.handle : '',
  email: props.station ? props.station.email : '',
  description: props.station ? props.station.description : ''
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

const submitRequestRouter = async () => {
  if (props.type == 'CREATE') {
    return createStation(form);
  }
  return updateStation(String(props.pubkey), form);
}

const submitHandler = async () => {
  isLoading.value = true;
  try {
    const { message, data } = await submitRequestRouter() as any;
    if (message) {
      useToast().setToast(message, 'SUCCESS');
    }
    setTimeout(() => { isLoading.value = false }, 3000);
    emit('submit');
  } catch (error: any) {
    const { message, data } = error.data;
    if (message) {
      useToast().setToast(message, 'ERROR');
    }
    setTimeout(() => { isLoading.value = false }, 1000);
    errorHandler(data);
  }
}

const errorHandler = (res: any) => {
  const obj = res;
  Object.keys(formErrors).forEach(key => {
    if (key in obj) {
      formErrors[`${key}`] = obj[key].length === 1 ? obj[key][0] : obj[key];
    } else {
      formErrors[key] = '';
    }
  });
}
</script>

<template>
  <div class="max-w-[600px] flex flex-col gap-4">
    <h1 class="text-3xl font-bold">{{ props.title }}</h1>

    <form id="form" class="w-full" @keydown.enter.prevent>
      <label class="form-control w-full">
        <div class="label flex flex-col items-start">
          <span class="label-text text-lg font-bold">Name</span>
          <span class="label-text">Choose a station name that represents your brand and content.</span>
        </div>
        <input v-model="form.name" id="name" name="name" type="text" placeholder="Enter station name"
          class="input input-ghost bg-neutral w-full" :class="formNameError" />
        <div class="label" :class="!formErrors.name ? 'invisible' : ''">
          <span class="label-text-alt text-error">
            {{ formErrors.name }}
          </span>
        </div>
      </label>

      <label class="form-control w-full">
        <div class="label flex flex-col items-start">
          <span class="label-text text-lg font-bold">Handle</span>
          <span class="label-text">Choose your unique handle by adding letters and numbers.</span>
        </div>
        <label class="input input-ghost bg-neutral flex items-center" :class="formHandleError">
          <Icon icon="streamline:sign-at-solid" />
          <input v-model="form.handle" id="handle" name="handle" type="text" placeholder="Set your handle"
            class="grow w-full" />
        </label>
        <div class="label" :class="!formErrors.handle ? 'invisible' : ''">
          <span class="label-text-alt text-error">
            {{ formErrors.handle }}
          </span>
        </div>
      </label>

      <label class="form-control w-full">
        <div class="label flex flex-col items-start">
          <span class="label-text text-lg font-bold">Email</span>
          <span class="label-text">Let people know how to contact you with business inquiries</span>
        </div>
        <input v-model="form.email" id="email" name="email" type="email" placeholder="Provide email address"
          class="input input-ghost bg-neutral w-full" :class="formEmailError" />
        <div class="label" :class="!formErrors.email ? 'invisible' : ''">
          <span class="label-text-alt text-error">
            {{ formErrors.email }}
          </span>
        </div>
      </label>

      <label class="form-control w-full">
        <div class="label">
          <span class="label-text text-lg font-bold">Description(optional)</span>
        </div>
        <textarea v-model="form.description" id="description" name="description"
          class="textarea textarea-ghost bg-neutral w-full h-48" :class="formDescriptionError"
          placeholder="Tell listeners about your station."></textarea>
        <div class="label">
          <span class="label-text-alt text-error" :class="!formErrors.description ? 'invisible' : ''">
            {{ formErrors.description }}
          </span>
        </div>
      </label>
    </form>

    <button @click="!isLoading ? submitHandler() : false" class="btn btn-primary rounded-[1rem] btn-block text-lg">
      {{ !isLoading ? 'Submit' : 'Processing' }}
      <span v-if="isLoading" class="loading loading-dots loading-md"></span>
    </button>

  </div>
</template>
