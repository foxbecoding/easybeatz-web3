<script setup lang="ts">
import { useCreateProjectStore } from "@/store/createProject";

const createProjectStore = useCreateProjectStore();

const sanitizeInput = (index: any, event: any) => {
  let value = event.target.value;

  // Remove non-digit characters
  value = value.replace(/\D/g, '');

  // Remove leading zeros
  value = value.replace(/^0+/, '');

  // Update the corresponding item in the array
  createProjectStore.trackFormFields[index]['price'] = value;
};

const addTrack = () => {
  createProjectStore.addTrack()
}

</script>

<template>
  <h1 class="text-2xl font-bold">Add project tracks</h1>

  <div class="my-4">
    <button onclick="add_track_modal.showModal()" class="btn btn-secondary text-md">
      <Icon icon="material-symbols:music-note-add-rounded" class="text-xl" />
      Add new track
    </button>
  </div>

  <dialog id="add_track_modal" class="modal modal-bottom sm:modal-middle">
    <div class="modal-box">
      <h3 class="text-lg font-bold">Add track</h3>
      <form>
        <div v-for="(track, t) in createProjectStore.trackFormFields" :key="t">
          <p class="text-xl font-bold">Track {{ t + 1 }}</p>
          <div class="mb-4">
            <label class="form-control w-full">
              <div class="label flex flex-col items-start">
                <span class="label-text text-lg font-bold">Title</span>
                <span class="label-text">Choose a title for your track.</span>
              </div>
              <input v-model="track.title" id="title" name="title" type="text" placeholder="Enter track title"
                class="input input-ghost bg-neutral w-full" />
            </label>
          </div>
          <div class="mb-4">
            <label class="form-control w-full">
              <div class="label flex flex-col items-start">
                <span class="label-text text-lg font-bold">Price</span>
              </div>
              <input v-model="track.price" @input="sanitizeInput(t, $event)" id="price" name="price" type="number"
                placeholder="Enter track price" class="input input-ghost bg-neutral w-full" />
            </label>
          </div>
        </div>
      </form>
      <div class="modal-action">
        <form id="form" method="dialog">
          <button class="btn">Close</button>
        </form>
      </div>
    </div>
  </dialog>
</template>
