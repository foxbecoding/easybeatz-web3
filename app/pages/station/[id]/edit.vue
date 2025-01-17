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
          class="input input-ghost bg-neutral w-full max-w-lg" />
        <div class="label invisible">
          <span class="label-text-alt">Bottom Left label</span>
        </div>
      </label>

      <label class="form-control w-full max-w-lg">
        <div class="label flex flex-col items-start">
          <span class="label-text text-lg font-bold">Handle</span>
          <span class="label-text">Choose your unique handle by adding letters and numbers.</span>
        </div>


        <label class="input input-ghost bg-neutral flex items-center gap-2">
          <Icon icon="streamline:sign-at-solid" />
          <input v-model="form.handle" id="handle" name="handle" type="text" placeholder="Set your handle"
            class="grow w-full max-w-lg" />
        </label>
        <div class="label invisible">
          <span class="label-text-alt">Bottom Left label</span>
        </div>
      </label>

      <label class="form-control w-full max-w-lg">
        <div class="label flex flex-col items-start">
          <span class="label-text text-lg font-bold">Email</span>
          <span class="label-text">Let people know how to contact you with business inquiries</span>
        </div>
        <input v-model="form.email" id="email" name="email" type="email" placeholder="provide email address"
          class="input input-ghost bg-neutral w-full max-w-lg" />
        <div class="label invisible">
          <span class="label-text-alt">Bottom Left label</span>
        </div>
      </label>

      <label class="form-control w-full max-w-lg">
        <div class="label">
          <span class="label-text text-lg font-bold">Description</span>
        </div>
        <textarea v-model="form.description" id="description" name="description"
          class="textarea textarea-ghost bg-neutral w-full max-w-lg h-48"
          placeholder="Tell listeners about your station."></textarea>
        <div class="label">
          <span class="label-text-alt invisible">Your bio</span>
        </div>
      </label>

    </form>
  </AppPageContainer>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: ["auth"]
})

const route = useRoute();
const pubkey = route.params.pubkey
const form = reactive({
  name: '',
  handle: '',
  email: '',
  description: ''
})

watch(form, (newForm) => {
  console.log(newForm)
})

</script>
