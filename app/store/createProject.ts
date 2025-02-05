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
  stems: TrackStemForm[] | [];
  title: string;
  wav?: File | null;
}

export const useCreateProjectStore = defineStore("use-create-project-store", () => {
  const coverPreviewUrl = ref<string | null>(null);
  const albumForm = reactive<AlbumForm | any>({
    title: '',
    cover: null,
    bio: ''
  });

  const trackForm: TrackForm = {
    bpm: '',
    collaborators: [],
    exclusive_price: '',
    genres: [],
    has_exclusive: false,
    mood: '',
    mp3: null,
    price: '',
    stems: [],
    title: '',
    wav: null
  };

  const trackFormFields = ref<TrackForm[]>([{
    bpm: '',
    collaborators: [],
    exclusive_price: '',
    genres: [],
    has_exclusive: false,
    mood: '',
    mp3: null,
    price: '',
    stems: [],
    title: '',
    wav: null
  }]);


  const validateAlbumForm = async () => {
    const formData = new FormData;
    formData.append('album[title]', albumForm.title)
    formData.append('album[cover]', albumForm.cover)
    formData.append('album[bio]', albumForm.bio)
    const res = await albumFormValidator(formData)
    if (res.errors) {
      console.error(res.errors)
      return false;
    }
    return true;
  }

  const addTrack = () => {
    trackFormFields.value.push({
      bpm: '',
      collaborators: [],
      exclusive_price: '',
      genres: [],
      has_exclusive: false,
      mood: '',
      mp3: null,
      price: '',
      stems: [],
      title: '',
      wav: null
    });
  }

  return {
    addTrack,
    albumForm,
    coverPreviewUrl,
    trackForm,
    trackFormFields,
    validateAlbumForm,
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useCreateProjectStore, import.meta.hot));
}
