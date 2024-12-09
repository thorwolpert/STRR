<script setup lang="ts">
const { t } = useTranslation()
const { header, contact } = defineProps<{
  header: string,
  contact: ContactI
}>()

const displayHostType = {
  [HostContactTypeE.INDIVIDUAL]: t('createAccount.contactForm.hostTypeIndividual'),
  [HostContactTypeE.BUSINESS]: t('createAccount.contactForm.hostTypeBusiness')
}

</script>

<template>
  <div>
    <h2 class="font-bold mb-6 mobile:mx-2 text-xl">
      {{ header }}
    </h2>
    <div class="bg-white p-8 m:px-2 grid d:grid-cols-3 d:grid-rows-4 d:grid-flow-col">
      <BcrosFormSectionReviewItem
        :title="t('common.formLabels.hostType')"
        :content="displayHostType[contact.contactType]"
        data-test-id="contact-info-host-type"
      />
      <BcrosFormSectionReviewItem
        :title="t('common.formLabels.name')"
        :content="displayContactFullName(contact.name)"
        data-test-id="contact-info-name"
      />
      <div class="grid grid-rows-subgrid row-span-2">
        <BcrosFormSectionReviewItem
          :title="t('common.formLabels.preferredName')"
          :content="contact.details.preferredName || '-'"
          data-test-id="contact-info-preferred-name"
        />
      </div>
      <BcrosFormSectionReviewItem
        :title="t('common.formLabels.dateOfBirth')"
        :content="contact.dateOfBirth ? convertDateToLongFormat(contact.dateOfBirth) : '-'"
      />
      <BcrosFormSectionReviewItem
        :title="t('common.formLabels.socialInsuranceNumber')"
        :content="contact.socialInsuranceNumber || '-'"
      />
      <BcrosFormSectionReviewItem
        :title="t('common.formLabels.businessLegalName')"
        :content="contact.businessLegalName || '-'"
      />
      <BcrosFormSectionReviewItem
        :title="t('common.formLabels.craBusinessNumber')"
        :content="contact.businessNumber || '-'"
      />
      <BcrosFormSectionReviewItem
        :title="t('common.formLabels.phoneNumber')"
        :content="displayPhoneAndExt(
          contact.details.phoneNumber,
          contact.details.extension) || '-'"
        data-test-id="contact-info-phone"
      />
      <BcrosFormSectionReviewItem
        :title="t('common.formLabels.faxNumber')"
        :content="displayFormattedPhone(contact.details.faxNumber) || '-'"
      />
      <BcrosFormSectionReviewItem
        :title="t('common.formLabels.emailAddress')"
        :content="contact.details.emailAddress || '-'"
        data-test-id="contact-info-email"
      />
      <BcrosFormSectionReviewItem
        :title="t('common.formLabels.mailingAddress')"
        data-test-id="contact-info-address"
      >
        <!-- eslint-disable-next-line vue/no-v-html -->
        <p v-html="displayFullAddress(contact.mailingAddress) || '-'" />
      </BcrosFormSectionReviewItem>
    </div>
  </div>
</template>
