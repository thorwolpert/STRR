export function formatOwnerHostAPI (owner: HostOwner): ApiHostContactPerson {
  return {
    contactType: owner.ownerType,
    name: {
      firstName: owner.firstName || '',
      ...(owner.middleName ? { middleName: owner.middleName } : {}),
      lastName: owner.lastName || ''
    },
    details: {
      ...(owner.preferredName ? { preferredName: owner.preferredName } : {}),
      emailAddress: owner.emailAddress || '',
      phoneCountryCode: owner.phone.countryCode || '',
      phoneNumber: owner.phone.number || '',
      extension: owner.phone.extension || '',
      faxNumber: owner.faxNumber || ''
    },
    ...(owner.dateOfBirth ? { dateOfBirth: owner.dateOfBirth } : {}),
    ...(owner.taxNumber ? { socialInsuranceNumber: owner.taxNumber } : {}),
    mailingAddress: formatAddress(owner.mailingAddress)
  }
}

export function formatOwnerHostUI (
  owner: ApiHostContactPerson,
  isCompParty: boolean,
  isCoHost?: boolean
): HostOwner {
  return {
    ownerType: owner.contactType,
    firstName: owner.name.firstName || '',
    middleName: owner.name.middleName || '',
    lastName: owner.name.lastName || '',
    preferredName: owner.details.preferredName || '',
    emailAddress: owner.details.emailAddress || '',
    phone: formatPhoneNumberUI(owner.details),
    faxNumber: owner.details.faxNumber || '',
    dateOfBirth: owner.dateOfBirth || '',
    taxNumber: owner.socialInsuranceNumber || '',
    mailingAddress: formatAddressUI(owner.mailingAddress),
    businessLegalName: '',
    businessNumber: '',
    role: isCoHost ? OwnerRole.CO_HOST : OwnerRole.HOST,
    isCompParty
  }
}

export function formatOwnerPropertyManagerAPI (owner: HostOwner): ApiPropertyManager {
  return {
    initiatedByPropertyManager: owner.isCompParty,
    propertyManagerType: owner.ownerType,
    ...(owner.ownerType === OwnerType.INDIVIDUAL
      ? {
          contact: {
            ...formatParty(owner),
            ...(owner.preferredName ? { preferredName: owner.preferredName } : {}),
            mailingAddress: formatAddress(owner.mailingAddress)
          }
        }
      : {
          business: {
            legalName: owner.businessLegalName,
            ...(owner.businessNumber ? { businessNumber: owner.businessNumber } : {}),
            mailingAddress: formatAddress(owner.mailingAddress),
            primaryContact: {
              ...formatParty(owner),
              ...(owner.preferredName ? { preferredName: owner.preferredName } : {})
            }
          }
        }
    )
  }
}

export function formatOwnerPropertyManagerUI (owner: ApiPropertyManager): HostOwner {
  return {
    ownerType: owner.propertyManagerType,
    firstName: owner.contact?.firstName || owner.business?.primaryContact?.firstName || '',
    middleName: owner.contact?.middleName || owner.business?.primaryContact?.middleName || '',
    lastName: owner.contact?.lastName || owner.business?.primaryContact?.lastName || '',
    preferredName: owner.contact?.preferredName || owner.business?.primaryContact?.preferredName || '',
    emailAddress: owner.contact?.emailAddress || owner.business?.primaryContact?.emailAddress || '',
    phone: formatPhoneNumberUI((owner.contact || owner.business?.primaryContact) as ApiParty),
    faxNumber: owner.contact?.faxNumber || owner.business?.primaryContact?.faxNumber || '',
    mailingAddress: formatAddressUI((owner.contact?.mailingAddress || owner.business?.mailingAddress) as ApiAddress),
    businessLegalName: owner.business?.legalName || '',
    businessNumber: owner.business?.businessNumber || '',
    dateOfBirth: '',
    taxNumber: '',
    role: OwnerRole.PROPERTY_MANAGER,
    isCompParty: owner.initiatedByPropertyManager
  }
}

export function formatHostUnitDetailsAPI (unitDetails: UiUnitDetails, blInfo: UiBlInfo): ApiUnitDetails {
  return {
    propertyType: unitDetails.propertyType,
    ownershipType: unitDetails.ownershipType,
    numberOfRoomsForRent: unitDetails.numberOfRoomsForRent,
    isUnitOnPrincipalResidenceProperty: unitDetails.rentalUnitSetupType !== RentalUnitSetupType.UNIT_NOT_ON_PR_PROPERTY,
    hostResidence: unitDetails.rentalUnitSetupType === RentalUnitSetupType.WHOLE_PRINCIPAL_RESIDENCE
      ? ResidenceType.SAME_UNIT
      : ResidenceType.ANOTHER_UNIT,
    rentalUnitSpaceType: unitDetails.typeOfSpace,
    ...(unitDetails.parcelIdentifier ? { parcelIdentifier: unitDetails.parcelIdentifier } : {}),
    ...(blInfo.businessLicense ? { businessLicense: blInfo.businessLicense } : {}),
    ...(blInfo.businessLicenseExpiryDate ? { businessLicenseExpiryDate: blInfo.businessLicenseExpiryDate } : {})
  }
}

export function formatHostUnitDetailsUI (unitDetails: ApiUnitDetails): UiUnitDetails {
  // TODO: review rentalSetupType mapping
  const rentalSetupType = unitDetails.isUnitOnPrincipalResidenceProperty
    ? unitDetails.hostResidence === ResidenceType.SAME_UNIT
      ? RentalUnitSetupType.WHOLE_PRINCIPAL_RESIDENCE
      : RentalUnitSetupType.UNIT_ON_PR_PROPERTY
    : RentalUnitSetupType.UNIT_NOT_ON_PR_PROPERTY
  return {
    parcelIdentifier: unitDetails.parcelIdentifier || '',
    propertyType: unitDetails.propertyType,
    ownershipType: unitDetails.ownershipType,
    numberOfRoomsForRent: unitDetails.numberOfRoomsForRent,
    rentalUnitSetupType: rentalSetupType,
    typeOfSpace: unitDetails.rentalUnitSpaceType
  }
}

export function formatHostUnitDetailsBlInfoUI (unitDetails: ApiUnitDetails): UiBlInfo {
  return {
    businessLicense: unitDetails.businessLicense || '',
    businessLicenseExpiryDate: unitDetails.businessLicenseExpiryDate || ''
  }
}

export function formatHostUnitAddressApi (unitAddress: HostPropertyAddress): ApiUnitAddress {
  return {
    ...formatAddress(unitAddress),
    nickname: unitAddress.nickname || '',
    streetName: unitAddress.streetName || '',
    streetNumber: unitAddress.streetNumber || '',
    unitNumber: unitAddress.unitNumber || ''
  }
}

export function formatHostUnitAddressUI (unitAddress: ApiUnitAddress): HostPropertyAddress {
  if (!unitAddress.address) {
    unitAddress.address = unitAddress.unitNumber
      ? `${unitAddress.unitNumber}-${unitAddress.streetNumber} ${unitAddress.streetName}`
      : `${unitAddress.streetNumber} ${unitAddress.streetName}`
  }
  const address = formatAddressUI(unitAddress)
  return {
    ...address,
    nickname: unitAddress.nickname || '',
    streetName: unitAddress.streetName || '',
    streetNumber: unitAddress.streetNumber || '',
    unitNumber: unitAddress.unitNumber || ''
  }
}