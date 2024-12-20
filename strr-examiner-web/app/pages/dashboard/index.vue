<script setup lang="ts">
import { useExaminerStore } from '~/store/examiner'
import { displayFullUnitAddress } from '~/utils/format-helper'
const localePath = useLocalePath()
const { t } = useI18n()

useHead({
  title: t('page.dashboardList.title')
})

definePageMeta({
  layout: 'examiner',
  middleware: ['auth', 'require-account']
})

setBreadcrumbs([
  {
    label: t('label.bcregDash'),
    to: useRuntimeConfig().public.registryHomeURL + 'dashboard',
    appendAccountId: true,
    external: true
  },
  { label: t('page.dashboardList.h1') }
])

const HOST_TYPE = 'Host'
const PROPERTY_MANAGER_TYPE = 'Property Manager'
const STRATA_HOTEL_TYPE = 'Strata Hotel'
const PLATFORM_TYPE = 'Platform'

const applications = ref()

applications.value = await useExaminerStore().getAllApplications()

const mappedApplications = applications.value.map(
  (application: HostApplicationResp | PlatformApplicationResp | StrataApplicationResp) => {
    const {
      header: {
        applicationNumber,
        registrationNumber,
        examinerStatus,
        status,
        applicationDateTime
      },
      registration: { registrationType }
    } = application

    let applicationType = ''
    let applicantName = ''
    let propertyAddress = ''
    if (registrationType === ApplicationType.HOST) {
      const hostApplication: ApiHostApplication = application.registration as ApiHostApplication
      if (hostApplication.propertyManager && hostApplication.propertyManager.initiatedByPropertyManager) {
        applicationType = PROPERTY_MANAGER_TYPE
      } else {
        applicationType = HOST_TYPE
      }
      applicantName = displayContactFullName(hostApplication.primaryContact) || ''
      propertyAddress = displayFullUnitAddress(hostApplication.unitAddress) || '-'
    } else if (registrationType === ApplicationType.PLATFORM) {
      const platformApplication = application.registration
      applicationType = PLATFORM_TYPE
      applicantName = platformApplication.businessDetails.legalName
      propertyAddress = displayFullAddress(platformApplication.businessDetails.mailingAddress) || '-'
    } else if (registrationType === ApplicationType.STRATA_HOTEL) {
      const strataApplication = application.registration
      applicationType = STRATA_HOTEL_TYPE
      const { firstName, middleName, lastName } = strataApplication.completingParty
      applicantName = displayContactFullName({ firstName, middleName, lastName }) || '-'
      propertyAddress = displayFullAddress(strataApplication.strataHotelDetails.location) || '-'
    }

    return {
      applicationNumber,
      registrationNumber: registrationNumber ?? '-',
      registrationType: applicationType,
      propertyAddress,
      applicantName,
      status: examinerStatus || status,
      isPaid: status !== 'DRAFT' && status !== 'PAYMENT_DUE',
      submissionDate: dateToString(applicationDateTime, 'MMMM d, yyyy')
    }
  }
)

const columns = [
  { key: 'applicationNumber', label: 'Application Number', sortable: false },
  { key: 'registrationNumber', label: 'Registration Number', sortable: false },
  { key: 'registrationType', label: 'Type', sortable: false },
  { key: 'propertyAddress', label: 'Address', sortable: false },
  { key: 'applicantName', label: 'Applicant Name', sortable: false },
  { key: 'status', label: 'Status', sortable: false },
  { key: 'submissionDate', label: 'Submission Date', sortable: false },
  { key: 'actions', label: t('label.actions') }
]

async function handleItemSelect (row: any) {
  await navigateTo(localePath('/dashboard/' + row.applicationNumber))
}

</script>
<template>
  <div class="space-y-8 py-8 sm:space-y-10 sm:py-10">
    <div class="bg-white">
      <UTable :columns="columns" :rows="mappedApplications">
        <template #actions-data="{ row }">
          <UButton :label="$t('btn.view')" @click="handleItemSelect(row)" />
        </template>
      </UTable>
    </div>
  </div>
</template>
