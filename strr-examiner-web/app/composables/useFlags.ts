export const useFlags = (application: HostApplicationResp) => {
  const REGISTRATIONS_LIMIT = 2

  /**
   * @description Requirement: If Property Type is condo or apartment, multi-unit housing,
   * townhome, strata unit
   */
  const isUnitNumberMissing = computed((): boolean => {
    const unitNumberRequired = [
      PropertyType.CONDO_OR_APT,
      PropertyType.MULTI_UNIT_HOUSING,
      PropertyType.TOWN_HOME,
      PropertyType.STRATA_HOTEL
    ]
    return (
      unitNumberRequired.includes(application.registration.unitDetails.propertyType) &&
      !application.registration.unitAddress?.unitNumber
    )
  })

  const isProhibited = computed(() => application.registration.strRequirements?.isStrProhibited)

  /**
   * @description Requirement: address in Principal Residence area without PR exemption,
   * when rental unit setup is "not on same property as host".
   */
  const isNotSameProperty = computed((): boolean => {
    const { isPrincipalResidenceRequired } = application.registration?.strRequirements as PropertyRequirements
    const { prExemptReason, hostResidence } = application.registration.unitDetails as ApiUnitDetails

    return isPrincipalResidenceRequired && !prExemptReason && hostResidence === ResidenceType.ANOTHER_UNIT
  })

  /**
   * @description Requirement: Host is a business
   */
  const isHostTypeBusiness = computed(
    (): boolean => application.registration.primaryContact?.contactType === OwnerType.BUSINESS
  )

  /**
   * @description Requirement: Host exceeds registration limit
   */
  const isRegLimitExceeded = computed((): boolean => application.header.existingHostRegistrations > REGISTRATIONS_LIMIT)

  return {
    isUnitNumberMissing,
    isNotSameProperty,
    isProhibited,
    isHostTypeBusiness,
    isRegLimitExceeded
  }
}
