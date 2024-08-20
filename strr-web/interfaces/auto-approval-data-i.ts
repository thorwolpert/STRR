export interface AutoApprovalDataI {
  record: {
    id: number,
    applicationId: number,
    creationDate: string,
    record: {
      renting?: boolean,
      service_provider?: boolean,
      pr_exempt?: boolean,
      address_match?: boolean,
      business_license_required?: boolean,
      business_license_required_not_provided?: boolean,
      business_license_required_provided?: boolean,
      business_license_not_required_not_provided?: boolean,
      title_check?: boolean
    }
  }
}
