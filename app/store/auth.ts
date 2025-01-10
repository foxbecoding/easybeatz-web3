import { jwtDecode } from 'jwt-decode';
import { useUserStore } from "@/store/user";

export const useAuthStore = defineStore("use-auth-store", () => {
  const accessToken = ref<string | null>(null);
  const isAuthenticated = ref<boolean>(false);

  const setAuthData = (token: string, authStatus: boolean): void => {
    isAuthenticated.value = authStatus;
    setAccessToken(token);
  }

  const setAccessToken = (token: string) => {
    accessToken.value = token;

    // Decode the token
    const decoded = jwtDecode(token);
    const expiryTime = decoded.exp * 1000; // Convert to milliseconds

    // Set up a timer to handle token expiration
    const currentTime = Date.now();
    const timeUntilExpiry = expiryTime - currentTime;

    if (timeUntilExpiry > 0) {
      setTimeout(() => {
        logout(); // Or refresh the token
      }, timeUntilExpiry);
    } else {
      logout();
    }
  }

  const logout = () => {
    accessToken.value = null;
    isAuthenticated.value = false;
    useUserStore().setUserData(null, null);
    useRouter().push({ name: "index" })
  }

  return {
    accessToken,
    isAuthenticated,
    setAuthData
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot));
} 
