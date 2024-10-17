<script setup lang="ts">
const { t } = useI18n()

const tPlat = (path: string) => t(`platform.${path}`)

const { isComplete } = defineProps<{ isComplete: boolean }>()

const { getContactSchema, getNewRepresentative } = useStrrPlatformContact()
const { isCompletingPartyRep, completingParty, primaryRep, secondaryRep } = storeToRefs(useStrrPlatformContact())

const radioOptions = [
  { value: true, label: t('word.Yes') },
  { value: false, label: t('word.No') }]

watch(isCompletingPartyRep, (val) => {
  primaryRep.value = getNewRepresentative(val)
})

const validateForm = (formRef: any) => {
  if (formRef && isComplete) {
    formRef.validate()
  }
}

const compPartyRef = ref()
const primaryRepRef = ref()
const secondaryRepRef = ref()
watch(compPartyRef, validateForm)
watch(primaryRepRef, validateForm)
watch(secondaryRepRef, validateForm)
</script>

<template>
  <div data-testid="contact-information" class="space-y-10">
    <URadioGroup
      v-model="isCompletingPartyRep"
      :class="isComplete && isCompletingPartyRep === undefined ? 'border-red-600 border-2 p-2' : 'p-2'"
      :legend="tPlat('text.isUserRep')"
      :options="radioOptions"
      :ui="{ legend: 'mb-3 text-default font-bold text-gray-700' }"
      :ui-radio="{ inner: 'space-y-2' }"
    />
    <div v-if="isCompletingPartyRep !== undefined" class="space-y-10">
      <div v-if="!isCompletingPartyRep" class="space-y-10">
        <ConnectPageSection
          class="bg-white"
          :heading="{ label: tPlat('section.title.completingParty'), labelClass: 'ml-6 font-bold' }"
        >
          <UForm
            ref="compPartyRef"
            :schema="getContactSchema(true)"
            :state="completingParty"
            class="pb-10"
          >
            <FormCommonContact
              v-model:first-name="completingParty.firstName"
              v-model:last-name="completingParty.lastName"
              v-model:phone="completingParty.phone"
              v-model:emailAddress="completingParty.emailAddress"
              id-prefix="platform-completing-party"
              name-divider
              prepopulate-name
              prepopulate-type="Bceid"
            />
          </UForm>
        </ConnectPageSection>
        <ConnectPageSection
          v-if="primaryRep"
          class="bg-white"
          :heading="{ label: tPlat('section.title.primaryRep'), labelClass: 'ml-6 font-bold' }"
        >
          <UForm
            ref="primaryRepRef"
            :schema="getContactSchema(false)"
            :state="primaryRep"
            class="space-y-10 pb-10"
          >
            <FormCommonContact
              v-model:first-name="primaryRep.firstName"
              v-model:middle-name="primaryRep.middleName"
              v-model:last-name="primaryRep.lastName"
              v-model:phone="primaryRep.phone"
              v-model:emailAddress="primaryRep.emailAddress"
              v-model:fax-number="primaryRep.faxNumber"
              v-model:position="primaryRep.position"
              id-prefix="platform-primary-rep"
              name-divider
              :prepopulate-name="false"
              email-warning
              :section-info="t('platform.text.primaryContact')"
            />
          </UForm>
        </ConnectPageSection>
      </div>
      <div v-else-if="primaryRep">
        <ConnectPageSection
          class="bg-white"
          :heading="{ label: tPlat('section.title.primaryRep'), labelClass: 'ml-6 font-bold' }"
        >
          <UForm
            ref="primaryRepRef"
            :schema="getContactSchema(false)"
            :state="primaryRep"
            class="space-y-10 pb-10"
          >
            <FormCommonContact
              v-model:first-name="primaryRep.firstName"
              v-model:middle-name="primaryRep.middleName"
              v-model:last-name="primaryRep.lastName"
              v-model:phone="primaryRep.phone"
              v-model:emailAddress="primaryRep.emailAddress"
              v-model:fax-number="primaryRep.faxNumber"
              v-model:position="primaryRep.position"
              id-prefix="platform-primary-rep"
              prepopulate-name
              prepopulate-type="Bceid"
              name-divider
              email-warning
            />
          </UForm>
        </ConnectPageSection>
      </div>
      <div v-if="!secondaryRep">
        <UButton
          :label="tPlat('label.addRepresentative')"
          class="px-5 py-3"
          color="primary"
          icon="i-mdi-account-plus"
          variant="outline"
          @click="secondaryRep = getNewRepresentative(false)"
        />
      </div>
      <ConnectPageSection
        v-else
        class="bg-white"
      >
        <template #header>
          <div class="flex">
            <h2 class="ml-6 grow font-bold">
              {{ tPlat('section.title.secondaryRep') }}
            </h2>
            <UButton
              :label="t('word.Remove')"
              class="px-5"
              color="red"
              trailing-icon="i-mdi-close"
              variant="outline"
              @click="secondaryRep = undefined"
            />
          </div>
        </template>
        <UForm
          ref="secondaryRepRef"
          :schema="getContactSchema(false)"
          :state="secondaryRep"
          class="space-y-10 pb-10"
        >
          <FormCommonContact
            v-model:first-name="secondaryRep.firstName"
            v-model:middle-name="secondaryRep.middleName"
            v-model:last-name="secondaryRep.lastName"
            v-model:phone="secondaryRep.phone"
            v-model:emailAddress="secondaryRep.emailAddress"
            v-model:fax-number="secondaryRep.faxNumber"
            v-model:position="secondaryRep.position"
            id-prefix="platform-secondary-rep"
            :prepopulate-name="false"
            name-divider
          />
        </UForm>
      </ConnectPageSection>
    </div>
  </div>
</template>
