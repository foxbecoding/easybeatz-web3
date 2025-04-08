<script setup lang="ts">
import { type Track } from "@/services/models/album";
import { useAuthStore } from "@/store/auth";
import type { NuxtLink } from "~/components";

const route = useRoute();
const config = useRuntimeConfig();
const authStore = useAuthStore();
const isAuthenticated = computed(() => authStore.isAuthenticated)
const img = useImage();

// Track request logic
const tid = ref(route.params.tid)
const fetchPath = `${config.public.API_TRACK}/${route.params.tid}/track_page/`;

const { data: cachedTrack } = useNuxtData<{ message: string; data: any }>(`track-${tid.value}`);
const { data: fetchedTrack, error, status, refresh } = await useLazyFetch<{ message: string; data: any }>(fetchPath, {
  server: false,
  key: `track-${tid.value}`,
  watch: [isAuthenticated],
  onRequest({ request, options }) {
    if (authStore.accessToken) {
      options.headers.set('Authorization', `Bearer ${authStore.accessToken}`)
    }
  },
  onResponseError({ request, response, options }) {
    console.log(response);
  }
});

const track = computed<Track>(() => fetchedTrack.value?.data as Track || cachedTrack.value?.data as Track);

// Album cover logic
const albumCover = computed(() => {
  const { album } = track.value;
  if (!album) return "";
  return `${config.public.MEDIA_URL}` + album.cover
});

const albumCoverStyles = computed(() => {
  const imgUrl = img(albumCover.value, { width: 100 })
  return { backgroundImage: `url('${imgUrl}')`, backgroundSize: 'cover', backgroundPosition: 'center' }
});

// Track play audio logic
const playHandler = () => { }

// Track details logic
interface TrackDetail {
  label: string;
  content: string;
  icon: string;
  to?: string;
}

const trackDetailItems = computed<TrackDetail[]>(() => [
  { label: "Duration", content: track.value.formatted_duration, icon: "solar:clock-circle-bold" },
  { label: "BPM", content: track.value.bpm, icon: "solar:playback-speed-bold" },
  { label: "Uploaded", content: track.value.uploaded_at, icon: "solar:upload-track-2-bold" },
  { label: "Genre", content: track.value.genres.name, icon: "solar:music-notes-bold" },
  { label: "Mood", content: track.value.mood.name, icon: "solar:music-notes-bold" },
  {
    label: "Project",
    content: track.value.album?.title,
    icon: "solar:music-library-2-bold",
    to: {
      name: "project-aid", params: { aid: track.value.album?.aid }
    }
  },
] as TrackDetail[]);
// Favorite track logic
const { isFavoriteTrack, favoriteIcon, favoriteIconColor, favoriteTrackHandler } = useFavoriteTrack(tid.value.toString());
</script>

<template>
  <AppPageContainer>
    <div v-if="(status == 'success' && track) || cachedTrack" class="flex flex-col gap-8 w-full max-w-[1000px]">
      <div class="flex flex-col md:flex-row gap-4 items-center md:items-start">
        <div :style="albumCoverStyles"
          class="w-full md:w-auto md:min-w-[300px] md:h-[300px] group relative aspect-square bg-neutral rounded-[1rem]">
        </div>
        <div class="flex flex-col gap-4 items-center md:items-start md:justify-between md:h-[300px] w-full">
          <div class="md:items-start w-full flex flex-col gap-2">
            <p class="text-lg md:text-xl lg:text-2xl font-bold">{{ track.title }}</p>
            <AppStationBlock v-if="track.station" class="md:w-fit flex gap-2 justify-start" :station="track.station" />
          </div>
          <div class="flex gap-2 items-center w-full">
            <button @click="playHandler()" class="btn btn-primary flex-1 rounded-[1rem] text-lg">
              <Icon class="text-lg lg:text-xl" icon="solar:play-line-duotone" />
              Play
            </button>
            <button class="btn btn-ghost btn-square btn-active mask mask-squircle rounded-[1rem] text-lg">
              <Icon class="text-lg lg:text-xl" icon="solar:heart-outline" />
            </button>
            <button class="btn btn-ghost btn-active btn-square mask mask-squircle rounded-[1rem] text-lg">
              <Icon class="text-lg lg:text-xl" icon="solar:square-share-line-bold" />
            </button>
          </div>
        </div>
      </div>
      <div tabindex="0" class="collapse collapse-arrow bg-base-200 w-full">
        <input type="checkbox" />
        <div class="collapse-title text-xl opacity-60 font-medium">Track details</div>
        <div class="collapse-content">
          <div class="stats shadow w-full">
            <div class="stat">
              <div class="stat-figure text-secondary">
                <Icon class="text-lg lg:text-xl" icon="solar:play-bold" />
              </div>
              <div class="stat-title">Plays</div>
              <div class="stat-value">10,000</div>
            </div>

            <div class="stat">
              <div class="stat-figure text-secondary">
                <Icon class="text-lg lg:text-xl text-error" icon="solar:heart-bold" />
              </div>
              <div class="stat-title">Favorite</div>
              <div class="stat-value">180</div>
            </div>
          </div>
          <ul class="py-4">
            <div v-for="(item, i) in trackDetailItems" :key="i">
              <li class="font-semibold flex items-center gap-2 md:text-lg">
                <Icon :icon="item.icon" />
                <p>
                  {{ item.label }}:
                  <NuxtLink v-if="item.to" :to="item.to" class="hover:opacity-60 text-primary">{{ item.content }}
                  </NuxtLink>
                  <span v-else>{{ item.content }}</span>
                </p>
              </li>
              <li v-if="trackDetailItems.length !== i + 1" class="divider my-2"></li>
            </div>
          </ul>
        </div>
      </div>
    </div>
    <div v-if="(status == 'idle' || status == 'pending') && !cachedTrack"
      class="flex flex-col gap-8 w-full max-w-[1000px]">
      <div class="flex flex-col md:flex-row gap-4 items-center md:items-start">
        <div class="skeleton min-w-[300px] h-[300px] rounded-[1rem]"></div>
        <div class="flex flex-col gap-4 items-center md:items-start md:justify-between md:h-[300px] w-full">
          <div class="items-center md:items-start w-full flex flex-col gap-2">
            <div class="skeleton h-[36px] w-full max-w-[300px]"></div>
            <div class="flex gap-2">
              <div class="skeleton h-[44px] w-[44px] mask mask-squircle"></div>
              <div class="flex flex-col h-[44px] w-[120px] gap-2">
                <div class="skeleton h-[16px] w-full"></div>
                <div class="skeleton h-[16px] w-full"></div>
              </div>
            </div>
            <div class="skeleton h-[20px] w-[120px]"></div>
          </div>

          <div class="flex gap-2 items-center w-full">
            <div class="skeleton flex-1 rounded-[1rem] h-12"></div>
            <div class="skeleton  rounded-[1rem] w-12 h-12 mask mask-squircle"></div>
          </div>

        </div>
      </div>
    </div>
  </AppPageContainer>
</template>
