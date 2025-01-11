<script setup lang="ts">
import { useExaminerStore } from '~/store/examiner'

const props = defineProps<{ application: HostApplicationResp }>()

const { t } = useI18n()
const { header, registration } = props.application
const { unitDetails } = registration

const emit = defineEmits<{
  approveApplication: [],
  rejectApplication: []
}>()

const { getDocument } = useExaminerStore()

const openDocInNewTab = async (supportingDocument: ApiDocument) => {
  const file = await getDocument(header.applicationNumber, supportingDocument.fileKey)
  const blob = new Blob([file], { type: 'application/pdf' })
  const url = URL.createObjectURL(blob)
  window.open(url, '_blank')
  URL.revokeObjectURL(url)
}

</script>

<template>
  <div>
    <div class="text-bcGovColor-midGray grid grid-cols-4 gap-x-5 divide-x text-sm">
      <div class="space-y-2">
        <strong>RENTAL UNIT</strong>
        <div class="w-[150px]">
          <UIcon name="i-mdi-map-marker-outline" />
          {{ displayFullUnitAddress(registration?.unitAddress) }}
        </div>
        <div v-if="registration?.strRequirements?.organizationNm">
          <UIcon name="i-mdi-map-outline" />
          {{ registration?.strRequirements?.organizationNm }}
        </div>
      </div>

      <div class="space-y-2 pl-5">
        <strong>HOST</strong>
        <div class="w-[150px]">
          <UIcon name="i-mdi-map-marker-outline" />
          {{ displayFullAddress(registration?.primaryContact.mailingAddress) }}
        </div>
        <div>
          <UIcon name="i-mdi-account" />
          {{ displayContactFullName(registration?.primaryContact) }}
        </div>
        <div>
          <UIcon name="i-mdi-at" />
          {{ registration?.primaryContact.emailAddress }}
        </div>
        <div>
          <strong>Host Type:</strong>
          {{ registration?.primaryContact.contactType }}
        </div>
        <div>
          <strong>Owner / Renter:</strong>
          {{ unitDetails.ownershipType }}
        </div>
      </div>

      <div class="space-y-2 pl-5">
        <div>
          {{ t(`propertyType.${unitDetails.propertyType}`) }}
        </div>
        <div>
          {{ t(`rentalUnitType.${unitDetails.rentalUnitSpaceType}`) }} ({{ unitDetails.numberOfRoomsForRent }} Rooms)
        </div>
        <div>{{ t(`hostResidence.${unitDetails.hostResidence}`) }}</div>
        <div><strong>PID:</strong> {{ unitDetails.parcelIdentifier }}</div>
        <div>
          <strong>PR Registered Rentals:</strong>
          <!-- TODO: Get number of registered rentals for the host -->
        </div>
      </div>

      <div class="space-y-2 pl-5">
        <div>
          <UIcon name="i-mdi-account-multiple-outline" />
          {{ registration?.secondaryContact?.contactType === OwnerType.INDIVIDUAL
            ? displayContactFullName(registration?.secondaryContact) :
              registration?.secondaryContact?.businessLegalName }}
        </div>

        <div>
          <UIcon name="i-mdi-at" />
          {{ registration?.propertyManager?.propertyManagerType === OwnerType.INDIVIDUAL
            ? displayContactFullName(registration?.propertyManager.contact) :
              registration?.propertyManager?.business?.legalName }}
        </div>
      </div>
    </div>

    <!-- APPLICATION SECTIONS -->
    <div class="mt-6 divide-y">
      <ApplicationDetailsSection label="Short-term rentals prohibited">
        <div class="flex items-center justify-between">
          <div class="flex">
            {{ registration?.strRequirements?.isStrProhibited ? 'Yes' : 'No' }}
          </div>
        </div>
      </ApplicationDetailsSection>

      <ApplicationDetailsSection label="Principal Residence">
        <div>
          {{ registration?.strRequirements?.isPrincipalResidenceRequired ?
            'Required.' : 'Not Required.' }} {{ registration?.strRequirements?.isStraaExempt ?
            'Exempt.' : 'Not Exempt.' }}
        </div>

        <div class="mt-2">
          <UButton
            v-for="document in registration.documents"
            :key="document.fileKey"
            class="mr-4 gap-x-1 p-0"
            variant="link"
            icon="mdi-file-document-outline"
            @click="openDocInNewTab(document)"
          >
            {{ t(`documentLabels.${document.documentType}`) }}
          </UButton>
        </div>
      </ApplicationDetailsSection>

      <ApplicationDetailsSection label="" hide-checkbox class="pt-8">
        <div class="flex justify-end gap-x-2">
          <UButton
            icon="i-mdi-close"
            :label="t('btn.decline')"
            color="red"
            variant="outline"
            size="lg"
            @click="emit('rejectApplication')"
          />
          <UButton
            icon="i-mdi-check"
            :label="t('btn.approve')"
            color="green"
            variant="outline"
            size="lg"
            @click="emit('approveApplication')"
          />
        </div>
      </ApplicationDetailsSection>
    </div>
  </div>
</template>

<style scoped></style>
