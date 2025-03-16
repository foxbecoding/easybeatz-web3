import { jwtDecode } from 'jwt-decode';
import { useAuthStore } from "@/store/auth";
import { useUserStore } from "@/store/user";
import type { ApiData } from "@/composables/useApi";

export const useAuth = () => {
  const config = useRuntimeConfig();
  const authStore = useAuthStore();
  const userStore = useUserStore();

  const requestLoginNonce = async (pubkey: string): Promise<string> => {
    const apiData: ApiData = {
      method: 'POST',
      path: `${config.public.API_WEB3_LOGIN_NONCE}/`,
      data: {
        pubkey
      }
    }

    const res = await useApi(apiData)

    if (res.error) {
      throw new Error(`requestLoginNonce() - Response status: ${res.error}`);
    }

    return res;
  }

  const login = async (signature: any, message: string, pubkey: string): Promise<void> => {
    const apiData: ApiData = {
      method: 'POST',
      path: `${config.public.API_WEB3_LOGIN}/`,
      data: {
        signedMessage: signature,
        originalMessage: message,
        pubkey
      }
    }

    try {
      const res = await useApi(apiData);
      _setDataAfterLogin(res);
    } catch (error: any) {
      const { message, data } = error.data;
      if (message) {
        useToast().setToast(message, "ERROR");
      }
    }
  }

  const _setDataAfterLogin = (res: any) => {
    const { message, data } = res;
    if (message) {
      useToast().setToast(message, "INFO")
    }
    userStore.setUserData(data.pubkey, data.favorite_tracks);
    authStore.setAuthData(data.access_token, true);
    setTokenTimer(data.access_token);
  }

  const logout = async () => {
    const apiData: ApiData = { method: 'POST', path: `${config.public.API_LOGOUT}/` };

    try {
      const { message, data } = await useApi(apiData);
      authStore.clearAuthData();
      userStore.clearUserData();
      useRouter().push({ name: "index" });
      if (message) {
        useToast().setToast(message, "INFO");
      }
    } catch (error: any) {
      useToast().setToast("Internal error, please try again.", "ERROR");
    }
  }

  const setTokenTimer = (token: string) => {
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

  return {
    requestLoginNonce,
    login,
    logout
  }
}
