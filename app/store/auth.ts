export const useAuthStore = defineStore("use-auth-store", () => {
  const accessToken = ref<string | null>(null);
  const isAuthenticated = ref<boolean>(false);

  const setAuthData = (token: string | null, authStatus: boolean): void => {
    isAuthenticated.value = authStatus;
    accessToken.value = token;
  }

  const clearAuthData = (): void => {
    isAuthenticated.value = false;
    accessToken.value = null;
  }

  return {
    accessToken,
    isAuthenticated,
    setAuthData,
    clearAuthData
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot));
}
