export const useStrrPlatformApplication = defineStore('strr/platformApplication', () => {
  // const { $strrApi } = useNuxtApp()
  // const { platformDetails } = storeToRefs(useStrrPlatformDetails())
  const strrModal = useStrrModals()
  const platContactStore = useStrrPlatformContact()
  const platBusinessStore = useStrrPlatformBusiness()
  const platDetailsStore = useStrrPlatformDetails()

  const confirmInfoAccuracy = ref(false)
  const confirmDelistAndCancelBookings = ref(false)

  function createApplicationBody (): PlatformApplicationPayload {
    const applicationBody: PlatformApplicationPayload = {
      registration: {
        registrationType: ApplicationType.PLATFORM,
        completingParty: formatParty(platContactStore.completingParty),
        platformRepresentatives: [],
        businessDetails: formatBusinessDetails(platBusinessStore.platformBusiness),
        platformDetails: formatPlatformDetails(platDetailsStore.platformDetails)
      }
    }

    if (platContactStore.primaryRep !== undefined) {
      applicationBody.registration.platformRepresentatives.push(
        formatRepresentative(platContactStore.primaryRep)
      )
    }

    if (platContactStore.secondaryRep !== undefined) {
      applicationBody.registration.platformRepresentatives.push(
        formatRepresentative(platContactStore.secondaryRep)
      )
    }

    return applicationBody
  }

  async function submitPlatformApplication () {
    try {
      const contactResults = await platContactStore.validatePlatformContact()
      const businessResults = await platBusinessStore.validatePlatformBusiness()
      const detailsResults = await platDetailsStore.validatePlatformDetails()

      console.info('contact validations: ', contactResults)
      console.info('business validations: ', businessResults)
      console.info('details validations: ', detailsResults)

      const body = createApplicationBody()

      console.info('submitting application: ', body)
      // await $strrApi('/applications', {
      //   method: 'POST',
      //   body
      // })
    } catch (e) {
      logFetchError(e, 'Error creating platform application')
      strrModal.openAppSubmitError() // pass in error object ??
    }
  }

  return {
    confirmInfoAccuracy,
    confirmDelistAndCancelBookings,
    // getPlatformApplication,
    submitPlatformApplication
  }
})
