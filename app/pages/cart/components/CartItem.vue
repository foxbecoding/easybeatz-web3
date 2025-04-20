<script setup lang="ts">
import { type CartItem, type CartResponse, removeCartItem } from "@/services/models/cart";
import { TrackPriceEnum } from "@/services/enums/track-price-enums";
import CartItemDeleteModal from "./CartItemDeleteModal.vue";

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
const img = useImage();
const albumCover = computed(() => `${config.public.MEDIA_URL}${props.cartItem.album.cover}`);

const albumCoverStyles = computed(() => {
  const imgUrl = img(albumCover.value)
  return {
    backgroundImage: `url('${imgUrl}')`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    width: '88px',
    minWidth: '88px',
    height: '88px',
    minHeight: '88px'
  }
});

//Remove cart item logic
const deleteModel = ref(false);
const openDeleteModal = () => deleteModel.value = true;
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
  <div class="flex w-full h-[88px] justify-between items-center">
    <div class="flex gap-2">
      <div :style="albumCoverStyles" class="relative aspect-square bg-neutral rounded-[0.5rem]">
      </div>
      <div class="flex flex-col gap-0 items-start">
        <p class="font-bold line-clamp-2 overflow-hidden text-ellipsis [line-height:1rem] ">
          {{ cartItem.track.title }}
        </p>
        <p>{{ trackLicense }}</p>
        <p class="font-semibold">${{ cartItem.price }}</p>
      </div>
    </div>
    <button @click="openDeleteModal()" class="btn btn-square btn-ghost btn-md mask mask-squircle">
      <Icon icon="solar:trash-bin-trash-bold" class="text-error" width="24" height="24" />
    </button>
  </div>
  <CartItemDeleteModal v-model="deleteModel" :cart-item="cartItem" @submit="removeItem()" />
</template>
