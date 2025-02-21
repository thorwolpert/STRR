<script setup lang="ts">

const props = defineProps<{ application: StrataApplicationResp }>()

const { registration } = props.application
const { businessDetails } = registration

const strataExpansion = useStrataExpansion(props.application)

const attorney = businessDetails.registeredOfficeOrAttorneyForServiceDetails
const hasAttorneyAddress = Object.values(attorney.mailingAddress).some(Boolean)

</script>

<template>
  <div
    data-testid="strata-sub-header"
    class="app-inner-container"
  >
    <div class="text-bcGovColor-midGray grid grid-cols-4 gap-x-5 divide-x bg-white py-4 text-sm">
      <div class="space-y-2">
        <b>{{ $t('strr.label.primaryBuilding').toUpperCase() }}</b>
        <ConnectInfoWithIcon
          icon="i-mdi-map-marker-outline"
          :content="displayFullAddress(registration?.strataHotelDetails.location)"
        />
        <UButton
          v-if="registration?.strataHotelDetails.buildings.length > 0"
          :label="$t('strr.label.viewAllBuildings')"
          :padded="false"
          variant="link"
          @click="strataExpansion.openAllBuildings()"
        />
      </div>

      <div class="space-y-4 pl-5">
        <div class="space-y-2">
          <b>{{ $t('strr.label.business').toUpperCase() }}</b>
          <ConnectInfoWithIcon
            icon="i-mdi-domain"
            class="whitespace-nowrap"
          >
            <UButton
              :label="businessDetails?.legalName"
              :padded="false"
              variant="link"
              @click="strataExpansion.openBusiness()"
            />
          </ConnectInfoWithIcon>

          <ConnectInfoWithIcon
            icon="i-mdi-envelope-outline"
            :content="displayFullAddress(businessDetails.mailingAddress)"
          />
        </div>
        <div
          v-if="attorney.attorneyName || hasAttorneyAddress"
          class="space-y-2"
        >
          <b>{{ $t('strr.label.attorneyForService').toUpperCase() }}</b>
          <ConnectInfoWithIcon
            v-if="attorney.attorneyName"
            icon="i-mdi-domain"
            :content="attorney.attorneyName"
          />
          <ConnectInfoWithIcon
            v-if="hasAttorneyAddress"
            icon="i-mdi-map-marker-outline"
            :content="displayFullAddress(attorney.mailingAddress)"
          />
        </div>
      </div>

      <div class="space-y-4 pl-5">
        <div class="space-y-2">
          <!--Main Representative -->
          <b>{{ $t('strr.label.representative').toUpperCase() }}</b>
          <ConnectInfoWithIcon
            icon="i-mdi-account"
            class="whitespace-nowrap"
          >
            <UButton
              :label="displayContactFullName(registration?.strataHotelRepresentatives[0])"
              :padded="false"
              variant="link"
              @click="strataExpansion.openIndividuals()"
            />
          </ConnectInfoWithIcon>

          <ConnectInfoWithIcon
            v-if="registration?.strataHotelRepresentatives[0]?.phoneNumber"
            icon="i-mdi-phone"
            :content="displayPhoneAndExt(registration?.strataHotelRepresentatives[0]?.phoneNumber)"
          />

          <ConnectInfoWithIcon
            icon="i-mdi-at"
            :content="registration?.strataHotelRepresentatives[0]?.emailAddress"
          />
        </div>
        <div v-if="registration?.strataHotelRepresentatives[1]" class="space-y-2">
          <!-- Second Representative if available -->
          <b>{{ $t('strr.label.secondaryRepresentative').toUpperCase() }}</b>
          <ConnectInfoWithIcon
            icon="i-mdi-account"
            class="whitespace-nowrap"
          >
            <UButton
              :label="displayContactFullName(registration?.strataHotelRepresentatives[1])"
              :padded="false"
              variant="link"
              @click="strataExpansion.openIndividuals()"
            />
          </ConnectInfoWithIcon>
        </div>
        <div class="space-y-2">
          <!-- Completing Party -->
          <b>{{ $t('strr.label.completingParty').toUpperCase() }}</b>
          <ConnectInfoWithIcon
            icon="i-mdi-account"
            class="whitespace-nowrap"
          >
            <UButton
              :label="displayContactFullName(registration?.completingParty)"
              :padded="false"
              variant="link"
              @click="strataExpansion.openIndividuals()"
            />
          </ConnectInfoWithIcon>
        </div>
      </div>

      <div class="space-y-2 pl-5">
        <b>{{ $t('strr.label.additionalInformation').toUpperCase() }}</b>
        <div>
          <b>{{ $t('strr.label.numberOfRentalUnits') }}</b>
          {{ registration.strataHotelDetails.numberOfUnits }}
        </div>
        <div>
          <b>{{ $t('label.strataHotelCategory') }}:</b>
          {{ $t(`strataHotelCategoryReview.${registration.strataHotelDetails.category}`) }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
