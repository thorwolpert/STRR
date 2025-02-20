import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect, vi, beforeAll } from 'vitest'
import { mockStrataApplication } from '../mocks/mockedData'
import { enI18n } from '../mocks/i18n'
import ApplicationDetails from '~/pages/examine/[applicationId].vue'
import {
  ConnectPageSection, ApplicationInfoHeader, HostSubHeader, HostSupportingInfo,
  StrataSubHeader, PlatformSubHeader, UBadge, UButton,
  ConnectButtonControl,
  StrataSupportingInfo
} from '#components'

vi.mock('@/stores/examiner', () => ({
  useExaminerStore: () => ({
    getNextApplication: vi.fn().mockResolvedValue(mockStrataApplication)
  })
}))

describe('Examiner - Strata Application Details Page', () => {
  let wrapper: any

  beforeAll(async () => {
    wrapper = await mountSuspended(ApplicationDetails, {
      global: { plugins: [enI18n] }
    })
  })

  it('renders Application Details page and its components', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.findComponent(ApplicationInfoHeader).exists()).toBe(true)
    expect(wrapper.findComponent(HostSubHeader).exists()).toBe(false)
    expect(wrapper.findComponent(HostSupportingInfo).exists()).toBe(false)
    expect(wrapper.findComponent(StrataSupportingInfo).exists()).toBe(true)
    expect(wrapper.findComponent(StrataSubHeader).exists()).toBe(true)
    expect(wrapper.findComponent(PlatformSubHeader).exists()).toBe(false)
  })

  it('renders ApplicationInfoHeader component for Host application', () => {
    const appHeaderInfo = wrapper.findComponent(ApplicationInfoHeader)
    expect(appHeaderInfo.exists()).toBe(true)
    expect(appHeaderInfo.findComponent(UBadge).exists()).toBe(true)
    expect(appHeaderInfo.findTestId('strata-brand-website').exists()).toBe(true)

    const appHeaderInfoText = appHeaderInfo.text()
    expect(appHeaderInfoText).toContain(mockStrataApplication.header.applicationNumber)
    expect(appHeaderInfoText).toContain(mockStrataApplication.header.examinerStatus)
    expect(appHeaderInfoText).toContain('Strata Hotel')
  })

  it('renders Host SubHeader component for Host application', () => {
    const strataSubHeader = wrapper.findComponent(StrataSubHeader)
    expect(strataSubHeader.exists()).toBe(true)

    const { registration } = mockStrataApplication
    const strataSubHeaderText = strataSubHeader.text()
    expect(strataSubHeaderText).toContain(registration.businessDetails.legalName)
    expect(strataSubHeaderText).toContain(registration.businessDetails.mailingAddress.address)

    const attorney = registration.businessDetails.registeredOfficeOrAttorneyForServiceDetails
    expect(strataSubHeaderText).toContain(attorney.attorneyName)
    expect(strataSubHeaderText).toContain(attorney.mailingAddress.address)

    expect(strataSubHeaderText).toContain(registration.strataHotelRepresentatives[0]?.firstName)
    expect(strataSubHeaderText).toContain(registration.strataHotelRepresentatives[0]?.emailAddress)
    expect(strataSubHeaderText).toContain(registration.completingParty.firstName)
    expect(strataSubHeaderText).toContain(registration.completingParty.lastName)
    expect(strataSubHeaderText).toContain(registration.strataHotelDetails.numberOfUnits)
    expect(strataSubHeaderText).toContain(registration.strataHotelDetails.category)
  })
})
