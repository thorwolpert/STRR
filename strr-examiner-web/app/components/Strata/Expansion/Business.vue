<script setup lang="ts">
const props = defineProps<{
  application: StrataApplicationResp
}>()

defineEmits<{
  close: [void]
}>()

const { registration } = props.application
const { businessDetails } = registration

</script>

<template>
  <CommonExpansionTemplate
    :label="$t('strr.label.businesses')"
  >
    <div class="flex gap-x-10">
      <div class="space-y-2">
        <b>{{ $t('strr.label.business').toUpperCase() }}</b>
        <ConnectInfoWithIcon
          icon="i-mdi-domain"
          :content="businessDetails?.legalName"
        />
        <ConnectInfoWithIcon
          v-if="businessDetails?.businessNumber"
          icon="i-mdi-pound"
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
        <b>{{ $t('strr.label.attorneyForService').toUpperCase() }}</b>
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
    </div>
  </CommonExpansionTemplate>
</template>

<style scoped>

</style>
