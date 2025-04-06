<script setup lang="ts">
import { type Track } from "@/services/models/album";
import { useAuthStore } from "@/store/auth";
import type { NuxtLink } from "~/components";

const route = useRoute();
const config = useRuntimeConfig();
const authStore = useAuthStore();
const isAuthenticated = computed(() => authStore.isAuthenticated)
const img = useImage();

<template>
  <AppPageContainer>
  </AppPageContainer>
</template>
