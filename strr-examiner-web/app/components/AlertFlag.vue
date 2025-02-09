<script setup lang="ts">
const props = defineProps<{ tooltipText?: string }>()

</script>

<template>
  <UTooltip
    :text="props.tooltipText"
    :popper="{
      placement: 'right',
      arrow: true
    }"
    :ui="{
      base: 'p-4'
    }"
  >
    <UIcon
      name="i-mdi-alert"
      class="-mb-1 size-5 bg-red-600"
    />
  </UTooltip>
</template>
