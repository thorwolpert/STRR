<template>
  <div data-test-id="form-section-address">
    <BcrosFormSection :title="t('createAccount.propertyForm.rentalUnitAddress')">
      <div class="flex flex-row justify-between w-full mb-[40px] mobile:mb-[16px]">
        <UFormGroup name="nickname" class="d:pr-[16px] flex-grow" :help="t('createAccount.propertyForm.nicknameHelp')">
          <UInput v-model="nickname" aria-label="nickname" :placeholder="t('createAccount.propertyForm.nickname')" />
        </UFormGroup>
      </div>
      <div class="flex flex-row justify-between w-full mb-[40px] mobile:mb-[16px]">
        <UFormGroup name="country" class="d:pr-[16px] flex-grow">
          <USelect
            v-model="country"
            :options="countryItems"
            option-attribute="name"
            class="w-full"
            aria-label="country"
          />
        </UFormGroup>
      </div>
      <div class="flex flex-row justify-between w-full mb-[40px] mobile:mb-[16px]">
        <UFormGroup
          name="streetNumber"
          class="d:pr-[16px] flex-grow"
        >
          <UInput
            :id="streetNumberId"
            v-model="streetNumber"
            :aria-label="t('createAccount.contactForm.streetNumber')"
            :placeholder="t('createAccount.contactForm.streetNumber')"
            @keypress.once="addressComplete(false)"
            @click="addressComplete(false)"
          />
        </UFormGroup>
        <UFormGroup
          name="streetName"
          class="d:pr-[16px] flex-grow"
        >
          <UInput
            :id="streetNameId"
            v-model="streetName"
            :aria-label="t('createAccount.contactForm.streetName')"
            :placeholder="t('createAccount.contactForm.streetName')"
            @keypress.once="addressComplete(true)"
            @click="addressComplete(true)"
          />
        </UFormGroup>
        <UFormGroup
          name="unitNumber"
          class="d:pr-[16px] flex-grow"
        >
          <UInput
            v-model="unitNumber"
            :aria-label="t('createAccount.contactForm.unitNumberRequired')"
            :placeholder="unitNumberPlaceholder"
          />
        </UFormGroup>
      </div>
      <div class="flex flex-row justify-between w-full mb-[40px] mobile:mb-[16px]">
        <UFormGroup name="AddressLineTwo" class="d:pr-[16px] flex-grow">
          <UInput
            v-model="addressLineTwo"
            aria-label="address line two"
            :placeholder="t('createAccount.contactForm.addressLineTwo')"
            data-test-id="address-line-two-input"
          />
        </UFormGroup>
      </div>
      <div class="flex flex-row justify-between w-full mb-[40px] mobile:flex-col mobile:mb-[16px]">
        <UFormGroup
          name="city"
          class="d:pr-[16px] flex-grow mobile:mb-[16px]"
        >
          <UInput
            v-model="city"
            aria-label="city"
            :placeholder="t('createAccount.contactForm.city')"
            data-test-id="address-city-input"
          />
        </UFormGroup>
        <UFormGroup
          name="province"
          class="d:pr-[16px] flex-grow mobile:mb-[16px]"
          :error="addressInBC ? '' : 'Address must be in BC'"
        >
          <UInput
            v-model="province"
            aria-label="province"
            :placeholder="t('createAccount.contactForm.province')"
            disabled
          />
        </UFormGroup>
        <UFormGroup name="postalCode" class="d:pr-[16px] flex-grow mobile:mb-[16px]">
          <UInput
            ref="inputRef"
            v-model="postalCode"
            aria-label="postal code"
            :placeholder="t('createAccount.contactForm.postalCode')"
            data-test-id="address-postal-code-input"
          />
        </UFormGroup>
      </div>
    </BcrosFormSection>
  </div>
</template>

<script setup lang="ts">
import type { UInput } from '#build/components'
import { CountryItem } from '@/interfaces/address-i'
import { PropertyTypeE } from '@/enums/property-type-e'
import countries from '@/utils/countries.json'
const { t } = useTranslation()
const unitNumberPlaceholder = ref('')

const country = defineModel<string>('country')
const streetNumber = defineModel<string>('streetNumber')
const streetName = defineModel<string>('streetName')
const unitNumber = defineModel<string>('unitNumber')
const addressLineTwo = defineModel<string>('addressLineTwo')
const city = defineModel<string>('city')
const province = defineModel<string>('province')
const postalCode = defineModel<string>('postalCode')
const nickname = defineModel<string>('nickname')
const countryItems = ref<CountryItem[]>([])

const addressComplete = (initiatedFromStreetName: boolean) => {
  if (typeof country.value === 'string') {
    if (initiatedFromStreetName) {
      enableAddressComplete(streetNameId, 'CA', false)
    } else {
      enableAddressComplete(streetNumberId, 'CA', false)
    }
  }
}

const {
  streetNumberId,
  streetNameId,
  defaultCountryIso2,
  enableAddressComplete,
  addressInBC
} = defineProps<{
  streetNumberId: string,
  streetNameId: string,
  defaultCountryIso2: string,
  enableAddressComplete:(id: string, countryIso2: string, countrySelect: boolean) => void,
  addressInBC?: boolean
}>()

// const emit = defineEmits([
//   'autoCompleteSelected'
// ])

// const onAddressInput = () => {
//   addressComplete()
//   // reset errors for the fields by calling input event on them
//   emit('autoCompleteSelected')
// }

country.value = defaultCountryIso2

const getUnitNumberPlaceholder = (propertyType?: string) => {
  if (!propertyType) {
    return t('createAccount.contactForm.unitNumberOptional')
  }
  switch (propertyType) {
    case PropertyTypeE.SECONDARY_SUITE:
    case PropertyTypeE.ACCESSORY_DWELLING:
    case PropertyTypeE.TOWN_HOME:
    case PropertyTypeE.MULTI_UNIT_HOUSING:
    case PropertyTypeE.CONDO_OR_APT:
    case PropertyTypeE.STRATA_HOTEL:
      return t('createAccount.contactForm.unitNumberRequired')
    default:
      return t('createAccount.contactForm.unitNumberOptional')
  }
}

unitNumberPlaceholder.value = getUnitNumberPlaceholder(formState.propertyDetails.propertyType)

watch(() => formState.propertyDetails.propertyType, (newType) => {
  unitNumberPlaceholder.value = getUnitNumberPlaceholder(newType)
})

// Rental addresses for registration can only be in Canada
onMounted(() => {
  countryItems.value = countries
    .filter(country => country.iso2 === 'CA')
    .map(country => ({
      value: country.iso2,
      name: country.en
    }))
})

</script>
