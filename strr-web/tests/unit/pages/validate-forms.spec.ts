import { mountSuspended } from '@nuxt/test-utils/runtime'
import { flushPromises } from '@vue/test-utils'
import Stepper from '~/components/bcros/stepper/Stepper.vue'
import CreateApplication from '@/pages/create-account.vue'
import {
  BcrosFormSectionBusinessDetails,
  BcrosFormSectionContactDetails,
  BcrosFormSectionContactInformationForm,
  BcrosFormSectionContactName,
  BcrosFormSectionPropertyForm,
  BcrosFormSectionPropertyManagerBusinessMailingAddress,
  BcrosFormSectionPropertyManagerForm,
  UForm
} from '#components'

const FIELD_ERROR = '.data-field-error' // css of the field error

// Define required fields for Property Manager
const PROPERTY_MANAGER_REQUIRED_FIELDS = [
  'address',
  'city',
  'province',
  'postal code',
  'first name',
  'last name',
  'phone number',
  'email'
]

// Define required fields for Individual Host Type
const INDIVIDUAL_HOST_REQUIRED_FIELDS = [
  'first name',
  'last name',
  'dob day',
  'dob month',
  'dob year',
  'sin',
  'phone number',
  'email',
  'address',
  'city',
  'province',
  'postal code'
]

// Define required fields for Business Host Type
const BUSINESS_HOST_REQUIRED_FIELDS = [
  'business legal name',
  'first name',
  'last name',
  'phone number',
  'email',
  'address',
  'city',
  'province',
  'postal code'
]

// Define required fields for Property Details
const PROPERTY_DETAILS_REQUIRED_FIELDS = [
  'space type',
  'is on principal residence',
  'type of property',
  'ownership type',
  'rental unit street number',
  'rental unit street name',
  'rental unit city',
  'rental unit postal code'
]

describe('Rental Application Validations', () => {
  let wrapper: any

  // go to specific step in Stepper
  const goToStep = async (stepNumber: number) => {
    const stepId = `[data-test-id=step-index-${stepNumber - 1}]`
    wrapper.findComponent(Stepper).find(stepId).trigger('click')
    await nextTick()
    await flushPromises()
  }

  beforeAll(async () => {
    wrapper = await mountSuspended(CreateApplication)
    // go thru all steps to trigger validations
    await goToStep(2)
    await goToStep(3)
    await goToStep(4)
    await goToStep(5)
  })

  it('should validate Step 1 - Property Manager', async () => {
    await goToStep(1)

    const propertyManager = wrapper.findComponent(BcrosFormSectionPropertyManagerForm)

    expect(propertyManager.findAll(FIELD_ERROR)).toHaveLength(PROPERTY_MANAGER_REQUIRED_FIELDS.length)

    // business mailing address
    expect(propertyManager.findComponent(BcrosFormSectionPropertyManagerBusinessMailingAddress).exists()).toBe(true)
    propertyManager.findTestId('property-manager-address-input').setValue('123 Main St')
    propertyManager.findTestId('property-manager-city-input').setValue('Vancouver')
    propertyManager.findTestId('property-manager-province-select').setValue('BC')
    propertyManager.findTestId('property-manager-postal-code-input').setValue('V6A1A1')

    // contact name
    expect(propertyManager.findComponent(BcrosFormSectionContactName).exists()).toBe(true)
    propertyManager.findTestId('contact-first-name-input').setValue('John')
    propertyManager.findTestId('contact-last-name-input').setValue('Doe')

    // contact details
    expect(propertyManager.findComponent(BcrosFormSectionContactDetails).exists()).toBe(true)
    propertyManager.findTestId('phone-number').setValue('123-456-7890')
    propertyManager.findTestId('email-address').setValue('abc@abc.com')

    // validate form
    await propertyManager.findComponent(UForm).vm.validate(null, { silent: true })

    // there should be no errors after all required fields populated
    expect(propertyManager.findTestId('property-manager-form').findAll(FIELD_ERROR)).toHaveLength(0)
  })

  it('should validate Step 2 - Host Information', async () => {
    await goToStep(2)

    const hostInformation = wrapper.findComponent(BcrosFormSectionContactInformationForm)

    expect(hostInformation.findAll(FIELD_ERROR)).toHaveLength(INDIVIDUAL_HOST_REQUIRED_FIELDS.length)

    // switch to Business type
    formState.primaryContact.contactType = HostContactTypeE.BUSINESS
    await nextTick()
    await flushPromises()

    expect(hostInformation.findComponent(BcrosFormSectionBusinessDetails).exists()).toBe(true)
    expect(hostInformation.findComponent(BcrosFormSectionContactName).exists()).toBe(true)

    expect(hostInformation.findAll(FIELD_ERROR)).toHaveLength(BUSINESS_HOST_REQUIRED_FIELDS.length)

    // populate fields to trigger validations and reset errors
    hostInformation.findTestId('business-legal-name-input').setValue('Acme Corporation')

    hostInformation.findTestId('contact-first-name-input').setValue('John')
    hostInformation.findTestId('contact-last-name-input').setValue('Doe')

    hostInformation.findTestId('phone-number').setValue('1234567890')
    hostInformation.findTestId('email-address').setValue('john.doe@example.com')

    // mailing address
    hostInformation.findTestId('contact-info-address-input').setValue('123 Main St')
    hostInformation.findTestId('contact-info-city-input').setValue('Vancouver')
    hostInformation.findTestId('contact-info-province-input').setValue('BC')
    hostInformation.findTestId('contact-info-postal-code-input').setValue('V6A1A1')

    // validate form
    await hostInformation.findComponent(UForm).vm.validate(null, { silent: true })

    // there should be no errors after all required fields populated
    expect(hostInformation.findTestId('host-information-form').findAll(FIELD_ERROR)).toHaveLength(0)
  })

  it.only('should validate Step 3 - Property Details', async () => {
    await goToStep(3)

    const propertyDetails = wrapper.findComponent(BcrosFormSectionPropertyForm)

    expect(propertyDetails.findAll(FIELD_ERROR)).toHaveLength(PROPERTY_DETAILS_REQUIRED_FIELDS.length)

    // populate fields to trigger validations and reset errors
    propertyDetails.findTestId('rental-unit-space-type-select').setValue(RentalUnitSpaceTypeE.ENTIRE_HOME)
    propertyDetails.findTestId('rental-unit-principal-residence-select').setValue('true')
    await nextTick() // wait for dynamic Host Residence field to show up
    propertyDetails.findTestId('rental-unit-host-residence-select').setValue(HostResidenceE.SAME_UNIT)

    propertyDetails.findTestId('rental-unit-type-select').setValue(PropertyTypeE.SINGLE_FAMILY_HOME)
    propertyDetails.findTestId('rental-unit-ownership-type-select').setValue(OwnershipTypeE.RENT)
    propertyDetails.findTestId('rental-unit-pid').setValue('111-222-333') // not a required field

    // // mailing address
    propertyDetails.findTestId('address-street-number').setValue('123')
    propertyDetails.findTestId('address-street-name').setValue('Main St.')
    propertyDetails.findTestId('address-unit-number').setValue('55') // not a required field
    propertyDetails.findTestId('address-line-two').setValue('Basement Unit') // not a required field
    propertyDetails.findTestId('address-city').setValue('Vancouver')
    propertyDetails.findTestId('address-postal-code').setValue('V6A1A1')

    // validate form
    await propertyDetails.findComponent(UForm).vm.validate(null, { silent: true })

    // there should be no errors after all required fields populated
    expect(propertyDetails.findTestId('property-form-section').findAll(FIELD_ERROR)).toHaveLength(0)
  })
})
