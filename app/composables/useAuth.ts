import { useAuthStore } from "@/store/auth";
import { useUserStore } from "@/store/user";
import type { ApiData } from "@/composables/useApi";

export const useAuth = async (): Promise<any> => {
  const authStore = useAuthStore();
  const userStore = useUserStore();

  const requestLoginNonce = async (pubkey: string) => {
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

  const login = () => { }

  const logout = () => { }

  return {
    requestLoginNonce,
    login,
    logout
  }
}
