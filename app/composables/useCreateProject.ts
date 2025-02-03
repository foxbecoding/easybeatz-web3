import { albumFormValidator } from "@/services/models/album";

interface AlbumForm {
  title: string;
  cover: File | null;
  bio: string;
}

interface TrackStemForm {
  name: string;
  file: File | null;
}

interface TrackForm {
  bpm: string;
  collaborators: string[];
  exclusive_price: string;
  genres: string[];
  has_exclusive: boolean;
  mood: string;
  mp3: File | null;
  price: string;
  stems: TrackStemForm[];
  title: string;
  wav?: File | null;
}

export const useCreateProject = () => {
  const isStep1 = ref(true);
  const isStep2 = ref(false);
  const isStep3 = ref(false);

  const albumForm = reactive<AlbumForm>({
    title: '',
    cover: null,
    bio: ''
  });

  const isStep1Completed = computed(() => albumForm.title && albumForm.cover ? true : false);

  const isStep2Active = computed(() => isStep1.value && isStep2.value && isStep1Completed.value ? true : false);

  const validateAlbumForm = async () => {
    const res = await albumFormValidator(albumForm)
    if ('errors' in res) {
      return
    }
    isStep2.value = true
  }

  return {
    albumForm,
    isStep1,
    isStep2,
    isStep3,
    isStep1Completed,
    isStep2Active,
  }

}
