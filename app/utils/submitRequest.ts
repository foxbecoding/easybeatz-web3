import { type ApiData } from "@/composables/useApi";

export const submitRequest = async (
  method: 'GET' | 'POST' | 'PUT' | 'DELETE',
  path: string,
  data?: any,
  isMultiPart = false
) => {
  const apiData: ApiData = { method, path, data, isMultiPart };
  return await useApi(apiData);
};
