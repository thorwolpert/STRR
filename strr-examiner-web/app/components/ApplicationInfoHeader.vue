<script setup lang="ts">
import { type HousApplicationResponse } from '~/types/application-response'

const props = defineProps<{ application: HousApplicationResponse }>()
const { header, registration } = props.application

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
      return (registration as ApiBaseStrataApplication).businessDetails.legalName
    case ApplicationType.HOST:
      return (registration as ApiHostApplication).unitAddress?.nickname || ''
    case ApplicationType.PLATFORM:
      return (registration as ApiBasePlatformApplication).businessDetails?.legalName || ''
    default:
      return ''
  }
}

</script>
<template>
  <div class="border-b bg-white py-6">
    <div class="app-inner-container">
      <div class="mb-2 text-2xl">
        <strong>
          {{ header?.applicationNumber }} |
        </strong>
        {{ getApplicationName() }}
        <UButton
          v-if="registration.registrationType === ApplicationType.STRATA_HOTEL"
          icon="mdi-web"
          :padded="false"
          variant="link"
          :to="(application.registration as ApiBaseStrataApplication).strataHotelDetails.brand.website"
          target="_blank"
          data-testid="strata-brand-website"
        />
      </div>
      <div class="text-sm">
        <UBadge
          class="mr-3 font-bold"
          :label="header.examinerStatus"
          :color="getBadgeColor(header.status)"
        />
        <strong>Type:</strong>
        {{ $t(`applicationType.${application.registration?.registrationType}`) }} |
        <strong>Submitted:</strong> {{ dateToString(header.applicationDateTime, 'y-MM-dd t') }}
        ({{ dayCountdown(header.applicationDateTime.toString(), true) }} days ago)
      </div>
    </div>
  </div>
</template>
