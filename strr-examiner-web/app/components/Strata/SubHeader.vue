<script setup lang="ts">

const props = defineProps<{ application: StrataApplicationResp }>()

const { t } = useI18n()
const { registration } = props.application
const { businessDetails } = registration

</script>

<template>
  <div class="app-inner-container">
    <div class="grid grid-cols-4 gap-x-5 divide-x bg-white py-4 text-sm text-bcGovColor-midGray">
      <div class="space-y-2">
        <b>{{ t('strr.label.primaryBuilding').toUpperCase() }}</b>
        <ConnectInfoWithIcon
          icon="i-mdi-map-marker-outline"
          :content="displayFullAddress(registration?.strataHotelDetails.buildings[0])"
        />
        <UButton
          v-if="registration?.strataHotelDetails.buildings.length > 1"
          :label="t('strr.label.viewAllBuildings')"
          :padded="false"
          variant="link"
        />
      </div>

      <div class="space-y-4 pl-5">
        <div class="space-y-2">
          <b>{{ t('strr.label.business').toUpperCase() }}</b>
          <ConnectInfoWithIcon icon="i-mdi-domain" :content="businessDetails?.legalName" />
          <ConnectInfoWithIcon
            icon="i-mdi-envelope-outline"
            :content="displayFullAddress(businessDetails.mailingAddress)"
          />
        </div>
        <div class="space-y-2">
          <b>{{ t('strr.label.attorneyForService').toUpperCase() }}</b>
          <ConnectInfoWithIcon
            icon="i-mdi-domain"
            :content="businessDetails.registeredOfficeOrAttorneyForServiceDetails.attorneyName"
          />
          <ConnectInfoWithIcon
            icon="i-mdi-map-marker-outline"
            :content="displayFullAddress(businessDetails.registeredOfficeOrAttorneyForServiceDetails.mailingAddress)"
          />
        </div>
      </div>

      <div class="space-y-4 pl-5">
        <div class="space-y-2">
          <!--Main Representative -->
          <b>{{ t('strr.label.representative').toUpperCase() }}</b>
          <ConnectInfoWithIcon
            icon="i-mdi-account"
            :content="displayContactFullName(registration?.strataHotelRepresentatives[0] as ApiRep)"
          />

          <ConnectInfoWithIcon
            icon="i-mdi-phone"
            :content="displayPhoneAndExt(registration?.strataHotelRepresentatives[0]?.phoneNumber)"
          />

          <ConnectInfoWithIcon icon="i-mdi-at" :content="registration?.strataHotelRepresentatives[0]?.emailAddress" />
        </div>
        <div v-if="registration?.strataHotelRepresentatives[1]" class="space-y-2">
          <!-- Second Representative if available -->
          <b>{{ t('strr.label.secondaryRepresentative').toUpperCase() }}</b>
          <ConnectInfoWithIcon
            icon="i-mdi-account"
            :content="displayContactFullName(registration?.strataHotelRepresentatives[1] as ApiRep)"
          />
        </div>
        <div class="space-y-2">
          <!-- Completing Party -->
          <b>{{ t('strr.label.completingParty').toUpperCase() }}</b>
          <ConnectInfoWithIcon icon="i-mdi-account" :content="displayContactFullName(registration?.completingParty)" />
        </div>
      </div>

      <div class="space-y-2 pl-5">
        <b>{{ t('strr.label.additionalInformation').toUpperCase() }}</b>
        <div>
          <b>{{ t('strr.label.numberOfRentalUnits') }}</b>
          {{ registration.strataHotelDetails.numberOfUnits }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
