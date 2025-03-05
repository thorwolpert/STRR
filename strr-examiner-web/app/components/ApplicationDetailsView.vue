<script setup lang="ts">
const { isApplication, activeRecord } = useExaminerStore()

const reg = isApplication
  ? activeRecord.registration
  : activeRecord
</script>

<template>
  <main>
    <div class="bg-white">
      <slot name="header" />
      <HostSubHeader
        v-if="reg.registrationType === ApplicationType.HOST"
      />
      <StrataSubHeader
        v-if="reg.registrationType === ApplicationType.STRATA_HOTEL"
      />
      <!-- @open-expansion="manageExpansion" -->
      <PlatformSubHeader
        v-if="reg.registrationType === ApplicationType.PLATFORM"
      />
    </div>

    <div class="app-inner-container space-y-10 py-10">
      <ConnectExpansionRoot />

      <HostSupportingInfo
        v-if="reg.registrationType === ApplicationType.HOST"
      />

      <StrataSupportingInfo
        v-if="reg.registrationType === ApplicationType.STRATA_HOTEL"
      />

      <!--
        <PlatformDetailsView
        v-if="reg.registrationType === ApplicationType.PLATFORM"
      />-->
    </div>
  </main>
</template>
