import { it, expect } from 'vitest'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { createI18n } from 'vue-i18n'
import { BcrosFormSectionContactName } from '#components'

const i18n = createI18n({
  // vue-i18n options here ...
})
let wrapper: any

it('can mount Contact Name component', async () => {
  wrapper = await mountSuspended(BcrosFormSectionContactName,
    {
      global: { plugins: [i18n] },
      props: {}
    }
  )
  expect(wrapper.findTestId('form-section-contact-name').exists()).toBe(true)
  expect(wrapper.findTestId('contact-first-name-input').exists()).toBe(true)
  expect(wrapper.findTestId('contact-middle-name-input').exists()).toBe(true)
  expect(wrapper.findTestId('contact-last-name-input').exists()).toBe(true)
  expect(wrapper.findTestId('property-manager-preferred-name-input').exists()).toBe(true)
})
