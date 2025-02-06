<script setup lang="ts">
import { useCreateProjectStore } from "@/store/createProject";
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";


const props = defineProps<{
  genres: Genre[] | null;
  moods: Mood[] | null;
}>();

const projectStore = useCreateProjectStore();

const numbersOnlyInput = (event: any) => {
  let value = event.target.value;

  // Remove non-digit characters
  value = value.replace(/\D/g, '');

  // Remove leading zeros
  value = value.replace(/^0+/, '');

  // Update the corresponding item in the array
  projectStore.trackForm['price'] = value;
};

const addTrack = () => {
  projectStore.addTrack()
}
</script>

<template>
  <h1 class="text-2xl font-bold">Add project tracks</h1>
  {{ projectStore.trackForm }}
  <div class="my-4">
    <button onclick="add_track_modal.showModal()" class="btn btn-secondary text-lg">
      <Icon icon="material-symbols:music-note-add-rounded" class="text-xl" />
      Add new track
    </button>
  </div>

  <dialog id="add_track_modal" class="modal modal-bottom sm:modal-middle">
    <div class="modal-box lg:translate-x-[150px]">
      <h2 class="text-2xl font-bold">Add track</h2>
      <form>
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
            <input v-model="projectStore.trackForm.price" @input="numbersOnlyInput" id="price" name="price"
              type="number" placeholder="Enter track price" class="input input-ghost bg-neutral w-full" />
          </label>

          <label class="form-control w-full">
            <div class="label flex flex-col items-start">
              <span class="label-text text-lg font-bold">BPM</span>
            </div>
            <input v-model="projectStore.trackForm.bpm" @input="numbersOnlyInput" id="bpm" name="bpm" type="number"
              placeholder="Enter track bpm" class="input input-ghost bg-neutral w-full" />
          </label>
        </section>

        <div class="divider" />

        <section class="flex flex-col gap-2 mt-4">
          <h3 class="text-xl font-bold">Genres and Mood</h3>
        </section>

        <div class="divider" />

        <section class="flex flex-col gap-2 mt-4">
          <h3 class="text-xl font-bold">MP3 and WAV</h3>
        </section>

        <div class="divider" />

        <section class="flex flex-col gap-2 mt-4">
          <h3 class="text-xl font-bold">Collaborators</h3>
        </section>

        <div class="divider" />

        <section class="flex flex-col gap-2 mt-4">
          <div class="flex flex-col">
            <h3 v-if="projectStore.trackForm.has_exclusive" class="text-xl font-bold">Exclusive details</h3>
            <div class="form-control">
              <label class="label cursor-pointer justify-start gap-4">
                <span class="label-text text-lg">Sell as exclusive?</span>
                <input v-model="projectStore.trackForm.has_exclusive" type="checkbox" class="checkbox" />
              </label>
            </div>
          </div>
        </section>
      </form>
      <div class="modal-action">
        <form id="form" method="dialog">
          <button class="btn">Close</button>
        </form>
      </div>
    </div>
  </dialog>
</template>
