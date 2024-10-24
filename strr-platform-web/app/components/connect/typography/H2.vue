<script setup lang="ts">
defineProps<{ text: string }>()
</script>
<template>
  <h2 :class="`font-bold text-lg`" data-testid="h2">
    {{ text }}
  </h2>
</template>
