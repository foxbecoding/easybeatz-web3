export const useStationStore = defineStore("use-station-store", () => {
  const has_station = ref<boolean>(false);

  const setStationData = (_has_station: boolean): void => {
    has_station.value = _has_station;
  }

  return {
    has_station,
    setStationData,
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useStationStore, import.meta.hot));
} 
