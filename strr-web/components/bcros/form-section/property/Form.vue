<template>
  <div data-test-id="property-form-section" class="relative h-full">
    <div class="desktop:mb-[180px] mobile:mb-[32px] bg-white rounded-[4px]">
      <div class="bg-bcGovColor-gray2 rounded-t-[4px]">
        <p class="px-[40px] py-[15px] font-bold">
          {{ t('createAccount.propertyForm.subtitle') }}
        </p>
      </div>
      <UForm ref="propertyDetailsForm" :schema="propertyDetailsSchema" :state="formState.propertyDetails">
        <BcrosFormSectionPropertyDetails
          v-model:property-type="formState.propertyDetails.propertyType"
          v-model:ownership-type="formState.propertyDetails.ownershipType"
          v-model:business-license="formState.propertyDetails.businessLicense"
          v-model:parcel-identifier="formState.propertyDetails.parcelIdentifier"
          v-model:business-license-expiry-date="formState.propertyDetails.businessLicenseExpiryDate"
          v-model:rental-unit-space-type="formState.propertyDetails.rentalUnitSpaceType"
          v-model:is-unit-on-principal-residence-property="formState.propertyDetails.isUnitOnPrincipalResidenceProperty"
          v-model:host-residence="formState.propertyDetails.hostResidence"
          v-model:number-of-rooms-for-rent="formState.propertyDetails.numberOfRoomsForRent"
          :host-residence-error="hostResidenceError"
          :number-of-rooms-for-rent-error="numberOfRoomsForRentError"
          @validate-host-residence="validateHostResidence"
          @validate-number-of-rooms-for-rent="validateNumberOfRoomsForRent"
        />
        <BcrosFormSectionPropertyAddress
          v-model:nickname="formState.propertyDetails.nickname"
          v-model:country="formState.propertyDetails.country"
          v-model:street-number="formState.propertyDetails.streetNumber"
          v-model:street-name="formState.propertyDetails.streetName"
          v-model:unit-number="formState.propertyDetails.unitNumber"
          v-model:address-line-two="formState.propertyDetails.addressLineTwo"
          v-model:city="formState.propertyDetails.city"
          v-model:province="formState.propertyDetails.province"
          v-model:postal-code="formState.propertyDetails.postalCode"
          street-number-id="propertyAddressStreetNumber"
          street-name-id="propertyAddressStreetName"
          :enable-address-complete="enableAddressComplete"
          default-country-iso2="CA"
          :address-in-b-c="isAddressInBC"
        />
        <BcrosFormSectionPropertyListingDetails
          v-model:listing-details="formState.propertyDetails.listingDetails"
          :add-platform="addPlatform"
          :remove-detail-at-index="removeDetailAtIndex"
          :invalid-urls="listingURLErrors"
          @validate-field="(index: number) => validateField(index)"
        />
      </UForm>
    </div>
  </div>
</template>

<script setup lang="ts">
import { sanitizeUrl } from '@braintree/sanitize-url'

const { isComplete } = defineProps<{
  isComplete: boolean
}>()

const {
  activeAddressField,
  addressWithStreetAttributes: canadaPostAddress,
  enableAddressComplete
} = useCanadaPostAddress(true)

const isValid = ref(false)
const propertyDetailsForm = ref()
const isAddressInBC = ref(true)
const hostResidenceError = ref('')
const numberOfRoomsForRentError = ref('')

const { t } = useTranslation()

const listingURLErrors = ref<(({
    errorIndex: string | number;
    message: string;
} | undefined)[] | undefined)>([])

const addPlatform = () => {
  formState.propertyDetails.listingDetails.push({ url: '' })
}

const removeDetailAtIndex = (index: number) => {
  formState.propertyDetails.listingDetails.splice(index, 1)
}

const validateField = (index: number) => {
  const listingDetailsErrorsExist = propertyDetailsSchema.safeParse(formState.propertyDetails).error?.errors
    .find(error => error.path[0] === 'listingDetails')
  const currentUrl = formState.propertyDetails.listingDetails[index]?.url

  if (currentUrl) {
    const sanitizedUrl = sanitizeUrl(currentUrl)
    if (sanitizedUrl === 'about:blank' || sanitizedUrl === 'javascript:void(0)') {
      listingURLErrors.value = listingURLErrors.value || []
      listingURLErrors.value[index] = {
        errorIndex: index,
        message: 'Invalid URL format'
      }
      return
    }
    formState.propertyDetails.listingDetails[index].url = sanitizedUrl
  }

  if (listingDetailsErrorsExist) {
    const invalidUrl = propertyDetailsSchema.safeParse(formState.propertyDetails).error?.errors
      .filter(error => error.path[0] === 'listingDetails' && error.path[1].toString() === index.toString())
      .map((error) => {
        return {
          errorIndex: error.path[1],
          message: error.message
        }
      })
    // if validation isn't passed
    if (invalidUrl) {
      listingURLErrors.value?.length
        // if other errors exist add this one
        ? listingURLErrors.value.push(invalidUrl[0])
        // if no other errors this becomes the error object
        : listingURLErrors.value = invalidUrl
    } else if (listingURLErrors.value?.length === 0) {
      // if no other errors and URL is valid replace value with undefined
      listingURLErrors.value = undefined
    } else {
      const removalIndex = listingURLErrors.value?.findIndex(nonerror => nonerror?.errorIndex === index)
      if (removalIndex !== -1) {
        listingURLErrors.value?.splice(removalIndex, 1)
      }
    }
  } else {
    listingURLErrors.value = undefined
  }
}

const validateAllPropertyListingUrls = () => {
  if (propertyDetailsSchema.safeParse(formState.propertyDetails).error) {
    const invalidUrls = propertyDetailsSchema.safeParse(formState.propertyDetails).error?.errors
      .filter(error => error.path[0] === 'listingDetails')
      .map((error) => {
        return {
          errorIndex: error.path[1],
          message: error.message
        }
      })
    listingURLErrors.value = invalidUrls
  }
}

const validateHostResidence = () => {
  hostResidenceError.value =
    (formState.propertyDetails.isUnitOnPrincipalResidenceProperty && !formState.propertyDetails.hostResidence)
      ? t('createAccount.propertyForm.hostResidenceRequiredError')
      : ''
}

const validateNumberOfRoomsForRent = () => {
  let value = formState.propertyDetails?.numberOfRoomsForRent

  if (!Number.isInteger(Number(value))) {
    value = Math.floor(Number(value))
    formState.propertyDetails.numberOfRoomsForRent = value
  }

  if (value < 1) {
    numberOfRoomsForRentError.value = t('createAccount.propertyForm.numberOfRoomsForRentRequired')
  } else if (value > 5000) {
    numberOfRoomsForRentError.value = t('createAccount.propertyForm.numberOfRoomsForRentMaxExceeded')
  } else {
    numberOfRoomsForRentError.value = ''
  }
}

const getActiveAddressState = (): PropertyDetailsI | null => {
  if (activeAddressField.value === 'propertyAddressStreetNumber' ||
      activeAddressField.value === 'propertyAddressStreetName') {
    return formState.propertyDetails
  }
  return null
}

watch(() => formState.propertyDetails.isUnitOnPrincipalResidenceProperty, (newValue) => {
  if (!newValue) {
    formState.propertyDetails.hostResidence = undefined // Reset if not required
  }
  validateHostResidence() // Ensure validation reflects changes
})

watch(formState.propertyDetails, () => {
  isValid.value = propertyDetailsSchema.safeParse(formState.propertyDetails).success
})

watch(
  () => formState.propertyDetails.isUnitOnPrincipalResidenceProperty,
  (newValue) => {
    // Coerce string "true"/"false" to boolean true/false
    if (newValue === 'true') {
      formState.propertyDetails.isUnitOnPrincipalResidenceProperty = true
    } else if (newValue === 'false') {
      formState.propertyDetails.isUnitOnPrincipalResidenceProperty = false
    }
  }
)

watch(canadaPostAddress, (newAddress) => {
  const activeAddressState = getActiveAddressState()
  if (newAddress && activeAddressState) {
    if (newAddress.province === 'BC') {
      isAddressInBC.value = true
      activeAddressState.streetNumber = newAddress.streetNumber
      activeAddressState.streetName = newAddress.streetName
      activeAddressState.addressLineTwo = newAddress.addressLineTwo
      activeAddressState.country = newAddress.country
      activeAddressState.city = newAddress.city
      activeAddressState.province = newAddress.province
      activeAddressState.postalCode = newAddress.postalCode
    } else {
      isAddressInBC.value = false
    }
    // clear errors when address autocomplete was used
    propertyDetailsForm.value.clear('streetNumber')
    propertyDetailsForm.value.clear('streetName')
    propertyDetailsForm.value.clear('addressLineTwo')
    propertyDetailsForm.value.clear('unitNumber')
    propertyDetailsForm.value.clear('city')
    propertyDetailsForm.value.clear('province')
    propertyDetailsForm.value.clear('postalCode')
  }
})

onMounted(async () => {
  if (isComplete) {
    await propertyDetailsForm.value.validate(null, { silent: true })
    validateAllPropertyListingUrls()
    validateHostResidence()
    validateNumberOfRoomsForRent()
  }
})
</script>
