<template>
</template>

<script setup lang="ts">

interface LinkList {
  title: string,
  to: string
}

const config = useRuntimeConfig();
const company_name = ref<string>(`${config.public.COMPANY_NAME}`)
const auxLinks = ref<LinkList[]>([
  { title: 'About', to: '/about' },
  { title: 'Contact', to: '/contact' },
  { title: 'FAQ', to: '/faq' },
  // { title: 'How it works', to: '/how-it-works' },
  // { title: 'Blog', to: '/blog' },
  { title: 'Terms', to: '/terms' },
  { title: 'Privacy', to: '/privacy' },
])

</script>
<style scoped>
.aux-links {
  text-decoration: none;
  font-size: 0.8rem;
  opacity: 0.8;
}

.aux-links:hover {
  opacity: 0.65;
}

.legal-content {
  font-size: 0.8rem;
  opacity: 0.8;
}
</style>
