<template>
  <div data-test-id="form-section-business-details">
    <BcrosFormSection :title="t('common.formLabels.businessDetails')">
      <div class="flex flex-row justify-between w-full mb-10 m:flex-col m:mb-4">
        <UFormGroup name="businessLegalName" class="flex-grow">
          <UInput
            v-model="businessName"
            type="text"
            :placeholder="isBusinessNameRequired
              ? t('common.formLabels.businessLegalName')
              : t('common.formLabels.businessLegalNameOptional')"
            data-test-id="business-legal-name-input"
          />
        </UFormGroup>
      </div>
      <div class="flex flex-row justify-between w-full mb-10 m:flex-col m:mb-4">
        <UFormGroup name="businessNumber" class="flex-grow">
          <UInput
            v-model="businessNumber"
            type="text"
            :placeholder="t('common.formLabels.craBusinessNumberOptional')"
            data-test-id="cra-business-number-input"
          />
        </UFormGroup>
      </div>
    </BcrosFormSection>
  </div>
</template>

<script setup lang="ts">
const { t } = useTranslation()

const businessName = defineModel<string>('businessName')
const businessNumber = defineModel<string>('businessNumber')

defineProps<{
  isBusinessNameRequired?: boolean,
}>()
</script>
