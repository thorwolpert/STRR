<script setup lang="ts">
import { useFlags } from '~/composables/useFlags'

const props = defineProps<{ application: HostApplicationResp }>()
const reg = props.application.registration
const { header } = props.application

const { t } = useI18n()
const alertFlags = reactive(useFlags(props.application as HostApplicationResp))

const hostExp = useHostExpansion()
</script>
<template>
  <div
    data-testid="host-sub-header"
    class="app-inner-container"
  >
    <div class="grid grid-cols-4 gap-x-5 divide-x py-4 text-sm text-bcGovColor-midGray">
      <div
        id="rental-unit-details"
        class="space-y-2"
      >
        <strong>{{ t('strr.label.rentalUnit').toUpperCase() }}</strong>
        <div class="w-[150px]">
          <UIcon name="i-mdi-map-marker-outline" />
          {{ displayFullUnitAddress(reg.unitAddress) }}
          <AlertFlag
            v-if="alertFlags.isUnitNumberMissing"
            data-testid="flag-unit-number-missing"
          />
        </div>
        <div v-if="reg.strRequirements?.organizationNm">
          <UIcon name="i-mdi-map-outline" />
          {{ reg.strRequirements.organizationNm }}
        </div>
        <div
          v-if="alertFlags.isUnitNumberMissing"
          class="font-bold text-red-600"
        >
          {{ t('strr.alertFlags.unitNumberMissing') }}
        </div>
      </div>

      <div
        id="host-details"
        class="space-y-2 pl-5"
      >
        <strong>{{ t('strr.label.host').toUpperCase() }}</strong>
        <div class="w-[150px]">
          <UIcon name="i-mdi-map-marker-outline" />
          {{ displayFullAddress(reg.primaryContact?.mailingAddress) }}
        </div>
        <div class="flex items-center gap-1">
          <UIcon name="i-mdi-account" class="size-5 shrink-0 text-gray-700" />
          <UButton
            :label="displayContactFullName(reg.primaryContact!)"
            :padded="false"
            variant="link"
            @click="hostExp.openHostOwners(application, 'primaryContact')"
          />
        </div>
        <div>
          <UIcon name="i-mdi-at" />
          {{ reg.primaryContact?.emailAddress }}
        </div>
        <div v-if="reg.primaryContact?.contactType" class="flex gap-x-1">
          <strong>{{ t('strr.label.hostType') }}</strong>
          {{ t(`ownerType.${reg.primaryContact?.contactType}`) }}
          <AlertFlag
            v-if="alertFlags.isHostTypeBusiness"
            :tooltip-text="t('strr.alertFlags.hostIsBusiness')"
            data-testid="flag-host-business"
          />
        </div>
        <div>
          <strong>{{ t('strr.label.ownerRenter') }}</strong>
          {{ t(`ownershipType.${reg.unitDetails?.ownershipType}`) }}
        </div>
      </div>

      <div class="space-y-2 pl-5">
        <div>
          {{ t(`propertyType.${reg.unitDetails?.propertyType}`) }}
        </div>
        <div v-if="reg.unitDetails?.numberOfRoomsForRent">
          {{ t(`rentalUnitType.${reg.unitDetails?.rentalUnitSpaceType}`) }}
          ({{
            reg.unitDetails?.numberOfRoomsForRent + ' ' + t('strr.label.room', reg.unitDetails?.numberOfRoomsForRent)
          }})
        </div>
        <div>
          {{ t(`hostResidence.${reg.unitDetails?.hostResidence}`) }}
          <AlertFlag
            v-if="alertFlags.isNotSameProperty"
            :tooltip-text="t('strr.alertFlags.hostAddressNotSame')"
            data-testid="flag-host-address-not-same"
          />
        </div>
        <div><strong>{{ t('strr.label.pid') }}</strong> {{ reg.unitDetails?.parcelIdentifier }}</div>
        <div class="flex gap-x-1">
          <strong>{{ t('strr.label.registeredRentals') }}</strong>
          {{ header.existingHostRegistrations }}
          <AlertFlag
            v-if="alertFlags.isRegLimitExceeded"
            :tooltip-text="t('strr.alertFlags.exceedsRegistrationLimit')"
            data-testid="flag-exceeds-reg-limit"
          />
        </div>
        <div>
          <strong>{{ t('strr.label.prRegisteredRentals') }}</strong>
          <!-- TODO: Get number of PR registered rentals -->
        </div>
      </div>

      <div
        id="additional-details"
        class="space-y-2 pl-5"
      >
        <div v-if="reg?.secondaryContact" class="flex items-center gap-1">
          <UIcon name="i-mdi-account-multiple-outline" class="size-5 shrink-0 text-gray-700" />
          <UButton
            :label="reg?.secondaryContact?.contactType === OwnerType.BUSINESS
              ? reg?.secondaryContact?.businessLegalName
              : displayContactFullName(reg?.secondaryContact)"
            :padded="false"
            variant="link"
            @click="hostExp.openHostOwners(application, 'secondaryContact')"
          />
        </div>

        <div v-if="reg?.propertyManager?.propertyManagerType" class="flex items-center gap-1">
          <UIcon name="i-mdi-at" class="size-5 shrink-0 text-gray-700" />
          <UButton
            :label="reg?.propertyManager?.propertyManagerType === OwnerType.INDIVIDUAL
              ? displayContactFullName(reg?.propertyManager.contact)
              : reg?.propertyManager?.business?.legalName"
            :padded="false"
            variant="link"
            @click="hostExp.openHostOwners(application, 'propertyManager')"
          />
        </div>
      </div>
    </div>
  </div>
</template>
