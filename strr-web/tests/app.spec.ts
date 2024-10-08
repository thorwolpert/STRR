import { expect, describe, test } from 'vitest'
import { VueWrapper } from '@vue/test-utils'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { mockI18n } from '~/tests/mocks/mockI18n'
import app from '~/app.vue'
import LoadingIndicator from '~/components/common/LoadingIndicator.vue'
import Header from '~/components/bcros/header/Header.vue'
import Footer from '~/components/bcros/footer/Footer.vue'
import Breadcrumb from '~/components/Breadcrumb.vue'

describe('App level test', () => {
  let wrapper: VueWrapper<any>

  beforeEach(async () => {
    wrapper = await mountSuspended(app, { global: { plugins: [mockI18n] } })
  })
  afterEach(() => { wrapper.unmount() })

  test('app initializes with layouts and default page', () => {
    expect(wrapper.findComponent(LoadingIndicator).exists()).toBe(true)
    expect(wrapper.findComponent(Header).exists()).toBe(true)
    expect(wrapper.findComponent(Footer).exists()).toBe(true)
    expect(wrapper.findComponent(Breadcrumb).exists()).toBeTruthy()
  })
})
