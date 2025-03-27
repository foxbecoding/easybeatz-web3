<script lang="ts" setup>
import { useAuthStore } from "@/store/auth";
import { type TrackList, useMusicPlayerStore } from "@/store/musicPlayer";
import { type Album, type Track } from "@/services/models/album";
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";
import AlbumFormModal from "@/pages/project/components/AlbumFormModal.vue";
import TrackFormModal from "@/pages/project/components/TrackFormModal.vue";
import _ from 'lodash';

const route = useRoute();
const authStore = useAuthStore();
const config = useRuntimeConfig();
const musicPlayerStore = useMusicPlayerStore();
const aid = ref(route.params.aid)
const isAuthenticated = computed(() => authStore.isAuthenticated)
const fetchPath = `${config.public.API_ALBUM}/${aid.value}/retrieve_with_tracks_and_relations/`;
const demoTracks = Array.from({ length: 6 }, (_, i) => i);

// Album request logic
const { data: cachedAlbum } = useNuxtData<Album>(`project-${aid.value}`);
const { data: fetchedAlbum, error, status, refresh } = await useLazyFetch(fetchPath, {
  server: false,
  key: `project-${aid.value}`,
  watch: [isAuthenticated],
  onRequest({ request, options }) {
    if (authStore.accessToken) {
      options.headers.set('Authorization', `Bearer ${authStore.accessToken}`)
    }
  },
  onResponseError({ request, response, options }) {
    return navigateTo({ name: 'index' })
    //isOwner.value = response._data.is_owner;
  }
});

const album = computed<Album>(() => fetchedAlbum.value.data as Album || cachedAlbum.value as Album)
const albumTracks = computed(() => album.value?.tracks || [])
const albumCover = computed(() => `${config.public.MEDIA_URL}` + album.value?.cover);

const img = useImage()
const albumCoverStyles = computed(() => {
  const imgUrl = img(albumCover.value, { width: 100 })
  return { backgroundImage: `url('${imgUrl}')`, backgroundSize: 'cover', backgroundPosition: 'center' }
})

// Genres request logic
const { data: cachedGenres } = useNuxtData<Album>(`project-aid-genres`);
const fetchGenrePath = `${config.public.API_GENRE}/`;
const { data: fetchedGenres, status: genre_status } = await useLazyFetch(fetchGenrePath, {
  server: false,
  key: `project-aid-genres`,
});
const genres = computed<Genre[]>(() => fetchedGenres.value.data as Genre[]);

// Moods request logic
const fetchMoodPath = `${config.public.API_MOOD}/`;
const { data: cachedMoods } = useNuxtData<Album>(`project-aid-moods`);
const { data: fetchedMoods, status: mood_status } = await useLazyFetch(fetchMoodPath, {
  server: false,
  key: `project-aid-moods`,
});
const moods = computed<Mood[]>(() => fetchedMoods.value.data as Mood[]);

// Music player logic
const playHandler = () => {
  if (album.value) {
    const trackList = trackListBuilder();
    musicPlayerStore.isShuffled = false;
    setMusicPlayerDetails(trackList);
  }
}

const shuffleHandler = () => {
  if (album.value) {
    const trackList = trackListBuilder();
    const newTrackList = _.shuffle(trackList);
    musicPlayerStore.ogTrackList = trackList;
    musicPlayerStore.isShuffled = true;
    setMusicPlayerDetails(newTrackList);
  }
}

const setMusicPlayerDetails = (trackList: TrackList[]) => {
  const trackListItem: TrackList = trackList[0];
  musicPlayerStore.setMusicPlayerDetails(trackListItem, trackList, String(route.path));
}

const trackListBuilder = (): TrackList[] => {
  let trackList: TrackList[] = [];

  if (album.value) {
    const { tracks, station } = album.value
    tracks.forEach(track => {
      trackList.push({ album: album.value as Album, station: station, track })
    });
  }

  return trackList
}

// Edit mode
const isEditMode = ref(false);
const editModeLabel = computed(() => {
  const label = 'Edit mode: ';
  let state = isEditMode.value ? 'On' : 'Off';
  return label + state;
});

//Album form modal logic
const showAlbumFormModal = ref(false);
const openAlbumFormModal = () => showAlbumFormModal.value = true;

// Track form modal logic
const selectedEditTrack = ref<Track | null>();
const showTrackForm = ref(false);
const editDetailsHandler = (track: Track) => {
  selectedEditTrackSetter(track);
  setTimeout(() => {
    showTrackForm.value = true;
  }, 200);
}

const editPriceHandler = (e: any) => { console.log(e) }
const editExclusivePriceHandler = (e: any) => { console.log(e) }
const selectedEditTrackSetter = (track: Track) => {
  selectedEditTrack.value = null;
  setTimeout(() => {
    selectedEditTrack.value = track;
  }, 100);
};

</script>

<template>
  <AppPageContainer>
    <div v-if="(status == 'success' && album) || cachedAlbum" class="flex flex-col gap-8">
      <div class="flex flex-col md:flex-row gap-4 items-center md:items-start">
        <div :style="albumCoverStyles" class="min-w-[300px] h-[300px] group relative bg-neutral rounded-[1rem]"></div>
        <div
          class="flex flex-col gap-4 items-center md:items-start md:justify-between md:h-[300px] w-full max-w-[600px]">
          <div class="items-center md:items-start w-full flex flex-col gap-2">
            <p class="text-2xl md:text-3xl font-bold">{{ album.title }}</p>
            <AppStationBlock class="md:w-fit flex gap-2 items-center justify-center md:justify-start"
              :station="album.station" />
            <p class="opacity-70">{{ album.uploaded_at }}</p>
            <button v-if="isEditMode" @click="openAlbumFormModal()" class="btn btn-secondary rounded-[1rem] text-lg">
              Edit details
            </button>
          </div>
          <div class="flex gap-2 items-center w-full">
            <button @click="playHandler()" class="btn btn-primary flex-1 rounded-[1rem] text-lg">
              <Icon class="text-lg lg:text-xl" icon="solar:play-line-duotone" />
              Play
            </button>
            <button @click="shuffleHandler()" class="btn btn-primary flex-1 rounded-[1rem] text-lg">
              <Icon class="text-lg lg:text-xl" icon="solar:shuffle-outline" />
              Shuffle
            </button>
          </div>
        </div>
      </div>
      <div v-if="album.is_owner" class="flex gap-2">
        <input v-model="isEditMode" type="checkbox" :checked="false" class="toggle toggle-primary" />
        <span>{{ editModeLabel }}</span>
      </div>
      <AppTrackList v-model:edit="isEditMode" :tracks="albumTracks" :station="album.station" :album="album"
        @edit-details="editDetailsHandler" @edit-price="editPriceHandler"
        @edit-exclusive-price="editExclusivePriceHandler" />
    </div>

    <div v-if="(status == 'idle' || status == 'pending') && !cachedAlbum" class="flex flex-col gap-8">
      <div class="flex flex-col md:flex-row gap-4 items-center md:items-start">
        <div class="skeleton min-w-[300px] h-[300px] rounded-[1rem]"></div>
        <div
          class="flex flex-col gap-4 items-center md:items-start md:justify-between md:h-[300px] w-full max-w-[600px]">
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
            <div class="skeleton flex-1 rounded-[1rem] h-[48px]"></div>
            <div class="skeleton flex-1 rounded-[1rem] h-[48px]"></div>
          </div>

        </div>
      </div>

      <div class="flex flex-col gap-4 w-full">
        <div v-for="demo in demoTracks" class="skeleton h-[128px]"></div>
      </div>
    </div>
    <AlbumFormModal v-if="(status == 'success' && album) || cachedAlbum" v-model="showAlbumFormModal"
      :title="album.title" :bio="album.bio" @submit="refresh()" />
    <TrackFormModal v-if="selectedEditTrack && (genre_status === 'success' && mood_status === 'success')"
      v-model="showTrackForm" :track="selectedEditTrack" :genres="genres" :moods="moods" @submitDetails="refresh()" />
  </AppPageContainer>
</template>
