<script setup lang="ts">
const exStore = useExaminerStore()
const { activeReg } = storeToRefs(exStore)
const registration = activeReg.value
</script>

<template>
  <main>
    <div class="bg-white">
      <slot name="header" />
      <HostSubHeader
        v-if="registration.registrationType === ApplicationType.HOST"
      />
      <StrataSubHeader
        v-if="registration.registrationType === ApplicationType.STRATA_HOTEL"
      />
      <!-- @open-expansion="manageExpansion" -->
      <PlatformSubHeader
        v-if="registration.registrationType === ApplicationType.PLATFORM"
      />
    </div>

    <div class="app-inner-container space-y-10 py-10">
      <ConnectExpansionRoot />

      <HostSupportingInfo
        v-if="registration.registrationType === ApplicationType.HOST"
      />

      <StrataSupportingInfo
        v-if="registration.registrationType === ApplicationType.STRATA_HOTEL"
      />

      <!--
        <PlatformDetailsView
        v-if="registration.registrationType === ApplicationType.PLATFORM"
      />-->
    </div>
  </main>
</template>
