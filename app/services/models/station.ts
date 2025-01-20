import { type ApiData } from "@/composables/useApi"

export interface Station {
    created: string;
    description: string;
    email: string;
    handle: string;
    is_owner: boolean;
    name: string;
    error?: any;
}

export const getStation = async (pubkey: string): Promise<Station> => {
    const config = useRuntimeConfig();
    const fetchPath = `${config.public.API_STATION}/${pubkey}/`;
    const apiData: ApiData = { method: 'GET', path: fetchPath };
    const res = await useApi(apiData);
    if (res.error) {
        console.error(res.error);
    }
    return res
}

export const createStation = async (data: object): Promise<Station> => {
    const config = useRuntimeConfig();
    const fetchPath = `${config.public.API_STATION}/`;
    const apiData: ApiData = { method: 'POST', path: fetchPath, data };
    const res = await useApi(apiData);
    if (res.error) {
        console.error(res.error);
    }
    return res
}

export const updateStation = async (pubkey: string, data: object): Promise<Station> => {
    const config = useRuntimeConfig();
    const fetchPath = `${config.public.API_STATION}/${pubkey}/`;
    const apiData: ApiData = { method: 'PUT', path: fetchPath, data };
    const res = await useApi(apiData);
    if (res.error) {
        console.error(res.error);
    }
    return res
}

export const hasStationChecker = async (): Promise<boolean> => {
    const config = useRuntimeConfig();
    const fetchPath = `${config.public.API_STATION}/has_station/`;
    const apiData: ApiData = { method: 'GET', path: fetchPath };
    const res = await useApi(apiData);
    return res
}
