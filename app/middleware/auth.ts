import { useAuthStore } from "@/store/auth";
import { useStationStore } from "@/store/station";

export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();
  const stationStore = useStationStore();

  if (!authStore.isAuthenticated) {
    return navigateTo({ name: 'index' });
  }

  if ((to.name == 'station-edit' && !stationStore.has_station)
    || (to.name == 'station-create' && stationStore.has_station)) {
    return navigateTo({ name: 'index' });
  }
})
