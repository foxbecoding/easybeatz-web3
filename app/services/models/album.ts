import { type ApiData } from "@/composables/useApi";
import { type Station } from "@/services/models/station";

export interface Album {
    aid: string;
    bio: string;
    cover: string;
    title: string;
    total_duration: number;
    uploaded_at: string;
    station: Station;
    tracks: Track[];
};

export interface Track {
    bpm: string;
    duration: number;
    formatted_duration: string;
    tid: string;
    title: string;
    display: string;
    oder_no: number;
    price: number;
    exclusive_price: number | null;
    mood: {
        name: string;
        slug: string;
    };
    genres: {
        name: string;
        slug: string;
    };
};

export const submitAlbumProject = async (data: any) => {
    const config = useRuntimeConfig();
    const fetchPath = `${config.public.API_ALBUM_PROJECT}/`;
    const apiData: ApiData = { method: 'POST', path: fetchPath, data, isMultiPart: true };
    const res = await useApi(apiData);
    return res;
}

export const albumFormValidator = async (data: any) => {
    const config = useRuntimeConfig();
    const fetchPath = `${config.public.API_ALBUM_PROJECT}/validate_album_form/`;
    const apiData: ApiData = { method: 'POST', path: fetchPath, data, isMultiPart: true };
    const res = await useApi(apiData);
    return res;
}
