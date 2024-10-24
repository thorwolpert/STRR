<script setup lang="ts">
defineProps<{ text: string }>()
</script>
<template>
  <h1 class="text-xl font-bold" data-testid="h1">
    {{ text }}
  </h1>
</template>
