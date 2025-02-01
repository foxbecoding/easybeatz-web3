interface AlbumForm {
  title: string;
  cover: File | null;
  bio: string;
}

export const useCreateProject = () => {
  const isStep1 = ref(true);
  const isStep2 = ref(false);
  const isStep3 = ref(false);

  const isStep2Active = computed(() => {
    if (isStep1.value && isStep2.value && albumForm.title && albumForm.cover) {
      return true
    }
    return false;
  });

  const albumForm = reactive<AlbumForm>({
    title: '',
    cover: null,
    bio: ''
  });

  return {
    isStep1,
    isStep2,
    isStep3,

  }

}
