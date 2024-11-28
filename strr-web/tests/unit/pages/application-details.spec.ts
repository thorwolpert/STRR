import { mountSuspended } from '@nuxt/test-utils/runtime'
import { ref } from 'vue'
import ApplicationDetails from '@/pages/application-details/[id]/index.vue'
import {
  mockApplicationApproved,
  mockApplicationPaymentDue,
  mockApplicationApprovedWithSecondaryContact,
  mockApplicationApprovedWithDocuments
} from '~/tests/mocks/mockApplication'

import { BcrosFormSectionReviewItem } from '#components'

const { t } = useTranslation()
const tApplicationDetails = (key: string) => t(`applicationDetails.${key}`)
const tStatuses = (key: string) => t(`statuses.${key}`)

vi.mock('~/composables/useApplications', () => ({
  useApplications: vi.fn()
}))

const mockUseApplications = (applicationData: any = mockApplicationApproved) => {
  // @ts-ignore: Ignore TypeScript error for mockImplementation
  useApplications.mockImplementation(() => ({
    getApplication: vi.fn().mockResolvedValue(applicationData),
    getApplicationHistory: vi.fn().mockResolvedValue([])
  }))
}

vi.mock('@/stores/keycloak', () => ({
  useBcrosKeycloak: vi.fn()
}))

const mockUseBcrosKeycloak = (isExaminer: boolean = false) => {
  // @ts-ignore: Ignore TypeScript error for mockImplementation
  useBcrosKeycloak.mockImplementation(() => ({
    isExaminer: ref(isExaminer)
  }))
}

vi.mock('~/composables/useChipFlavour', () => ({
  useChipFlavour: () => ({
    getChipFlavour: () => ({
      text: 'success',
      color: 'bg-green-100'
    })
  })
}))

describe('Application Details Page', () => {
  let wrapper: any

  beforeEach(() => {
    vi.resetAllMocks()
    mockUseApplications()
    mockUseBcrosKeycloak()
  })

  it('renders the application details page correctly', async () => {
    wrapper = await mountSuspended(ApplicationDetails)
    expect(wrapper.findTestId('application-details').exists()).toBe(true)
    expect(wrapper.findTestId('application-header').exists()).toBe(true)
    expect(wrapper.findTestId('application-title').exists()).toBe(true)
  })

  it('displays application status correctly', async () => {
    wrapper = await mountSuspended(ApplicationDetails)
    const statusSection = wrapper.findTestId('application-status')
    expect(statusSection.exists()).toBe(true)
    expect(statusSection.find('h2').text()).toBe(tApplicationDetails('applicationStatus'))
  })

  it('displays rental unit information correctly', async () => {
    wrapper = await mountSuspended(ApplicationDetails)
    expect(wrapper.findTestId('unit-nickname').exists()).toBe(true)
    expect(wrapper.findTestId('ownership-type').exists()).toBe(true)
    expect(wrapper.findTestId('unit-address').exists()).toBe(true)
    expect(wrapper.findTestId('parcel-identifier').exists()).toBe(true)
    expect(wrapper.findTestId('property-type').exists()).toBe(true)
    const statusText = wrapper.findTestId('application-status-text')
    expect(statusText.text()).toBe(tStatuses('hostStatuses.fullReviewApproved'))
  })

  it('displays primary contact information correctly', async () => {
    mockUseApplications(mockApplicationApproved)

    const mockPrimaryContact = (mockApplicationApproved.registration as HostApplicationDetailsI).primaryContact

    wrapper = await mountSuspended(ApplicationDetails)
    const primaryContact = wrapper.findComponent('[data-test-id=primary-contact]')
    expect(primaryContact.exists()).toBe(true)
    expect(primaryContact.findAllComponents(BcrosFormSectionReviewItem)).toHaveLength(11)
    expect(primaryContact.findTestId('contact-info-host-type').text()).toContain('Individual')
    expect(primaryContact.findTestId('contact-info-email').text()).toContain(mockPrimaryContact.details.emailAddress)
    expect(primaryContact.findTestId('contact-info-name').text()).toContain(mockPrimaryContact.name.firstName)
  })

  it('displays payment due banner when payment is due', async () => {
    mockUseApplications(mockApplicationPaymentDue)

    wrapper = await mountSuspended(ApplicationDetails)
    const statusText = wrapper.findTestId('application-status-text')
    expect(statusText.text()).toBe(tStatuses('paymentDue'))
    const banner = wrapper.findTestId('payment-due-banner')
    expect(banner.exists()).toBe(true)
    expect(banner.text()).toContain(tApplicationDetails('paymentDueBannerTitle'))
  })

  it('displays documents section when documents exist', async () => {
    mockUseApplications(mockApplicationApprovedWithDocuments)

    wrapper = await mountSuspended(ApplicationDetails)
    const documentId = wrapper.vm.documents[0].fileKey
    const documents = wrapper.findTestId(`document-${documentId}`)
    expect(documents.exists()).toBe(true)
    const documentsSection = wrapper.findTestId('documents-section')
    expect(documentsSection.exists()).toBe(true)
  })

  it('displays examiner-specific sections when user is examiner', async () => {
    mockUseBcrosKeycloak(true)

    wrapper = await mountSuspended(ApplicationDetails)
    // expect(wrapper.findTestId('ltsa-info-section').exists()).toBe(true)
    expect(wrapper.findTestId('auto-approval-section').exists()).toBe(true)
  })

  it('displays secondary contact information when available', async () => {
    mockUseApplications(mockApplicationApprovedWithSecondaryContact)

    const mockSecondaryContact =
      (mockApplicationApprovedWithSecondaryContact.registration as HostApplicationDetailsI).secondaryContact as ContactI

    wrapper = await mountSuspended(ApplicationDetails)
    const secondaryContact = wrapper.findComponent('[data-test-id=secondary-contact]')
    expect(secondaryContact.exists()).toBe(true)
    expect(secondaryContact.findAllComponents(BcrosFormSectionReviewItem)).toHaveLength(11)
    expect(secondaryContact.findTestId('contact-info-host-type').text()).toContain('Individual')
    expect(secondaryContact.findTestId('contact-info-email').text())
      .toContain(mockSecondaryContact.details.emailAddress)
    expect(secondaryContact.findTestId('contact-info-name').text())
      .toContain(mockSecondaryContact.name.firstName)
  })
})
