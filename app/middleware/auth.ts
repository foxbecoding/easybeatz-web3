import { useUserStore } from "@/store/user";
import { useAuthStore } from "@/store/auth";

export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();
  const userStore = useUserStore();

  if (!authStore.isAuthenticated) {
    return navigateTo({ name: 'index' });
  }

  if (to.name == 'station-id-edit' && (userStore.pubkey != to.params.id)) {
    return navigateTo({ name: 'index' });
  }
})
