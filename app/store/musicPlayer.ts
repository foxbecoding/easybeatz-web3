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
  const currentTime = ref(0);
  const selectedTrackIndex = ref<number | null>(null);
  const trackList = ref<TrackList[]>([]);
  const playingFrom = ref("");
  const isPlaying = ref(false);
  const show = ref(false);

  const selectedTrackListItem = computed<TrackList | null>(() =>
    selectedTrackIndex.value !== null ? trackList.value[selectedTrackIndex.value] ?? null : null
  );

  const currentTimeStr = computed<string>((): string => {
    let hrs: number = ~~(currentTime.value / 3600)
    let mins: number = ~~((currentTime.value % 3600) / 60)
    let secs: number = ~~currentTime.value % 60
    let ret: string = ""

    hrs > 0 ? ret += "" + hrs + ":" + (mins < 10 ? "0" : "") : ''

    ret += "" + mins + ":" + (secs < 10 ? "0" : "")
    ret += "" + secs
    return ret
  });

  const setMusicPlayerDetails = (_selectedTrackIndex: number, _trackList: TrackList[], _playingFrom: string) => {
    const isSameTrack = selectedTrackIndex.value === _selectedTrackIndex && playingFrom.value === _playingFrom;

    if (isSameTrack) {
      resetCurrentTime();
    } else {
      if (playingFrom.value !== _playingFrom) {
        selectedTrackIndex.value = null;
        trackList.value = _trackList;
      }

      setTimeout(() => {
        selectedTrackIndex.value = _selectedTrackIndex;
      }, 30);

      playingFrom.value = _playingFrom;
    }
  };

  const setMediaSessionData = () => {
    if ('mediaSession' in navigator && selectedTrackListItem.value) {
      const { track, album, station } = selectedTrackListItem.value;
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

  const setMediaSource = () => {
    resetAudio();
    if (selectedTrackListItem.value) {
      const newAudio = new Audio(`${config.public.MEDIA_URL}${selectedTrackListItem.value.track.display}`);
      setAudioEventListeners(newAudio);
      audio.value = newAudio;
      audioLoader();
    }
  };

  const setAudioEventListeners = (_audio: HTMLAudioElement) => {
    _audio.addEventListener('ended', audioEndedHandler);
    _audio.addEventListener('timeupdate', audioTimeUpdateHandler);
    _audio.addEventListener('play', audioPlayHandler);
    _audio.addEventListener('pause', audioPauseHandler);
    _audio.addEventListener("seeking", (event) => { console.log('seeking') });
  }

  const audioEndedHandler = () => nextTrackHandler();

  const audioPlayHandler = () => {
    isPlaying.value = true;
  }

  const audioPauseHandler = () => {
    isPlaying.value = false;
  }

  const audioLoader = () => audio.value?.load();

  const restartTrack = () => {
    if (audio.value) {
      audio.value.currentTime = 0;
    }
  };

  const playTrackHandler = () => {
    audio.value?.play();
  };

  const pauseTrackHandler = () => {
    audio.value?.pause();
  };

  const nextTrackHandler = () => {
    if (selectedTrackIndex.value !== null && selectedTrackIndex.value < trackList.value.length - 1) {
      selectedTrackIndex.value++;
    }
  };

  const prevTrackHandler = () => {
    if (audio.value) {
      if (audio.value.currentTime > 5) {
        restartTrack();
        return;
      }
    }
    if (selectedTrackIndex.value && selectedTrackIndex.value > 0) {
      selectedTrackIndex.value--;
    }
  };

  watch(selectedTrackIndex, (newIndex) => {
    if (newIndex !== null) {
      setMediaSource();
      setMediaSessionData();
      playTrackHandler();
    }
  });

  return {
    pauseTrackHandler,
    playTrackHandler,
    prevTrackHandler,
    nextTrackHandler,
    setMusicPlayerDetails,
  };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useMusicPlayerStore, import.meta.hot));
}
