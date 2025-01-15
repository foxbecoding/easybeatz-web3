export const useStationStore = defineStore("use-station-store", () => {
  const has_station = ref<boolean>(false);

  const setHasStation = (_has_station: boolean): void => {
    has_station.value = _has_station;
  }

  return {
    setHasStation,
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useStationStore, import.meta.hot));
} 
