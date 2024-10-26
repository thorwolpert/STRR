<script setup lang="ts">
import type { Form } from '#ui/types'
import { z } from 'zod'
const { t } = useI18n()

const props = defineProps<{ isComplete: boolean }>()

const {
  compPartySchema,
  primaryRepSchema,
  secondaryRepSchema,
  getNewRepresentative
} = useStrrPlatformContact()
const {
  isCompletingPartyRep,
  completingParty,
  primaryRep,
  secondaryRep
} = storeToRefs(useStrrPlatformContact())

type CompletingPartySchema = z.output<typeof compPartySchema>
type PrimaryRepSchema = z.output<typeof primaryRepSchema>
type SecondaryRepSchema = z.output<typeof secondaryRepSchema>

const compPartyFormRef = ref<Form<CompletingPartySchema>>()
const primaryRepFormRef = ref<Form<PrimaryRepSchema>>()
const secondaryRepFormRef = ref<Form<SecondaryRepSchema>>()

const radioOptions = [
  { value: true, label: t('word.Yes') },
  { value: false, label: t('word.No') }
]

watch(isCompletingPartyRep, (val) => {
  primaryRep.value = getNewRepresentative(val)
})

onMounted(async () => {
  // validate form if step marked as complete
  if (props.isComplete) {
    // validate all form refs
    const validations = [
      validateForm(compPartyFormRef.value, props.isComplete),
      validateForm(primaryRepFormRef.value, props.isComplete),
      validateForm(secondaryRepFormRef.value, props.isComplete)
    ]
    await Promise.all(validations) // remove this if adding the scroll into view stuff

    // TODO: implement ? leaving this here for reference
    // disabled scrolling to errors as validation results must be sorted
    // in order to match the form input order for the first element to be consistently correct

    // get all errors and filter out undefined results (secondary rep form validate might return undefined)
    // const validationResults = (await Promise.all(validations)).filter(item => item !== undefined)

    // if (validationResults.length > 0) {
    //   const firstError = validationResults[0]?.[0]?.path // get first error found
    //   if (firstError) {
    //     focusAndScrollToInputByName(firstError)
    //   }
    // }
  }
})
</script>

<template>
  <div data-testid="contact-information" class="space-y-10">
    <URadioGroup
      id="completing-party-radio-group"
      v-model="isCompletingPartyRep"
      :class="isComplete && isCompletingPartyRep === undefined ? 'border-red-600 border-2 p-2' : 'p-2'"
      :legend="$t('platform.text.isUserRep')"
      :options="radioOptions"
      :ui="{ legend: 'mb-3 text-default font-bold text-gray-700' }"
      :ui-radio="{ inner: 'space-y-2' }"
    />
    <div v-if="isCompletingPartyRep !== undefined" class="space-y-10">
      <ConnectPageSection
        v-if="!isCompletingPartyRep"
        class="bg-white"
        :heading="{ label: $t('platform.section.title.completingParty'), labelClass: 'font-bold md:ml-6' }"
      >
        <UForm
          ref="compPartyFormRef"
          :schema="compPartySchema"
          :state="completingParty"
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
            :error-details="hasFormErrors(compPartyFormRef, ['phone.countryCode', 'phone.number', 'email'])"
          />
        </UForm>
      </ConnectPageSection>
      <ConnectPageSection
        v-if="primaryRep"
        class="bg-white"
        :heading="{ label: $t('platform.section.title.primaryRep'), labelClass: 'font-bold md:ml-6' }"
      >
        <UForm
          ref="primaryRepFormRef"
          :schema="primaryRepSchema"
          :state="primaryRep"
          class="space-y-10"
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
            :prepopulate-name="isCompletingPartyRep"
            prepopulate-type="Bceid"
            email-warning
            :section-info="isCompletingPartyRep ? undefined : $t('platform.text.primaryContact')"
            :error-name="hasFormErrors(primaryRepFormRef, ['firstName', 'lastName'])"
            :error-details="
              hasFormErrors(primaryRepFormRef, ['position', 'phone.countryCode', 'phone.number', 'email'])
            "
          />
        </UForm>
      </ConnectPageSection>
      <div v-if="!secondaryRep">
        <UButton
          :label="$t('platform.label.addRepresentative')"
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
              {{ $t('platform.section.title.secondaryRep') }}
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
          ref="secondaryRepFormRef"
          :schema="secondaryRepSchema"
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
            :error-name="hasFormErrors(secondaryRepFormRef, ['firstName', 'lastName'])"
            :error-details="
              hasFormErrors(secondaryRepFormRef, ['position', 'phone.countryCode', 'phone.number', 'email'])
            "
          />
        </UForm>
      </ConnectPageSection>
    </div>
  </div>
</template>
<style>
/* smooth scroll not working without this, add to layer? */
html {
  scroll-behavior: smooth;
}
</style>
