<script setup lang="ts">

const props = defineProps<{ label: string, hideCheckbox?: boolean, hideChecklist?: boolean }>()

</script>

<template>
  <div class="flex items-center py-4 text-sm">
    <div class="flex w-1/5 items-start justify-start">
      <UCheckbox v-if="!hideCheckbox" name="checkbox">
        <template #label>
          <span class="text-sm font-bold">{{ props.label }}</span>
        </template>
      </UCheckbox>
    </div>
    <div class="flex-auto">
      <slot />
    </div>
    <div
      v-if="!hideChecklist"
      class="flex"
    >
      <UButton
        label="Checklist"
        variant="link"
        class="p-0 text-sm"
        icon="mdi-chevron-down"
        size="sm"
        trailing
      />
    </div>
  </div>
</template>

<style scoped></style>
