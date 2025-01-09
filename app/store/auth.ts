export const useAuthStore = defineStore("use-auth-store", () => {
  const accessKey = ref<string | null>(null);
  const isAuthenticated = ref<boolean>(false);

  return {
    accessKey,
    isAuthenticated,
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot));
} 
