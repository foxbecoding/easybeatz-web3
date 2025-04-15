export const getCart = () => {
    const config = useRuntimeConfig();
    return submitRequest('GET', `${config.public.API_CART}/get-cart/`);
}

