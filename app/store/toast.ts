export const useToastStore = defineStore("use-toast-store", () => {
  const show = ref<boolean>(false);
  const text = ref<string>("");
  const alertClass = ref<string>("")

  const setToast = (_show: boolean, _text: string, _alertClass: string) => {
    show.value = _show;
    text.value = _text;
    alertClass.value = _alertClass;
  }

  const clearToast = () => {
    show.value = false;
    text.value = "";
    alertClass.value = "";
  }

  return {
    show,
    text,
    alertClass,
    setToast,
    clearToast
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useToastStore, import.meta.hot));
}
