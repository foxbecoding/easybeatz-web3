export const useStationStore = defineStore("use-station-store", () => {
  const hasStation = ref<boolean>(false);

  const setStationData = (_hasStation: boolean): void => {
    hasStation.value = _hasStation;
  }

  return {
    hasStation,
    setStationData,
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useStationStore, import.meta.hot));
} 
