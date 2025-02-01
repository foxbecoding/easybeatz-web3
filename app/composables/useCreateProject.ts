interface AlbumForm {
  title: string;
  cover: File | null;
  bio: string;
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

  return {
    albumForm,
    isStep1,
    isStep2,
    isStep3,
    isStep1Completed,
    isStep2Active,
  }

}
