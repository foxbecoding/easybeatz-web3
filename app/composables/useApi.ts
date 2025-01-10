import { useAuthStore } from "@/store/auth";

export interface ApiData {
  data?: object
  isMultiPart?: boolean
  method: "GET" | "HEAD" | "PATCH" | "POST" | "PUT" | "DELETE"
  path: string
}

export const useApi = async (apiData: ApiData): Promise<any> => {
  const csrftoken: any = useCookie('csrftoken')

  const requestHeaders = new Headers();
  requestHeaders.append("accept", "application/json");
  requestHeaders.append("Content-Type", "application/json");
  requestHeaders.append("X-CSRFToken", csrftoken.value);

  const authStore = useAuthStore();

  console.log("start: ", authStore.accessToken)
  if (authStore.accessToken) {
    console.log("end", authStore.accessToken)
    requestHeaders.append("Authorization", `Bearer ${authStore.accessToken}`)
  }

  if (apiData.isMultiPart) {
    requestHeaders.append("X-CSRFToken", csrftoken.value);
  }

  return await $fetch(apiData.path, {
    method: apiData.method,
    body: apiData.data,
    headers: requestHeaders,
    credentials: 'include'
  });
}
