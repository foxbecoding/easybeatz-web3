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

<template>
  <div class="flex w-full h-[72px] justify-between items-center">
    <div class="flex gap-2">
      <img class="rounded-[0.5rem]" :src="albumCover" width="72px" height="72px" />
      <div class="flex flex-col gap-0 items-start">
        <p class="font-bold line-clamp-1 overflow-hidden text-ellipsis [line-height:0.8rem] md:[line-height:1rem]">
          {{ cartItem.track.title }}
        </p>
        <p>${{ cartItem.price }} - {{ trackLicense }}</p>
      </div>
    </div>
    <button class="btn btn-square btn-ghost btn-md mask mask-squircle">
      <Icon icon="solar:trash-bin-trash-bold" class="text-error" width="24" height="24" />
    </button>
  </div>
</template>
