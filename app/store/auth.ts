export const useAuthStore = defineStore("use-auth-store", () => {
  const accessToken = ref<string | null>(null);
  const isAuthenticated = ref<boolean>(false);

  return {
    accessToken,
    isAuthenticated,
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot));
} 
