<script setup lang="ts">
defineProps<{ label?: string }>()
const { close } = useStrrExpansion()
</script>
<template>
  <div class="-mx-8 flex rounded bg-white px-8 py-6">
    <div v-if="label" class="w-1/5">
      <span class="text-base font-bold text-gray-900">{{ label }}</span>
    </div>
    <div class="grow pt-1 text-sm">
      <slot />
    </div>
    <div>
      <UButton
        :label="$t('btn.close')"
        variant="ghost"
        icon="i-mdi-close"
        trailing
        @click="close"
      />
    </div>
  </div>
</template>
