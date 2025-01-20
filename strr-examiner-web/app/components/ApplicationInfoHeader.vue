<script setup lang="ts">
import { type HousApplicationResponse } from '~/types/application-response'

const props = defineProps<{ application: HousApplicationResponse }>()

const { application } = props
const { registration } = application

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
  <div class="border-b bg-white py-6">
    <div class="app-inner-container">
      <div class="mb-2 text-2xl">
        <strong>
          {{ application.header?.applicationNumber }} |
        </strong>
        {{ getApplicationName() }}
        <UButton
          v-if="registration.registrationType === ApplicationType.STRATA_HOTEL"
          icon="mdi-web"
          :padded="false"
          variant="link"
          :to="(application.registration as ApiBaseStrataApplication).strataHotelDetails.brand.website"
          target="_blank"
        />
      </div>
      <div class="text-sm">
        <UBadge
          class="mr-3 font-bold"
          :label="application.header.examinerStatus"
          :color="getBadgeColor(application.header.status)"
        />
        <strong>Type:</strong>
        {{ $t(`applicationType.${application.registration?.registrationType}`) }} |
        <strong>Submitted:</strong> {{ dateToString(application.header.applicationDateTime, 'y-MM-dd t') }}
        ({{ dayCountdown(application.header.applicationDateTime.toString(), true) }} days ago)
      </div>
    </div>
  </div>
</template>
