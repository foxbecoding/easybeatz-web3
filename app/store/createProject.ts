import cloneDeep from 'lodash/cloneDeep';
import { albumFormValidator, submitAlbumProject } from "@/services/models/album";

interface AlbumForm {
  title: string;
  cover: File | null;
  bio: string;
}

interface TrackStemForm {
  name: string;
  file: File | null;
}

interface CollaboratorForm {
  pubkey: string;
}

interface TrackForm {
  bpm: string;
  collaborators: CollaboratorForm[];
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
  const coverPreviewUrl = ref<string>('');
  const selectedGenre = ref('');
  const albumForm = reactive<AlbumForm | any>({
    title: '',
    cover: null,
    bio: ''
  });

  const trackForm = reactive<TrackForm>({
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

  const clearAlbumForm = () => {
    albumForm.title = '';
    albumForm.cover = null;
    albumForm.bio = '';
    coverPreviewUrl.value = '';
  }

  const isTrackFormValid = computed(() => {
    let validationFields = ['bpm', 'genres', 'mood', 'mp3', 'price', 'title'];
    if (trackForm.has_exclusive) {
      validationFields.push('exclusive_price', 'stems')
    }

    const validatedFields = validationFields.map((field: keyof typeof trackForm) => {
      if (field == 'genres') {
        return trackForm[field].length > 0 ? true : false;
      }

      if (field == 'stems') {
        const validStems = trackForm.stems.map(stem => {
          return stem.name && stem.file ? true : false;
        })
        return validStems.every(value => value === true);
      }

      return !!trackForm[field];
    })

    return validatedFields.every(value => value === true);
  });

  const isAlbumFormValid = computed(() => {
    let validationFields = ['title', 'cover'];
    const validatedFields = validationFields.map((field: keyof typeof albumForm) => !!albumForm[field]);
    return validatedFields.every(value => value === true);
  });

  const isProjectValid = computed(() => isAlbumFormValid.value && tracks.value.length > 0 ? true : false);

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

  const tracks = ref<TrackForm[]>([]);

  const addTrack = () => {
    const track = cloneDeep(trackForm);
    tracks.value.push(track);
    clearTrackForm();
  }

  const editTrack = (index: number) => {
    tracks.value[index] = cloneDeep(trackForm);
    clearTrackForm();
  }

  const setEditTrackFields = (index: number) => {
    clearTrackForm();
    const track = tracks.value[index];
    Object.keys(track).forEach(key => {
      if (key == 'genres') {
        selectedGenre.value = track[key][0];
      }
      trackForm[key] = track[key];
    });
  };

  const removeTrack = (index: number) => tracks.value.splice(index, 1);

  const clearTrackForm = () => {
    trackForm.bpm = '';
    trackForm.collaborators = [];
    trackForm.exclusive_price = '';
    trackForm.genres = [];
    trackForm.has_exclusive = false;
    trackForm.mood = '';
    trackForm.mp3 = null;
    trackForm.price = '';
    trackForm.stems = [];
    trackForm.title = '';
    trackForm.wav = null;
    resetSelectedGenre();
  }

  const setGenresField = (genre_pk: string) => {
    trackForm.genres = [];
    trackForm.genres.push(genre_pk);
  }

  const setMp3File = (file: File) => trackForm.mp3 = file;
  const setWavFile = (file: File) => trackForm.wav = file;

  const addCollab = () => trackForm.collaborators.push({ pubkey: '' });

  const removeCollab = (index: number) => trackForm.collaborators.splice(index, 1);

  const addStem = () => trackForm.stems.push({ name: '', file: null });

  const removeStem = (index: number) => trackForm.stems.splice(index, 1);

  const setStemFile = (index: number, file: File) => trackForm.stems[index].file = file;

  const resetSelectedGenre = () => selectedGenre.value = '';

  const submit = () => {
    const formData = new FormData;
    Object.keys(albumForm).forEach(key => {
      formData.append(`album[${key}]`, albumForm[key])
    });
    //formData.append('album[title]', albumForm.title)
    //formData.append('album[cover]', albumForm.cover)
    //formData.append('album[bio]', albumForm.bio)
  }

  watch(selectedGenre, (newSelected) => {
    if (!newSelected) return false;
    setGenresField(String(newSelected));
  });

  watch(() => trackForm.has_exclusive, (newValue) => {
    if (newValue && !trackForm.stems.length) {
      addStem();
    }
  })

  return {
    addCollab,
    addStem,
    addTrack,
    albumForm,
    clearTrackForm,
    coverPreviewUrl,
    editTrack,
    isProjectValid,
    isTrackFormValid,
    removeCollab,
    removeStem,
    removeTrack,
    resetSelectedGenre,
    selectedGenre,
    setEditTrackFields,
    setGenresField,
    setMp3File,
    setStemFile,
    setWavFile,
    submit,
    trackForm,
    tracks,
    validateAlbumForm,
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useCreateProjectStore, import.meta.hot));
}
