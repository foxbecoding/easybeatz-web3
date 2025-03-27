<script setup lang="ts">
import { type Track, updateTrack } from "@/services/models/album";
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";

const props = defineProps<{
  track: Track;
  genres: Genre[];
  moods: Mood[];
}>();

// Modal control logic
const model = defineModel({ default: false, required: true });
const closeModal = () => model.value = false;
watch(model, (newVal) => {
  if (newVal) {
    document.getElementById('track_form_modal')?.showModal();
  } else {
    document.getElementById('track_form_modal')?.close();
  }
});

// Form fields logic
const form = ref();
const formFields = reactive<any>({
  title: props.track.title,
  bpm: props.track.bpm,
  genres: props.track.genres.slug,
  mood: props.track.mood.slug,
});

const formErrors = reactive<any>({
  title: '',
  bpm: '',
  genres: '',
  mood: '',
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
const emit = defineEmits(["submitDetails"]);
const submit = async () => {
  if (isLoading.value) return;
  isLoading.value = true;

  const selectedGenre = findSelectedGenre(formFields.genres);
  const selectedMood = findSelectedMood(formFields.mood);
  const requestData = {
    title: formFields.title,
    bpm: formFields.bpm,
    genres: [selectedGenre.pk],
    mood: selectedMood.pk
  }

  try {
    const { message, data } = await updateTrack(props.track.tid, requestData);
    if (message) {
      useToast().setToast(message, "INFO");
      emit("submitDetails");
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

const findSelectedGenre = (slug: string): Genre =>
  findSelectedValue(slug, props.genres) as Genre;

const findSelectedMood = (slug: string): Mood =>
  findSelectedValue(slug, props.moods) as Mood;

const findSelectedValue = (slug: string, arr: Genre[] | Mood[]): Genre | Mood =>
  arr.find(x => x.slug === slug) as Genre | Mood;

</script>

<template>
  <dialog id="track_form_modal" class="modal modal-bottom sm:modal-middle">
    <div class="modal-box">
      <h2 class="text-2xl font-bold">Edit track details</h2>
      <form id="track-form" ref="form" class="flex flex-col gap-4" @keydown.enter.prevent>
        <label class="form-control w-full">
          <div class="label flex flex-col items-start">
            <span class="label-text text-lg font-semibold">Title</span>
          </div>
          <input v-model="formFields.title" id=" title" name="title" type="text" placeholder="Enter album title"
            class="input input-ghost bg-neutral w-full" :class="formErrors.title ? 'input-error' : ''" />
          <div v-if="formErrors.title" class="label">
            <span class="label-text-alt text-error">
              {{ formErrors.title }}
            </span>
          </div>
        </label>

      </form>
    </div>
    <div class="modal-action">
      <form id="dialog-form" method="dialog" class="flex justify-end gap-2">
        <button class="btn btn-neutral">Close</button>
        <button class="btn btn-primary">
          Submit
        </button>
      </form>
    </div>
  </dialog>
</template>
