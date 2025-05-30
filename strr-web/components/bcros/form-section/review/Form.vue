<template>
  <div data-test-id="review-form" class="relative h-full">
    <div class="d:mb-[180px] m:mb-[32px] rounded-1">
      <div class="bg-white px-[30px] py-[22px] m:px-2">
        <p>{{ tReview('reviewInstructions') }}</p>
        <p>{{ tReview('reviewInstructionsContinued') }}</p>
      </div>
      <div>
        <!-- Property Manager Information -->
        <BcrosFormSectionPropertyManagerSummaryView
          v-if="formState.hasPropertyManager"
          :property-manager="formState.propertyManager"
          data-test-id="property-manager-review"
          class="mt-12"
        />
        <div class="mt-[48px]">
          <p class="font-bold mb-[24px] mobile:mx-[8px]">
            {{ tReview('hostInformation') }}
          </p>
          <BcrosFormSectionReviewSubsection
            :state="formState.primaryContact"
            :is-individual-co-host="formState.primaryContact.contactType === HostContactTypeE.INDIVIDUAL"
            is-primary
            data-test-id="primary-contact-review"
          />
        </div>
        <!-- Secondary Contact -->
        <div v-if="secondaryContact" class="mt-12">
          <p class="font-bold mb-6 m:mx-2">
            {{ tReview(isHostTypeBusiness ? 'secondaryContactBusiness' : 'secondaryContactIndividual') }}
          </p>
          <BcrosFormSectionReviewSubsection
            :state="formState.secondaryContact"
            :is-individual-co-host="formState.primaryContact.contactType === HostContactTypeE.INDIVIDUAL"
            data-test-id="secondary-contact-review"
          />
        </div>
        <!-- Property Details -->
        <BcrosFormSectionPropertySummaryView
          :property-details="formState.propertyDetails"
          data-test-id="property-details-review"
          class="mt-12"
        />
        <!-- Principal Residence -->
        <div class="mt-12">
          <p class="font-bold mb-6 m:mx-2">
            {{ tReview('principal') }}
          </p>
          <div class="bg-white py-[22px] px-[30px] mb-6 m:px-2">
            <p>
              {{ formState.principal.isPrincipalResidence ? tPrincipal('yes') : tPrincipal('no') }}
            </p>
            <div v-if="!formState.principal.isPrincipalResidence">
              <p>
                <b>{{ tReview('reason') }}: </b>
                {{ formState.principal.specifiedServiceProvider
                  ? `${formState.principal.nonPrincipalOption}: ${formState.principal.specifiedServiceProvider}`
                  : (formState.principal.nonPrincipalOption || '-')
                }}
              </p>
            </div>
          </div>
          <div v-if="formState.principal.isPrincipalResidence">
            <div class="bg-white py-[22px] px-[30px] m:px-2">
              <p class="font-bold mb-2">
                {{ tReview('proof') }}
              </p>
              <div class="mb-6">
                <div v-for="(supportingDocument) in formState.supportingDocuments" :key="supportingDocument.name">
                  <div class="flex flex-row items-center">
                    <img
                      class="mr-1 h-[18px] w-[18px]"
                      src="/icons/create-account/attach_dark.svg"
                      alt="Attach icon"
                    >
                    <p>{{ supportingDocument.name }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Review and Confirm -->
        <div class="mt-12">
          <p class="font-bold mb-6 m:mx-2">
            {{ tReview('confirmation') }}
          </p>
          <div class="bg-white p-8 mb-6">
            <div class="space-y-6">
              <div data-test-id="terms-and-conditions-confirmation">
                <p>
                  <span class="font-bold">{{ tReview('confirmTermsAndConditionsLabel') }}</span>
                  {{ tReview('confirmTermsAndConditionsFirst') }}
                  <a
                    class="text-bcGovColor-activeBlue"
                    target="_blank"
                    href="https://www2.gov.bc.ca/gov/content/housing-tenancy/short-term-rentals/\
                    registry/registry-toc-hosts"
                    rel="noopener noreferrer"
                  >
                    {{ tReview('confirmTermsAndConditionsLink') }}
                  </a>
                  {{ tReview('confirmTermsAndConditionsSecond') }}
                </p>
                <hr class="mt-4 border-gray-500">
              </div>
              <div data-test-id="tax-auditing-confirmation">
                <p>
                  <span class="font-bold">{{ tReview('confirmTaxAuditingLabel') }}</span>
                  {{ tReview('confirmTaxAuditing') }}
                </p>
                <hr class="mt-4 border-gray-500">
              </div>
              <div data-test-id="info-accuracy-confirmation">
                <p>
                  <span class="font-bold">{{ tReview('confirmInfoAccuracyLabel') }}</span>
                  {{ tReview('confirmInfoAccuracy') }}
                </p>
                <hr class="mt-4 border-gray-500">
              </div>
              <div v-if="formState.isPropertyManagerRole" data-test-id="host-auth-confirmation">
                <p>
                  <span class="font-bold">{{ tReview('confirmHostAuthorizationLabel') }}</span>
                  {{ tReview('confirmHostAuthorization') }}
                </p>
                <hr class="mt-4 border-gray-500">
              </div>
              <UCheckbox
                v-model="confirmationCheckboxValue"
                :label="tReview('confirmAll')"
                :ui="{
                  label: isComplete && (
                    !formState.principal.agreedToSubmit ||
                    (formState.isPropertyManagerRole && !formState.hasHostAuthorization)
                  ) ? 'text-bcGovColor-error' : ''
                }"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { formState } from '@/stores/strr'
const { t } = useTranslation()
const { secondaryContact, isComplete } = defineProps<{ secondaryContact: boolean, isComplete: boolean }>()

const tReview = (translationKey: string) => t(`createAccount.review.${translationKey}`)
const tPrincipal = (translationKey: string) => t(`createAccount.principalResidence.${translationKey}`)
const confirmationCheckboxValue = computed({
  get: () => formState.principal.agreedToSubmit && formState.principal.agreedToRentalAct,
  set: (value: boolean) => {
    formState.principal.agreedToSubmit = value
    formState.principal.agreedToRentalAct = value
    if (formState.isPropertyManagerRole) {
      formState.hasHostAuthorization = value
    }
  }
})

const isHostTypeBusiness = computed(():boolean => formState.primaryContact.contactType === HostContactTypeE.BUSINESS)
</script>
