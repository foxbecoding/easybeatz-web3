export const useUserStore = defineStore("use-user-store", () => {
  const pubkey = ref<string | null>(null);
  const favoriteTracks = ref<String[]>([]);

  const setUserData = (_pubkey: string | null, _favoriteTracks: string[]): void => {
    pubkey.value = _pubkey;
    favoriteTracks.value = _favoriteTracks;
  }

  const clearUserData = () => {
    pubkey.value = null;
    favoriteTracks.value = [];
  }

  return {
    pubkey,
    setUserData,
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useUserStore, import.meta.hot));
} 
