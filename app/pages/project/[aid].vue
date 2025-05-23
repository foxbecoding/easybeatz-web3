<script lang="ts" setup>
import { useAuthStore } from "@/store/auth";
import { type TrackList, useMusicPlayerStore } from "@/store/musicPlayer";
import { type Album, type Track, updateAlbumCover, addAlbumTrack } from "@/services/models/album";
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";
import AlbumFormModal from "@/pages/project/components/AlbumFormModal.vue";
import TrackDetailsFormModal from "@/pages/project/components/TrackDetailsFormModal.vue";
import TrackPriceFormModal from "@/pages/project/components/TrackPriceFormModal.vue";
import TrackExclusiveFormModal from "@/pages/project/components/TrackExclusiveFormModal.vue";
import _ from 'lodash';

const route = useRoute();
const authStore = useAuthStore();
const config = useRuntimeConfig();
const musicPlayerStore = useMusicPlayerStore();
const img = useImage();
const aid = ref(route.params.aid)
const isAuthenticated = computed(() => authStore.isAuthenticated)
const fetchPath = `${config.public.API_ALBUM}/${aid.value}/retrieve_with_tracks_and_relations/`;
const demoTracks = Array.from({ length: 6 }, (_, i) => i);

// Album request logic
interface AlbumResponse {
  message: string;
  data: Album
}

const { data: cachedAlbum } = useNuxtData<AlbumResponse>(`project-${aid.value}`);
const { data: fetchedAlbum, error, status, refresh } = await useLazyFetch<AlbumResponse>(fetchPath, {
  server: false,
  key: `project-${aid.value}`,
  watch: [isAuthenticated],
  default() {
    return cachedAlbum.value as AlbumResponse;
  },
  onRequest({ request, options }) {
    if (authStore.accessToken) {
      options.headers.set('Authorization', `Bearer ${authStore.accessToken}`)
    }
  },
  onResponseError({ request, response, options }) {
    return navigateTo({ name: 'index' })
  }
});

const album = computed<Album>(() => fetchedAlbum.value?.data as Album)
const albumTracks = computed(() => album.value?.tracks || []);

// Genres request logic
interface GenreResponse {
  message: string;
  data: Genre[];
}

const { data: cachedGenres } = useNuxtData<GenreResponse>(`project-aid-genres`);
const fetchGenrePath = `${config.public.API_GENRE}/`;
const { data: fetchedGenres, status: genre_status } = await useLazyFetch<GenreResponse>(fetchGenrePath, {
  server: false,
  key: `project-aid-genres`,
});
const genres = computed<Genre[]>(() => fetchedGenres.value?.data as Genre[] || cachedGenres.value?.data as Genre[]);

// Moods request logic
interface MoodResponse {
  message: string;
  data: Mood[];
}

const fetchMoodPath = `${config.public.API_MOOD}/`;
const { data: cachedMoods } = useNuxtData<MoodResponse>(`project-aid-moods`);
const { data: fetchedMoods, status: mood_status } = await useLazyFetch<MoodResponse>(fetchMoodPath, {
  server: false,
  key: `project-aid-moods`,
});
const moods = computed<Mood[]>(() => fetchedMoods.value?.data as Mood[] || cachedMoods.value?.data as Mood[]);

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
    const { tracks, station } = album.value;
    tracks?.forEach(track => {
      if (!station) return;
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

// Add Track form modal logic
const addTrackModalRef = ref();
const showAddTrackModal = ref(false);
const openAddTrackFormModal = () => showAddTrackModal.value = true;
const submitTrackHandler = async (e: FormData) => {
  addTrackModalRef.value.isLoading = true;
  try {
    const { message, data } = await addAlbumTrack(aid.value.toString(), e);
    refresh();
    addTrackModalRef.value.closeModal();
    addTrackModalRef.value.clearTrackForm();

    if (message) {
      useToast().setToast(message, "SUCCESS");
    }

  } catch (error: any) {
    const { message, data } = error.data;

    if (message) {
      useToast().setToast(message, "ERROR");
    }

  } finally {
    setTimeout(() => { addTrackModalRef.value.isLoading = false; }, 2000)
  }
}

// Shared Track form modal logic
const selectedEditTrack = ref<Track | null>();
const selectedEditTrackSetter = (track: Track) => {
  selectedEditTrack.value = null;
  setTimeout(() => {
    selectedEditTrack.value = track;
  }, 100);
};


// Track form modal logic
const showTrackForm = ref(false);
const editDetailsHandler = (track: Track) => {
  selectedEditTrackSetter(track);
  setTimeout(() => {
    showTrackForm.value = true;
  }, 200);
}

// Track Price form modal logic
const showTrackPriceForm = ref(false);
const editPriceHandler = (track: Track) => {
  selectedEditTrackSetter(track);
  setTimeout(() => {
    showTrackPriceForm.value = true;
  }, 200);
}

// Track Exclusive Price form modal logic
const showTrackExclusiveForm = ref(false);
const editExclusiveHandler = (track: Track) => {
  selectedEditTrackSetter(track);
  setTimeout(() => {
    showTrackExclusiveForm.value = true;
  }, 200);
}


//Album Cover logic
const albumCoverStyles = computed(() => {
  const imgUrl = img(albumCover.value, { width: 100 })
  return { backgroundImage: `url('${imgUrl}')`, backgroundSize: 'cover', backgroundPosition: 'center' }
});
const albumCover = computed(() => `${config.public.MEDIA_URL}` + album.value?.cover);
const onFileChange = (e: any) => {
  const file: File = e.target.files[0];
  if (!file) return;
  //upload picture
  uploadPicture(file);
}

const fileInput = ref();
const triggerFileInput = () => {
  fileInput.value.click();
}
const uploadPicture = async (file: File) => {
  const formData = new FormData;
  formData.append('picture', file);
  try {
    const { message, data } = await updateAlbumCover(aid.value.toString(), formData);
    await refresh()
    useToast().setToast(message, "SUCCESS");
  } catch (error: any) {
    const { message, data } = error.data;
    await refresh()
    useToast().setToast(message, "ERROR");
  }
}

</script>

<template>
  <AppPageContainer>
    <div v-if="status == 'success' || album" class="flex flex-col gap-8">
      <div class="flex flex-col md:flex-row gap-4 items-center md:items-start">
        <div :style="albumCoverStyles"
          class="min-w-[300px] h-[300px] group relative aspect-square bg-neutral rounded-[1rem]">
          <button v-show="isEditMode" @click="triggerFileInput"
            class="btn btn-neutral mask mask-squircle upload-button">
            <Icon icon="solar:camera-add-bold" class="text-xl" />
          </button>
          <input v-if="isEditMode" ref="fileInput" type="file" id="fileInput" accept=".png,.jpg,.jpeg,.avif,.bmp,.webp"
            @change="onFileChange" class="hidden" />
        </div>

        <div
          class="flex flex-col gap-4 items-center md:items-start md:justify-between md:h-[300px] w-full max-w-[600px]">
          <div class="items-center md:items-start w-full flex flex-col gap-2">
            <p class="text-2xl md:text-3xl font-bold">{{ album.title }}</p>
            <AppStationBlock v-if="album.station"
              class="md:w-fit flex gap-2 items-center justify-center md:justify-start" :station="album.station" />
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
      <div v-if="album.is_owner" class="flex items-center justify-between h-[48px]">
        <div class="flex gap-2">
          <input v-model="isEditMode" type="checkbox" :checked="false" class="toggle toggle-primary" />
          <span>{{ editModeLabel }}</span>
        </div>
        <button v-if="isEditMode" @click="openAddTrackFormModal()" class="btn btn-secondary rounded-[1rem] text-lg">
          <Icon class="text-lg lg:text-xl" icon="material-symbols:music-note-add-rounded" />
          Add track
        </button>
      </div>
      <AppTrackList v-if="album.station" v-model:edit="isEditMode" :tracks="albumTracks" :station="album.station"
        :album="album" @edit-details="editDetailsHandler" @edit-price="editPriceHandler"
        @edit-exclusive="editExclusiveHandler" />
    </div>

    <div v-if="(status == 'idle' || status == 'pending') && !album" class="flex flex-col gap-8">
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
    <AppTrackFormModal v-if="genre_status === 'success' && mood_status === 'success'" ref="addTrackModalRef"
      v-model="showAddTrackModal" form-title="Add track" :genres="genres" :moods="moods" @submit="submitTrackHandler" />
    <AlbumFormModal v-if="(status == 'success' && album) || cachedAlbum" v-model="showAlbumFormModal"
      :title="album.title" :bio="album.bio" @submit="refresh()" />
    <TrackDetailsFormModal v-if="selectedEditTrack && (genre_status === 'success' && mood_status === 'success')"
      v-model="showTrackForm" :track="selectedEditTrack" :genres="genres" :moods="moods" @submit-details="refresh()" />
    <TrackPriceFormModal v-if="selectedEditTrack" v-model="showTrackPriceForm" :track="selectedEditTrack"
      @submit-price="refresh()" />
    <TrackExclusiveFormModal v-if="selectedEditTrack" v-model="showTrackExclusiveForm" :track="selectedEditTrack"
      @submit-exclusive="refresh()" />
  </AppPageContainer>
</template>

<style scoped>
.upload-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) !important;
}
</style>
