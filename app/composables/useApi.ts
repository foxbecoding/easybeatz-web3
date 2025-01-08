export interface ApiData {
  data?: object
  isMultiPart?: boolean
  method: "GET" | "HEAD" | "PATCH" | "POST" | "PUT" | "DELETE"
  path: string
}

export const useApi = async (apiData: ApiData): Promise<any> => {
  const csrftoken: any = useCookie('csrftoken')
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

  const { data, error } = await useFetch(apiData.path, {
    method: apiData.method,
    body: apiData.data,
    headers: requestHeaders,
    credentials: 'include'
  });

  return { data, error }
}
