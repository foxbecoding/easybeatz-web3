<script setup lang="ts">
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";
import { useCreateProjectStore } from "@/store/createProject";
import AlbumForm from "./AlbumForm.vue";
import TrackForm from "./TrackForm.vue";

const props = defineProps<{
  genres: Genre[] | null;
  moods: Mood[] | null;
}>();

const isLoading = ref(false);
const createProjectStore = useCreateProjectStore();
const isProjectValid = computed(() => createProjectStore.isProjectValid);
const submitBtnLabel = computed(() => !isLoading.value ? 'Submit' : 'Submitting')

const submitHandler = async () => {
  if (isLoading.value) return;
  isLoading.value = true;
  if (!isProjectValid.value) return;
  const res = await createProjectStore.submit();
  if (!res) {
    isLoading.value = false;
    return;
  }
  isLoading.value = false;
  useToast().setToast('Project created', 'INFO');
};
</script>

<template>
  <div class="card bg-base-100 max-w-[600px] w-full block">
    <div class="card-body px-0 pt-0 pb-4">
      <AlbumForm />
      <div class="divider" />
      <TrackForm :genres="genres" :moods="moods" />
    </div>
    <div class="card-actions">
      <button @click="submitHandler()" class="btn btn-primary w-full rounded-[1rem] text-lg"
        :disabled="!isProjectValid">
        {{ submitBtnLabel }}
        <span v-if="isLoading" class="loading loading-dots loading-md"></span>
      </button>
    </div>
  </div>
</template>
