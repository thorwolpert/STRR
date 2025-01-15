<script setup lang="ts">

const props = defineProps<{ application: ApiApplicationBaseResp }>()

const { t } = useI18n()
const { header, registration } = props.application

const displayApplicationType = {
  [ApplicationType.HOST]: t('strr.label.host'),
  [ApplicationType.PLATFORM]: t('strr.label.platform'),
  [ApplicationType.STRATA_HOTEL]: t('strr.label.strataHotel')
}

const getBadgeColor = (status: ApplicationStatus): string => {
  switch (status) {
    case ApplicationStatus.DECLINED:
      return 'red'
    case ApplicationStatus.AUTO_APPROVED:
    case ApplicationStatus.FULL_REVIEW_APPROVED:
    case ApplicationStatus.PROVISIONALLY_APPROVED:
      return 'green'
    default:
      return 'primary'
  }
}

const getApplicationName = (): string => {
  switch (registration.registrationType) {
    case ApplicationType.STRATA_HOTEL:
      return registration.businessDetails.legalName
    case ApplicationType.HOST:
      return registration.unitAddress?.nickname || ''
    case ApplicationType.PLATFORM:
      return registration.businessDetails?.legalName || ''
    default:
      return ''
  }
}

</script>

<template>
  <div class="border-b bg-white px-4 py-6">
    <div class="mb-2 text-2xl">
      <strong>
        {{ header?.applicationNumber }} |
      </strong>
      {{ getApplicationName() }}
    </div>
    <div class="text-sm">
      <UBadge class="mr-3 font-bold" :label="header.examinerStatus" :color="getBadgeColor(header.status)" />
      <strong>Type:</strong>
      {{ displayApplicationType[registration?.registrationType as keyof typeof displayApplicationType] }} |
      <strong>Submitted:</strong> {{ dateToString(header.applicationDateTime, 'y-MM-dd t') }}
      ({{ dayCountdown(header.applicationDateTime.toString(), true) }} days ago)
    </div>
  </div>
</template>

<style scoped></style>
