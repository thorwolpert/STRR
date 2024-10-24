import { z } from 'zod'
import type { MultiFormValidationResult } from '~/interfaces/validation'

export const useStrrPlatformApplication = defineStore('strr/platformApplication', () => {
  // const { $strrApi } = useNuxtApp()
  const platContactStore = useStrrPlatformContact()
  const platBusinessStore = useStrrPlatformBusiness()
  const platDetailsStore = useStrrPlatformDetails()

  const platformConfirmation = reactive({
    confirmInfoAccuracy: false,
    confirmDelistAndCancelBookings: false
  })

  const getConfirmationSchema = () => z.object({
    confirmInfoAccuracy: z.literal(true),
    confirmDelistAndCancelBookings: z.literal(true)
  })

  const platformConfirmationSchema = getConfirmationSchema()

  const validatePlatformConfirmation = (returnBool = false): MultiFormValidationResult | boolean => {
    const result = validateSchemaAgainstState(
      getConfirmationSchema(), platformConfirmation, 'platform-confirmation-form'
    )

    if (returnBool) {
      return result.success === true
    } else {
      return [result]
    }
  }

  const createApplicationBody = (): PlatformApplicationPayload => {
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

  const submitPlatformApplication = async () => {
    const body = createApplicationBody()

    console.info('submitting application: ', body)
    // await $strrApi('/applications', {
    //   method: 'POST',
    //   body
    // })
  }

  return {
    platformConfirmation,
    platformConfirmationSchema,
    // confirmInfoAccuracy,
    // confirmDelistAndCancelBookings,
    // getPlatformApplication,
    submitPlatformApplication,
    validatePlatformConfirmation
  }
})
