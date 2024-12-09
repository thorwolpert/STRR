export interface PropertyManagerContactI {
  emailAddress: string
  extension: string
  faxNumber: string
  firstName: string
  lastName: string
  middleName: string
  phoneCountryCode: string
  phoneNumber: string
  preferredName?: string
}

export interface PropertyManagerBusinessAddressI {
  address: string
  addressLineTwo: string | undefined
  city: string
  province: string
  postalCode: string
  country: string
}

export interface PropertyManagerBusinessI {
  legalName?: string
  businessNumber?: string
  mailingAddress: PropertyManagerBusinessAddressI
  primaryContact: PropertyManagerContactI
}

export interface PropertyManagerIndividualContactI extends PropertyManagerContactI {
  mailingAddress: MailingAddressAPII
}

export interface PropertyManagerI {
  business?: PropertyManagerBusinessI
  contact?: PropertyManagerIndividualContactI
  initiatedByPropertyManager: boolean | undefined
  propertyManagerType: HostContactTypeE
}
