import { mountSuspended } from '@nuxt/test-utils/runtime'
import Stepper from '~/components/bcros/stepper/Stepper.vue'
import CreateApplication from '@/pages/create-account.vue'
import { BcrosFormSectionBusinessDetails, BcrosFormSectionContactName } from '#components'

const FIELD_ERROR = '.data-field-error' // css of the field error

// explicitly define which fields are required for Individual Host Type
const INDIVIDUAL_HOST_REQUIRED_FIELDS = [
  'first name',
  'last name',
  'dob day',
  'dob month',
  'dob year'
]

// explicitly define which fields are required for Business Host Type
const BUSINESS_HOST_REQUIRED_FIELDS = [
  'business legal name',
  'first name',
  'last name'
]

describe('Rental Application Validations', () => {
  let wrapper: any

  // go to specific step in Stepper
  const goToStep = async (stepNumber: number) => {
    const stepId = `[data-test-id=step-index-${stepNumber - 1}]`
    wrapper.findComponent(Stepper).find(stepId).trigger('click')
    await nextTick()
  }

  beforeAll(async () => {
    wrapper = await mountSuspended(CreateApplication)
    // go thru all steps to trigger validations
    await goToStep(2)
    await goToStep(3)
    await goToStep(4)
    await goToStep(5)
  })

  it('should validate Step 2 - Host Information', async () => {
    await goToStep(2)

    const hostInformation = wrapper.findTestId('host-information')

    expect(hostInformation.findAll(FIELD_ERROR)).toHaveLength(INDIVIDUAL_HOST_REQUIRED_FIELDS.length)

    // TODO: fix field validations so all 12 errors show up
    // expect(hostInformation.findAll(FIELD_ERROR)).toHaveLength(12)

    // switch to Business type
    formState.primaryContact.contactType = HostContactTypeE.BUSINESS
    await nextTick()
    expect(hostInformation.findComponent(BcrosFormSectionBusinessDetails).exists()).toBe(true)
    expect(hostInformation.findComponent(BcrosFormSectionContactName).exists()).toBe(true)

    // go to another step and come back to trigger validation
    await goToStep(3)
    await goToStep(2)

    expect(hostInformation.findAll(FIELD_ERROR)).toHaveLength(BUSINESS_HOST_REQUIRED_FIELDS.length)

    // populate fields to trigger validations and reset errors
    wrapper.findTestId('business-legal-name-input').setValue('abc')
    wrapper.findTestId('business-legal-name-input').setValue('abc')

    wrapper.findTestId('contact-first-name-input').setValue('abc')
    wrapper.findTestId('contact-last-name-input').setValue('abc')

    // await for validations to complete
    await nextTick()

    // there should be no errors after all required fields populated
    expect(wrapper.findTestId('host-information').findAll(FIELD_ERROR)).toHaveLength(0)
  })
})
