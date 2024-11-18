<template>
  <div data-test-id="form-section-contact-details">
    <BcrosFormSection :title="t('createAccount.contactForm.contactDetails')">
      <div class="flex flex-row justify-between w-full mb-10 m:flex-col m:mb-4">
        <UFormGroup name="phoneNumber" class="d:pr-4 flex-grow m:mb-4">
          <UInput
            v-model="phoneNumber"
            :placeholder="t('createAccount.contactForm.phoneNumber')"
            data-test-id="phone-number"
          />
        </UFormGroup>
        <UFormGroup name="extension" class="flex-grow">
          <UInput
            v-model="extension"
            :placeholder="t('createAccount.contactForm.extension')"
            data-test-id="extension"
          />
        </UFormGroup>
      </div>
      <div class="flex flex-row justify-between w-full mb-10 m:mb-4">
        <UFormGroup name="faxNumber" class="flex-grow">
          <UInput
            v-model="faxNumber"
            type="tel"
            :placeholder="t('createAccount.contactForm.faxNumber')"
            data-test-id="fax-number"
          />
        </UFormGroup>
      </div>
      <div class="flex flex-row justify-between w-full mb-10 m:mb-4">
        <UFormGroup name="emailAddress" type="email" class="flex-grow">
          <UInput
            v-model="emailAddress"
            :placeholder="t('createAccount.contactForm.emailAddress')"
            data-test-id="email-address"
          />
        </UFormGroup>
      </div>
      <div class="mb-10 m:flex-col m:mb-4">
        <BcrosAlertsMessage :flavour="AlertsFlavourE.INFO">
          <p>
            <b>{{ t('createAccount.contactForm.boldWarning') }}</b>
            {{ t('createAccount.contactForm.warning') }}
          </p>
        </BcrosAlertsMessage>
      </div>
    </BcrosFormSection>
  </div>
</template>

<script setup lang="ts">
const { t } = useTranslation()

const phoneNumber = defineModel<string>('phoneNumber')
const extension = defineModel<string>('extension')
const faxNumber = defineModel<string>('faxNumber')
const emailAddress = defineModel<string>('emailAddress')
</script>
