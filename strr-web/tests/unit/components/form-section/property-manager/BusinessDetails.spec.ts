import { it, expect } from 'vitest'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { createI18n } from 'vue-i18n'
import { BcrosFormSectionPropertyManagerBusinessDetails } from '#components'

const i18n = createI18n({
  // vue-i18n options here ...
})

it('can mount Business Details component', async () => {
  const businessDetails = await mountSuspended(BcrosFormSectionPropertyManagerBusinessDetails,
    {
      global: { plugins: [i18n] }
    })
  expect(businessDetails.find('[data-test-id="property-manager-business-details"]').exists()).toBe(true)
  expect(businessDetails.find('[data-test-id="property-manager-business-name-input"]').exists()).toBe(true)
  expect(businessDetails.find('[data-test-id="property-manager-business-number-input"]').exists()).toBe(true)
})

it('has correct input placeholders', async () => {
  const { t } = useTranslation()
  const businessDetails = await mountSuspended(BcrosFormSectionPropertyManagerBusinessDetails,
    {
      global: { plugins: [i18n] }
    })
  const businessNameInput = businessDetails.find('[data-test-id="property-manager-business-name-input"]')
  const businessNumberInput = businessDetails.find('[data-test-id="property-manager-business-number-input"]')

  expect(businessNameInput.attributes('placeholder')).toBe(t('createAccount.propertyManagerForm.businessName'))
  expect(businessNumberInput.attributes('placeholder')).toBe(t('createAccount.propertyManagerForm.businessNumber'))
})

it('uses defineModel for businessName and businessNumber', async () => {
  const wrapper = await mountSuspended(BcrosFormSectionPropertyManagerBusinessDetails, {
    global: { plugins: [i18n] },
    props: {
      businessName: 'Test Business',
      businessNumber: '123456'
    }
  })

  const businessNameInput = wrapper.find('[data-test-id="property-manager-business-name-input"]')
  const businessNumberInput = wrapper.find('[data-test-id="property-manager-business-number-input"]')

  expect((businessNameInput.element as HTMLInputElement).value).toBe('Test Business')
  expect((businessNumberInput.element as HTMLInputElement).value).toBe('123456')
})
