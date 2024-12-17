<script setup lang="ts">
import ApplicationDetails from '~/components/ApplicationDetails.vue'
import RegistrationDetails from '~/components/RegistrationDetails.vue'
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
  middleware: ['auth', 'require-account']
})

let applicationId = ''
const application = ref<ApiApplicationResp | undefined>()
const applicationActions = ref<any[] | undefined>([]) // examiner actions
const permitStore = useHostPermitStore()

// const {
//   application: appOrg
//   // registration,
//   // permitDetails,
//   // isPaidApplication,
//   // showPermitDetails
// } = storeToRefs(permitStore)

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
  // await permitStore.loadHostData(applicationId)

  applicationActions.value = header.value?.examinerActions && header.value?.examinerActions.map((action) => {
    const actionConfig = {
      APPROVE: {
        label: 'Approve',
        color: 'green',
        trailingIcon: 'i-mdi-tick',
        variant: 'outline',
        click: () => approveApplicationHandler(header.value?.applicationNumber as string)
      },
      REJECT: {
        label: 'Reject',
        color: 'red',
        trailingIcon: 'i-mdi-close',
        variant: 'outline',
        click: () => rejectApplicationHandler(header.value?.applicationNumber as string)
      }
    }

    return actionConfig[action]
  })
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
  <div v-else class="py-14">
    <!-- APPLICATION DETAILS -->
    <ApplicationDetails
      v-if="application"
      :application="application"
      :application-actions="applicationActions"
    />

    <!-- REGISTRATION DETAILS -->
    <RegistrationDetails
      v-if="application && header?.registrationNumber"
      :application="application"
    />

    <!-- PRIMARY CONTACT -->
    <ConnectPageSection
      v-if="(registration as ApiHostApplication)?.primaryContact"
      :heading="{
        label: 'Primary Contact',
        labelClass: 'font-bold',
        icon: 'mdi-user-star'
      }"
      class="mt-10 pb-4"
    >
      <ConnectFormSection title="Contact Type" class="pt-4">
        {{ (registration as ApiHostApplication)?.primaryContact.contactType }}
      </ConnectFormSection>

      <ConnectFormSection title="Full Name" class="pt-4">
        {{ displayContactFullName((registration as ApiHostApplication)?.primaryContact.name) }}
      </ConnectFormSection>

      <ConnectFormSection title="Email Address" class="pt-4">
        {{ (registration as ApiHostApplication)?.primaryContact.details.emailAddress }}
      </ConnectFormSection>

      <ConnectFormSection title="Phone Number" class="pt-4">
        {{ (registration as ApiHostApplication)?.primaryContact.details.phoneNumber }}
      </ConnectFormSection>

      <ConnectFormSection title="Mailing Address" class="pt-4">
        {{ displayFullAddress((registration as ApiHostApplication)?.primaryContact.mailingAddress) }}
      </ConnectFormSection>
    </ConnectPageSection>

    <!-- STRATA HOTEL -->
    <ConnectPageSection
      v-if="(registration)?.registrationType === ApplicationType.STRATA_HOTEL"
      :heading="{
        label: 'Strata Hotel Details',
        labelClass: 'font-bold',
        icon: 'mdi-building'
      }"
      class="mt-10 pb-4"
    >
      <ConnectFormSection title="Brand Name" class="pt-4">
        <div class="w-[500px] overflow-hidden text-ellipsis">
          {{ (registration as ApiBaseStrataApplication)?.strataHotelDetails.brand.name }}
        </div>
      </ConnectFormSection>

      <ConnectFormSection title="Location" class="pt-4">
        {{ displayFullAddress((registration as ApiBaseStrataApplication)?.strataHotelDetails.location) }}
      </ConnectFormSection>

      <ConnectFormSection title="Number of Units" class="pt-4">
        {{ (registration as ApiBaseStrataApplication)?.strataHotelDetails.numberOfUnits }}
      </ConnectFormSection>
    </ConnectPageSection>
  </div>
</template>

<style scoped></style>
