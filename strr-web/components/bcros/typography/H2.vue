<template>
  <h2 :class="`${className} font-bold text-[24px] py-[25px]`" data-cy="h2">
    {{ text }}
  </h2>
</template>

<script setup lang="ts">
const { text, className } = defineProps<{ text: string, className?: string }>()
</script>
