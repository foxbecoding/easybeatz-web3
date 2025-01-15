export const useStationStore = defineStore("use-station-store", () => {
  const has_station = ref<boolean>(false);

  const setHasStation = (status: boolean): void => {
    has_station.value = status;
  }

  return {
    setHasStation,
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useStationStore, import.meta.hot));
} 
