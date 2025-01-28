import { mockNuxtImport, mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect, beforeEach } from 'vitest'
import { mockApplications } from '../mocks/mockedData'
import { enI18n } from '../mocks/i18n'
import Dashboard from '~/pages/dashboard.vue'

mockNuxtImport('useStrrBasePermitList', () => () => ({
  limit: 50,
  page: 1,
  getApplicationList: () => ({ applications: mockApplications, total: mockApplications.length })
}))

describe('Examiner Dashboard Page', () => {
  let wrapper: any

  beforeEach(async () => {
    wrapper = await mountSuspended(Dashboard, {
      global: { plugins: [enI18n] }
    })
  })

  it('should setup tests', () => {
    const result = useStrrBasePermitList()
    expect(result).toHaveProperty('limit', 50)
    expect(result).toHaveProperty('page', 1)
  })

  it('should produce correct Host PR Requirements', () => {
    const getPrReq = (reg: ApiHostApplication) => wrapper.vm.getHostPrRequirements(reg)

    const prRequirements = getPrReq(mockApplications[0]?.registration)
    expect(prRequirements).toBe('PR/BL')

    const prRequirements2 = getPrReq({
      ...mockApplications[0]?.registration,
      strRequirements: {
        isBusinessLicenceRequired: true,
        isPrincipalResidenceRequired: false,
        isStrProhibited: true,
        isStraaExempt: null,
        organizationNm: ''
      }
    })

    expect(prRequirements2).toBe('BL/Prohibited')

    const prRequirements3 = getPrReq({
      ...mockApplications[0]?.registration,
      unitDetails: {
        ...mockApplications[0]?.registration.unitDetails,
        prExemptReason: PrExemptionReason.FARM_LAND
      },
      strRequirements: {
        isBusinessLicenceRequired: true,
        isPrincipalResidenceRequired: false,
        isStrProhibited: true,
        isStraaExempt: null,
        organizationNm: ''
      }
    })

    expect(prRequirements3).toBe('PR-ex-farm/BL/Prohibited')
  })

  it('renders the Dashboard page and applications table', () => {
    expect(wrapper.findTestId('examiner-dashboard-page').exists()).toBe(true)
    expect(wrapper.findTestId('applications-table').exists()).toBe(true)
    expect(wrapper.findTestId('applications-pagination').exists()).toBe(mockApplications.length > 50)

    const applications = wrapper.vm.applications

    expect(applications.length).toBe(mockApplications.length)
    expect(applications[0].applicantName).toEqual(
      displayContactFullName(mockApplications[0]?.registration.primaryContact)
    )

    const applicationText = wrapper.findTestId('applications-table').text()
    const { header, registration } = mockApplications[0] as ApiApplicationBaseResp
    expect(applicationText).toContain(header.applicationNumber)
    expect(applicationText).toContain(header.examinerStatus)
    expect(applicationText).toContain(registration.unitAddress.city)
  })
})
