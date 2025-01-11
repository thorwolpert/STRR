<script setup lang="ts">

const props = defineProps<{ application: ApiApplicationBaseResp }>()

const { t } = useI18n()
const { header, registration } = props.application

const displayApplicationType = {
  [ApplicationType.HOST]: t('strr.label.host'),
  [ApplicationType.PLATFORM]: t('strr.label.platform'),
  [ApplicationType.STRATA_HOTEL]: t('strr.label.strataHotel')
}

</script>

<template>
  <div class="border-b py-6">
    <div class="mb-2 text-2xl">
      <strong>
        {{ header?.applicationNumber }} |
      </strong>
      {{ registration.unitAddress.nickname }}
    </div>
    <div class="text-sm">
      <UBadge class="mr-3 font-bold" :label="header.examinerStatus" color="primary" />
      <strong>Type:</strong>
      {{ displayApplicationType[registration?.registrationType as keyof typeof displayApplicationType] }} |
      <strong>Submitted:</strong> {{ dateToString(header.applicationDateTime, 'y-MM-dd t') }}
      ({{ dayCountdown(header.applicationDateTime.toString(), true) }} days ago)
    </div>
  </div>
</template>

<style scoped></style>
