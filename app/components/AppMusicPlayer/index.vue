<script setup lang="ts">
import { type TrackList, useMusicPlayerStore } from "@/store/musicPlayer";
import { type Album, type Track } from "@/services/models/album";
import { type Station } from "@/services/models/station";

const config = useRuntimeConfig();
const img = useImage();
const musicPlayerStore = useMusicPlayerStore();
const show = computed(() => musicPlayerStore.show);
const trackList = computed<TrackList>(() => musicPlayerStore.selectedTrackListItem as TrackList);
const album = computed<Album>(() => trackList.value.album as Album);
const albumCover = computed(() => `${config.public.MEDIA_URL}${album.value.cover}`);
const track = computed<Track>(() => trackList.value.track);
const station = computed<Station>(() => trackList.value.station);

const albumCoverStyles = computed(() => {
  const imgUrl = img(albumCover.value, { width: 108 })
  return { backgroundImage: `url('${imgUrl}')`, backgroundSize: 'cover', backgroundPosition: 'center' }
})

</script>

