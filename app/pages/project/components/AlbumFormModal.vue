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

</script>

<template>
</template>
