<script setup lang="ts">
import { RoutesE } from '~/enums/routes'
import type { HostApplicationResp } from '~/interfaces/host-i'
import type { ApiBasePlatformApplication, PlatformApplicationResp } from '~/interfaces/platform-i'
import type { StrataApplicationResp } from '~/interfaces/strata-i'
import { useExaminerStore } from '~/store/examiner'
import { displayFullUnitAddress } from '~/utils/format-helper'
const localePath = useLocalePath()
const { t } = useI18n()
const { loading } = storeToRefs(useConnectDetailsHeaderStore())

useHead({
  title: t('page.dashboardList.title')
})

definePageMeta({
  layout: 'examiner',
  middleware: ['auth', 'require-account']
})

const HOST_TYPE = 'Host'
const PROPERTY_MANAGER_TYPE = 'Property Manager'
const STRATA_HOTEL_TYPE = 'Strata Hotel'
const PLATFORM_TYPE = 'Platform'

const applications = ref()
const mappedApplications = ref()

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
  await navigateTo(localePath(`${RoutesE.EXAMINE}/${row.applicationNumber}`))
}

onMounted(async () => {
  loading.value = true

  applications.value = await useExaminerStore().getAllApplications()

  mappedApplications.value = applications.value.map(
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
        const platformApplication = application.registration as ApiBasePlatformApplication
        applicationType = PLATFORM_TYPE
        applicantName = platformApplication.businessDetails.legalName
        propertyAddress = displayFullAddress(platformApplication.businessDetails.mailingAddress) || '-'
      } else if (registrationType === ApplicationType.STRATA_HOTEL) {
        const strataApplication = application.registration as ApiBaseStrataApplication
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

  loading.value = false
})

</script>
<template>
  <div v-if="loading" class="w-full justify-center p-14">
    Loading...
  </div>
  <div v-else class="space-y-8 py-8 sm:space-y-10 sm:py-10">
    <div class="bg-white">
      <UTable :columns="columns" :rows="mappedApplications">
        <template #actions-data="{ row }">
          <UButton :label="$t('btn.view')" @click="handleItemSelect(row)" />
        </template>
      </UTable>
    </div>
  </div>
</template>
