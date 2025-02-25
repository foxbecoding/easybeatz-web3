import { type Station } from "@/services/models/station";
import { type Album, type Track } from "@/services/models/album";

export interface TrackList {
  album: Album;
  station: Station;
  track: Track;
}

export const useMusicPlayerStore = defineStore("use-music-player-store", () => {
  const config = useRuntimeConfig();
  const audio = ref<HTMLAudioElement | null>(null);
  const selectedTrackIndex = ref<number | null>(null);
  const trackList = ref<TrackList[]>([]);
  const playingFrom = ref("");

  const selectedTrackListItem = computed<TrackList | null>(() =>
    selectedTrackIndex.value !== null ? trackList.value[selectedTrackIndex.value] ?? null : null
  );

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useMusicPlayerStore, import.meta.hot));
}
