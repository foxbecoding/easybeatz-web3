<script setup lang="ts">
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";

//component types and interfaces
interface TrackStemForm {
  name: string;
  file: File | null;
}

interface CollaboratorForm {
  pubkey: string;
}

interface TrackForm {
  bpm: string;
  collaborators: CollaboratorForm[];
  exclusive_price: string;
  genres: string[];
  mood: string;
  mp3: File | null;
  price: string;
  stems: TrackStemForm[];
  title: string;
  wav?: File | null;
}

// Component props
const props = defineProps<{
  genres: Genre[];
  moods: Mood[];
  formTitle: string;
}>();

// Emiiters
const emit = defineEmits(['submit'])

// Modal control logic
const model = defineModel({ default: false, required: true });
const closeModal = () => model.value = false;
watch(model, (newVal) => {
  if (newVal) {
    document.getElementById('app_track_form_modal')?.showModal();
  } else {
    document.getElementById('app_track_form_modal')?.close();
  }
});

// Track form logic
const trackForm = reactive<TrackForm>({
  bpm: '',
  collaborators: [],
  exclusive_price: '',
  genres: [],
  mood: '',
  mp3: null,
  price: '',
  stems: [],
  title: '',
  wav: null
});

const clearTrackForm = () => {
  trackForm.bpm = '';
  trackForm.collaborators = [];
  trackForm.exclusive_price = '';
  trackForm.genres = [];
  trackForm.mood = '';
  trackForm.mp3 = null;
  trackForm.price = '';
  trackForm.stems = [];
  trackForm.title = '';
  trackForm.wav = null;
  resetSelectedGenre();
}

const isTrackFormValid = computed(() => {
  let validationFields = ['bpm', 'genres', 'mood', 'mp3', 'price', 'title'];

  if (trackForm.stems.length > 0 || trackForm.exclusive_price) {
    validationFields.push('stems')
  }

  if (trackForm.exclusive_price) {
    validationFields.push('exclusive_price')
  }

  const validatedFields = validationFields.map((field: keyof typeof trackForm) => {
    if (field == 'genres') {
      return trackForm[field].length > 0 ? true : false;
    }

    if (field == 'exclusive_price') {
      return trackForm['stems'].length > 0 ? true : false;
    }

    if (field == 'stems') {
      const validStems = trackForm.stems.map(stem => {
        return stem.name && stem.file ? true : false;
      })
      return validStems.every(value => value === true);
    }

    return !!trackForm[field];
  })

  return validatedFields.every(value => value === true);
});

// Genres logic
const selectedGenre = ref('');
const resetSelectedGenre = () => selectedGenre.value = '';
const setGenresField = (genre_pk: string) => {
  trackForm.genres = [];
  trackForm.genres.push(genre_pk);
}
watch(selectedGenre, (newSelected) => {
  if (!newSelected) return false;
  setGenresField(String(newSelected));
});

// MP3 & WAV Media file logic
const onMediaChange = (e: any) => {
  const file: File = e.target.files[0];
  const fileType = e.target.files[0].type;
  if (fileType == 'audio/mpeg') {
    setMp3File(file);
  } else if (fileType == 'audio/wav') {
    setWavFile(file);
  }
}
const setMp3File = (file: File) => trackForm.mp3 = file;
const setWavFile = (file: File) => trackForm.wav = file;

// Colaborators logic
const addCollabHandler = () => trackForm.collaborators.push({ pubkey: '' });
const removeCollabHandler = (index: number) => trackForm.collaborators.splice(index, 1);

// Stems logic
const ExclusivesAndStemsMessage = "If you enter an exclusive price you must include stem files.";
const addStemHandler = () => trackForm.stems.push({ name: '', file: null });
const removeStemHandler = (index: number) => trackForm.stems.splice(index, 1);
const setStemFile = (index: number, file: File) => trackForm.stems[index].file = file;
const onStemChange = (index: number, e: any) => {
  const file: File = e.target.files[0];
  setStemFile(index, file);
}

// Submit form logic
const isLoading = ref(false);
const submitHandler = () => {
  if (isLoading.value) return;
  if (!isTrackFormValid.value) return;
  const formData = new FormData;
  formDataPreparer(formData);
  emit("submit", formData);
}

const formDataPreparer = (formData: FormData) => {
  formData.append(`track[genre_count]`, `${trackForm.genres.length}`);
  formData.append(`track[collab_count]`, `${trackForm.collaborators.length}`);
  formData.append(`track[stem_count]`, `${trackForm.stems.length}`);
  Object.keys(trackForm).forEach(key => {
    if (key == 'wav' && !trackForm.wav) return;
    if (key == 'genres') {
      trackForm.genres.forEach((genre, gi) => {
        formData.append(`track[${key}][${gi}]`, genre)
      });
      return;
    } else if (key == 'collaborators') {
      if (trackForm.collaborators.length < 1) return;
      trackForm.collaborators.forEach((collab, ci) => {
        formData.append(`track[${key}][${ci}]`, collab.pubkey)
      });
      return;
    } else if (key == 'stems') {
      if (trackForm.stems.length < 1) return;
      trackForm.stems.forEach((stem, si) => {
        formData.append(`track[stems][${si}][name]`, stem.name);
        formData.append(`track[stems][${si}][file]`, stem.file);
      });

      return;
    }
    formData.append(`track[${key}]`, trackForm[key]);
  })
}

defineExpose({
  isLoading,
  clearTrackForm,
  closeModal
});

</script>

<template>

  <dialog id="app_track_form_modal" class="modal modal-bottom sm:modal-middle">
    <div class="modal-box">
      <h2 class="text-2xl font-bold">{{ formTitle }}</h2>
      <form id="track-form">
        <section class="flex flex-col gap-2 mt-4">
          <h3 class="text-xl font-bold">Details</h3>
          <label class="form-control w-full">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-semibold">Title</span>
              <span class="label-text">Choose a title for your track.</span>
            </div>
            <input v-model="trackForm.title" id="title" name="title" type="text" placeholder="Enter track title"
              class="input input-ghost bg-neutral w-full" />
          </label>

          <label class="form-control w-full">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-semibold">Price</span>
            </div>
            <label class="input input-ghost bg-neutral flex items-center">
              <Icon icon="material-symbols:attach-money-rounded" width="24" height="24" />
              <input v-model="trackForm.price" @input="numbersOnlyInput" @keydown="numbersOnlyInput" id="price"
                name="price" type="number" placeholder="Enter track price" class="grow w-full" />
            </label>
          </label>

          <label class="form-control w-full">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-semibold">Exclusive price(optional)</span>
              <p class="label-text text-md">
                <span class="text-error">*</span>
                {{ ExclusivesAndStemsMessage }}
              </p>
            </div>
            <label class="input input-ghost bg-neutral flex items-center">
              <Icon icon="material-symbols:attach-money-rounded" class="text-warning" width="24" height="24" />
              <input v-model="trackForm.exclusive_price" @input="numbersOnlyInput" @keydown="numbersOnlyInput"
                id="exclusive_price" name="exclusive_price" type="number" placeholder="Enter track exclusive price"
                class="grow w-full" />
            </label>
          </label>

          <label class="form-control w-full">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-semibold">BPM</span>
            </div>
            <input v-model="trackForm.bpm" @input="numbersOnlyInput" @keydown="numbersOnlyInput" id="bpm" name="bpm"
              type="number" placeholder="Enter track bpm" class="input input-ghost bg-neutral w-full" />
          </label>
        </section>

        <div class="divider" />

        <section class="flex flex-col gap-2 mt-4">
          <h3 class="text-xl font-bold">Genres and Moods</h3>
          <label class="form-control w-full">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-semibold">Genres</span>
            </div>
            <select v-model="selectedGenre" class="select select-ghost bg-neutral w-full" id="genres" name="genres">
              <option disabled selected>Select a genre</option>
              <option v-for="(genre, g) in genres" :key="g" :value="genre.pk" selected>
                {{ genre.name }}
              </option>
            </select>
          </label>

          <label class="form-control w-full">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-semibold">Moods</span>
            </div>
            <select v-model="trackForm.mood" id="moods" name="moods" class="select select-ghost bg-neutral w-full">
              <option disabled selected>Select a mood</option>
              <option v-for="(mood, m) in moods" :key="m" :value="mood.pk" selected>
                {{ mood.name }}
              </option>
            </select>
          </label>
        </section>

        <div class="divider" />

        <section class="flex flex-col gap-2 mt-4">
          <h3 class="text-xl font-bold">Media files</h3>
          <label class="form-control w-full">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-semibold">MP3</span>
            </div>
            <input @change="onMediaChange" type="file" class="file-input file-input-bordered w-full" accept=".mp3"
              id="mp3" name="mp3" />
          </label>

          <label class="form-control w-full">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-semibold">WAV(optional)</span>
            </div>
            <input @change="onMediaChange" type="file" class="file-input file-input-bordered w-full" accept=".wav"
              id="wav" name="wav" />
          </label>

          <div class="flex flex-col gap-3">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-semibold">Stems</span>
              <p>Upload stems files in wav format.</p>
              <p class="label-text text-md">
                <span class="text-error">*</span>
                {{ ExclusivesAndStemsMessage }}
              </p>

            </div>
            <div v-for="(stem, s) in trackForm.stems" :key="s" class="flex flex-col gap-2">
              <div class="flex gap-4">
                <span class="label-text text-lg font-bold">Stem {{ s + 1 }}</span>
                <div class="tooltip" data-tip="Remove stem">
                  <Icon @click="removeStemHandler(s)" icon="solar:trash-bin-minimalistic-bold"
                    class="cursor-pointer opacity-100 hover:opacity-80 active:opacity-60 text-error" width="24"
                    height="24" />
                </div>
              </div>
              <input v-model="stem.name" :id="`stem_${s}`" :name="`stem_${s}`" type="text" placeholder="Enter stem name"
                class="input input-ghost bg-neutral w-full" />
              <input @change="onStemChange(s, $event)" type="file" class="file-input file-input-bordered w-full"
                accept=".wav" :id="`stem_file_${s}`" :name="`stem_file_${s}`" />
            </div>
          </div>

          <a @click="addStemHandler()" class="btn btn-secondary rounded-[1rem] w-40">
            <Icon icon="solar:add-square-bold" width="24" height="24" />
            Add stem
          </a>
        </section>

        <div class="divider" />

        <section class="flex flex-col gap-4 mt-4">
          <div class="flex flex-col gap-1">
            <h3 class="text-xl font-bold">Collaborators</h3>
            <p class="text-md">
              <span class="text-error">*</span>
              Split profits evenly amongst you and collaborators by adding thier Solana wallet address.
            </p>
          </div>
          <div v-if="trackForm.collaborators.length > 0" class="flex flex-col gap-2">
            <div v-for="(collab, c) in trackForm.collaborators" :key="c">
              <label class="form-control w-full">
                <div class="label flex flex-col items-start">
                  <span class="label-text text-lg font-semibold">Collab {{ c + 1 }}</span>
                </div>
                <label class="input input-ghost bg-neutral flex items-center">
                  <input v-model="collab.pubkey" :id="`collab_${c}`" :name="`collab_${c}`" type="text"
                    placeholder="Enter wallet address" class="grow w-full" />
                  <div class="tooltip" data-tip="Remove collab">
                    <Icon @click.stop="removeCollabHandler(c)" icon="solar:trash-bin-minimalistic-bold"
                      class="cursor-pointer opacity-100 hover:opacity-80 active:opacity-60 text-error" width="24"
                      height="24" />
                  </div>
                </label>
              </label>
            </div>
          </div>

          <a @click="addCollabHandler()" class="btn btn-secondary rounded-[1rem] w-40">
            <Icon icon="solar:user-plus-rounded-bold" width="24" height="24" />
            Add collab
          </a>
        </section>
      </form>

      <div class="modal-action flex justify-end gap-2">
        <button @click="closeModal()" class="btn btn-neutral">Close</button>
        <button @click="submitHandler()" class="btn btn-primary" :disabled="!isTrackFormValid">
          Submit
          <span v-if="isLoading" class="loading loading-dots loading-md"></span>
        </button>
      </div>
    </div>
  </dialog>

</template>
