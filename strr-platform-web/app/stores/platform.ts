export const useStrrPlatformStore = defineStore('strr/platform', () => {
  const { $strrApi } = useNuxtApp()
  const { primaryRep, secondaryRep } = storeToRefs(useStrrPlatformContact())
  const { platformBusiness } = storeToRefs(useStrrPlatformBusiness())
  const { platformDetails } = storeToRefs(useStrrPlatformDetails())

  const activePlatform = ref<PlatformRegistrationPayload | ApiBaseRegistration | undefined>(undefined)

  const getAccountRegistrations = async () => {
    // TODO: add error handling / modal popup?
    const resp = await $strrApi('/registrations', { method: 'GET' }) as { registrations: PlatformRegistrationPayload[] }
    return resp?.registrations
  }

  const getAccountApplications = async () => {
    // TODO: add error handling / modal popup?
    const resp = await $strrApi('/applications', { method: 'GET' }) as { applications: PlatformApplicationPayload[] }
    return resp.applications
  }

  const loadPlatform = async () => {
    // get registrations under this account
    const registrations = await getAccountRegistrations()
    if (registrations.length) {
      // set active platform to the most recent registration (ordered by api)
      activePlatform.value = registrations[0]
    } else {
      // No registrations under the account so get applications
      const applications = await getAccountApplications()
      if (applications.length) {
        // set active platform to the most recent application (ordered by api)
        activePlatform.value = applications[0]?.registration
      }
    }

    if (activePlatform.value) {
      // set relevant sub store values to active platform data
      if (activePlatform.value.platformRepresentatives[0]) {
        primaryRep.value = formatRepresentativeUI(activePlatform.value.platformRepresentatives[0])
      }
      if (activePlatform.value.platformRepresentatives[1]) {
        secondaryRep.value = formatRepresentativeUI(activePlatform.value.platformRepresentatives[1])
      }
      platformBusiness.value = formatBusinessDetailsUI(activePlatform.value.businessDetails)
      platformDetails.value = activePlatform.value.platformDetails
    }
  }

  return {
    activePlatform,
    loadPlatform
  }
})
