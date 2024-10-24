<template>
  <div data-test-id="property-manager-contact-details">
    <BcrosFormSection :title="t('createAccount.propertyManagerForm.contactDetails')">
      <div class="flex flex-row justify-between w-full mb-[40px] mobile:flex-col mobile:mb-[16px]">
        <UFormGroup
          name="phoneNumber"
          class="desktop:d:pr-[16px] flex-grow mobile:mb-[16px]"
        >
          <UInput
            v-model="phoneNumber"
            type="tel"
            aria-label="phone number"
            :placeholder="t('createAccount.propertyManagerForm.phoneNumber')"
          />
        </UFormGroup>
        <UFormGroup name="extension" class="flex-grow">
          <UInput
            v-model="extension"
            :placeholder="t('createAccount.propertyManagerForm.extension')"
            aria-label="extension"
          />
        </UFormGroup>
      </div>
      <div class="flex flex-row justify-between w-full mb-[40px] mobile:mb-[16px]">
        <UFormGroup name="faxNumber" class="flex-grow">
          <UInput
            v-model="faxNumber"
            :placeholder="t('createAccount.propertyManagerForm.faxNumber')"
            aria-label="fax number"
          />
        </UFormGroup>
      </div>
      <div class="flex flex-row justify-between w-full mb-[40px] mobile:mb-[16px]">
        <UFormGroup
          type="email"
          name="emailAddress"
          class="flex-grow"
        >
          <UInput
            v-model="emailAddress"
            :placeholder="t('createAccount.propertyManagerForm.emailAddress')"
            aria-label="email address"
          />
        </UFormGroup>
      </div>
      <div class="mb-[40px] mobile:flex-col mobile:mb-[16px]">
        <BcrosAlertsMessage :flavour="AlertsFlavourE.INFO">
          <p>
            <b>{{ t('createAccount.propertyManagerForm.boldWarning') }}</b>
            {{ t('createAccount.propertyManagerForm.warning') }}
          </p>
        </BcrosAlertsMessage>
      </div>
    </BcrosFormSection>
    <div v-if="divider" class="h-[1px] w-full bg-bcGovGray-300 mobile:hidden" />
  </div>
</template>

<script setup lang="ts">
const { t } = useTranslation()

const { divider } = defineProps<{
  divider: boolean
}>()

const phoneNumber = defineModel<string>('phoneNumber')
const extension = defineModel<string>('extension')
const faxNumber = defineModel<string>('faxNumber')
const emailAddress = defineModel<string>('emailAddress')
</script>
