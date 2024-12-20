<script setup lang="ts">

const props = defineProps<{ application: ApiApplicationResp, applicationActions?: HeaderAction[] }>()

const displayApplicationType = {
  [ApplicationType.HOST]: 'Host',
  [ApplicationType.PLATFORM]: 'Platform',
  [ApplicationType.STRATA_HOTEL]: 'Strata Hotel'
}

const { header, registration } = props.application

</script>
<template>
  <ConnectPageSection
    :heading="{
      label: 'Application Details',
      labelClass: 'font-bold',
      icon: 'i-mdi-file-document-move-outline'
    }"
    :actions="applicationActions"
    class="pb-4"
  >
    <ConnectFormSection title="Application Number" class="pt-4">
      {{ header?.applicationNumber }}
    </ConnectFormSection>

    <ConnectFormSection title="Status" class="pt-4">
      {{ header?.examinerStatus }}
    </ConnectFormSection>

    <ConnectFormSection title="Submission Date" class="pt-4">
      {{ dateToString(header?.applicationDateTime, 'MMMM d, yyyy') }}
    </ConnectFormSection>

    <ConnectFormSection title="Decision Date" class="pt-4">
      {{ header?.decisionDate ? dateToString(header?.decisionDate, 'MMMM d, yyyy') : '-' }}
    </ConnectFormSection>

    <ConnectFormSection title="Registration Type" class="pt-4">
      {{ displayApplicationType[registration?.registrationType as keyof typeof displayApplicationType] }}
    </ConnectFormSection>

    <ConnectFormSection title="Submitted By" class="pt-4">
      {{ header.submitter.displayName }}
    </ConnectFormSection>
  </ConnectPageSection>
</template>

<style scoped></style>
