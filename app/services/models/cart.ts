import { TrackPriceEnum } from "@/services/enums/track-price-enums";

export interface CartResponse {
    items: CartItem[];
    cart_count: number;
    cart_subtotal: number;
};

export interface CartItem {
    price_type: TrackPriceEnum.TRACK_PRICE | TrackPriceEnum.TRACK_EXCLUSIVE_PRICE;
    price: number;
    track: Track;
    album: Album;
    station: Station;
};

interface Track {
    tid: string;
    title: string;
    duration: number;
    formatted_duration: string;
    display: string;
    order_no: number;
};

interface Album {
    aid: string;
    cover: string;
};

interface Station {
    name: string;
    handle: string;
    picture: string;
    pubkey: string;
};

export const getCart = () => {
    const config = useRuntimeConfig();
    return submitRequest('GET', `${config.public.API_CART}/get_cart/`);
}

export const addCartItem = (data: { tid: string, type: TrackPriceEnum }) => {
    const config = useRuntimeConfig();
    return submitRequest('POST', `${config.public.API_CART}/add_cart_item/`, data);
}

export const removeCartItem = (data: { tid: string, type: TrackPriceEnum }) => {
    const config = useRuntimeConfig();
    return submitRequest('DELETE', `${config.public.API_CART}/remove_cart_item/`, data);
}

