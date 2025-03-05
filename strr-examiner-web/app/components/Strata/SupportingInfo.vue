<script setup lang="ts">
import { ConnectPageSection } from '#components'

const { isApplication, activeRecord } = useExaminerStore()
const reg = isApplication
  ? activeRecord.registration
  : activeRecord

const { t } = useI18n()
</script>
<template>
  <ConnectPageSection v-if="reg?.documents?.length">
    <div class="divide-y px-10 py-6">
      <ApplicationDetailsSection :label="t('strr.label.supportingInfo')">
        <SupportingDocuments />
      </ApplicationDetailsSection>
    </div>
  </ConnectPageSection>
</template>
