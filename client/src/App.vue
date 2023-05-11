<script setup>
import { watch } from 'vue';
import { useRouter, useRoute, RouterView } from 'vue-router';
import { ref } from 'vue';

const scrollToHash = (hash) => {
  if (hash.value) {
    const elementId = hash.value.slice(1);
    setTimeout(() => {
      const element = document.getElementById(elementId)
      if (element) {
        element.scrollIntoView({ behavior: "auto" });
      }
    }, 200)

  }
};

const router = useRouter();
const route = useRoute();

watch(() => route.fullPath, () => {
  const hash = ref(route.hash);
  scrollToHash(hash);
});
</script>

<template>
  <RouterView />
</template>

<style scoped>
body,
html {
  margin: 0;
}
</style>
