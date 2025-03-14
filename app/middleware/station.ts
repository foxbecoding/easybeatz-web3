import { hasStationChecker } from "@/services/models/station";

export default defineNuxtRouteMiddleware(async (to, from) => {
  let hasStation = false;
  try {
    const { message, data } = await hasStationChecker();
    hasStation = data;
  } catch (e) {
    return navigateTo({ name: "index" });
  }
  if ((to.name == 'station-edit' && !hasStation)
    || (to.name == 'station-create' && hasStation)) {
    return navigateTo({ name: 'index' });
  }
})
