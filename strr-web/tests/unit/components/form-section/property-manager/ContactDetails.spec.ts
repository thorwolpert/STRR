import { it, expect } from 'vitest'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { createI18n } from 'vue-i18n'
import { BcrosFormSectionPropertyManagerContactDetails, BcrosAlertsMessage } from '#components'

const i18n = createI18n({
  // vue-i18n options here ...
})

it('can mount Contact Details component', async () => {
  const contactDetails = await mountSuspended(BcrosFormSectionPropertyManagerContactDetails,
    {
      global: { plugins: [i18n] },
      props: {
        errors: {}
      }
    })
  expect(contactDetails.find('[data-test-id="property-manager-contact-details"]').exists()).toBe(true)
  expect(contactDetails.find('[data-test-id="property-manager-phone-number"]').exists()).toBe(true)
  expect(contactDetails.find('[data-test-id="property-manager-extension"]').exists()).toBe(true)
  expect(contactDetails.find('[data-test-id="property-manager-fax-number"]').exists()).toBe(true)
  expect(contactDetails.find('[data-test-id="property-manager-email-address"]').exists()).toBe(true)
  expect(contactDetails.findComponent(BcrosAlertsMessage).exists()).toBe(true)
})

it('emits events on input changes', async () => {
  const contactDetails = await mountSuspended(BcrosFormSectionPropertyManagerContactDetails,
    {
      global: { plugins: [i18n] },
      props: {
        errors: {}
      }
    })
  await contactDetails.find('[data-test-id="property-manager-phone-number"]').trigger('input')
  expect(contactDetails.emitted('resetFieldError')).toBeTruthy()
  await contactDetails.find('[data-test-id="property-manager-phone-number"]').trigger('blur')
  expect(contactDetails.emitted('validateField')).toBeTruthy()
})
