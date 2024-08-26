<template>
  <div data-test-id="default-layout">
    <div class="flex justify-between flex-col min-h-screen">
      <BcrosHeader />
      <div class="flex grow justify-center">
        <div class="grow desktop:px-[56px] pt-[75px] mobile:pt-[20px] max-w-[1360px]">
          <NuxtPage class="px-4" />
        </div>
      </div>
      <BcrosFooter :extra-space="true" />
    </div>
  </div>
</template>
