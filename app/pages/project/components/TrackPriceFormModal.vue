<script setup lang="ts">
import { type Track, updateTrackPrice } from "@/services/models/album";

const props = defineProps<{
  track: Track;
}>();

// Modal control logic
const model = defineModel({ default: false, required: true });
const closeModal = () => model.value = false;
watch(model, (newVal) => {
  if (newVal) {
    document.getElementById('form_modal')?.showModal();
  } else {
    document.getElementById('form_modal')?.close();
  }
});

// Form fields logic
const form = ref();
const formFields = reactive<any>({
  price: props.track.price,
});

const formErrors = reactive<any>({
  price: '',
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
const emit = defineEmits(["submitPrice"]);
const submit = async () => {
  if (isLoading.value) return;
  isLoading.value = true;
  const requestData = { value: formFields.price }

  try {
    const { message, data } = await updateTrackPrice(props.track.tid, requestData);
    if (message) {
      useToast().setToast(message, "INFO");
      emit("submitPrice");
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
</template>
