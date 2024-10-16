<script setup lang="ts">

const { t } = useI18n()

const {
  feeOptions,
  fees,
  placeholderFeeItem,
  total,
  totalServiceFees,
  totalFutureEffectiveFees,
  totalPriorityFees,
  totalProcessingFees,
  totalGst,
  totalPst
} = storeToRefs(useConnectFee())

const isPlaceholderActive = ref(false)

const feeItems = computed<ConnectFeeItem[]>(() => {
  if (fees.value && (Object.keys(fees.value).length > 0)) {
    // @ts-ignore
    isPlaceholderActive.value = false
    return Object.values(fees.value)
  }
  isPlaceholderActive.value = true
  return [placeholderFeeItem.value]
})

// folding stuff
const folded = ref(false)

const { width } = useScreenSize()
const isFoldable = computed(() => {
  const threshold = width.value < 1024
  if (!threshold) {
    folded.value = false
  }
  return threshold
})

const toggleFolded = () => {
  if (isFoldable) {
    folded.value = !folded.value
  }
}

</script>
<template>
  <div
    data-testid="fee-widget"
    class="z-10 mr-5 w-full rounded bg-white shadow-md lg:mr-0 lg:w-[320px]"
  >
    <div
      :class="`
        ${folded ? 'rounded' : 'rounded-t'}
        px-[15px] py-[10px] pt-[10px] bg-midnightBlue-900 flex flex-row justify-between
        cursor-pointer lg:cursor-auto
        `
      "
      @click="toggleFolded"
    >
      <p class="font-bold text-white">
        {{ t("feeSummary.title") }}
      </p>
      <div class="flex lg:hidden">
        <img
          src="/icons/caret.svg"
          alt="Toggle fee widget shown"
          :class="`cursor-pointer transition-all ${folded ? 'rotate-180': ''}`"
        >
      </div>
    </div>
    <div :class="`transition-all ${folded ? 'h-[0px] overflow-hidden p-[0px]': 'px-[15px] pb-[10px] '}`">
      <div
        v-for="feeItem in feeItems"
        :key="feeItem.filingTypeCode"
        class="flex flex-row justify-between border-b border-bcGovGray-300 py-[10px]"
      >
        <p class="font-bold">
          {{ t(`feeSummary.itemLabels.${feeItem.filingTypeCode}`) }}
        </p>
        <p>
          {{
            feeItem.waived
              ? t('feeSummary.noFee')
              : !feeItem.isPlaceholder ? `$${feeItem.filingFees.toFixed(2)}` : '$ -' }}
        </p>
      </div>
      <ConnectFeeExtraFee
        v-if="feeOptions.showFutureEffectiveFees"
        :description="t('feeSummary.futureEffectiveFees')"
        :fee="totalFutureEffectiveFees"
        :show-fee-value="isPlaceholderActive"
      />
      <ConnectFeeExtraFee
        v-if="feeOptions.showPriorityFees"
        :description="t('feeSummary.priorityFees')"
        :fee="totalPriorityFees"
        :show-fee-value="isPlaceholderActive"
      />
      <ConnectFeeExtraFee
        v-if="feeOptions.showProcessingFees"
        :description="t('feeSummary.processingFees')"
        :fee="totalProcessingFees"
        :show-fee-value="isPlaceholderActive"
      />
      <ConnectFeeExtraFee
        v-if="feeOptions.showServiceFees"
        :description="t('feeSummary.serviceFees')"
        :fee="isPlaceholderActive ? placeholderFeeItem.serviceFees : totalServiceFees"
        show-fee-value
      />
      <ConnectFeeExtraFee
        v-if="feeOptions.showPst"
        :description="t('feeSummary.pst')"
        :fee="totalPst"
        :show-fee-value="isPlaceholderActive"
      />
      <ConnectFeeExtraFee
        v-if="feeOptions.showGst"
        :description="t('feeSummary.gst')"
        :fee="totalGst"
        :show-fee-value="isPlaceholderActive"
      />
      <div class="flex flex-row items-end justify-between py-[10px] text-sm" aria-label="null">
        <p class="mb-1 font-bold">
          {{ t("feeSummary.total") }}
        </p>
        <p class="flex items-end text-sm text-bcGovGray-700">
          <span class="mb-1">{{ t("currency.cad") }}</span>
          <b class="ml-[5px] flex items-end text-2xl text-black">
            {{ !isPlaceholderActive ? `$${total.toFixed(2)}` : '$ -' }}
          </b>
        </p>
      </div>
    </div>
  </div>
</template>
