<script setup lang="ts">
import { type Track } from "@/services/models/album";
import { TrackPriceEnum } from "@/services/enums/track-price-enums";
import { useAuthStore } from "@/store/auth";
import { type TrackList, useMusicPlayerStore } from "@/store/musicPlayer";
import { type CartResponse, type CartItem, addCartItem, removeCartItem } from "@/services/models/cart";
import { useCartStore } from "@/store/cart";

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
    //console.log(response);
  }
});

const track = computed<Track>(() => fetchedTrack.value?.data as Track || cachedTrack.value?.data as Track);
const trackIncludesText = computed(() => `Includes: MP3 ${track.value.has_wav_file ? " + WAV" : ""} ${track.value.stems.length > 0 ? " + STEMS" : ""} `)


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
const musicPlayerStore = useMusicPlayerStore();
const setMusicPlayerDetails = (trackList: TrackList[]) => {
  const trackListItem: TrackList = trackList[0];
  musicPlayerStore.setMusicPlayerDetails(trackListItem, trackList, String(route.path));
}

const playHandler = () => {
  const { album, station } = track.value;
  if (!album || !station) return;
  let trackList: TrackList[] = [{ album: album, station: station, track: track.value }];
  setMusicPlayerDetails(trackList);
}

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

// Cart handler logic
const cartStore = useCartStore();
const isCartActionLoading = reactive<Record<TrackPriceEnum, boolean>>({
  [TrackPriceEnum.TRACK_PRICE]: false,
  [TrackPriceEnum.TRACK_EXCLUSIVE_PRICE]: false
});

const isPriceInCart = computed(() => {
  let found = cartStore.items.find(x => (x.price_type == TrackPriceEnum.TRACK_PRICE) && (x.track.tid === tid.value.toString()))
  return found ? true : false;
})

const isExclusiveInCart = computed(() => {
  let found = cartStore.items.find(x => (x.price_type == TrackPriceEnum.TRACK_EXCLUSIVE_PRICE) && (x.track.tid === tid.value.toString()))
  return found ? true : false;
})

const addCartItemHandler = (tid: string, type: TrackPriceEnum) => cartActionHandler(tid, type, addCartItem);
const removeCartItemHandler = (tid: string, type: TrackPriceEnum) => cartActionHandler(tid, type, removeCartItem);

const cartActionHandler = async (tid: string, type: TrackPriceEnum, actionHandler: Function) => {
  if (isCartActionLoading[type]) return;
  isCartActionLoading[type] = true;

  try {
    const { message, data } = await actionHandler({ tid, type });
    useCart().cartSetter(data as CartResponse);
    if (message) {
      useToast().setToast(message, "INFO");
    }
  } catch (error: any) {
    useToast().setToast(error.data.message, "ERROR");
  } finally {
    setTimeout(() => { isCartActionLoading[type] = false }, 2000);
  }
}
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
            <div class="tooltip" :data-tip="!isFavoriteTrack ? 'add favorite' : 'remove favorite'">
              <button @click.stop="favoriteTrackHandler()"
                class="btn btn-square btn-ghost btn-active mask mask-squircle">
                <Icon :icon="`solar:heart-${favoriteIcon}`" class="text-2xl" :class="favoriteIconColor" />
              </button>
            </div>
            <div class="tooltip" data-tip="share track">
              <button class="btn btn-ghost btn-active btn-square mask mask-squircle">
                <Icon class="text-2xl" icon="solar:square-share-line-bold" />
              </button>
            </div>
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
              <div class="stat-value">{{ track.total_favorite_count }}</div>
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
      <div id="pricing" class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="card bg-gradient-to-b from-[rgba(36,36,36,1)] to-[rgba(18,18,18,1)]">
          <div class="card-body">
            <div class="flex justify-between">
              <h2 class="card-title">Unlimited license</h2>
              <span class="font-bold text-2xl">${{ track.price }}</span>
            </div>
            <h3>{{ trackIncludesText }}</h3>
            <ul class="list-none space-y-2 py-4">
              <li class="flex items-center gap-2">
                <Icon icon="mingcute:check-2-fill" /> First item
              </li>
              <li class="flex items-center gap-2">
                <Icon icon="mingcute:check-2-fill" /> Second item
              </li>
              <li class="flex items-center gap-2">
                <Icon icon="mingcute:check-2-fill" /> Third item
              </li>
            </ul>
            <div class="card-actions">
              <button @click="addCartItemHandler(tid.toString(), TrackPriceEnum.TRACK_PRICE)"
                class="btn btn-primary btn-block rounded-[1rem] text-lg" :disabled="isPriceInCart">
                {{ cartBtnLabelPrice }}
                <span v-if="isAddingCartItem[TrackPriceEnum.TRACK_PRICE]"
                  class="loading loading-dots loading-md"></span>

              </button>
            </div>
          </div>
        </div>
        <div v-if="track.exclusive_price" class="card bg-gradient-to-b from-[rgba(36,36,36,1)] to-[rgba(18,18,18,1)]">
          <div class="card-body">
            <div class="flex justify-between">
              <h2 class="card-title">Exclusive license</h2>
              <span class="font-bold text-2xl text-warning">${{ track.exclusive_price }}</span>
            </div>
            <h3>{{ trackIncludesText }}</h3>
            <ul class="list-none space-y-2 py-4">
              <li class="flex items-center gap-2">
                <Icon icon="mingcute:check-2-fill" /> First item
              </li>
              <li class="flex items-center gap-2">
                <Icon icon="mingcute:check-2-fill" /> Second item
              </li>
              <li class="flex items-center gap-2">
                <Icon icon="mingcute:check-2-fill" /> Third item
              </li>
            </ul>
            <div class="card-actions">
              <button @click="addCartItemHandler(tid.toString(), TrackPriceEnum.TRACK_EXCLUSIVE_PRICE)"
                class="btn btn-warning btn-block rounded-[1rem] text-lg" :disabled="isExclusiveInCart">
                {{ cartBtnLabelExclusive }}
                <span v-if="isAddingCartItem[TrackPriceEnum.TRACK_EXCLUSIVE_PRICE]"
                  class="loading loading-dots loading-md"></span>
              </button>
            </div>
          </div>
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
