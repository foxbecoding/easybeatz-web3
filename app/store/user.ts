export const useUserStore = defineStore("use-user-store", () => {
  const pubkey = ref<string | null>(null);
  const username = ref<string | null>(null);

  const setUserData = (_pubkey: string, _username: string): void => {
    pubkey.value = _pubkey;
    username.value = _username;
  }

  return {
    pubkey,
    setUserData,
    username,
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useUserStore, import.meta.hot));
} 
