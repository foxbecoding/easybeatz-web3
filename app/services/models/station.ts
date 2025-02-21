import { type ApiData } from "@/composables/useApi"

interface StationAlbum {
    aid: string,
    bio: string,
    title: string,
    cover: string,
}

export interface Station {
    albums: StationAlbum[];
    formatted_launched_date: string;
    description: string;
    email: string;
    handle: string;
    is_owner: boolean;
    name: string;
    picture: string;
    pubkey: string;
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

export const uploadStationPicture = async (data: object) => {
    try {
        const config = useRuntimeConfig();
        const fetchPath = `${config.public.API_STATION_PICTURE}/upload/`;
        const apiData: ApiData = { method: 'POST', path: fetchPath, data, isMultiPart: true };
        const res = await useApi(apiData);
        return res
    } catch (e: any) {
        console.error(e);
    }
}

export const hasStationChecker = async (): Promise<boolean> => {
    const config = useRuntimeConfig();
    const fetchPath = `${config.public.API_STATION}/has_station/`;
    const apiData: ApiData = { method: 'GET', path: fetchPath };
    const res = await useApi(apiData);
    return res
}
