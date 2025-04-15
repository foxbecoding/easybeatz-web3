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

export const getCart = () => {
    const config = useRuntimeConfig();
    return submitRequest('GET', `${config.public.API_CART}/get-cart/`);
}

export const addCartItem = (data: any) => {
    const config = useRuntimeConfig();
    return submitRequest('POST', `${config.public.API_CART}/add-cart-item/`, data);
}
