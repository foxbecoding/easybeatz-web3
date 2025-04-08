import { useUserStore } from "@/store/user";
import { submitTrackFavorite, removeTrackFavorite } from "@/services/models/album";

export const useFavoriteTrack = (tid: string) => {
  const userStore = useUserStore();
  const isFavoriteTrack = computed(() => userStore.favoriteTracks.includes(tid))
  const favoriteIcon = computed(() => !isFavoriteTrack.value ? 'linear' : 'bold')
  const favoriteIconColor = computed(() => !isFavoriteTrack.value ? '' : 'text-error')

  const favoriteTrackHandler = async () => {
    if (!isFavoriteTrack.value) {
      await addFavoriteTrack();
      return;
    }

    await removeFavoriteTrack();

  }

  const addFavoriteTrack = async () => {
    try {
      const res = await submitTrackFavorite(tid);
      userStore.favoriteTracks.push(res.data);
      useToast().setToast(res.message, "SUCCESS");
    } catch (error: any) {
      if (error.status === 401) {
        useToast().setToast("Please login", "INFO");
        return;
      }
      useToast().setToast(error.data.message, "ERROR");
    }
  }

  const removeFavoriteTrack = async () => {
    try {
      const res = await removeTrackFavorite(tid);
      userStore.favoriteTracks = userStore.favoriteTracks.filter(x => x !== res.data);
      useToast().setToast(res.message, "SUCCESS");
    } catch (error: any) {
      if (error.status === 401) {
        useToast().setToast("Please login", "INFO");
        return;
      }
      useToast().setToast(error.data.message, "ERROR");
    }
  }

  return {
    isFavoriteTrack,
    favoriteIcon,
    favoriteIconColor,
    favoriteTrackHandler
  }

}
