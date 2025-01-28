<template>
  <div class="relative h-full">
    <div class="d:mb-[180px] m:mb-8 rounded-[4px]">
      <div class="mb-8">
        <div class="mb-6">
          <URadioGroup
            id="role-property-manager-radio"
            v-model="formState.isPropertyManagerRole"
            data-test-id="property-manager-is-pm"
            :legend="tPropertyManager('roleRadioLegend')"
            :options="roleRadioOptions"
            class="[&_legend]:font-bold [&_legend]:text-lg"
          />
        </div>
        <div>
          <URadioGroup
            v-if="!formState.isPropertyManagerRole"
            id="has-property-manager-radio"
            v-model="formState.hasPropertyManager"
            data-test-id="property-manager-has-pm"
            :legend="tPropertyManager('propertyManagerRadioLegend')"
            :options="havePropertyManagerRadioOptions"
            class="[&_legend]:font-bold [&_legend]:text-lg"
          />
        </div>
      </div>
      <div
        v-if="
          (!formState.isPropertyManagerRole && formState.hasPropertyManager) || formState.isPropertyManagerRole
        "
        data-test-id="property-manager-form"
      >
        <div class="d:pr-5 mb-132px bg-white rounded-1">
          <div class="bg-bcGovColor-gray2 d:-mr-5">
            <p class="px-10 py-[15px] font-bold">
              {{ t('createAccount.propertyManager.primary') }}
            </p>
          </div>
          <UForm
            ref="propertyManagerForm"
            :schema="propertyManagerSchema"
            :state="flatFormState"
          >
            <BcrosFormSectionBusinessDetails
              v-model:business-name="formState.propertyManager.businessLegalName"
              v-model:business-number="formState.propertyManager.businessNumber"
            />
            <div class="m:hidden h-[1px] ml-10 mr-5 bg-bcGovGray-300" />
            <BcrosFormSectionPropertyManagerBusinessMailingAddress
              id="propertyManagerBusinessAddress"
              v-model:country="formState.propertyManager.businessMailingAddress.country"
              v-model:address="formState.propertyManager.businessMailingAddress.address"
              v-model:address-line-two="formState.propertyManager.businessMailingAddress.addressLineTwo"
              v-model:city="formState.propertyManager.businessMailingAddress.city"
              v-model:province="formState.propertyManager.businessMailingAddress.province"
              v-model:postal-code="formState.propertyManager.businessMailingAddress.postalCode"
              :enable-address-complete="enableAddressComplete"
              default-country-iso2="CA"
            />
            <div class="m:hidden h-[1px] ml-10 mr-5 bg-bcGovGray-300" />
            <BcrosFormSectionContactName
              v-model:preferred-name="formState.propertyManager.contact.preferredName"
              v-model:first-name="formState.propertyManager.contact.firstName"
              v-model:last-name="formState.propertyManager.contact.lastName"
              v-model:middle-name="formState.propertyManager.contact.middleName"
            />
            <div class="m:hidden h-[1px] ml-10 mr-5 bg-bcGovGray-300" />
            <BcrosFormSectionContactDetails
              v-model:phone-number="formState.propertyManager.contact.phoneNumber"
              v-model:extension="formState.propertyManager.contact.extension"
              v-model:fax-number="formState.propertyManager.contact.faxNumber"
              v-model:email-address="formState.propertyManager.contact.emailAddress"
            />
          </UForm>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { t } = useTranslation()
const tPropertyManager = (translationKey: string) => t(`createAccount.propertyManager.${translationKey}`)

const { isComplete } = defineProps<{ isComplete: boolean }>()

const roleRadioOptions = [{
  value: false,
  label: tPropertyManager('propertyHostRoleOption')
}, {
  value: true,
  label: tPropertyManager('propertyManagerRoleOption')
}]

const havePropertyManagerRadioOptions = [{
  value: true,
  label: tPropertyManager('yesOption')
}, {
  value: false,
  label: tPropertyManager('noOption')
}]

const {
  activeAddressField,
  address: canadaPostAddress,
  enableAddressComplete
} = useCanadaPostAddress()

const getActiveAddressState = (): PropertyManagerBusinessAddressI | null => {
  if (activeAddressField.value === 'propertyManagerBusinessAddress') {
    return formState.propertyManager.businessMailingAddress
  }
  return null
}

watch(canadaPostAddress, (newAddress) => {
  const activeAddressState = getActiveAddressState()

  if (newAddress && activeAddressState) {
    activeAddressState.address = newAddress.address
    activeAddressState.addressLineTwo = newAddress.addressLineTwo
    activeAddressState.country = newAddress.country
    activeAddressState.city = newAddress.city
    activeAddressState.province = newAddress.province
    activeAddressState.postalCode = newAddress.postalCode

    // clear errors when address autocomplete was used
    propertyManagerForm.value.clear('address')
    propertyManagerForm.value.clear('addressLineTwo')
    propertyManagerForm.value.clear('city')
    propertyManagerForm.value.clear('province')
    propertyManagerForm.value.clear('postalCode')
  }
})

const propertyManagerForm = ref()

// create a flat form state for validation
const flatFormState = computed(() => ({
  businessLegalName: formState.propertyManager.businessLegalName,
  businessNumber: formState.propertyManager.businessNumber,
  address: formState.propertyManager.businessMailingAddress.address,
  addressLineTwo: formState.propertyManager.businessMailingAddress.addressLineTwo,
  city: formState.propertyManager.businessMailingAddress.city,
  postalCode: formState.propertyManager.businessMailingAddress.postalCode,
  province: formState.propertyManager.businessMailingAddress.province,
  country: formState.propertyManager.businessMailingAddress.country,
  firstName: formState.propertyManager.contact.firstName,
  middleName: formState.propertyManager.contact.middleName,
  lastName: formState.propertyManager.contact.lastName,
  preferredName: formState.propertyManager.contact.preferredName,
  phoneNumber: formState.propertyManager.contact.phoneNumber,
  extension: formState.propertyManager.contact.extension,
  faxNumber: formState.propertyManager.contact.faxNumber,
  emailAddress: formState.propertyManager.contact.emailAddress
}))

watch([() => formState.isPropertyManagerRole, () => formState.hasPropertyManager], () => {
  if (!formState.isPropertyManagerRole && !formState.hasPropertyManager) {
    formState.propertyManager = {
      businessLegalName: '',
      businessNumber: '',
      businessMailingAddress: {
        address: '',
        addressLineTwo: '',
        city: '',
        postalCode: '',
        province: '',
        country: ''
      },
      contact: {
        firstName: '',
        middleName: '',
        lastName: '',
        preferredName: '',
        phoneNumber: '',
        extension: '',
        faxNumber: '',
        emailAddress: ''
      },
      initiatedByPropertyManager: undefined
    }
  }
  // reset Host Authorization flag if role is not Property manager
  if (!formState.isPropertyManagerRole) {
    formState.hasHostAuthorization = false
  }
})

onMounted(async () => {
  if (isComplete) {
    await propertyManagerForm.value.validate(null, { silent: true })
  }
})
</script>
