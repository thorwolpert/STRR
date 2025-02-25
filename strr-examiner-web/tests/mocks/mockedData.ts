const mockDocuments: ApiDocument[] = [
  {
    documentType: DocumentUploadType.LOCAL_GOVT_BUSINESS_LICENSE,
    fileKey: 'abc12345-6789-0abc-def1-234567890abc',
    fileName: 'business-license.pdf',
    fileType: 'application/pdf'
  },
  {
    documentType: DocumentUploadType.PROPERTY_ASSESSMENT_NOTICE,
    fileKey: 'abc12345-6789-0abc-def1-345245das',
    fileName: 'property-assessment.pdf',
    fileType: 'application/pdf'
  }
]

const primaryContactPerson: ApiHostContactPerson = {
  contactType: OwnerType.INDIVIDUAL,
  dateOfBirth: '1985-05-15',
  emailAddress: 'alice.smith@example.com',
  extension: '',
  firstName: 'Alice',
  lastName: 'Smith',
  mailingAddress: {
    address: '123 Main St',
    addressLineTwo: '',
    city: 'Vancouver',
    country: 'CA',
    locationDescription: '',
    postalCode: 'V5K 0A1',
    province: 'BC'
  },
  phoneCountryCode: '1',
  phoneNumber: '6041234567',
  socialInsuranceNumber: '123 456 789'
}

const primaryContactBusiness: ApiHostContactBusiness = {
  ...primaryContactPerson,
  contactType: OwnerType.BUSINESS,
  businessLegalName: 'ABC Rentals',
  businessNumber: '123123123'
}

export const mockHostApplication: HostApplicationResp = {
  header: {
    applicationDateTime: new Date('2025-01-01T10:30:00.000000+00:00'),
    applicationNumber: '12345678901234',
    decisionDate: undefined,
    examinerActions: ['APPROVE'],
    examinerStatus: 'Full Examination',
    existingHostRegistrations: 0,
    hostActions: [],
    hostStatus: 'Pending Approval',
    isCertificateIssued: false,
    name: 'registration',
    paymentAccount: '9876',
    paymentMethod: ConnectPaymentMethod.PAD,
    paymentStatus: 'COMPLETED',
    paymentToken: 12345,
    status: ApplicationStatus.FULL_REVIEW
  },
  registration: {
    documents: mockDocuments,
    listingDetails: [],
    primaryContact: primaryContactPerson,
    registrationType: ApplicationType.HOST,
    strRequirements: {
      isBusinessLicenceRequired: true,
      isPrincipalResidenceRequired: true,
      isStrProhibited: false,
      isStraaExempt: false,
      organizationNm: 'City of Vancouver'
    },
    unitAddress: {
      addressLineTwo: '',
      city: 'Vancouver',
      country: 'CA',
      locationDescription: '',
      nickname: 'Downtown Unit',
      postalCode: 'V6B 1A1',
      province: 'BC',
      streetName: 'Robson St',
      streetNumber: '456',
      unitNumber: '101'
    },
    unitDetails: {
      hostResidence: ResidenceType.SAME_UNIT,
      isUnitOnPrincipalResidenceProperty: true,
      numberOfRoomsForRent: 2,
      ownershipType: OwnershipType.OWN,
      parcelIdentifier: '123-456-789',
      propertyType: PropertyType.CONDO_OR_APT,
      rentalUnitSpaceType: RentalUnitType.ENTIRE_HOME,
      businessLicense: '123123123'
    }
  }
}

export const mockWithPrExemptAndStrataHotel = {
  ...mockHostApplication,
  registration: {
    ...mockHostApplication.registration,
    unitDetails: {
      ...mockHostApplication.registration.unitDetails,
      prExemptReason: PrExemptionReason.STRATA_HOTEL,
      strataHotelCategory: StrataHotelCategory.FULL_SERVICE
    }
  }
}

export const mockWithBlExempt = {
  ...mockHostApplication,
  registration: {
    ...mockHostApplication.registration,
    unitDetails: {
      ...mockHostApplication.registration.unitDetails,
      blExemptReason: 'OVER 30 DAYS'
    }
  }
}

// Host application with flags for Examiner:
export const mockHostApplicationWithFlags: HostApplicationResp = {
  ...mockHostApplication,
  header: {
    ...mockHostApplication.header,
    existingHostRegistrations: 10 // flag
  },
  registration: {
    ...mockHostApplication.registration,
    primaryContact: primaryContactBusiness, // flag
    strRequirements: {
      isBusinessLicenceRequired: true, // flag
      isPrincipalResidenceRequired: true,
      isStrProhibited: true, // flag
      isStraaExempt: false,
      organizationNm: 'City of Vancouver'
    },
    unitAddress: {
      ...mockHostApplication.registration.unitAddress,
      unitNumber: '' // flag
    } as ApiUnitAddress
  }
}

export const mockStrataApplication: StrataApplicationResp =
{
  header: {
    applicationDateTime: new Date('2025-01-14T19:58:57.549356+00:00'),
    applicationNumber: '12345678901234',
    decisionDate: undefined,
    examinerActions: [],
    examinerStatus: 'Draft',
    existingHostRegistrations: 0,
    hostActions: [],
    hostStatus: 'Draft',
    isCertificateIssued: false,
    name: 'strataApplication',
    paymentAccount: '1234',
    paymentStatus: 'COMPLETED',
    paymentToken: 12345,
    status: ApplicationStatus.FULL_REVIEW,
    paymentMethod: ConnectPaymentMethod.DIRECT_PAY
  },
  registration: {
    businessDetails: {
      businessNumber: '987654321',
      homeJurisdiction: 'BC',
      legalName: 'Doe Enterprises',
      mailingAddress: {
        address: '123 Main St',
        addressLineTwo: 'Suite 100',
        city: 'Vancouver',
        country: 'CA',
        locationDescription: 'Downtown',
        postalCode: 'V5K 0A1',
        province: 'BC'
      },
      registeredOfficeOrAttorneyForServiceDetails: {
        attorneyName: 'Jane Smith',
        mailingAddress: {
          address: '456 Elm St',
          addressLineTwo: '',
          city: 'Victoria',
          country: 'CA',
          locationDescription: 'Near the park',
          postalCode: 'V8W 1A1',
          province: 'BC'
        }
      }
    },
    completingParty: {
      emailAddress: 'alice@example.com',
      extension: '789',
      firstName: 'Alice',
      lastName: 'Johnson',
      phoneCountryCode: '+61',
      phoneNumber: '412345678'
    },
    documents: [],
    registrationType: ApplicationType.STRATA_HOTEL,
    strataHotelDetails: {
      brand: {
        name: 'Luxury Stays',
        website: 'https://luxurystays.com'
      },
      buildings: [],
      location: {
        address: '789 Pine St',
        addressLineTwo: '',
        city: 'Kelowna',
        country: 'CA',
        locationDescription: 'Near the lake',
        postalCode: 'V1Y 1A1',
        province: 'BC'
      },
      numberOfUnits: 1,
      category: StrataHotelCategory.FULL_SERVICE
    },
    strataHotelRepresentatives: [{
      lastName: 'Smith',
      emailAddress: 'jane.smith@example.com',
      firstName: 'Jane',
      middleName: 'B',
      preferredName: '',
      faxNumber: '987-654-3210'
    }] as ApiRep[]
  }
}

export const mockApplications: ApiApplicationBaseResp [] = [
  mockHostApplication,
  mockStrataApplication
]
