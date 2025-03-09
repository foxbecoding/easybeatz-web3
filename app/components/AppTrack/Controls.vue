<script setup lang="ts">
import { submitTrackFavorite, removeTrackFavorite } from "@/services/models/album";
import { useUserStore } from "@/store/user";
import { useAuthStore } from "@/store/auth";
import { type Album, type Track } from "@/services/models/album";
import { type Station } from "@/services/models/station";

<template>
  <div class="flex">
    <button class="btn btn-square btn-ghost mask mask-squircle">
      <Icon icon="solar:heart-linear" width="24" height="24" />
    </button>
    <button class="btn btn-square btn-ghost mask mask-squircle">
      <Icon icon="solar:menu-dots-bold" width="24" height="24" />
    </button>
  </div>
</template>
