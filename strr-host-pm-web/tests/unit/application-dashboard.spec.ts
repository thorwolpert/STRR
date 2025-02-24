import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect, vi, beforeAll } from 'vitest'
import { baseEnI18n } from '../mocks/i18n'
import { mockApplication } from '../mocks/mockedData'
import ApplicationDashboard from '~/pages/dashboard/[applicationId].vue'
import {
  ConnectDashboardSection, Todo, TodoEmpty, SummaryProperty,
  SummarySupportingInfo, ConnectAccordion
} from '#components'

vi.mock('@/stores/hostPermit', () => ({
  useHostPermitStore: () => ({
    loadHostData: vi.fn(),
    downloadApplicationReceipt: vi.fn(),
    permitDetails: ref({
      unitAddress: mockApplication.registration.unitAddress,
      documents: [],
      primaryContact: mockApplication.registration.primaryContact
    }),
    isPaidApplication: ref(false),
    showPermitDetails: ref(true),
    application: ref(mockApplication),
    registration: ref(mockApplication.registration)
  })
}))

vi.mock('@/stores/connectDetailsHeader', () => ({
  useConnectDetailsHeaderStore: () => ({
    loading: ref(false),
    title: ref(''),
    subtitles: ref([])
  })
}))

vi.mock('@/stores/hostProperty', () => ({
  useHostPropertyStore: () => ({
    unitAddress: ref({ address: mockApplication.registration.unitAddress }),
    unitDetails: ref(mockApplication.registration.unitDetails),
    blInfo: ref({
      businessLicense: '12345',
      businessLicenseExpiryDate: '2025-01-01'
    })
  })
}))

describe('Dashboard Application Page', () => {
  let wrapper: any

  beforeAll(async () => {
    wrapper = await mountSuspended(ApplicationDashboard, {
      global: { plugins: [baseEnI18n] }
    })
  })

  it('renders the dashboard page', () => {
    expect(wrapper.find('[data-test-id="host-dashboard-page"]').exists()).toBe(true)
  })

  it('renders all dashboard sections', () => {
    const sections = [
      'todo-section',
      'rental-section',
      'supporting-info-section',
      'individuals-business-section'
    ]

    sections.forEach(section => {
      expect(wrapper.find(`[data-test-id="${section}"]`).exists()).toBe(true)
    })
  })

  it('renders summary components', () => {
    const summaryComponents = [
      'summary-property',
      'summary-supporting-info'
    ]

    summaryComponents.forEach(component => {
      expect(wrapper.find(`[data-test-id="${component}"]`).exists()).toBe(true)
    })
  })

  it('renders all components', () => {
    const components = [
      { component: ConnectDashboardSection, testId: 'connect-dashboard-section' },
      { component: SummaryProperty, testId: 'summary-property' },
      { component: SummarySupportingInfo, testId: 'summary-supporting-info' },
      { component: ConnectAccordion, testId: 'owners-accordion' }
    ]

    components.forEach(({ component }) => {
      expect(wrapper.findComponent(component).exists()).toBe(true)
    })
  })

  it('renders todo components based on store state', async () => {
    mockApplication.header = {
      applicationNumber: 'ABC123',
      status: 'DRAFT',
      hostActions: []
    }
    wrapper = await mountSuspended(ApplicationDashboard, {
      global: { plugins: [baseEnI18n] }
    })
    await wrapper.vm.$forceUpdate()
    expect(wrapper.findComponent(TodoEmpty).exists()).toBe(false)
    expect(wrapper.findComponent(Todo).exists()).toBe(true)
  })
})
