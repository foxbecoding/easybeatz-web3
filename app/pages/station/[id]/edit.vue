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
        <label class="input input-ghost bg-neutral flex items-center">
          <Icon icon="streamline:sign-at-solid" />
          <input v-model="form.handle" id="handle" name="handle" type="text" placeholder="Set your handle"
            class="grow w-full max-w-lg" :class="formHandleError" />
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
          <span class="label-text text-lg font-bold">Description</span>
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
    <button @click="saveHandler()" class="btn btn-primary text-lg">Save</button>
  </AppPageContainer>
</template>

<script setup lang="ts">
import { type Station, partialUpdateStation } from "@/services/models/station";

definePageMeta({
  middleware: ["auth"]
})

const route = useRoute();
const pubkey = String(route.params.id)
const form = reactive({
  name: '',
  handle: '',
  email: '',
  description: ''
});

const formErrors = reactive({
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

watch(form, (newForm) => {
  console.log(newForm)
});

const saveHandler = async () => {
  const res = await partialUpdateStation(pubkey, form);
}

</script>
