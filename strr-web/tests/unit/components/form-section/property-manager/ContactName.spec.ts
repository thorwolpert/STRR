import { it, expect } from 'vitest'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { createI18n } from 'vue-i18n'
import { BcrosFormSectionPropertyManagerContactName } from '#components'

const i18n = createI18n({
  // vue-i18n options here ...
})

it('can mount Contact Name component', async () => {
  const contactName = await mountSuspended(BcrosFormSectionPropertyManagerContactName,
    {
      global: { plugins: [i18n] },
      props: {
        errors: {}
      }
    })
  expect(contactName.find('[data-test-id="property-manager-contact-name"]').exists()).toBe(true)
  expect(contactName.find('[data-test-id="property-manager-first-name-input"]').exists()).toBe(true)
  expect(contactName.find('[data-test-id="property-manager-middle-name-input"]').exists()).toBe(true)
  expect(contactName.find('[data-test-id="property-manager-last-name-input"]').exists()).toBe(true)
  expect(contactName.find('[data-test-id="property-manager-preferred-name-input"]').exists()).toBe(true)
})

it('emits events on input changes', async () => {
  const contactName = await mountSuspended(BcrosFormSectionPropertyManagerContactName,
    {
      global: { plugins: [i18n] },
      props: {
        errors: {}
      }
    })

  const firstNameInput = contactName.find('[data-test-id="property-manager-first-name-input"]')
  await firstNameInput.trigger('input')
  expect(contactName.emitted('resetFieldError')).toBeTruthy()

  await firstNameInput.trigger('blur')
  expect(contactName.emitted('validateField')).toBeTruthy()

  const lastNameInput = contactName.find('[data-test-id="property-manager-last-name-input"]')
  await lastNameInput.trigger('input')
  expect(contactName.emitted('resetFieldError')).toBeTruthy()

  await lastNameInput.trigger('blur')
  expect(contactName.emitted('validateField')).toBeTruthy()
})

it('does not emit events for middle name and preferred name inputs', async () => {
  const contactName = await mountSuspended(BcrosFormSectionPropertyManagerContactName,
    {
      global: { plugins: [i18n] },
      props: {
        errors: {}
      }
    })

  const middleNameInput = contactName.find('[data-test-id="property-manager-middle-name-input"]')
  await middleNameInput.trigger('input')
  await middleNameInput.trigger('blur')

  const preferredNameInput = contactName.find('[data-test-id="property-manager-preferred-name-input"]')
  await preferredNameInput.trigger('input')
  await preferredNameInput.trigger('blur')

  expect(contactName.emitted('resetFieldError')).toBeFalsy()
  expect(contactName.emitted('validateField')).toBeFalsy()
})
