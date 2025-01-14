export enum OwnerType {
  INDIVIDUAL = 'INDIVIDUAL',
  BUSINESS = 'BUSINESS'
}

export enum PropertyType {
  SECONDARY_SUITE = 'SECONDARY_SUITE',
  ACCESSORY_DWELLING = 'ACCESSORY_DWELLING',
  TOWN_HOME = 'TOWN_HOME',
  MULTI_UNIT_HOUSING = 'MULTI_UNIT_HOUSING',
  CONDO_OR_APT = 'CONDO_OR_APT',
  STRATA_HOTEL = 'STRATA_HOTEL',
  SINGLE_FAMILY_HOME = 'SINGLE_FAMILY_HOME',
  RECREATIONAL = 'RECREATIONAL',
  BED_AND_BREAKFAST = 'BED_AND_BREAKFAST',
  FLOAT_HOME = 'FLOAT_HOME'
}

export enum OwnershipType {
  RENT = 'RENT',
  OWN = 'OWN',
  CO_OWN = 'CO_OWN',
  OTHER = 'OTHER'
}

export enum RentalUnitType {
  ENTIRE_HOME = 'ENTIRE_HOME',
  SHARED_ACCOMMODATION = 'SHARED_ACCOMMODATION'
}

export enum ResidenceType {
  SAME_UNIT = 'SAME_UNIT',
  ANOTHER_UNIT = 'ANOTHER_UNIT'
}

export enum PrExemptionReason {
  STRATA_HOTEL = 'STRATA_HOTEL',
  FARM_LAND = 'FARM_LAND',
  FRACTIONAL_OWNERSHIP = 'FRACTIONAL_OWNERSHIP'
}

export interface ApiHostContactPerson extends ApiPartyWithAddress {
  contactType: OwnerType
  dateOfBirth?: string
  socialInsuranceNumber?: string
  businessLegalName?: string
  businessNumber?: string
}

export interface ApiHostContactBusiness extends ApiHostContactPerson {
  businessLegalName: string
  businessNumber: string
}

export interface ApiUnitDetails {
  parcelIdentifier?: string
  businessLicense?: string
  businessLicenseExpiryDate?: string
  propertyType: PropertyType | undefined
  ownershipType: OwnershipType | undefined
  rentalUnitSpaceType: RentalUnitType | undefined
  hostResidence: ResidenceType | undefined
  isUnitOnPrincipalResidenceProperty: boolean | undefined
  numberOfRoomsForRent: number | undefined
  prExemptReason?: PrExemptionReason
}

export interface ApiUnitAddress extends ApiBaseAddress {
  nickname: string
  streetName: string
  streetNumber: string
  unitNumber: string
}

export interface ApiPropertyManagerBusiness {
  legalName: string
  businessNumber?: string
  mailingAddress: ApiAddress
  primaryContact: ApiParty
  secondaryContact?: ApiParty
}

export interface ApiPartyWithAddress extends ApiParty {
  mailingAddress: ApiAddress
}

export interface ApiPropertyManager {
  initiatedByPropertyManager: boolean
  propertyManagerType: OwnerType
  business?: ApiPropertyManagerBusiness // required if OwnerType.BUSINESS
  contact?: ApiPartyWithAddress // required if OwnerType.INDIVIDUAL
}

export interface PropertyRequirements {
  isBusinessLicenceRequired: boolean
  isPrincipalResidenceRequired: boolean
  isStrProhibited: boolean
  isStraaExempt: boolean | null
  organizationNm: string
}

export enum DocumentUploadType {
  BC_DRIVERS_LICENSE = 'BC_DRIVERS_LICENSE',
  BCSC = 'BCSC',
  COMBINED_BCSC_LICENSE = 'COMBINED_BCSC_LICENSE',
  PROPERTY_ASSESSMENT_NOTICE = 'PROPERTY_ASSESSMENT_NOTICE',
  SPEC_TAX_CONFIRMATION = 'SPEC_TAX_CONFIRMATION',
  HOG_DECLARATION = 'HOG_DECLARATION',
  ICBC_CERTIFICATE_OF_INSURANCE = 'ICBC_CERTIFICATE_OF_INSURANCE',
  HOME_INSURANCE_SUMMARY = 'HOME_INSURANCE_SUMMARY',
  PROPERTY_TAX_NOTICE = 'PROPERTY_TAX_NOTICE',
  UTILITY_BILL = 'UTILITY_BILL',
  GOVT_OR_CROWN_CORP_OFFICIAL_NOTICE = 'GOVT_OR_CROWN_CORP_OFFICIAL_NOTICE',
  FRACTIONAL_OWNERSHIP_AGREEMENT = 'FRACTIONAL_OWNERSHIP_AGREEMENT',
  STRATA_HOTEL_DOCUMENTATION = 'STRATA_HOTEL_DOCUMENTATION',
  TENANCY_AGREEMENT = 'TENANCY_AGREEMENT',
  RENT_RECEIPT_OR_BANK_STATEMENT = 'RENT_RECEIPT_OR_BANK_STATEMENT',
  LOCAL_GOVT_BUSINESS_LICENSE = 'LOCAL_GOVT_BUSINESS_LICENSE',
  OTHERS = 'OTHERS'
}

export interface ApiDocument {
  documentType: DocumentUploadType
  fileKey: string
  fileName: string
  fileType: string
}

export interface ApiHostApplication {
  registrationType: ApplicationType
  primaryContact: ApiHostContactPerson | ApiHostContactBusiness
  secondaryContact?: ApiHostContactPerson | ApiHostContactBusiness
  unitDetails: ApiUnitDetails
  unitAddress: ApiUnitAddress
  propertyManager?: ApiPropertyManager
  strRequirements?: PropertyRequirements
  documents: ApiDocument[]
  listingDetails: string[]
}

export interface HostApplicationPayload {
  registration: ApiHostApplication
}

export interface HostApplicationResp extends HostApplicationPayload {
  header: ApplicationHeader
}
