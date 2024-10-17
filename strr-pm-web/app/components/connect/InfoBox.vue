<script setup lang="ts">
defineProps<{ title?: string, titleClass?: string, content?: string }>()
</script>
<template>
  <div>
    <strong v-if="title" :class="titleClass || 'text-[smaller] font-bold italic tracking-wider'">
      {{ title }}
    </strong>
    <slot>
      <p v-if="content" data-testid="content">
        {{ content }}
      </p>
    </slot>
  </div>
</template>
