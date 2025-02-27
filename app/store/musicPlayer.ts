import { type Station } from "@/services/models/station";
import { type Album, type Track } from "@/services/models/album";
import _ from "lodash";

export interface TrackList {
  album: Album;
  station: Station;
  track: Track;
}

export const useMusicPlayerStore = defineStore("use-music-player-store", () => {
  const config = useRuntimeConfig();
  const audio = ref<HTMLAudioElement | null>(null);
  const currentTime = ref(0);
  const trackList = ref<TrackList[]>([]);
  const selectedTrackListItem = ref<TrackList>();
  const ogTrackList = ref<TrackList[]>([]);
  const playingFrom = ref("");
  const isPlaying = ref(false);
  const isShuffled = ref(false);
  const show = ref(false);

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

  const currentTrackIndex = computed<number>(() => {
    if (!selectedTrackListItem.value) {
      return 0;
    }

    const index = trackList.value.findIndex(x => x == selectedTrackListItem.value);
    return index;

  });

  const setMusicPlayerDetails = (_selectedTrackListItem: TrackList, _trackList: TrackList[], _playingFrom: string) => {
    const isSameTrack = selectedTrackListItem.value === _selectedTrackListItem;

    trackList.value = _trackList;
    playingFrom.value = _playingFrom;

    if (isSameTrack) {
      resetCurrentTime();
    } else {
      setTimeout(() => {
        selectedTrackListItem.value = _selectedTrackListItem;
      }, 30);

      setTimeout(() => {
        show.value = true;
      }, 100)
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
  }

  const audioEndedHandler = () => nextTrackHandler();

  const audioPlayHandler = () => {
    isPlaying.value = true;
  }

  const audioPauseHandler = () => {
    isPlaying.value = false;
  }

  const audioTimeUpdateHandler = () => {
    currentTime.value = audio.value?.currentTime || 0;
  };

  const removeAudioEventListners = () => {
    audio.value?.removeEventListener('ended', audioEndedHandler);
    audio.value?.removeEventListener('timeupdate', audioTimeUpdateHandler);
  };

  const resetAudio = () => {
    pauseTrackHandler();
    resetCurrentTime();
    audioLoader();
    removeAudioEventListners();
  };

  const audioLoader = () => audio.value?.load();

  const resetCurrentTime = () => {
    if (audio.value) {
      audio.value.currentTime = 0;
    }
  };

  const playTrackHandler = () => audio.value?.play();

  const pauseTrackHandler = () => audio.value?.pause();

  const nextTrackHandler = () => {
    const trackIndex = currentTrackIndex.value;
    if (trackIndex < trackList.value.length - 1) {
      const index = trackIndex + 1;
      selectedTrackListItem.value = trackList.value[index];
    }
  };

  const prevTrackHandler = () => {
    if (audio.value) {
      if (audio.value.currentTime > 5) {
        resetCurrentTime();
        return;
      }
    }

    const trackIndex = currentTrackIndex.value;
    if (trackIndex > 0) {
      const index = trackIndex - 1;
      selectedTrackListItem.value = trackList.value[index];
    }
  };

  const shuffleHandler = () => {
    if (!isShuffled.value) {
      const newTrackList: TrackList[] = _.shuffle(trackList.value);

      if (selectedTrackListItem.value) {
        const foundIndex = newTrackList.findIndex(x => x == selectedTrackListItem.value);

        if (foundIndex) {
          newTrackList.splice(foundIndex, 1)
          newTrackList.unshift(selectedTrackListItem.value);
        }
      }

      ogTrackList.value = trackList.value;
      trackList.value = newTrackList;

      isShuffled.value = true;
      return
    }

    isShuffled.value = false;
  };

  const setMediaAndPlay = () => {
    setMediaSource();
    setMediaSessionData();
    playTrackHandler();
  }

  watch(selectedTrackListItem, (newItem) => {
    if (newItem) {
      setMediaAndPlay();
    }
  });

  watch(isShuffled, (newVal) => {
    if (!newVal) {
      trackList.value = ogTrackList.value;
    }
  });

  return {
    audio,
    currentTime,
    currentTimeStr,
    isPlaying,
    isShuffled,
    nextTrackHandler,
    ogTrackList,
    pauseTrackHandler,
    playTrackHandler,
    prevTrackHandler,
    selectedTrackListItem,
    setMusicPlayerDetails,
    show,
    shuffleHandler,
  };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useMusicPlayerStore, import.meta.hot));
}
