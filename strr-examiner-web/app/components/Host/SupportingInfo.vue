<script setup lang="ts">
import isEmpty from 'lodash/isEmpty'
import { ConnectPageSection } from '#components'
import { useExaminerStore } from '~/stores/examiner'
import { useFlags } from '~/composables/useFlags'

const props = defineProps<{
  application: HostApplicationResp | undefined
}>()
const reg = props.application?.registration

const { t } = useI18n()
const { getDocument } = useExaminerStore()
const alertFlags = reactive(useFlags(props.application as HostApplicationResp))

const openDocInNewTab = async (supportingDocument: ApiDocument) => {
  if (props.application !== undefined) {
    const file = await getDocument(props.application.header.applicationNumber, supportingDocument.fileKey)
    const blob = new Blob([file], { type: 'application/pdf' })
    const url = URL.createObjectURL(blob)
    window.open(url, '_blank')
    URL.revokeObjectURL(url)
  }
}

const businessLicenceDoc = reg?.documents
  ? reg.documents
    .find(doc => doc.documentType === DocumentUploadType.LOCAL_GOVT_BUSINESS_LICENSE)
  : undefined

// Principal Residence Requirements:
const getPrRequired = (): string =>
  reg?.strRequirements?.isPrincipalResidenceRequired
    ? t('pr.required')
    : t('pr.notRequired')

const blExemptReason = reg?.unitDetails?.blExemptReason

const getPrExemptReason = (): string =>
  reg?.unitDetails?.prExemptReason
    ? t(`prExemptReason.${reg.unitDetails.prExemptReason}`)
    : t('prExemptReason.notExempt')

const getOwnershipType = (): string =>
  reg?.unitDetails?.ownershipType === OwnershipType.RENT ? `${t('ownershipType.RENT')}.` : ''
</script>
<template>
  <ConnectPageSection>
    <div class="divide-y px-10 py-6">
      <ApplicationDetailsSection
        v-if="reg?.strRequirements?.isStrProhibited"
        :label="t('strr.label.strProhibited')"
        data-testid="str-prohibited-section"
      >
        <template #icon>
          <AlertFlag data-testid="flag-str-prohibited" />
        </template>
        {{ t('strr.label.strProhibitedAction') }}
      </ApplicationDetailsSection>

      <ApplicationDetailsSection
        v-if="reg?.strRequirements?.isBusinessLicenceRequired"
        :label="t('strr.label.businessLicence')"
        data-testid="business-lic-section"
      >
        <div class="flex gap-x-8">
          <span v-if="blExemptReason">
            {{ t('strr.label.exemptionReason') }}: {{ blExemptReason }}
          </span>
          <template v-else>
            <UButton
              v-if="businessLicenceDoc"
              class="mr-4 gap-x-1 p-0"
              variant="link"
              icon="mdi-file-document-outline"
              data-testid="open-business-lic-btn"
              @click="openDocInNewTab(businessLicenceDoc)"
            >
              {{ t(`documentLabels.${DocumentUploadType.LOCAL_GOVT_BUSINESS_LICENSE}`) }}
            </UButton>
            <span v-if="reg.unitDetails?.businessLicense">
              {{ t('strr.label.businessLicenceNumber') }} {{ reg.unitDetails.businessLicense }}
            </span>
            <span v-if="reg.unitDetails?.businessLicenseExpiryDate">
              {{ t('strr.label.businessLicenceExpiryDate') }}
              {{ dateToString(reg.unitDetails.businessLicenseExpiryDate, 'MMM dd, yyyy') }}
            </span>
          </template>
        </div>
      </ApplicationDetailsSection>

      <ApplicationDetailsSection
        :label="t('strr.label.prRequirement')"
        data-testid="pr-req-section"
      >
        <template #icon>
          <AlertFlag
            v-if="alertFlags.isNotSameProperty || alertFlags.isHostTypeBusiness"
            data-testid="flag-pr-requirement"
          />
        </template>
        <div class="flex">
          <div>
            <div v-if="!isEmpty(reg?.strRequirements)">
              {{ getPrRequired() }}
              {{ getPrExemptReason() }}
              {{ getOwnershipType() }}
            </div>

            <div
              v-if="!isEmpty(reg?.documents)"
              class="mt-2"
              data-testid="pr-req-documents"
            >
              <UButton
                v-for="document in application.registration.documents.filter(
                  doc => doc.documentType !== DocumentUploadType.LOCAL_GOVT_BUSINESS_LICENSE
                )"
                :key="document.fileKey"
                class="mr-4 gap-x-1 p-0"
                variant="link"
                icon="mdi-file-document-outline"
                @click="openDocInNewTab(document)"
              >
                {{ t(`documentLabels.${document.documentType}`) }}
              </UButton>
            </div>
          </div>
          <div
            v-if="alertFlags.isNotSameProperty"
            class="ml-3 w-1/3 font-bold text-red-600"
          >
            {{ t('strr.alertFlags.notSameProperty') }}
          </div>
          <div
            v-if="alertFlags.isHostTypeBusiness"
            class="ml-3 w-1/3 font-bold text-red-600"
          >
            {{ t('strr.alertFlags.hostIsBusiness') }}
          </div>
        </div>
      </ApplicationDetailsSection>
    </div>
  </ConnectPageSection>
</template>
