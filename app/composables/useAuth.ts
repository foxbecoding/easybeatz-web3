import { jwtDecode } from 'jwt-decode';
import { useAuthStore } from "@/store/auth";
import { useUserStore } from "@/store/user";
import { useStationStore } from "@/store/station";
import type { ApiData } from "@/composables/useApi";

export const useAuth = () => {
  const authStore = useAuthStore();
  const userStore = useUserStore();
  const stationStore = useStationStore();

  const requestLoginNonce = async (pubkey: string): Promise<string> => {
    const apiData: ApiData = {
      method: 'POST',
      path: '/api/web3-login-nonce/',
      data: {
        pubkey
      }
    }

    const res = await useApi(apiData)

    if (res.error) {
      throw new Error(`requestLoginNonce() - Response status: ${res.error}`);
    }

    return res.nonce;
  }

  const login = async (signature: any, message: string, pubkey: string): Promise<void> => {
    const apiData: ApiData = {
      method: 'POST',
      path: '/api/web3-login/',
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

    userStore.setUserData(res.pubkey);
    authStore.setAuthData(res.access_token, true);
    stationStore.setStationData(res.station);
    setTokenTimer(res.access_token);
  }

  const logout = () => {
    authStore.setAuthData(null, false);
    userStore.setUserData(null);
    stationStore.setStationData("");
    useRouter().push({ name: "index" });
    // TODO send api request to logout user

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
