<script setup lang="ts">
import { useCreateProjectStore } from "@/store/createProject";
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";

const props = defineProps<{
  genres: Genre[] | null;
  moods: Mood[] | null;
}>();

const projectStore = useCreateProjectStore();
const showToast = ref(false);
const trackForm = ref();
const isTrackFormValid = computed(() => projectStore.isTrackFormValid);
const tracks = computed(() => projectStore.tracks);
const showDialog = ref(false);
const isEditMode = ref(false);
const editTrackIndex = ref(0);

const numbersOnlyInput = (key: string, event: any) => {
  let value = event.target.value;

  // Remove non-digit characters
  value = value.replace(/\D/g, '');

  // Remove leading zeros
  value = value.replace(/^0+/, '');

  // Update the corresponding item in the array
  projectStore.trackForm[key] = value;
};

const setDialog = (type: 'add' | 'edit', status: boolean) => {
  if (type == 'add') {
    if (isEditMode.value) {
      projectStore.clearTrackForm();
    }
    isEditMode.value = false;
  } else {
    isEditMode.value = true;
  }
  showDialog.value = status;
}

const addTrack = () => {
  projectStore.addTrack();
  resetForm();
  setShowToast();
}

const editTrack = () => projectStore.editTrack(editTrackIndex.value);

const openEditTrack = (index: number) => {
  projectStore.setEditTrackFields(index);
  editTrackIndex.value = index;
  setDialog('edit', true);
}

const submit = () => {
  if (isEditMode.value) {
    editTrack();
    return;
  }
  addTrack();
}

const removeTrack = (index: number) => projectStore.removeTrack(index);

const addCollab = () => projectStore.addCollab();

const removeCollab = (index: number) => projectStore.removeCollab(index);

const addStem = () => projectStore.addStem();

const removeStem = (index: number) => projectStore.removeStem(index);

const resetForm = () => trackForm.value.reset();

const setShowToast = () => {
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

</script>


<template>
  <div class="flex flex-col gap-4">
    <h1 class="text-2xl font-bold">Add project tracks</h1>
    <button @click="setDialog('add', true)" class="btn btn-secondary text-lg rounded-[1rem] w-48">
      <Icon icon="material-symbols:music-note-add-rounded" class="text-xl" />
      Add new track
    </button>

    <div class="flex flex-col w-full">
      <div v-for="(track, t) in tracks" :key="t"
        class="flex justify-between p-2 rounded-[1rem] bg-neutral cursor-pointer group opacity-100 active:opacity-60">
        <div class="flex gap-4 items-center">
          <div class="w-[48px] h-[48px] bg-base-100 rounded-[0.5rem]">
            <NuxtImg v-if="projectStore.coverPreviewUrl" :src="projectStore.coverPreviewUrl" class="rounded-[0.5rem]"
              alt="project cover" />
          </div>
          <span>{{ track.title }}</span>
        </div>
        <div class="flex gap-4 items-center">
          <span>${{ track.price }}</span>
          <div class="tooltip" data-tip="Edit track">
            <Icon @click.stop="openEditTrack(t)" icon="solar:pen-bold"
              class="cursor-pointer opacity-100 hover:opacity-80 active:opacity-60 text-warning" width="24"
              height="24" />
          </div>
          <div class="tooltip" data-tip="Remove track">
            <Icon @click.stop="removeTrack(t)" icon="solar:trash-bin-minimalistic-bold"
              class="cursor-pointer opacity-100 hover:opacity-80 active:opacity-60 text-error" width="24" height="24" />
          </div>
        </div>
      </div>
    </div>
  </div>

  <dialog id="add_track_modal" class="modal modal-bottom sm:modal-middle" :open="showDialog">
    <div class="modal-box lg:translate-x-[150px]">
      <h2 class="text-2xl font-bold">{{ !isEditMode ? 'Add' : 'Edit' }} track</h2>
      <form id="track-form" ref="trackForm">
        <section class="flex flex-col gap-2 mt-4">
          <h3 class="text-xl font-bold">Details</h3>
          <label class="form-control w-full">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-bold">Title</span>
              <span class="label-text">Choose a title for your track.</span>
            </div>
            <input v-model="projectStore.trackForm.title" id="title" name="title" type="text"
              placeholder="Enter track title" class="input input-ghost bg-neutral w-full" />
          </label>

          <label class="form-control w-full">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-bold">Price</span>
            </div>
            <label class="input input-ghost bg-neutral flex items-center">
              <Icon icon="material-symbols:attach-money-rounded" width="24" height="24" />
              <input v-model="projectStore.trackForm.price" @input="numbersOnlyInput('price', $event)" id="price"
                name="price" type="number" placeholder="Enter track price" class="grow w-full" />
            </label>
          </label>

          <label class="form-control w-full">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-bold">BPM</span>
            </div>
            <input v-model="projectStore.trackForm.bpm" @input="numbersOnlyInput('bpm', $event)" id="bpm" name="bpm"
              type="number" placeholder="Enter track bpm" class="input input-ghost bg-neutral w-full" />
          </label>
        </section>

        <div class="divider" />

        <section class="flex flex-col gap-2 mt-4">
          <h3 class="text-xl font-bold">Genres and Moods</h3>
          <label class="form-control w-full">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-bold">Genres</span>
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
              <span class="label-text text-lg font-bold">Moods</span>
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
                    <Icon @click.stop="removeCollab(c)" icon="solar:trash-bin-minimalistic-bold"
                      class="cursor-pointer opacity-100 hover:opacity-80 active:opacity-60 text-error" width="24"
                      height="24" />
                  </div>
                </label>
              </label>
            </div>
          </div>

          <a @click="addCollab()" class="btn btn-secondary rounded-[1rem] w-40">
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
                @input="numbersOnlyInput('exclusive_price', $event)" id="exclusive_price" name="exclusive_price"
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
                  <Icon @click="removeStem(s)" icon="solar:trash-bin-minimalistic-bold"
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

          <a v-if="projectStore.trackForm.has_exclusive" @click="addStem()"
            class="btn btn-secondary rounded-[1rem] w-40">
            <Icon icon="solar:add-square-bold" width="24" height="24" />
            Add stem
          </a>
        </section>
      </form>

      <div v-show="showToast" class="toast">
        <div class="alert alert-info">
          <span>Track added</span>
        </div>
      </div>

      <div class="modal-action">
        <form id="dialog-form" method="dialog" class="flex justify-end gap-2">
          <button class="btn btn-neutral">Close</button>
          <button @click="isTrackFormValid ? addTrack() : false" class="btn btn-primary"
            :disabled="!isTrackFormValid">Add track</button>
        </form>
      </div>
    </div>
  </dialog>
</template>
