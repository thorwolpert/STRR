import {
  RegistrationStatusE,
  ApplicationStatusE,
  HostApplicationStatusE,
  ExaminerApplicationStatusE,
  RegistrationTypeE
} from '#imports'
export interface ApplicationHeaderI {
  applicationDateTime: string
  decisionDate: string | null
  applicationNumber: string
  name: string
  paymentAccount: string
  paymentStatus: string
  hostActions: string[]
  examinerActions: string[]
  paymentToken: number
  registrationEndDate: string
  registrationId: number
  registrationNumber: string
  registrationStartDate: string
  isCertificateIssued: boolean,
  registrationStatus: RegistrationStatusE
  reviewer: {
    displayName: string
    username: string
  }
  status: ApplicationStatusE,
  hostStatus: HostApplicationStatusE,
  examinerStatus: ExaminerApplicationStatusE,
  submitter: {
    displayName: string
    username: string
  }
}

interface ListingDetailsI {
  url: string
}

export interface PropertyManagerI {
  businessLegalName?: string
  businessNumber?: string
  businessMailingAddress: {
    address: string
    city: string
    postalCode: string
    province: string
    country: string
  }
  contact: {
    firstName: string
    lastName: string
    middleName?: string
    preferredName?: string
    phoneNumber: string
    extension?: string
    faxNumber?: string
    emailAddress: string
  }
}

export interface ApplicationDetailsI {
  registrationType: RegistrationTypeE,
  listingDetails: ListingDetailsI[]
  primaryContact: ContactI
  secondaryContact?: ContactI
  principalResidence: PrincipalResidenceI
  propertyManager?: PropertyManagerI
  unitAddress: RegistrationAddressI
  propertyManager?: PropertyManagerI
  unitDetails: {
    parcelIdentifier?: string
    businessLicense?: string
    businessLicenseExpiryDate?: string
    propertyType: string
    ownershipType: string
  }
  documents?: DocumentUploadI[]
}

export interface PlatformApplicationDetailsI {
  registrationType: RegistrationTypeE.PLATFORM,
  completingParty?: ContactI,
  platformRepresentatives: ContactI[],
  businessDetails: {
    legalName: string,
    homeJurisdiction: string,
    businessNumber?: string,
    consumerProtectionBCLicenceNumber?: string,
    noticeOfNonComplianceEmail: string,
    noticeOfNonComplianceOptionalEmail?: string,
    takeDownRequestEmail: string,
    takeDownRequestOptionalEmail?: string,
    mailingAddress: RegistrationAddressI & { locationDescription?: string },
    registeredOfficeOrAttorneyForServiceDetails?: {
      attorneyName: string,
      mailingAddress: RegistrationAddressI & { locationDescription?: string }
    }
  },
  platformDetails: {
    brands: {
      name: string,
      website: string
    }[],
    listingSize: 'GREATER_THAN_THOUSAND' | 'LESS_THAN_THOUSAND'
  }
}

export interface ApplicationI {
  header: ApplicationHeaderI
  registration: ApplicationDetailsI | PlatformApplicationDetailsI
  selectedAccount: {
    sbc_account_id: string
  }
}
