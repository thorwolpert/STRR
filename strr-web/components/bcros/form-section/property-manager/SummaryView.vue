<script setup lang="ts">
import type { PropertyManagerContactI, PropertyManagerIndividualContactI } from '~/interfaces/property-manager-i'

const { t } = useTranslation()
const tReviewPM = (translationKey: string) => t(`createAccount.review.propertyManager.${translationKey}`)
const props = defineProps<{
  headerTag?: string,
  headerClass?: string,
  propertyManager: PropertyManagerI
}>()

// default values
const {
  headerTag = 'p',
  headerClass = 'font-bold mb-6 m:mx-2'
} = props

const isPMBusiness = computed(
  () => props.propertyManager.propertyManagerType === HostContactTypeE.BUSINESS)

const propertyManagerBus =
  computed((): PropertyManagerContactI | undefined => props.propertyManager.business?.primaryContact)
const propertyManagerInd =
  computed((): PropertyManagerIndividualContactI | undefined => props.propertyManager.contact)

const displayPropertyManagerType = {
  [HostContactTypeE.INDIVIDUAL]: t('createAccount.contactForm.hostTypeIndividual'),
  [HostContactTypeE.BUSINESS]: t('createAccount.contactForm.hostTypeBusiness')
}

const propertyManagerContact: PropertyManagerContactI | PropertyManagerIndividualContactI =
   isPMBusiness.value ? propertyManagerBus.value : propertyManagerInd.value

</script>

<template>
  <div>
    <component :is="headerTag" :class="headerClass">
      {{ tReviewPM('header') }}
    </component>
    <div
      class="bg-white p-8 m:px-2 d:min-h-[250px] grid d:grid-cols-3 d:grid-rows-3 d:grid-flow-col gap-y-3"
    >
      <BcrosFormSectionReviewItem
        :title="tReviewPM('propertyManagerType')"
        :content="displayPropertyManagerType[propertyManager.propertyManagerType]"
      />
      <BcrosFormSectionReviewItem
        :title="tReviewPM('contactName')"
        :content="displayContactFullName(isPMBusiness ? propertyManagerBus : propertyManagerInd) || '-'"
      />
      <BcrosFormSectionReviewItem
        v-if="isPMBusiness"
        :title="tReviewPM('businessMailingAddress')"
      >
        <!-- eslint-disable-next-line vue/no-v-html -->
        <p v-html="displayFullAddress(propertyManager.business?.mailingAddress) || '-'" />
      </BcrosFormSectionReviewItem>
      <BcrosFormSectionReviewItem
        v-else
        :title="tReviewPM('mailingAddress')"
      >
        <!-- eslint-disable-next-line vue/no-v-html -->
        <p v-html="displayFullAddress(propertyManager.contact?.mailingAddress) || '-'" />
      </BcrosFormSectionReviewItem>
      <div
        v-if="!isPMBusiness"
      >
        <BcrosFormSectionReviewItem
          :title="tReviewPM('preferredName')"
          :content="propertyManagerContact?.preferredName || '-'"
        />
      </div>
      <BcrosFormSectionReviewItem
        v-if="isPMBusiness"
        :title="tReviewPM('businessLegalName')"
        :content="propertyManager.business?.legalName || '-'"
      />
      <BcrosFormSectionReviewItem
        v-if="isPMBusiness"
        :title="tReviewPM('craBusinessNumber')"
        :content="propertyManager.business?.businessNumber || '-'"
      />
      <BcrosFormSectionReviewItem
        :title="tReviewPM('phoneNumber')"
        :content="displayPhoneAndExt(
          propertyManagerContact.phoneNumber, propertyManagerContact.extension, propertyManagerContact.phoneCountryCode
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
