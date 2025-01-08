export const useUserStore = defineStore("use-user-store", () => {
  const accessKey = ref<string | null>(null);
  const pubkey = ref<string | null>(null);
  const isAuthenticated = ref<boolean>(false);

  return {
    accessKey,
    isAuthenticated,
    pubkey
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useUserStore, import.meta.hot));
} 
