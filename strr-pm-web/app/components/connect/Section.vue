<script setup lang="ts">
const { title, optional, divider, className } = defineProps<{
  title?: string
  optional?: boolean
  divider?: boolean
  className?: string
}>()

const { t } = useI18n()
</script>
<template>
  <div
    data-testid="form-section"
    :class="`${className} mt-[40px] mobile:mt-[20px] ml-[40px] mr-[20px] mobile:mx-[8px]`"
  >
    <div class="flex flex-col sm:flex-row">
      <div v-if="title" class="w-[200px]">
        <p class="mb-[8px] sm:mb-0 sm:font-bold">
          {{ title }}
        </p>
        <p v-if="optional">
          {{ t('general.optional') }}
        </p>
      </div>
      <div class="w-full sm:pl-5">
        <slot />
      </div>
    </div>
    <div v-if="divider" class="hidden h-px w-full bg-bcGovGray-300 sm:block" />
  </div>
</template>
