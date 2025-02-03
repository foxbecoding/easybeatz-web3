import { type ApiData } from "@/composables/useApi";

export const validateAlbumForm = async (data: any) => {
    const config = useRuntimeConfig();
    const fetchPath = `${config.public.API_ALBUM_PROJECT}/validate_album_form/`;
    const apiData: ApiData = { method: 'POST', path: fetchPath, data, isMultiPart: true };
    const res = await useApi(apiData);
    return res
}
