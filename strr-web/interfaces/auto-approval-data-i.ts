export interface AutoApprovalDataI {
  id: number
  applicationNumber: string
  creationDate: string
  record: {
    renting?: boolean
    serviceProvider?: boolean
    businessLicenseRequired?: boolean
    businessLicenseProvided?: boolean
    prExempt: boolean
    strProhibited: boolean
    organizationNm: string
    titleCheck: boolean | null
    addressMatch: boolean | null
  }
}
