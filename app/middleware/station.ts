import { hasStationChecker } from "@/services/models/station";

export default defineNuxtRouteMiddleware(async (to, from) => {
  let hasStation = false;
  try {
    hasStation = await hasStationChecker();
  } catch (e) {
    console.error(e);
    return navigateTo({ name: "index" });
  }
  if ((to.name == 'station-edit' && !hasStation)
    || (to.name == 'station-create' && hasStation)) {
    return navigateTo({ name: 'index' });
  }
})
