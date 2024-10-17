export const useStrrPlatformApplication = defineStore('strr/platformApplication', () => {
  const { completingParty, primaryRep, secondaryRep } = storeToRefs(useStrrPlatformContact())
  const { platformBusiness } = storeToRefs(useStrrPlatformBusiness())
  const { platformDetails } = storeToRefs(useStrrPlatformDetails())

  const confirmInfoAccuracy = ref(false)
  const confirmDelistAndCancelBookings = ref(false)

  const getPlatformApplication = () => {
    return {
      completingParty: completingParty.value,
      primaryRep: primaryRep.value,
      secondaryRep: secondaryRep.value,
      platformBusiness: platformBusiness.value,
      platformDetails: platformDetails.value
    }
  }

  // TODO: submit

  return {
    confirmInfoAccuracy,
    confirmDelistAndCancelBookings,
    getPlatformApplication
  }
})
