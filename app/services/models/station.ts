import { type ApiData } from "@/composables/useApi"

export interface Station {
    created: string;
    description: string | null;
    email: string | null;
    handle: string | null;
    is_owner: boolean;
    name: string | null;
    error?: any;
}

export const getStation = async (pubkey: string): Promise<Station> => {
    const config = useRuntimeConfig();
    const fetchPath = `${config.public.API_STATION}/${pubkey}/public_station/`;
    const apiData: ApiData = { method: 'GET', path: fetchPath }
    const res = await useApi(apiData)
    if (res.error) {
        console.error(res.error);
    }
    return res
}

export const partialUpdateStation = async (pubkey: string, data: object): Promise<Station> => {
    const config = useRuntimeConfig();
    const fetchPath = `${config.public.API_STATION}/${pubkey}/`;
    const apiData: ApiData = { method: 'PATCH', path: fetchPath, data }
    const res = await useApi(apiData)
    if (res.error) {
        console.error(res.error);
    }
    return res
}
