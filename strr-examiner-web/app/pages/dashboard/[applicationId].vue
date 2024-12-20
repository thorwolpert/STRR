<script setup lang="ts">
import type { ApiHostApplication } from '#build/imports'
import ApplicationDetailsSection from '~/components/ApplicationDetailsSection.vue'
import { useExaminerStore } from '~/store/examiner'

const { t } = useI18n()
const localePath = useLocalePath()
const route = useRoute()
const config = useRuntimeConfig().public
const { loading } = storeToRefs(useConnectDetailsHeaderStore())
const { getApplication, approveApplication, rejectApplication } = useExaminerStore()

useHead({
  title: t('page.dashboardList.title')
})

definePageMeta({
  layout: 'examiner',
  middleware: ['auth', 'require-account']
})

let applicationId = ''
const application = ref<ApiApplicationResp>()

const approveApplicationHandler = async (appNum: string) => {
  try {
    loading.value = true
    await approveApplication(appNum)
    await fetchApplication(appNum)
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const rejectApplicationHandler = async (appNum: string) => {
  try {
    loading.value = true
    await rejectApplication(appNum)
    await fetchApplication(appNum)
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const fetchApplication = async (applicationNumber: string): Promise<void> => {
  applicationId = applicationNumber
  application.value = await getApplication(applicationNumber)
}

onMounted(async () => {
  loading.value = true

  await fetchApplication(route.params.applicationId as string)

  // update breadcrumbs with strata business name
  setBreadcrumbs([
    {
      label: t('label.bcregDash'),
      to: config.registryHomeURL + 'dashboard',
      appendAccountId: true,
      external: true
    },
    { label: t('strr.title.dashboard'), to: localePath('/dashboard') },
    { label: applicationId }
  ])

  loading.value = false
})

const header = computed((): ApplicationHeader | undefined => application.value?.header)
const registration = computed(
  (): ApiBaseApplication | ApiHostApplication | ApiBaseStrataApplication | undefined => application.value?.registration
)

</script>

<template>
  <div v-if="loading" class="w-full justify-center p-14">
    Loading...
  </div>
  <div v-else class="py-5">
    <div class="mb-2 align-middle text-lg">
      <strong>
        {{ header?.applicationNumber }}
      </strong>
      <UButton
        label="View History"
        variant="link"
        size="sm"
        class="mx-2 underline"
      />
    </div>

    <div class="flex flex-row gap-x-5 divide-x text-sm">
      <div>
        <dl class="grid grid-cols-[repeat(2,auto)] gap-x-4">
          <dt>Status:</dt>
          <dd>{{ header?.hostStatus }}</dd>

          <dt>Submitted:</dt>
          <dd>{{ dateToString(header?.applicationDateTime || '') }}</dd>

          <dt>Registration Type:</dt>
          <dd>{{ registration?.registrationType }}</dd>
        </dl>
      </div>
      <div>
        <dl class="grid grid-cols-[repeat(2,auto)] gap-x-4 pl-5">
          <dt>Unit Address:</dt>
          <dd class="w-[150px]">
            {{ displayFullUnitAddress((registration as ApiHostApplication)?.unitAddress) }}
          </dd>

          <dt>Municipality:</dt>
          <dd>{{ (registration as ApiHostApplication)?.strRequirements?.organizationNm }}</dd>
        </dl>
      </div>
      <div>
        <dl class="grid grid-cols-[repeat(2,auto)] gap-x-4 pl-5">
          <dt>Host Address:</dt>
          <dd class="w-[150px]">
            {{ displayFullAddress((registration as ApiHostApplication)?.primaryContact.mailingAddress) }}
          </dd>

          <dt>Address Type:</dt>
          <dd>Mailing</dd>

          <dt>Same as Unit Address:</dt>
          <dd>{{ (registration as ApiHostApplication)?.unitDetails.hostResidence }}</dd>

          <dt>Host Name:</dt>
          <dd>{{ displayContactFullName((registration as ApiHostApplication)?.primaryContact || {}) }}</dd>

          <dt>Host Type:</dt>
          <dd>{{ (registration as ApiHostApplication)?.primaryContact.contactType }}</dd>

          <dt>Ownership Type:</dt>
          <dd>{{ (registration as ApiHostApplication)?.unitDetails.ownershipType }}</dd>
        </dl>
      </div>
      <div>
        <dl class="grid grid-cols-[repeat(2,auto)] gap-x-4 pl-5">
          <dt>Property Type:</dt>
          <dd>{{ (registration as ApiHostApplication)?.unitDetails.propertyType }}</dd>

          <dt>Configuration:</dt>
          <dd>{{ (registration as ApiHostApplication)?.unitDetails.rentalUnitSpaceType }}</dd>

          <dt>Rooms:</dt>
          <dd>{{ (registration as ApiHostApplication)?.unitDetails.numberOfRoomsForRent }}</dd>
        </dl>
      </div>
    </div>
    <!-- APPLICATION SECTIONS -->

    <div class="mt-6 divide-y">
      <ApplicationDetailsSection
        label="Short-term rentals prohibited"
        hide-checklist
      >
        <div class="flex items-center justify-between">
          <div class="flex">
            {{ (registration as ApiHostApplication)?.strRequirements?.isStrProhibited ? 'Yes' : 'No' }}
          </div>
          <div class="flex items-start justify-end gap-x-2">
            <UButton
              label="Quick send to supervisor"
              color="primary"
            />
          </div>
        </div>
      </ApplicationDetailsSection>

      <ApplicationDetailsSection label="Business Licence">
        <div v-if="registration?.businessDetails?.businessNumber">
          Business Licence Number: {{ registration?.businessDetails?.businessNumber }}
        </div>
        <div v-else>
          Not Provided
        </div>
      </ApplicationDetailsSection>

      <ApplicationDetailsSection label="Principal Residence">
        <div>
          {{ (registration as ApiHostApplication)?.strRequirements?.isPrincipalResidenceRequired ?
            'Required' : 'Not Required' }}
        </div>
        <div>
          <strong>STR Accommodations Act: </strong>
          {{ (registration as ApiHostApplication)?.strRequirements?.isStraaExempt ?
            'Exempt' : 'Not Exempt' }}
        </div>
      </ApplicationDetailsSection>

      <ApplicationDetailsSection
        v-if="(registration as ApiBaseStrataApplication)?.businessDetails"
        label="Business Registration"
      >
        <div>
          <div>
            <strong>Mailing Address:</strong>
          </div>
        </div>
      </ApplicationDetailsSection>

      <ApplicationDetailsSection
        label=""
        hide-checkbox
        hide-checklist
        class="pt-8"
      >
        <div class="flex justify-end gap-x-2">
          <UButton
            label="Approve"
            color="primary"
            @click="approveApplicationHandler(applicationId)"
          />
          <UButton
            label="Reject"
            color="gray"
            @click="rejectApplicationHandler(applicationId)"
          />
        </div>
      </ApplicationDetailsSection>
    </div>
  </div>
</template>

<style scoped>
dl>dt {
  @apply font-bold text-black
}
</style>
