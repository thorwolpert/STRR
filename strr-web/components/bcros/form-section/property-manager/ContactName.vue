<template>
  <div data-test-id="property-manager-contact-name">
    <BcrosFormSection :title="t('createAccount.propertyManagerForm.contactName')">
      <div class="flex flex-row justify-between w-full mb-[40px] mobile:flex-col mobile:mb-[16px]">
        <UFormGroup name="firstName" class="d:pr-[16px] flex-grow mobile:mb-[16px]">
          <UInput
            v-model="firstName"
            :placeholder="t('createAccount.propertyManagerForm.firstName')"
            aria-label="firstName"
          />
        </UFormGroup>
        <UFormGroup name="middleName" class="d:pr-[16px] flex-grow mobile:mb-[16px]">
          <UInput
            v-model="middleName"
            :placeholder="t('createAccount.propertyManagerForm.middleName')"
            aria-label="middleName"
          />
        </UFormGroup>
        <UFormGroup name="lastName" class="flex-grow mobile:mb-[16px]">
          <UInput
            v-model="lastName"
            :placeholder="t('createAccount.propertyManagerForm.lastName')"
            aria-label="last name"
          />
        </UFormGroup>
      </div>
      <div class="flex flex-row justify-between w-full mb-[40px] mobile:mb-[16px]">
        <UFormGroup name="preferredName" class=" flex-grow">
          <UInput
            v-model="preferredName"
            type="name"
            aria-label="preferred name"
            :placeholder="t('createAccount.propertyManagerForm.preferredName')"
          />
        </UFormGroup>
      </div>
    </BcrosFormSection>
    <div v-if="divider" class="h-[1px] bg-bcGovGray-300 mobile:hidden" />
  </div>
</template>

<script setup lang="ts">
const { t } = useTranslation()

const { divider } = defineProps<{
    divider: boolean
}>()

const preferredName = defineModel<string>('preferredName')
const firstName = defineModel<string>('firstName')
const middleName = defineModel<string>('middleName')
const lastName = defineModel<string>('lastName')
</script>
