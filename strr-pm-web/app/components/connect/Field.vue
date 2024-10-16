<script setup lang="ts">
import { type UseEventBusReturn } from '@vueuse/core'
import { normalizeInput } from '~/utils/connect-validation'

const formBus = inject<UseEventBusReturn<any, string> | undefined>('form-events', undefined)

const model = defineModel({ type: String, default: '' })
const emit = defineEmits<{(e: 'update:modelValue', value: string): void }>()

const props = defineProps({
  label: { type: String, default: '' },
  placeholder: { type: String, default: '' },
  id: { type: String, required: true },
  name: { type: String, default: 'name.fullName' },
  help: { type: String, default: '' },
  isDisabled: { type: Boolean, default: false },
  wrapWithFormGrp: { type: Boolean, default: true }
})

watch(model, () => {
  formBus?.emit({ type: 'blur', path: props.name })
  formBus?.emit({ type: 'change', path: props.name })
}, { deep: true })

const normalize = () => {
  const normalizedValue = normalizeInput(model.value)
  emit('update:modelValue', normalizedValue)
}
</script>

<template>
  <UFormGroup v-if="wrapWithFormGrp" :label="label" :name="name" :help="help">
    <UInput
      :id="id"
      class="max-w-bcGovInput"
      :color="model ? 'primary' : 'gray'"
      type="text"
      v-bind="$attrs"
      :value="model"
      :placeholder="placeholder"
      :disabled="isDisabled"
      size="lg"
      @input="$emit('update:modelValue', $event.target.value)"
      @blur="normalize"
    />
  </UFormGroup>
  <UInput
    v-else
    :id="id"
    class="max-w-bcGovInput"
    :color="model ? 'primary' : 'gray'"
    type="text"
    v-bind="$attrs"
    :value="model"
    :placeholder="placeholder"
    :disabled="isDisabled"
    size="lg"
    @input="$emit('update:modelValue', $event.target.value)"
    @blur="normalize"
  />
</template>
