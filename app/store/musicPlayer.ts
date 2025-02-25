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

  const setMediaSessionData = () => {
    if ('mediaSession' in navigator && selectedTrackListItem.value) {
      const { track, album, station } = selectedTrackListItem.value;
      console.log(album)
      navigator.mediaSession.metadata = new MediaMetadata({
        title: track.title,
        artist: station.name,
        album: album.title,
        artwork: [{ src: `${config.public.MEDIA_URL}${album.cover}` }]
      });

      navigator.mediaSession.setActionHandler('play', playTrackHandler);
      navigator.mediaSession.setActionHandler('pause', pauseTrackHandler);
      navigator.mediaSession.setActionHandler('previoustrack', prevTrackHandler);
      navigator.mediaSession.setActionHandler('nexttrack', nextTrackHandler);
    }
  };

  const audioLoader = () => audio.value?.load();

  const restartTrack = () => {
    if (audio.value) {
      audio.value.currentTime = 0;
    }
  };

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useMusicPlayerStore, import.meta.hot));
}
