import { useToastStore } from "@/store/toast";

export const useToast = () => {
  const toastStore = useToastStore();

  type NotificationType = "SUCCESS" | "INFO" | "WARNING" | "ERROR";

  const setToast = (text: string, type: NotificationType) => {
    const alertClass = alertClassSelector(type);
    toastStore.setToast(true, text, alertClass);
    setTimeout(() => {
      clearToast();
    }, 6000);
  };

  const clearToast = () => {
    toastStore.clearToast();
  }

  const alertClassSelector = (type: NotificationType): string => {
    let alertClass: string = "";
    switch (type) {
      case "SUCCESS":
        alertClass = `alert-${type.toLowerCase()}`;
        break;
      case "INFO":
        alertClass = `alert-${type.toLowerCase()}`;
        break;
      case "WARNING":
        alertClass = `alert-${type.toLowerCase()}`;
        break;
      case "ERROR":
        alertClass = `alert-${type.toLowerCase()}`;
        break;
      default:
        alertClass = "alert-success";

    }

    return alertClass;
  }

  return {
    clearToast,
    setToast
  }

}
