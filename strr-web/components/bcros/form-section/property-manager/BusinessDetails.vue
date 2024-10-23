<template>
  <div data-test-id="form-business-details-info">
    <BcrosFormSection :title="t('createAccount.propertyManagerForm.businessDetails')">
      <div class="flex flex-row justify-between w-full mb-[40px] mobile:flex-col mobile:mb-[16px]">
        <UFormGroup name="businessName" class="flex-grow">
          <UInput
            v-model="businessName"
            type="text"
            aria-label="property manager business legal name"
            :placeholder="t('createAccount.propertyManagerForm.businessName')"
          />
        </UFormGroup>
      </div>
      <div class="flex flex-row justify-between w-full mb-[40px] mobile:flex-col mobile:mb-[16px]">
        <UFormGroup name="craBusinessNumber" class="flex-grow">
          <UInput
            v-model="craBusinessNumber"
            type="text"
            aria-label="property manager cra business number"
            :placeholder="t('createAccount.propertyManagerForm.businessNumber')"
          />
        </UFormGroup>
      </div>
    </BcrosFormSection>
    <div v-if="divider" class="h-[1px] w-full bg-bcGovGray-300 mobile:hidden" />
  </div>
</template>

<script setup lang="ts">
const { t } = useTranslation()
const { divider } = defineProps<{ divider: boolean }>()

const businessName = defineModel<string>('businessName')
const craBusinessNumber = defineModel<string>('craBusinessNumber')

</script>
