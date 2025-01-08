export const useUserStore = defineStore("user-store", () => {
  const accessKey = ref(null)
  const pubkey = ref(null)

  const isAuthenticated = computed(() => accessKey.value != null)

  return {
    accessKey,
    isAuthenticated,
    pubkey
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useUserStore, import.meta.hot));
}
