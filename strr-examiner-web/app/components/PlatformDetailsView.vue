<script setup lang="ts">
const props = defineProps<{ application: PlatformApplicationResp }>()

const { header, registration } = props.application

</script>

<template>
  <div>
    <div class="mb-2 align-middle text-lg">
      <strong>
        {{ header?.applicationNumber }}
      </strong>
      <UButton
        label="View History"
        variant="link"
        size="sm"
        class="mx-2 underline"
      />
    </div>

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
          <dt>Platform Representative</dt>
          <dd />

          <dt>Name:</dt>
          <dd>{{ displayContactFullName(registration?.platformRepresentatives[0]) }}</dd>

          <dt>Email:</dt>
          <dd>{{ registration?.completingParty.emailAddress }}</dd>
        </dl>
      </div>
    </div>

    <!-- APPLICATION SECTIONS -->
    <div class="mt-6 divide-y">
      <ApplicationDetailsSection
        label="Business Details"
        hide-checklist
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
