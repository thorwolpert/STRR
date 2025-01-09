<script setup lang="ts">
const props = defineProps<{ application: HostApplicationResp }>()

const { header, registration } = props.application

const emit = defineEmits<{
    approveApplication: [],
    rejectApplication: []
}>()

</script>

<template>
  <div>
    <div class="mb-2 align-middle text-lg">
      <strong>
        {{ header?.applicationNumber }}
      </strong>
      <UButton label="View History" variant="link" size="sm" class="mx-2 underline" />
    </div>
    <div
      v-if="registration?.registrationType === ApplicationType.HOST"
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
          <dt>Unit Address:</dt>
          <dd class="w-[150px]">
            {{ displayFullUnitAddress(registration?.unitAddress) }}
          </dd>

          <dt>Municipality:</dt>
          <dd>{{ registration?.strRequirements?.organizationNm }}</dd>
        </dl>
      </div>
      <div>
        <dl class="grid grid-cols-[repeat(2,auto)] gap-x-4 pl-5">
          <dt>Host Address:</dt>
          <dd class="w-[150px]">
            {{ displayFullAddress(registration?.primaryContact.mailingAddress) }}
          </dd>

          <dt>Address Type:</dt>
          <dd>Mailing</dd>

          <dt>Same as Unit Address:</dt>
          <dd>{{ registration?.unitDetails.hostResidence }}</dd>

          <dt>Host Name:</dt>
          <dd>{{ displayContactFullName(registration?.primaryContact || {}) }}</dd>

          <dt>Host Type:</dt>
          <dd>{{ registration?.primaryContact.contactType }}</dd>

          <dt>Ownership Type:</dt>
          <dd>{{ registration?.unitDetails.ownershipType }}</dd>
        </dl>
      </div>
      <div>
        <dl class="grid grid-cols-[repeat(2,auto)] gap-x-4 pl-5">
          <dt>Property Type:</dt>
          <dd>{{ registration?.unitDetails.propertyType }}</dd>

          <dt>Configuration:</dt>
          <dd>{{ registration?.unitDetails.rentalUnitSpaceType }}</dd>

          <dt>Rooms:</dt>
          <dd>{{ registration?.unitDetails.numberOfRoomsForRent }}</dd>
        </dl>
      </div>
    </div>

    <!-- APPLICATION SECTIONS -->
    <div class="mt-6 divide-y">
      <ApplicationDetailsSection label="Short-term rentals prohibited" hide-checklist>
        <div class="flex items-center justify-between">
          <div class="flex">
            {{ registration?.strRequirements?.isStrProhibited ? 'Yes' : 'No' }}
          </div>
          <div class="flex items-start justify-end gap-x-2">
            <UButton label="Quick send to supervisor" color="primary" />
          </div>
        </div>
      </ApplicationDetailsSection>

      <ApplicationDetailsSection label="Principal Residence">
        <div>
          {{ registration?.strRequirements?.isPrincipalResidenceRequired ?
            'Required' : 'Not Required' }}
        </div>
        <div>
          <strong>STR Accommodations Act: </strong>
          {{ registration?.strRequirements?.isStraaExempt ?
            'Exempt' : 'Not Exempt' }}
        </div>
      </ApplicationDetailsSection>

      <ApplicationDetailsSection label="" hide-checkbox hide-checklist class="pt-8">
        <div class="flex justify-end gap-x-2">
          <UButton label="Approve" color="primary" @click="emit('approveApplication')" />
          <UButton label="Reject" color="gray" @click="emit('rejectApplication')" />
        </div>
      </ApplicationDetailsSection>
    </div>
  </div>
</template>

<style scoped></style>
