<template>
  <footer class="block">
    <div class="flex justify-around pb-4">
      <button class="btn btn-ghost btn-square">
        <Icon icon="simple-icons:x" class="text-3xl primary" />
      </button>
    </div>
    <div class="px-4">
      <NuxtLink v-for="link in guideLinks" :to="link.to" class="text-sm mr-4">
        {{ link.title }}
      </NuxtLink>
    </div>

    <div class="px-4 pt-2">
      <p class="text-sm opacity-70">&copy {{ new Date().getFullYear() }} {{ company_name }} </p>
    </div>
  </footer>
</template>

<script setup lang="ts">
interface GuideLink {
  title: string,
  to: string
}

const config = useRuntimeConfig();
const company_name = `${config.public.COMPANY_NAME}`;
const guideLinks: GuideLink[] = [
  { title: 'About', to: '/about' },
  { title: 'Contact', to: '/contact' },
  { title: 'Terms', to: '/terms-of-service' },
  { title: 'Privacy', to: '/privacy-policy' },
];

</script>
