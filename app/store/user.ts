export const useUserStore = defineStore("use-user-store", () => {
  const pubkey = ref<string | null>(null);

  return {
    pubkey
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useUserStore, import.meta.hot));
} 
