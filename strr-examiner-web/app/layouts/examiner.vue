<script setup lang="ts">
import { useExaminerStore } from '~/store/examiner'

const { isAuthenticated } = useKeycloak()
const headerOptions = useAppConfig().connect.core.header.options
provide(headerOptionsSymbol, headerOptions)
const localePath = useLocalePath()

const { getNextApplication } = useExaminerStore()

const items = [{
  key: 'dashboard',
  label: 'Dashboard',
  icon: 'i-mdi-list-box-outline',
  path: '/dashboard'
}, {
  key: 'examine',
  label: 'Examine',
  icon: 'i-mdi-file-search-outline',
  path: '/dashboard'
}]

async function onChange (index: number) {
  const item = items[index]

  const nextApp = await getNextApplication()
  const navigateToPath = index === 0 ? item.path : `${item?.path}/${nextApp}`
  return navigateTo(localePath(navigateToPath))
}

</script>
<template>
  <div>
    <ConnectHeaderWrapper>
      <div class="flex items-center justify-between">
        <ConnectHeaderLogoHomeLink />
        <UTabs
          v-if="isAuthenticated"
          :items="items"
          :ui="{
            wrapper: 'relative h-full space-y-0',
            list: {
              padding: 'p-0',
              height: 'h-14',
              rounded: 'rounded-none',
              tab: {
                rounded: 'rounded-none',
                height: 'h-full'
              }
            }
          }"
          @change="onChange"
        />
        <ClientOnly>
          <div class="flex gap-1">
            <ConnectHeaderAuthenticatedOptions v-if="isAuthenticated" />
            <ConnectHeaderUnauthenticatedOptions v-else />
            <ConnectLocaleSelect v-if="headerOptions.localeSelect" />
          </div>
        </ClientOnly>
      </div>
    </ConnectHeaderWrapper>

    <ConnectSystemBanner />

    <main class="app-inner-container app-body">
      <slot />
    </main>
    <ConnectFooter />
  </div>
</template>
