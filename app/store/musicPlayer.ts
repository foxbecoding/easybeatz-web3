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

  const setMusicPlayerDetails = (_selectedTrackIndex: number, _trackList: TrackList[], _playingFrom: string) => {
    const isSameTrack = selectedTrackIndex.value === _selectedTrackIndex && playingFrom.value === _playingFrom;

    if (isSameTrack) {
      restartTrack();
    } else {
      if (playingFrom.value !== _playingFrom) {
        trackList.value = _trackList;
      }
      selectedTrackIndex.value = _selectedTrackIndex;
      playingFrom.value = _playingFrom;
    }
  };

  const setMediaSource = () => {
    if (selectedTrackListItem.value) {
      pauseTrackHandler();
      audioLoader();
      audio.value = new Audio(`${config.public.MEDIA_URL}${selectedTrackListItem.value.track.display}`);
      audioLoader();
    }
  };

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useMusicPlayerStore, import.meta.hot));
}
