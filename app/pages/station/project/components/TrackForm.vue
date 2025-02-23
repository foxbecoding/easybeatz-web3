<script setup lang="ts">
import { useCreateProjectStore } from "@/store/createProject";
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";

const props = defineProps<{
  genres: Genre[] | null;
  moods: Mood[] | null;
}>();

const projectStore = useCreateProjectStore();
const toast = useToast();
const showToast = ref(false);
const trackForm = ref();
const isTrackFormValid = computed(() => projectStore.isTrackFormValid);
const tracks = computed(() => projectStore.tracks);
const isEditMode = ref(false);
const editTrackIndex = ref(0);
const ExclusivesAndStemsMessage = "If you enter an exclusive price you must include stem files.";

const submitHandlerLabel = computed(() => !isEditMode.value ? 'Add' : 'Edit')


const numbersOnlyInput = (key: string, event: any) => {
  const invalidChars = ['+', '-'];

  if (invalidChars.includes(event.key)) {
    event.preventDefault(); // Block '+' and '-' from being entered
    return;
  }

  let value = event.target.value;

  // Remove non-digit characters (just in case)
  value = value.replace(/\D/g, '');

  // Remove leading zeros
  value = value.replace(/^0+/, '');

  // Update the corresponding item in the array
  projectStore.trackForm[key] = value;
};

const setDialogHandler = (type: 'add' | 'edit') => {
  if (type == 'add') {
    if (isEditMode.value) {
      projectStore.clearTrackForm();
    }
    isEditMode.value = false;
  } else {
    isEditMode.value = true;
  }
  document.getElementById('track_form_modal')?.showModal()
}

const addTrackHandler = () => {
  projectStore.addTrack();
  resetFormHandler();
  toastHandler();
}

const editTrackHandler = () => projectStore.editTrack(editTrackIndex.value);

const openEditTrackHandler = (index: number) => {
  projectStore.setEditTrackFields(index);
  editTrackIndex.value = index;
  setDialogHandler('edit');
}

const submitTrackHandler = () => {
  if (!isTrackFormValid.value) return;
  if (isEditMode.value) {
    editTrackHandler();
    document.getElementById('track_form_modal')?.close();
    toast.setToast('Track edited', 'INFO')
    return;
  }
  addTrackHandler();
}

const removingTrack = reactive({
  title: '',
  index: 0,
})

const setRemoveTrackModal = (title: string, index: number) => {
  removingTrack.title = title;
  removingTrack.index = index;
  document.getElementById('remove_track_modal')?.showModal();
}

const removeTrackHandler = () => {
  projectStore.removeTrack(removingTrack.index);
  document.getElementById('remove_track_modal')?.close();
}

const addCollabHandler = () => projectStore.addCollab();

const removeCollabHandler = (index: number) => projectStore.removeCollab(index);

const addStemHandler = () => projectStore.addStem();

const removeStemHandler = (index: number) => projectStore.removeStem(index);

const resetFormHandler = () => trackForm.value.reset();

const toastHandler = () => {
  showToast.value = true;
  setTimeout(() => {
    showToast.value = false;
  }, 3000)
}

const onMediaChange = (e: any) => {
  const file: File = e.target.files[0];
  const fileType = e.target.files[0].type;
  if (fileType == 'audio/mpeg') {
    projectStore.setMp3File(file);
  } else if (fileType == 'audio/wav') {
    projectStore.setWavFile(file);
  }
}

const onStemChange = (index: number, e: any) => {
  const file: File = e.target.files[0];
  projectStore.setStemFile(index, file);
}

const img = useImage()
const coverImgStyles = computed(() => {
  const imgUrl = img(projectStore.coverPreviewUrl, { width: 100 })
  return { backgroundImage: `url('${imgUrl}')`, backgroundSize: 'cover', backgroundPosition: 'center' }
})

</script>

<template>
  <div class="flex flex-col gap-4">
    <h2 class="text-2xl font-semibold">Add project tracks</h2>
    <button @click="setDialogHandler('add')" class="btn btn-secondary text-lg rounded-[1rem] w-48">
      <Icon icon="material-symbols:music-note-add-rounded" class="text-xl" />
      Add new track
    </button>

    <div class="flex flex-col gap-4 w-full">
      <div v-for="(track, t) in tracks" :key="t"
        class="flex justify-between p-2 rounded-[1rem] bg-neutral cursor-pointer opacity-100 active:opacity-60">
        <div class="flex gap-4 items-center">
          <div class="w-[48px] h-[48px] bg-base-100 rounded-[0.5rem]" :style="coverImgStyles">
          </div>
          <span>{{ track.title }}</span>
        </div>
        <div class="flex gap-4 items-center">
          <span>${{ track.price }}</span>
          <div class="tooltip" data-tip="Edit track">
            <Icon @click.stop="openEditTrackHandler(t)" icon="solar:pen-bold"
              class="cursor-pointer opacity-100 hover:opacity-80 active:opacity-60 text-warning" width="24"
              height="24" />
          </div>
          <div class="tooltip" data-tip="Remove track">
            <Icon @click.stop="setRemoveTrackModal(track.title, t)" icon="solar:trash-bin-minimalistic-bold"
              class="cursor-pointer opacity-100 hover:opacity-80 active:opacity-60 text-error" width="24" height="24" />
          </div>
        </div>
      </div>
    </div>
  </div>

  <dialog id="track_form_modal" class="modal modal-bottom sm:modal-middle">
    <div class="modal-box">
      <h2 class="text-2xl font-bold">{{ !isEditMode ? 'Add' : 'Edit' }} track</h2>
      <form id="track-form" ref="trackForm">
        <section class="flex flex-col gap-2 mt-4">
          <h3 class="text-xl font-bold">Details</h3>
          <label class="form-control w-full">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-semibold">Title</span>
              <span class="label-text">Choose a title for your track.</span>
            </div>
            <input v-model="projectStore.trackForm.title" id="title" name="title" type="text"
              placeholder="Enter track title" class="input input-ghost bg-neutral w-full" />
          </label>

          <label class="form-control w-full">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-semibold">Price</span>
            </div>
            <label class="input input-ghost bg-neutral flex items-center">
              <Icon icon="material-symbols:attach-money-rounded" width="24" height="24" />
              <input v-model="projectStore.trackForm.price" @input="numbersOnlyInput('price', $event)"
                @keydown="numbersOnlyInput('price', $event)" id="price" name="price" type="number"
                placeholder="Enter track price" class="grow w-full" />
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
              <input v-model="projectStore.trackForm.exclusive_price"
                @input="numbersOnlyInput('exclusive_price', $event)"
                @keydown="numbersOnlyInput('exclusive_price', $event)" id="exclusive_price" name="exclusive_price"
                type="number" placeholder="Enter track exclusive price" class="grow w-full" />
            </label>
          </label>

          <label class="form-control w-full">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-semibold">BPM</span>
            </div>
            <input v-model="projectStore.trackForm.bpm" @input="numbersOnlyInput('bpm', $event)"
              @keydown="numbersOnlyInput('bpm', $event)" id="bpm" name="bpm" type="number" placeholder="Enter track bpm"
              class="input input-ghost bg-neutral w-full" />
          </label>
        </section>

        <div class="divider" />

        <section class="flex flex-col gap-2 mt-4">
          <h3 class="text-xl font-bold">Genres and Moods</h3>
          <label class="form-control w-full">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-semibold">Genres</span>
            </div>
            <select v-model="projectStore.selectedGenre" class="select select-ghost bg-neutral w-full" id="genres"
              name="genres">
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
            <select v-model="projectStore.trackForm.mood" id="moods" name="moods"
              class="select select-ghost bg-neutral w-full">
              <option disabled selected>Select a mood</option>
              <option v-for="(mood, m) in moods" :key="m" :value="mood.pk" selected>
                {{ mood.name }}
              </option>
            </select>
          </label>
        </section>

        <div class="divider" />

        <section class="flex flex-col gap-2 mt-4">
          <h3 class="text-xl font-bold">MP3 and WAV</h3>
          <label class="form-control w-full">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-bold">MP3</span>
            </div>
            <input @change="onMediaChange" type="file" class="file-input file-input-bordered w-full" accept=".mp3"
              id="mp3" name="mp3" />
          </label>

          <label class="form-control w-full">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-bold">WAV(optional)</span>
            </div>
            <input @change="onMediaChange" type="file" class="file-input file-input-bordered w-full" accept=".wav"
              id="wav" name="wav" />
          </label>
        </section>

        <div class="divider" />

        <section class="flex flex-col gap-4 mt-4">
          <div class="flex flex-col gap-1">
            <h3 class="text-xl font-bold">Collaborators</h3>
            <p class="text-md">
              *Split profits evenly amongst you and collaborators by adding thier Solana wallet address.
            </p>
          </div>
          <div v-if="projectStore.trackForm.collaborators.length > 0" class="flex flex-col gap-2">
            <div v-for="(collab, c) in projectStore.trackForm.collaborators" :key="c">
              <label class="form-control w-full">
                <div class="label flex flex-col items-start">
                  <span class="label-text text-lg font-bold">Collab {{ c + 1 }}</span>
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

        <div class="divider" />

        <section class="flex flex-col gap-4 mt-4">
          <div class="flex flex-col">
            <h3 v-if="projectStore.trackForm.has_exclusive" class="text-xl font-bold">Exclusive details</h3>
            <div class="form-control">
              <label class="label cursor-pointer justify-start gap-4">
                <span class="label-text text-lg">Add an exclusive price?</span>
                <input v-model="projectStore.trackForm.has_exclusive" type="checkbox" class="checkbox" />
              </label>
            </div>
          </div>

          <label v-if="projectStore.trackForm.has_exclusive" class="form-control w-full">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-bold">Exclusive price</span>
            </div>
            <label class="input input-ghost bg-neutral flex items-center">
              <Icon icon="material-symbols:attach-money-rounded" class="text-warning" width="24" height="24" />
              <input v-model="projectStore.trackForm.exclusive_price"
                @input="numbersOnlyInput('exclusive_price', $event)"
                @keydown="numbersOnlyInput('exclusive_price', $event)" id="exclusive_price" name="exclusive_price"
                type="number" placeholder="Enter track exclusive price" class="grow w-full" />
            </label>
          </label>

          <div v-if="projectStore.trackForm.has_exclusive" class="flex flex-col gap-3">
            <div class="label flex flex-col items-start">
              <h3 class="label-text text-xl font-bold">Stems</h3>
              <p>Upload the stems wav files.</p>
            </div>
            <div v-for="(stem, s) in projectStore.trackForm.stems" :key="s" class="flex flex-col gap-2">
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

          <a v-if="projectStore.trackForm.has_exclusive" @click="addStemHandler()"
            class="btn btn-secondary rounded-[1rem] w-40">
            <Icon icon="solar:add-square-bold" width="24" height="24" />
            Add stem
          </a>
        </section>
      </form>

      <div v-show="showToast" class="toast sticky">
        <div class="alert alert-info flex">
          <span class="mx-auto">Track added</span>
        </div>
      </div>

      <div class="modal-action">
        <form id="dialog-form" method="dialog" class="flex justify-end gap-2">
          <button class="btn btn-neutral">Close</button>
          <button @click="submitTrackHandler()" class="btn btn-primary" :disabled="!isTrackFormValid">
            {{ submitHandlerLabel }}
            track
          </button>
        </form>
      </div>
    </div>
  </dialog>

  <dialog id="remove_track_modal" class="modal modal-bottom sm:modal-middle">
    <div class="modal-box">
      <h3 class="text-xl font-bold">Removing track "{{ removingTrack.title }}"?</h3>
      <div class="modal-action">
        <form method="dialog" class="flex justify-end gap-2">
          <button class="btn btn-neutral">Close</button>
          <button @click="removeTrackHandler()" class="btn btn-error">Remove</button>
        </form>
      </div>
    </div>
  </dialog>
</template>
