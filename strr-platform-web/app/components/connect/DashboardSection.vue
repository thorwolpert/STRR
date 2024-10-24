<script setup lang="ts">
defineProps<{ title: string, loading: boolean }>()
</script>
<template>
  <div class="space-y-2">
    <slot name="header">
      <ConnectTypographyH2 :text="title" />
    </slot>
    <div class="rounded bg-white">
      <slot v-if="loading" name="loading">
        <div class="min-w-[300px] animate-pulse space-y-2 p-5">
          <div class="h-5 w-full rounded bg-gray-200" />
          <div class="h-5 w-full rounded bg-gray-200" />
          <div class="h-5 w-full rounded bg-gray-200" />
        </div>
      </slot>
      <slot v-else name="default" />
    </div>
  </div>
</template>
