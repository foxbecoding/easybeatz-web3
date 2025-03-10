<script setup lang="ts">
import { submitTrackFavorite, removeTrackFavorite } from "@/services/models/album";
import { useUserStore } from "@/store/user";
import { type Album, type Track } from "@/services/models/album";
import { type Station } from "@/services/models/station";

const props = defineProps<{
  track: Track;
  station: Station;
  album: Album;
}>();

const userStore = useUserStore();
const toast = useToast();

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

const addFavoriteTrack = async (tid: string) => {
  try {
    const res = await submitTrackFavorite(tid);
    userStore.favoriteTracks.push(res)
  } catch (error: any) {
    // Handle Error
  }
}

const removeFavoriteTrack = async (tid: string) => {
  try {
    const res = await removeTrackFavorite(tid);
    userStore.favoriteTracks = userStore.favoriteTracks.filter(x => x !== res);
  } catch (error: any) {
    // Handle Error
  }
}


</script>

<template>
  <div class="flex">
    <button @click.stop="favoriteTrackHandler(track.tid)" class="btn btn-square btn-ghost mask mask-squircle">
      <Icon :icon="`solar:heart-${favoriteIcon}`" :class="favoriteIconColor" width="24" height="24" />
    </button>
    <button class="btn btn-square btn-ghost mask mask-squircle">
      <Icon icon="solar:menu-dots-bold" width="24" height="24" />
    </button>
  </div>
</template>
