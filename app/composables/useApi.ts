export interface ApiData {
  data?: object
  isMultiPart?: boolean
  method: "GET" | "HEAD" | "PATCH" | "POST" | "PUT" | "DELETE"
  path: string
}

export const useApi = async (apiData: ApiData): Promise<any> => {
  const csrftoken: any = useCookie('csrftoken')

  //const myHeaders = new Headers();
  //myHeaders.append("Content-Type", "application/json");

  const requestHeaders = ref<HeadersInit>({
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken.value
  })

  if (apiData.isMultiPart) {
    requestHeaders.value = {
      'X-CSRFToken': csrftoken.value
    }
  }

  return await $fetch(apiData.path, {
    method: apiData.method,
    body: apiData.data,
    headers: requestHeaders.value,
    credentials: 'include'
  });
}
