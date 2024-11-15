<template>
  <div data-test-id="form-section-contact-name">
    <BcrosFormSection :title="t('common.formLabels.contactName')">
      <p v-if="contactInfoDescription" class="mb-10 text-sm text-bcGovColor-darkGray">
        {{ contactInfoDescription }}
      </p>
      <div class="flex flex-row justify-between w-full mb-10 m:flex-col m:mb-4">
        <UFormGroup name="firstName" class="d:pr-4 flex-grow m:mb-4">
          <UInput
            v-model="firstName"
            :placeholder="t('createAccount.contactForm.firstName')"
            data-test-id="contact-first-name-input"
          />
        </UFormGroup>
        <UFormGroup name="middleName" class="d:pr-4 flex-grow m:mb-4">
          <UInput
            v-model="middleName"
            :placeholder="t('createAccount.contactForm.middleName')"
            data-test-id="contact-middle-name-input"
          />
        </UFormGroup>
        <UFormGroup name="lastName" class="flex-grow m:mb-4">
          <UInput
            v-model="lastName"
            :placeholder="t('createAccount.contactForm.lastName')"
            data-test-id="contact-last-name-input"
          />
        </UFormGroup>
      </div>
      <div class="flex flex-row justify-between w-full mb-10 m:mb-4">
        <UFormGroup name="preferredName" class=" flex-grow">
          <UInput
            v-model="preferredName"
            type="name"
            :placeholder="t('createAccount.contactForm.preferredName')"
            data-test-id="property-manager-preferred-name-input"
          />
        </UFormGroup>
      </div>
    </BcrosFormSection>
  </div>
</template>

<script setup lang="ts">
const { t } = useTranslation()

const preferredName = defineModel<string>('preferredName')
const firstName = defineModel<string>('firstName')
const middleName = defineModel<string>('middleName')
const lastName = defineModel<string>('lastName')

defineProps<{
  contactInfoDescription?: string
}>()

</script>
