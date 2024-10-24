<script setup lang="ts">
const { t } = useTranslation()
const tReviewPM = (translationKey: string) => t(`createAccount.review.propertyManager.${translationKey}`)
const { propertyManager } = defineProps<{ propertyManager: PropertyManagerI }>()
const propertyManagerContact = computed((): PropertyManagerContactI => propertyManager.contact)
</script>

<template>
  <div>
    <p class="font-bold mb-[24px] mobile:mx-[8px]">
      {{ tReviewPM('title') }}
    </p>
    <div
      class="bg-white p-8 mobile:px-[8px] d:min-h-[250px]
            grid d:grid-cols-3 d:grid-rows-3 d:grid-flow-col"
    >
      <BcrosFormSectionReviewItem
        :title="tReviewPM('businessLegalName')"
        :content="propertyManager.businessLegalName || '-'"
      />
      <BcrosFormSectionReviewItem
        :title="tReviewPM('craBusinessNumber')"
        :content="propertyManager.craBusinessNumber || '-'"
      />
      <BcrosFormSectionReviewItem
        :title="tReviewPM('businessMailingAddress')"
      >
        <!-- eslint-disable-next-line vue/no-v-html -->
        <p v-html="displayFullAddress(propertyManager.businessMailingAddress) || '-'" />
      </BcrosFormSectionReviewItem>
      <BcrosFormSectionReviewItem
        :title="tReviewPM('contactName')"
        :content="displayContactFullName(propertyManagerContact) || '-'"
      />
      <div class="grid grid-rows-subgrid row-span-2">
        <BcrosFormSectionReviewItem
          :title="tReviewPM('preferredName')"
          :content="propertyManagerContact.preferredName || '-'"
        />
      </div>
      <BcrosFormSectionReviewItem
        :title="tReviewPM('phoneNumber')"
        :content="displayPhoneAndExt(
          propertyManagerContact.phoneNumber, propertyManagerContact.extension
        ) || '-'
        "
      />
      <BcrosFormSectionReviewItem
        :title="tReviewPM('faxNumber')"
        :content="propertyManagerContact.faxNumber || '-'"
      />
      <BcrosFormSectionReviewItem
        :title="tReviewPM('emailAddress')"
        :content="propertyManagerContact.emailAddress || '-'"
      />
    </div>
  </div>
</template>

<style scoped>
</style>
