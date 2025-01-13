<script setup lang="ts">
const props = defineProps<{ application: StrataApplicationResp }>()

const { header, registration } = props.application

</script>

<template>
  <div>
    <div
      class="flex flex-row gap-x-5 divide-x text-sm"
    >
      <div>
        <dl class="grid grid-cols-[repeat(2,auto)] gap-x-4">
          <dt>Status:</dt>
          <dd>{{ header?.hostStatus }}</dd>

          <dt>Submitted:</dt>
          <dd>{{ dateToString(header?.applicationDateTime || '') }}</dd>

          <dt>Registration Type:</dt>
          <dd>{{ registration?.registrationType }}</dd>
        </dl>
      </div>

      <div>
        <dl class="grid grid-cols-[repeat(2,auto)] gap-x-4 pl-5">
          <dt>Completing Party</dt>
          <dd />

          <dt>Name:</dt>
          <dd>{{ displayContactFullName(registration?.completingParty) }}</dd>

          <dt>Email:</dt>
          <dd>{{ registration?.completingParty.emailAddress }}</dd>

          <dt>Phone:</dt>
          <dd>{{ registration?.completingParty.phoneNumber }}</dd>
        </dl>
      </div>

      <div>
        <dl class="grid grid-cols-[repeat(2,auto)] gap-x-4 pl-5">
          <dt>Strata Hotel Representative</dt>
          <dd />

          <dt>Name:</dt>
          <dd>{{ displayContactFullName(registration?.strataHotelRepresentatives[0]) }}</dd>

          <dt>Email:</dt>
          <dd>{{ registration?.completingParty.emailAddress }}</dd>
        </dl>
      </div>
    </div>

    <!-- APPLICATION SECTIONS -->
    <div class="mt-6 divide-y">
      <ApplicationDetailsSection
        label="Business Details"
      >
        <div class="flex items-center justify-between">
          <div class="flex">
            {{ registration?.businessDetails?.legalName }} |
            {{ displayFullAddress(registration?.businessDetails.mailingAddress) }}
          </div>
        </div>
      </ApplicationDetailsSection>
    </div>
  </div>
</template>

<style scoped></style>
