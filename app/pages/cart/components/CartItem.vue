<script setup lang="ts">
import { type CartItem, type CartResponse, removeCartItem } from "@/services/models/cart";
import { TrackPriceEnum } from "@/services/enums/track-price-enums";

const props = defineProps<{ cartItem: CartItem }>();

const config = useRuntimeConfig();

const trackLicense = computed(() => {
  const priceMap = {
    [TrackPriceEnum.TRACK_PRICE]: "Unlimited license",
    [TrackPriceEnum.TRACK_EXCLUSIVE_PRICE]: "Exclusive license"
  }
  return priceMap[props.cartItem.price_type];
});

// Album cover logic
const albumCover = computed(() => `${config.public.MEDIA_URL}${props.cartItem.album.cover}`);

//Remove cart item logic
const removeItem = async () => {
  try {
    const { message, data } = await removeCartItem({ tid: props.cartItem.track.tid, type: props.cartItem.price_type });
    useCart().cartSetter(data as CartResponse);
    if (message) {
      useToast().setToast(message, "INFO");
    }
  } catch (error: any) {
    useToast().setToast(error.data.message, "ERROR");
  }
}

</script>

