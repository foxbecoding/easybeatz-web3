export const useStationStore = defineStore("use-station-store", () => {
  const station = ref<string>();

  const setStationData = (_station: string): void => {
    station.value = _station;
  }

  return {
    station,
    setStationData,
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useStationStore, import.meta.hot));
} 
