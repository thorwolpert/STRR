import { z } from 'zod'
import { getRequiredNonEmptyString } from '~/utils/connect-validation'

export const useStrrPlatformDetails = defineStore('strr/platformDetails', () => {
  const { t } = useI18n()
  const platformDetailsSchema = z.object({
    brands: z.array(z.object({
      name: getRequiredNonEmptyString(t('validation.brand.name')),
      website: getRequiredNonEmptyString(t('validation.brand.site'))
    })).min(1),
    listingSize: getRequiredNonEmptyString(t('validation.listingSize'))
  })
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
  return {
    platformDetails,
    platformDetailsSchema,
    addNewEmptyBrand,
    removeBrandAtIndex
  }
})
