<template>
  <div data-test-id="property-manager-business-address">
    <BcrosFormSection :title="t('createAccount.propertyManagerForm.businessMailingAddress')">
      <div class="flex flex-row justify-between w-full mb-[40px] mobile:mb-[16px]">
        <UFormGroup name="country" class="flex-grow">
          <USelect
            v-model="country"
            aria-label="country"
            :options="countryItems"
            option-attribute="name"
            class="w-full"
          />
        </UFormGroup>
      </div>
      <div class="flex flex-row justify-between w-full mb-[40px] mobile:mb-[16px]">
        <UFormGroup name="address" class="flex-grow">
          <UInput
            :id="id"
            v-model="address"
            aria-label="address"
            :placeholder="t('createAccount.propertyManagerForm.address')"
            @input="onAddressInput"
            @click="addressComplete()"
          />
        </UFormGroup>
      </div>
      <div class="flex flex-row justify-between w-full mb-[40px] mobile:mb-[16px]">
        <UFormGroup name="addressLineTwo" class="flex-grow">
          <UInput
            v-model="addressLineTwo"
            :placeholder="t('createAccount.propertyManagerForm.addressLineTwo')"
            aria-label="address line two"
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
            :placeholder="t('createAccount.propertyManagerForm.city')"
            aria-label="city"
          />
        </UFormGroup>
        <UFormGroup name="province" class="d:pr-[16px] flex-grow mobile:mb-[16px]">
          <USelect
            v-if="['CA', 'US'].includes(country)"
            v-model="province"
            :options="provinceItems"
            option-attribute="name"
            :placeholder="t('createAccount.propertyManagerForm.province')"
            aria-label="province"
          />
          <UInput
            v-else
            v-model="province"
            :placeholder="t('createAccount.propertyManagerForm.province')"
            aria-label="province"
          />
        </UFormGroup>
        <UFormGroup name="postalCode" class="flex-grow mobile:mb-[16px]">
          <UInput
            v-model="postalCode"
            :placeholder="t('createAccount.propertyManagerForm.postalCode')"
            aria-label="postal code"
          />
        </UFormGroup>
      </div>
    </BcrosFormSection>
    <div v-if="divider" class="h-[1px] w-full bg-bcGovGray-300 mobile:hidden" />
  </div>
</template>

<script setup lang="ts">
import { CountryItem, ProvinceItem } from '@/interfaces/address-i'
import countries from '@/utils/countries.json'
import provinces from '@/utils/provinces.json'
const { t } = useTranslation()

const country = defineModel<string>('country')
const address = defineModel<string>('address')
const addressLineTwo = defineModel<string>('addressLineTwo')
const city = defineModel<string>('city')
const province = defineModel<string>('province')
const postalCode = defineModel<string>('postalCode')
const countryItems = computed<CountryItem[]>(() =>
  countries.map(country => ({
    value: country.iso2,
    name: country.en
  }))
)
const provinceItems = computed<ProvinceItem[]>(() => {
  if (['CA', 'US'].includes(country.value)) {
    return provinces
      .filter(province => province.country === country.value)
      .map(province => ({
        value: province.code,
        name: province.en
      }))
  }
  return []
})

const addressComplete = () => {
  if (country.value === 'CA' || country.value === 'US') {
    enableAddressComplete(id, country.value, true)
  }
}

const onAddressInput = () => {
  address.value = ''
  province.value = ''
  city.value = ''
  postalCode.value = ''
  addressComplete()
}

defineEmits<{
    setId: [id: string]
}>()

const {
  id,
  defaultCountryIso2,
  enableAddressComplete,
  divider
} = defineProps<{
    id: string,
    defaultCountryIso2: string,
    enableAddressComplete:(id: string, countryIso2: string, countrySelect: boolean) => void,
    divider: boolean
  }>()

country.value = defaultCountryIso2
</script>
