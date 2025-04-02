<script setup lang="ts">
import { type Genre } from "@/services/models/genre";
import { type Mood } from "@/services/models/mood";

//component types and interfaces
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
  mood: string;
  mp3: File | null;
  price: string;
  stems: TrackStemForm[];
  title: string;
  wav?: File | null;
}

// Component props
const props = defineProps<{
  genres: Genre[];
  moods: Mood[];
  formTitle: string;
}>();

// Emiiters
const emit = defineEmits(['submit'])

// Modal control logic
const model = defineModel({ default: false, required: true });
const closeModal = () => model.value = false;
watch(model, (newVal) => {
  if (newVal) {
    document.getElementById('app_track_form_modal')?.showModal();
  } else {
    document.getElementById('app_track_form_modal')?.close();
  }
});

// Track form logic
const trackForm = reactive<TrackForm>({
  bpm: '',
  collaborators: [],
  exclusive_price: '',
  genres: [],
  mood: '',
  mp3: null,
  price: '',
  stems: [],
  title: '',
  wav: null
});

const clearTrackForm = () => {
  trackForm.bpm = '';
  trackForm.collaborators = [];
  trackForm.exclusive_price = '';
  trackForm.genres = [];
  trackForm.mood = '';
  trackForm.mp3 = null;
  trackForm.price = '';
  trackForm.stems = [];
  trackForm.title = '';
  trackForm.wav = null;
  resetSelectedGenre();
}

const isTrackFormValid = computed(() => {
  let validationFields = ['bpm', 'genres', 'mood', 'mp3', 'price', 'title'];

  if (trackForm.stems.length > 0 || trackForm.exclusive_price) {
    validationFields.push('stems')
  }

  if (trackForm.exclusive_price) {
    validationFields.push('exclusive_price')
  }

  const validatedFields = validationFields.map((field: keyof typeof trackForm) => {
    if (field == 'genres') {
      return trackForm[field].length > 0 ? true : false;
    }

    if (field == 'exclusive_price') {
      return trackForm['stems'].length > 0 ? true : false;
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

// Genres logic
const selectedGenre = ref('');
const resetSelectedGenre = () => selectedGenre.value = '';
const setGenresField = (genre_pk: string) => {
  trackForm.genres = [];
  trackForm.genres.push(genre_pk);
}
watch(selectedGenre, (newSelected) => {
  if (!newSelected) return false;
  setGenresField(String(newSelected));
});

// MP3 & WAV Media file logic
const onMediaChange = (e: any) => {
  const file: File = e.target.files[0];
  const fileType = e.target.files[0].type;
  if (fileType == 'audio/mpeg') {
    setMp3File(file);
  } else if (fileType == 'audio/wav') {
    setWavFile(file);
  }
}
const setMp3File = (file: File) => trackForm.mp3 = file;
const setWavFile = (file: File) => trackForm.wav = file;

// Colaborators logic
const addCollabHandler = () => trackForm.collaborators.push({ pubkey: '' });
const removeCollabHandler = (index: number) => trackForm.collaborators.splice(index, 1);

// Stems logic
const ExclusivesAndStemsMessage = "If you enter an exclusive price you must include stem files.";
const addStemHandler = () => trackForm.stems.push({ name: '', file: null });
const removeStemHandler = (index: number) => trackForm.stems.splice(index, 1);
const setStemFile = (index: number, file: File) => trackForm.stems[index].file = file;
const onStemChange = (index: number, e: any) => {
  const file: File = e.target.files[0];
  setStemFile(index, file);
}

</script>

<template>
</template>
