import { z } from 'zod'
import type { MultiFormValidationResult } from '~/interfaces/validation'

export const useStrrPlatformApplication = defineStore('strr/platformApplication', () => {
  const { $strrApi } = useNuxtApp()
  const platContactStore = useStrrPlatformContact()
  const platBusinessStore = useStrrPlatformBusiness()
  const platDetailsStore = useStrrPlatformDetails()

  const platformConfirmation = reactive({
    confirmInfoAccuracy: false,
    confirmDelistAndCancelBookings: false
  })

  // TODO: add validation messages - will add in future pr
  const getConfirmationSchema = () => z.object({
    confirmInfoAccuracy: z.literal(true),
    confirmDelistAndCancelBookings: z.literal(true)
  })

  const platformConfirmationSchema = getConfirmationSchema()

  const validatePlatformConfirmation = (returnBool = false): MultiFormValidationResult | boolean => {
    const result = validateSchemaAgainstState(
      platformConfirmationSchema, platformConfirmation, 'platform-confirmation-form'
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

    // TODO: implement
    // commenting this out now until payment is complete
    // const response = await $strrApi('/applications', {
    //   method: 'POST',
    //   body
    // })

    // console.info('strr api response: ', response)

    // return response
  }

  return {
    platformConfirmation,
    platformConfirmationSchema,
    submitPlatformApplication,
    validatePlatformConfirmation
  }
})
