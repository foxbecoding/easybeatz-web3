<script setup lang="ts">
import { type Album, type Track } from "@/services/models/album";
import { type Station } from "@/services/models/station";

const props = defineProps<{
  track: Track;
  station: Station;
  album: Album;
}>();

const { isFavoriteTrack, favoriteIcon, favoriteIconColor, favoriteTrackHandler } = useFavoriteTrack(props.track.tid);

</script>

<template>
  <div class="flex">
    <div class="tooltip" :data-tip="!isFavoriteTrack ? 'add favorite' : 'remove favorite'">
      <button @click.stop="favoriteTrackHandler()" class="btn btn-square btn-ghost mask mask-squircle">
        <Icon :icon="`solar:heart-${favoriteIcon}`" :class="favoriteIconColor" width="24" height="24" />
      </button>
    </div>
    <div class="tooltip" data-tip="more">
      <button class="btn btn-square btn-ghost mask mask-squircle">
        <Icon icon="solar:menu-dots-bold" width="24" height="24" />
      </button>
    </div>
  </div>
</template>
