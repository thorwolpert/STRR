<script setup lang="ts">
import { vMaska } from 'maska/vue'
import { Mask } from 'maska'
import type { ConnectPhone } from '#imports'

const phone = defineModel<ConnectPhone>({ required: true })

defineProps({
  name: { type: String, default: 'phone' }
})

const northAmericaMask = '(###) ###-####'
const otherMask = '##############'

const unmaskedvalue = ref()
const maskedPhoneNumber = ref(phone.value.number)
const inputMask = computed(() => phone.value.countryCode === '1' ? northAmericaMask : otherMask)

watchEffect(
  () => {
    const mask = new Mask({ mask: inputMask.value })
    phone.value.number = unmaskedvalue.value || mask.unmasked(maskedPhoneNumber.value || '')
  }
)

defineExpose({ unmaskedvalue })
</script>

<template>
  <div class="flex w-full max-w-bcGovInput flex-col gap-3 sm:flex-row">
    <UFormGroup :name="name + '.countryCode'" class="grow sm:max-w-[130px]">
      <ConnectPhoneNumberCountryCode
        v-model:country-calling-code="phone.countryCode"
        v-model:country-iso2="phone.countryIso2"
        :placeholder="$t('label.phone.countryCode')"
        data-testid="phone-countryCode"
      />
    </UFormGroup>
    <UFormGroup :name="name + '.number'" class="grow">
      <UInput
        v-model="maskedPhoneNumber"
        v-maska:unmaskedvalue.unmasked
        :color="maskedPhoneNumber ? 'primary' : 'gray'"
        :data-maska="inputMask"
        :placeholder="$t('label.phone.number')"
        size="lg"
        data-testid="phone-number"
      />
    </UFormGroup>
    <UFormGroup :name="name + '.extension'" class="grow sm:max-w-[170px]">
      <UInput
        v-model="phone.extension"
        class="max-w-bcGovInput"
        :placeholder="$t('label.phone.extension')"
        size="lg"
        data-testid="phone-extension"
      />
    </UFormGroup>
  </div>
</template>
