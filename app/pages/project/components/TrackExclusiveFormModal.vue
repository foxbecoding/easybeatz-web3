<script setup lang="ts">
import { type Track, updateTrackExclusivePrice } from "@/services/models/album";

const props = defineProps<{
  track: Track;
}>();

// Modal control logic
const model = defineModel({ default: false, required: true });
const closeModal = () => model.value = false;
watch(model, (newVal) => {
  if (newVal) {
    document.getElementById('track_exclusive_modal')?.showModal();
  } else {
    document.getElementById('track_exclusive_modal')?.close();
  }
});

// Form fields logic
const form = ref();
const formFields = reactive<any>({
  exclusive_price: props.track.exclusive_price,
});

const formErrors = reactive<any>({
  exclusive_price: '',
});

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

//Form submit logic
const isLoading = ref(false);
const emit = defineEmits(["submitExclusive"]);
const submit = async () => {
  if (isLoading.value) return;
  isLoading.value = true;
  const requestData = { value: formFields.exclusive_price }

  try {
    const { message, data } = await updateTrackExclusivePrice(props.track.tid, requestData);
    if (message) {
      useToast().setToast(message, "INFO");
      emit("submitExclusive");
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

</script>

<template>
  <dialog id="track_exclusive_modal" class="modal modal-bottom sm:modal-middle">
    <div class="modal-box">
      <h2 class="text-2xl font-bold">{{ track.exclusive_price ? 'Edit' : 'Add' }} track exclusive price</h2>
      <form id="track-form" ref="form" class="flex flex-col gap-4" @keydown.enter.prevent>
        <label class="form-control w-full">
          <div class="label flex flex-col items-start">
            <span class="label-text text-lg font-semibold">Exclusive price</span>
          </div>
          <input v-model="formFields.exclusive_price" @input="numbersOnlyInput" @keydown="numbersOnlyInput"
            id="exclusive_price" name="exclusive_price" type="number" placeholder="Enter track exclusive price"
            class="input input-ghost bg-neutral w-full" :class="formErrors.exclusive_price ? 'input-error' : ''" />
          <div v-if="formErrors.exclusive_price" class="label">
            <span class="label-text-alt text-error">
              {{ formErrors.exclusive_price }}
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
