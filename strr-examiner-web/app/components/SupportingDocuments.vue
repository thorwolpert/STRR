<script setup lang="ts">
import { isEmpty } from 'lodash'
import { useExaminerStore } from '~/store/examiner'

const props = defineProps<{
  application: HostApplicationResp | PlatformApplicationResp | StrataApplicationResp
  excludeTypes?: DocumentUploadType[]
}>()

const { t } = useI18n()
const { openDocInNewTab } = useExaminerStore()
const { applicationNumber } = props.application.header
const { documents } = props.application.registration as { documents: ApiDocument[] }

const filteredDocuments = props.excludeTypes
  ? documents.filter(doc => !props.excludeTypes?.includes(doc.documentType))
  : documents

</script>

<template>
  <div v-if="!isEmpty(filteredDocuments)">
    <UButton
      v-for="document in filteredDocuments"
      :key="document.fileKey"
      class="mr-4 gap-x-1 p-0"
      variant="link"
      icon="mdi-file-document-outline"
      @click="openDocInNewTab(applicationNumber, document)"
    >
      {{ t(`documentLabels.${document.documentType}`) }}
    </UButton>
  </div>
</template>
