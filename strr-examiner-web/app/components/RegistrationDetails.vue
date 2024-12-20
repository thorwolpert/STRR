<script setup lang="ts">

const props = defineProps<{ application: ApiApplicationResp }>()

const { header } = toRefs(props.application)

</script>
<template>
  <ConnectPageSection
    v-if="header?.registrationNumber"
    :heading="{
      label: 'Registration Details',
      labelClass: 'font-bold',
      icon: 'i-mdi-file-document-tick-outline'
    }"
    class="mt-10 pb-4"
  >
    <ConnectFormSection title="Registration Number" class="pt-4">
      {{ header?.registrationNumber }}
    </ConnectFormSection>

    <ConnectFormSection title="Status" class="pt-4">
      {{ header?.registrationStatus }}
    </ConnectFormSection>

    <ConnectFormSection title="Effective Date" class="pt-4">
      {{ dateToString(header?.registrationStartDate, 'MMMM d, yyyy') }}
    </ConnectFormSection>

    <ConnectFormSection title="Expiry Date" class="pt-4">
      {{ dateToString(header?.registrationEndDate, 'MMMM d, yyyy') }}
    </ConnectFormSection>

    <ConnectFormSection title="Reviewer" class="pt-4">
      {{ header?.reviewer?.displayName || '-' }}
    </ConnectFormSection>
  </ConnectPageSection>
</template>

<style scoped></style>
