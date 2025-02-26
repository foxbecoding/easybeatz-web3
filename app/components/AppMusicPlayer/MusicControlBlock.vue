<script setup lang="ts">
import { type TrackList, useMusicPlayerStore } from "@/store/musicPlayer";
import { type Album, type Track } from "@/services/models/album";
import { type Station } from "@/services/models/station";

const config = useRuntimeConfig();
const musicPlayerStore = useMusicPlayerStore();
const currentTime = computed(() => musicPlayerStore.currentTime);
const currentTimeStr = computed(() => musicPlayerStore.currentTimeStr);
const trackList = computed<TrackList>(() => musicPlayerStore.selectedTrackListItem as TrackList);
const track = computed<Track>(() => trackList.value.track);

const playOrPauseIcon = computed(() => musicPlayerStore.isPlaying ? 'pause' : 'play');
const playOrPause = computed(() => musicPlayerStore.isPlaying ? pauseHandler() : playHandler());

const playHandler = () => musicPlayerStore.playTrackHandler;
const pauseHandler = () => musicPlayerStore.pauseTrackHandler;
const nextHandler = () => musicPlayerStore.nextTrackHandler();
const prevHandler = () => musicPlayerStore.prevTrackHandler();

const onSliderChange = (e: any) => {
  if (musicPlayerStore.audio) {
    musicPlayerStore.audio.currentTime = Number(e.target.value)
  }
}

</script>

