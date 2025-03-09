<script setup lang="ts">
import { submitTrackFavorite, removeTrackFavorite } from "@/services/models/album";
import { useUserStore } from "@/store/user";
import { useAuthStore } from "@/store/auth";
import { type Album, type Track } from "@/services/models/album";
import { type Station } from "@/services/models/station";

const props = defineProps<{
  track: Track;
  station: Station;
  album: Album;
}>();

const authStore = useAuthStore();
const userStore = useUserStore();

const isFavoriteTrack = computed(() => userStore.favoriteTracks.includes(props.track.tid))

const favoriteIcon = computed(() => !isFavoriteTrack.value ? 'linear' : 'bold')
const favoriteIconColor = computed(() => !isFavoriteTrack.value ? '' : 'text-error')

const favoriteTrackHandler = async (tid: string) => {
  if (!authStore.isAuthenticated) return;

  if (!isFavoriteTrack.value) {
    await addFavoriteTrack(tid);
    return;
  }

  await removeFavoriteTrack(tid);

}
<template>
  <div class="flex">
    <button class="btn btn-square btn-ghost mask mask-squircle">
      <Icon icon="solar:heart-linear" width="24" height="24" />
    </button>
    <button class="btn btn-square btn-ghost mask mask-squircle">
      <Icon icon="solar:menu-dots-bold" width="24" height="24" />
    </button>
  </div>
</template>
