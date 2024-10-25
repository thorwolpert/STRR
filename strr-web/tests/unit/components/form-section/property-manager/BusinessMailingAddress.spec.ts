import { it, expect } from 'vitest'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { createI18n } from 'vue-i18n'
import { mockFn } from '@nuxt/test-utils'
import { BcrosFormSectionPropertyManagerBusinessMailingAddress } from '#components'

const i18n = createI18n({
  // vue-i18n options here ...
})

it('can mount Business Mailing Address component', async () => {
  const businessMailingAddress = await mountSuspended(BcrosFormSectionPropertyManagerBusinessMailingAddress,
    {
      global: { plugins: [i18n] },
      props: {
        id: 'propertyManagerBusinessAddress',
        defaultCountryIso2: 'CA',
        enableAddressComplete: mockFn,
        errors: {}
      }
    })
  expect(businessMailingAddress.find('[data-test-id="property-manager-business-address"]').exists()).toBe(true)
  expect(businessMailingAddress.find('[data-test-id="property-manager-country-select"]').exists()).toBe(true)
  expect(businessMailingAddress.find('[data-test-id="property-manager-address-input"]').exists()).toBe(true)
  expect(businessMailingAddress.find('[data-test-id="property-manager-address-line-two-input"]').exists()).toBe(true)
  expect(businessMailingAddress.find('[data-test-id="property-manager-city-input"]').exists()).toBe(true)
  expect(businessMailingAddress.find('[data-test-id="property-manager-postal-code-input"]').exists()).toBe(true)
})

it('shows province select for CA and US', async () => {
  const businessMailingAddress = await mountSuspended(BcrosFormSectionPropertyManagerBusinessMailingAddress,
    {
      global: { plugins: [i18n] },
      props: {
        id: 'propertyManagerBusinessAddress',
        defaultCountryIso2: 'CA',
        enableAddressComplete: mockFn,
        errors: {}
      }
    })
  expect(businessMailingAddress.find('[data-test-id="property-manager-province-select"]').exists()).toBe(true)
  expect(businessMailingAddress.find('[data-test-id="property-manager-province-input"]').exists()).toBe(false)
})

it('shows province input for other countries', async () => {
  const businessMailingAddress = await mountSuspended(BcrosFormSectionPropertyManagerBusinessMailingAddress,
    {
      global: { plugins: [i18n] },
      props: {
        id: 'propertyManagerBusinessAddress',
        defaultCountryIso2: 'FR',
        enableAddressComplete: mockFn,
        errors: {}
      }
    })
  expect(businessMailingAddress.find('[data-test-id="property-manager-province-select"]').exists()).toBe(false)
  expect(businessMailingAddress.find('[data-test-id="property-manager-province-input"]').exists()).toBe(true)
})
