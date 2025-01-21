<script setup lang="ts">
import { ConnectPageSection } from '#components'

const props = defineProps<{
  application: StrataApplicationResp
}>()

const { application: { registration } } = props

const { t } = useI18n()
</script>
<template>
  <ConnectPageSection>
    <div
      v-if="registration.documents && registration.documents.length > 0"
      class="divide-y px-10 py-6"
    >
      <ApplicationDetailsSection :label="t('strr.label.supportingInfo')">
        <SupportingDocuments :application />
      </ApplicationDetailsSection>
    </div>
  </ConnectPageSection>
</template>
