<script setup lang="ts">
const props = defineProps<{
  application: StrataApplicationResp
}>()

defineEmits<{
  close: [void]
}>()

const { t } = useI18n()
const { registration } = props.application
const { businessDetails } = registration

</script>

<template>
  <div class="text-bcGovColor-midGray grid grid-cols-4 gap-x-5 text-sm">
    <div class="flex w-[200px]">
      <b>Businesses</b>
    </div>
    <div class="space-y-2">
      <b>{{ t('strr.label.business').toUpperCase() }}</b>
      <ConnectInfoWithIcon
        icon="i-mdi-domain"
        :content="businessDetails?.legalName"
      />
      <ConnectInfoWithIcon
        v-if="businessDetails?.businessNumber"
        icon="i-mdi-domain"
        :content="businessDetails?.businessNumber"
      />
      <ConnectInfoWithIcon
        icon="i-mdi-envelope-outline"
        :content="displayFullAddress(businessDetails.mailingAddress)"
      />
      <ConnectInfoWithIcon
        v-if="businessDetails?.homeJurisdiction"
        icon="i-mdi-map-outline"
        :content="businessDetails?.homeJurisdiction"
      />
    </div>
    <div class="space-y-2">
      <b>{{ t('strr.label.attorneyForService').toUpperCase() }}</b>
      <ConnectInfoWithIcon
        v-if="businessDetails.registeredOfficeOrAttorneyForServiceDetails.attorneyName"
        icon="i-mdi-domain"
        :content="businessDetails.registeredOfficeOrAttorneyForServiceDetails.attorneyName"
      />
      <ConnectInfoWithIcon
        icon="i-mdi-map-marker-outline"
        :content="displayFullAddress(businessDetails.registeredOfficeOrAttorneyForServiceDetails.mailingAddress)"
      />
    </div>
    <div class="relative flex-1">
      <UButton
        :label="t('btn.close')"
        trailing-icon="i-mdi-close"
        variant="ghost"
        class="absolute right-0"
        @click="$emit('close')"
      />
    </div>
  </div>
</template>

<style scoped>

</style>
