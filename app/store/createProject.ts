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

export const useCreateProjectStore = defineStore("use-create-project-store", () => {
  const albumForm = reactive<AlbumForm | any>({
    title: '',
    cover: null,
    bio: ''
  });

  const isStep1Completed = computed(() => albumForm.title && albumForm.cover ? true : false);
  const activeSteps = ref<string[]>(['step1'])
  const step = ref('step1')


  const validateAlbumForm = async () => {
    const formData = new FormData;
    formData.append('album[title]', albumForm.title)
    formData.append('album[cover]', albumForm.cover)
    formData.append('album[bio]', albumForm.bio)
    const res = await albumFormValidator(formData)
    if (res.errors) {
      console.error(res.errors)
      return
    }
    activeSteps.value.push('step2')
    step.value = ('step2')
  }

  return {
    albumForm,
    activeSteps,
    isStep1Completed,
    step,
    validateAlbumForm,
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useCreateProjectStore, import.meta.hot));
}
