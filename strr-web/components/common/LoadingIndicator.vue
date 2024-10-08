<script setup lang="ts">
const nuxtApp = useNuxtApp()

const isLoading = ref(false)

// Listen for the 'page:start' event, which is triggered when a new page is about to be loaded
nuxtApp.hook('page:start', () => {
  isLoading.value = true
})

// Listen for the 'page:finish' event, which is triggered when the page has finished loading
nuxtApp.hook('page:finish', () => {
  isLoading.value = false
})
</script>

<template>
  <div>
    <UModal
      v-model="isLoading"
      prevent-close
      :ui="{
        container: 'items-center',
        base: 'p-10',
        overlay: {
          background: 'bg-black/60'
        },
        width: 'w-[500px]',
        rounded: 'rounded-md',
        transition: {
          leaveTo: 'opacity-0 translate-y-0'
        }
      }"
    >
      <p class="mb-4">
        Loading, please wait...
      </p>
      <UProgress animation="carousel" />
    </UModal>
  </div>
</template>

<style scoped></style>
