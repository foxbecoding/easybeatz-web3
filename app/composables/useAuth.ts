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

    const res = await useApi(apiData);

    if (res.error) {
      throw new Error(`authenticateNonce() - Response status: ${res.error}`);
    }

    userStore.setUserData(res.pubkey, res.favorite_tracks);
    authStore.setAuthData(res.access_token, true);
    setTokenTimer(res.access_token);
  }

  const logout = async () => {
    //backend logout
    const apiData: ApiData = { method: 'POST', path: `${config.public.API_LOGOUT}/` };
    await useApi(apiData);
    authStore.clearAuthData();
    userStore.clearUserData();
    useRouter().push({ name: "index" });

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
