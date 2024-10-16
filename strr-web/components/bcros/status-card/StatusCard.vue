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
        @click="navigateTo(`/registration-details/${registrationId}`, { open: { target: '_blank' } })"
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
        :action="() => navigateTo(`/application-details/${applicationNumber}`, { open: { target: '_blank' } })"
        :label="tRegistrationStatus('view')"
        class-name="px-4 py-1 mobile:grow-0"
        variant="ghost"
      />

      <BcrosButtonsPrimary
        v-if="showDownloadButton"
        :action="() => downloadCertificate(registrationId.toString())"
        :label="tRegistrationStatus('download')"
        class-name="px-4 py-1 mobile:grow-0"
        variant="ghost"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { RegistrationStatusE, HostApplicationStatusE, ExaminerApplicationStatusE } from '#imports'
const { downloadCertificate, isCertificateIssued } = useDownloadCertificate()

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

const canDownloadCertificate = ref(false)
const { registrationId, registrationNumber, status, hostStatus, examinerStatus, registrationStatus } = applicationHeader
const applicationNumber = applicationHeader.applicationNumber
const flavour = computed(() => {
  if (isExaminer) {
    return getChipFlavour(examinerStatus || status)
  } else {
    return getChipFlavour(hostStatus || status)
  }
})

const isRegistrationActive: boolean = registrationStatus === RegistrationStatusE.ACTIVE
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
const showDownloadButton = computed(() => isRegistrationActive && canDownloadCertificate.value)
onMounted(async () => {
  canDownloadCertificate.value = registrationId
    ? await isCertificateIssued(registrationId.toString())
    : false
})
</script>
