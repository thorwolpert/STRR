import { z, type ZodIssue } from 'zod'
import { getRequiredNonEmptyString, getRequiredUrl } from '~/utils/connect-validation'

export const useStrrPlatformDetails = defineStore('strr/platformDetails', () => {
  const { t } = useI18n()

  const getPlatformBrandSchema = () => z.object({
    name: getRequiredNonEmptyString(t('validation.brand.name')),
    website: getRequiredUrl(t('validation.brand.site'))
  })

  const getPlatformDetailsSchema = () => z.object({
    listingSize: z.enum([ListingSize.UNDER_THOUSAND, ListingSize.THOUSAND_OR_MORE]),
    brands: z.array(getPlatformBrandSchema())
  })

  const platformDetailSchema = getPlatformDetailsSchema()

  const platformDetails = ref<{ brands: PlatBrand[], listingSize: ListingSize | undefined }>({
    brands: [{ name: '', website: '' }],
    listingSize: undefined
  })

  const addNewEmptyBrand = () => {
    platformDetails.value.brands.push({ name: '', website: '' })
  }
  const removeBrandAtIndex = (index: number) => {
    platformDetails.value.brands.splice(index, 1)
  }

  const validatePlatformDetails = async (returnBool = false): Promise<
    { formId: string; success: boolean; errors: ZodIssue[] }[] | boolean
  > => {
    const validations = [
      validateSchemaAgainstState(platformDetailSchema, platformDetails.value, 'platform-details-form')
    ]

    const results = await Promise.all(validations)

    if (returnBool) {
      return results.every(result => result.success === true)
    } else {
      return results
    }
  }

  return {
    platformDetails,
    platformDetailSchema,
    getPlatformBrandSchema,
    getPlatformDetailsSchema,
    addNewEmptyBrand,
    removeBrandAtIndex,
    validatePlatformDetails
  }
})
