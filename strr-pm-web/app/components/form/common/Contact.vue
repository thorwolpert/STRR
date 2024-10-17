<script setup lang="ts">
const { t } = useI18n()

const tPlat = (path: string) => t(`platform.${path}`)

const fullName = defineModel<string>('fullName', { required: false })
const preferredName = defineModel<string>('preferredName', { required: false })
const firstName = defineModel<string>('firstName', { required: false })
const middleName = defineModel<string>('middleName', { required: false })
const lastName = defineModel<string>('lastName', { required: false })
const position = defineModel<string>('position', { required: false })
const faxNumber = defineModel<string>('faxNumber', { required: false })
const emailAddress = defineModel<string>('emailAddress', { required: false })
const phone = defineModel<ConnectPhone>('phone', { required: false })

defineProps<{
  idPrefix: string,
  prepopulateName: boolean,
  prepopulateType?: 'Bcsc' | 'Bceid'
  sectionInfo?: string
  nameDivider?: boolean
  emailWarning?: boolean
}>()

</script>

<template>
  <div class="space-y-10">
    <ConnectSection v-if="prepopulateName" :title="tPlat('section.subTitle.yourName')">
      <p class="font-bold">
        <span v-if="fullName">{{ fullName }}</span>
        <span v-else>{{ firstName }} {{ lastName }}</span>
      </p>
      <p v-if="prepopulateType" class="text-sm">
        {{ tPlat(`text.yourName${prepopulateType}`) }}
      </p>
    </ConnectSection>
    <ConnectSection v-else :title="tPlat('section.subTitle.contactName')">
      <div class="space-y-5">
        <p v-if="sectionInfo" class="mt-1 text-sm">
          {{ sectionInfo }}
        </p>
        <ConnectField
          v-if="fullName !== undefined"
          :id="idPrefix + '-full-name'"
          v-model="fullName"
          :aria-label="t('label.fullName')"
          name="fullName"
          :placeholder="t('label.fullName')"
        />
        <div v-else class="flex max-w-bcGovInput flex-col gap-3 sm:flex-row">
          <ConnectField
            v-if="firstName !== undefined"
            :id="idPrefix + '-first-name'"
            v-model="firstName"
            class="grow"
            :aria-label="t('label.firstName')"
            name="firstName"
            :placeholder="t('label.firstName')"
          />
          <ConnectField
            v-if="middleName !== undefined"
            :id="idPrefix + '-middle-name'"
            v-model="middleName"
            class="grow"
            :aria-label="t('label.middleName')"
            name="middleName"
            :placeholder="t('label.middleNameOpt')"
          />
          <ConnectField
            v-if="lastName !== undefined"
            :id="idPrefix + '-last-name'"
            v-model="lastName"
            class="grow"
            :aria-label="t('label.lastName')"
            name="lastName"
            :placeholder="t('label.lastName')"
          />
        </div>
        <ConnectField
          v-if="preferredName !== undefined"
          :id="idPrefix + '-preferred-name'"
          v-model="preferredName"
          name="preferredName"
          :placeholder="$t('label.preferredName')"
          :help="$t('text.preferredName.hint')"
          data-testid="preferredName"
        />
      </div>
    </ConnectSection>
    <div v-if="nameDivider" class="h-px w-full border-b border-gray-100" />
    <ConnectSection :title="tPlat('section.subTitle.contactDetails')">
      <div class="space-y-5">
        <ConnectField
          v-if="position !== undefined"
          :id="idPrefix + '-position'"
          v-model="position"
          :aria-label="t('label.positionTitle')"
          :help="t('platform.text.positionTitle')"
          name="position"
          :placeholder="t('label.positionTitle')"
        />
        <ConnectPhoneNumber v-if="phone" v-model="phone" />
        <ConnectField
          v-if="faxNumber !== undefined"
          :id="idPrefix + '-fax-number'"
          v-model="faxNumber"
          :aria-label="t('createAccount.contactForm.faxNumber')"
          name="faxNumber"
          :placeholder="t('createAccount.contactForm.faxNumber')"
        />
        <ConnectField
          v-if="emailAddress !== undefined"
          :id="idPrefix + '-party-email'"
          v-model="emailAddress"
          :aria-label="t('label.emailAddress')"
          name="emailAddress"
          :placeholder="t('label.emailAddress')"
        />
        <EmailAlert v-if="emailWarning" />
      </div>
    </ConnectSection>
  </div>
</template>
