export const useToastStore = defineStore("use-toast-store", () => {
  const show = ref<boolean>(false);
  const text = ref<string>("");

  const setShow = (_show: boolean) => {
    show.value = _show;
  }

  const setText = (_text: string) => {
    text.value = _text;
  }

  return {
    show,
    text,
    setShow,
    setText
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useToastStore, import.meta.hot));
}
