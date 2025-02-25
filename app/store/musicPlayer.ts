import { type Station } from "@/services/models/station";
import { type Album, type Track } from "@/services/models/album";

export interface TrackList {
  album: Album;
  station: Station;
  track: Track;
}

export const useMusicPlayerStore = defineStore("use-music-player-store", () => {

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useMusicPlayerStore, import.meta.hot));
}
