<template>
  <div
    data-test-id="status-card"
    :class="`${isSingle ? 'flex-1': ''}`"
    class="w-full mb-[42px] mobile:mb-6 justify-between flex-col
    bg-white px-[30px] mobile:px-[8px] py-[22px]
      border-[2px] border-bcGovColor-hairlinesOnWhite"
  >
    <div class="flex justify-between">
      <BcrosChip :flavour="flavour" class="mobile:hidden mb-6" />
      <a
        v-if="isApproved"
        @click="navigateTo(`/registration-details/${registrationId}`)"
      >
        {{ registrationNumber }}
      </a>
      <p v-else class="font-bold">
        {{ registrationNumber }}
      </p>
    </div>
    <div class="flex w-full justify-between mb-5">
      <slot />
      <BcrosChip :flavour="flavour" class="desktop:hidden mb-6" />
    </div>
    <div class="flex flex-row text-bcGovColor-activeBlue justify-start">
      <BcrosButtonsPrimary
        :action="() => navigateTo(`/application-details/${applicationNumber}`)"
        :label="tRegistrationStatus('view')"
        class-name="px-4 py-1 mobile:grow-0"
        variant="ghost"
        data-test-id="view-application-link"
      />

      <BcrosButtonsPrimary
        v-if="isPaid"
        :loading="downloadingReceipts.has(applicationNumber)"
        :action="() => downloadReceipt(applicationNumber)"
        :label="downloadingReceipts.has(applicationNumber) ? '' : tRegistrationStatus('downloadReceipt')"
        class-name="px-4 py-1 mobile:grow-0"
        variant="ghost"
        data-test-id="download-receipt-link"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { HostApplicationStatusE, ExaminerApplicationStatusE } from '#imports'
const { downloadReceipt, downloadingReceipts } = useDownloadReceipt()

const { t } = useTranslation()
const tRegistrationStatus = (translationKey: string) => t(`registrationStatus.${translationKey}`)

const { getChipFlavour } = useChipFlavour()
const { isExaminer } = useBcrosKeycloak()

const {
  applicationHeader,
  isSingle
} = defineProps<{
  applicationHeader: ApplicationHeaderI,
  isSingle: boolean,
}>()

const {
  registrationId,
  registrationNumber,
  status,
  hostStatus,
  examinerStatus,
  applicationNumber
} = applicationHeader

const hasPaymentReceipt = (status: string): boolean => {
  return status !== ApplicationStatusE.DRAFT && status !== ApplicationStatusE.PAYMENT_DUE
}

const isPaid = hasPaymentReceipt(status)

const flavour = computed(() => {
  if (isExaminer) {
    return getChipFlavour(examinerStatus || status)
  } else {
    return getChipFlavour(hostStatus || status)
  }
})

const isApproved = computed(() => {
  if (isExaminer) {
    return [
      ExaminerApplicationStatusE.AUTO_APPROVED,
      ExaminerApplicationStatusE.PROVISIONALLY_APPROVED,
      ExaminerApplicationStatusE.FULL_REVIEW_APPROVED
    ].includes(examinerStatus)
  } else {
    return [
      HostApplicationStatusE.AUTO_APPROVED,
      HostApplicationStatusE.PROVISIONALLY_APPROVED,
      HostApplicationStatusE.FULL_REVIEW_APPROVED
    ].includes(hostStatus)
  }
})
</script>
