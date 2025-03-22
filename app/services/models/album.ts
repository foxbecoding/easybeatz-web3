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
    is_owner: boolean;
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


export const updateAlbum = (albumAid: string, data: any) => {
    const config = useRuntimeConfig();
    return submitRequest('PUT', `${config.public.API_ALBUM}/${albumAid}/`, data);
}

export const updateAlbumCover = (albumAid: string, data: any) => {
    const config = useRuntimeConfig();
    return submitRequest('PUT', `${config.public.API_ALBUM_COVER}/${albumAid}/`, data, true);
}

export const removeTrackFavorite = async (trackTid: string) => {
    const config = useRuntimeConfig();
    const fetchPath = `${config.public.API_TRACK_FAVORITE}/${trackTid}/`;
    const apiData: ApiData = { method: 'DELETE', path: fetchPath };
    const res = await useApi(apiData);
    return res;
}
