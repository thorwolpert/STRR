<script setup lang="ts">
const {
  loading,
  title,
  subtitles,
  details,
  sideDetails,
  bottomButtons
} = storeToRefs(useConnectDetailsHeaderStore())
</script>

<template>
  <div class="bg-white py-5" data-testid="connect-details-header">
    <div class="app-inner-container">
      <div v-if="loading" class="flex animate-pulse flex-col gap-2 sm:flex-row">
        <div class="grow space-y-2">
          <div class="h-9 w-[400px] rounded bg-gray-200" />
          <div class="h-5 w-[250px] rounded bg-gray-200" />
          <div class="h-5 w-[200px] rounded bg-gray-200" />
          <div class="h-5 w-[150px] rounded bg-gray-200" />
        </div>
        <div class="space-y-2">
          <div class="h-5 w-[300px] rounded bg-gray-200" />
          <div class="h-5 w-[300px] rounded bg-gray-200" />
          <div class="h-5 w-[300px] rounded bg-gray-200" />
          <div class="h-5 w-[300px] rounded bg-gray-200" />
        </div>
      </div>
      <div v-else class="flex flex-col gap-2 sm:flex-row">
        <div class="grow space-y-4">
          <div class="space-y-2">
            <ConnectTypographyH1 v-if="title" :text="title" />
            <div v-if="subtitles.length" class="flex divide-x *:border-gray-500 *:px-2 first:*:pl-0">
              <p v-for="subtitle in subtitles" :key="subtitle" class="text-sm">
                {{ subtitle }}
              </p>
            </div>
          </div>
          <div class="space-y-2">
            <slot name="details">
              <p v-if="details" class="text-sm">
                {{ details }}
              </p>
            </slot>
            <slot name="buttons">
              <div v-if="bottomButtons.length" class="flex flex-wrap gap-2">
                <UButton
                  v-for="btn in bottomButtons"
                  :key="btn.label"
                  :label="btn.label"
                  :icon="btn.icon"
                  class="pl-0"
                  color="primary"
                  variant="link"
                  @click="btn.action()"
                />
              </div>
            </slot>
          </div>
        </div>
        <dl class="mr-14 space-y-1 text-sm">
          <template v-for="detail in sideDetails" :key="detail.label">
            <div>
              <UTooltip
                :close-delay="100"
                :popper="{ placement: 'right', arrow: false, offsetDistance: 0 }"
                :ui="{ background: 'bg-transparent', container: 'opacity-100', shadow: 'shadow-none' }"
              >
                <div class="flex flex-row flex-wrap gap-2">
                  <dt class="font-bold" :class="[detail.edit?.isEditing && 'mt-1']">
                    {{ detail.label }}:
                  </dt>
                  <dd v-if="!detail.edit?.isEditing">
                    {{ detail.value }}
                  </dd>
                  <UFormGroup
                    v-else
                    :name="detail.label"
                    :error="detail.edit?.validation?.error || undefined"
                    size="xs"
                  >
                    <UInput
                      v-model="detail.value"
                      size="2xs"
                      @change="detail.edit.validation
                        ? detail.edit.validation.error = detail.edit?.validation?.validate($event)
                        : console.info('no validation')"
                    />
                  </UFormGroup>
                </div>
                <template #text>
                  <UButton
                    v-if="detail.edit"
                    icon="i-mdi-edit"
                    :label="!detail.edit.isEditing ? $t('word.Edit') : $t('word.Save')"
                    :padded="false"
                    variant="link"
                    @click="detail.edit.isEditing = !detail.edit.isEditing"
                  />
                </template>
              </UTooltip>
            </div>
          </template>
        </dl>
      </div>
    </div>
  </div>
</template>
