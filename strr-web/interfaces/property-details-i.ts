export interface PropertyDetailsI {
    primaryResidence: string | undefined
    whichPlatform: string | undefined
    parcelIdentifier: string | undefined
    businessLicense: string | undefined
    businessLicenseExpiryDate: string | undefined
    propertyType: string | undefined
    ownershipType: string | undefined
    nickname: string
    country: string
    streetNumber: string
    streetName: string
    unitNumber: string
    addressLineTwo: string
    city: string
    province: string
    postalCode: string
    listingDetails: { url: string }[]
    rentalUnitSpaceType: string
    isUnitOnPrincipalResidenceProperty: boolean | undefined
    hostResidence: string | undefined
    numberOfRoomsForRent: number
  }
