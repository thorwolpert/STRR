import { z } from 'zod'

export const useHostOwnerStore = defineStore('host/owner', () => {
  // TODO: pull common pieces of this and useStrrContactStore into base composable
  const { t } = useI18n()
  const { getNewContact } = useStrrContactStore()

  const getHostOwnerSchema = (type: OwnerType, role?: OwnerRole) => {
    return z.object({
      role: z.enum([OwnerRole.HOST, OwnerRole.CO_HOST, OwnerRole.PROPERTY_MANAGER], {
        errorMap: () => ({ message: t('validation.ownerRole') })
      }),
      firstName: getRequiredNonEmptyString(t('validation.name.first')),
      middleName: optionalOrEmptyString,
      lastName: getRequiredNonEmptyString(t('validation.name.last')),
      preferredName: optionalOrEmptyString,
      faxNumber: optionalOrEmptyString,
      emailAddress: getRequiredEmail(t('validation.email')),
      phone: getRequiredPhone(t('validation.required'), t('validation.phone.number')),
      mailingAddress: getRequiredAddress(
        t('validation.address.street'),
        t('validation.address.city'),
        t('validation.address.region'),
        // TODO: postal code optional for individuals (a residential address can't require it?)
        t('validation.address.postalCode'),
        t('validation.address.country')
      ),
      businessLegalName: type === OwnerType.BUSINESS
        ? getRequiredNonEmptyString(t('validation.business.legalName'))
        : optionalOrEmptyString,
      businessNumber: optionalOrEmptyString,
      dateOfBirth: type === OwnerType.INDIVIDUAL && role === OwnerRole.HOST
        ? getRequiredNonEmptyString(t('validation.dateOfBirth'))
        : optionalOrEmptyString,
      taxNumber: type === OwnerType.INDIVIDUAL && role === OwnerRole.HOST
        ? getOptionalSin(t('validation.craTaxNumberIndividual'))
        : optionalOrEmptyString
    })
  }

  const getNewHostOwner = (isActiveUser = false, ownerType: OwnerType): HostOwner => ({
    ...(getNewContact(isActiveUser)),
    ownerType,
    preferredName: '',
    dateOfBirth: '',
    businessLegalName: '',
    businessNumber: '',
    mailingAddress: {
      street: '',
      streetAdditional: '',
      region: '',
      city: '',
      country: '',
      postalCode: '',
      locationDescription: ''
    },
    role: undefined,
    isCompParty: isActiveUser,
    taxNumber: ''
  })

  const hostOwners = ref<HostOwner[]>([])

  const findByRole = (ownerRole: OwnerRole) => hostOwners.value.find(val => val.role === ownerRole)
  const findCompPartyIndex = () => hostOwners.value.findIndex(val => val.isCompParty)

  const hasHost = computed(() => !!findByRole(OwnerRole.HOST))
  const hasCoHost = computed(() => !!findByRole(OwnerRole.CO_HOST))
  const hasPropertyManager = computed(() => !!findByRole(OwnerRole.PROPERTY_MANAGER))
  const hasCompParty = computed(() => findCompPartyIndex() !== -1)

  const addHostOwner = (owner: HostOwner) => {
    hostOwners.value.push(owner)
  }

  const removeHostOwner = (index: number) => {
    hostOwners.value.splice(index, 1)
  }

  const updateHostOwner = (owner: HostOwner, index: number) => {
    hostOwners.value.splice(index, 1, owner)
  }

  const SetOwnerNameWithUserCreds = (owner: Ref<HostOwner>) => {
    // Set the first, middle, and last name of the owner by the logged in user credentials
    const userInfo = getNewContact(true)
    owner.value.firstName = userInfo.firstName
    owner.value.middleName = userInfo.middleName
    owner.value.lastName = userInfo.lastName
  }

  const validateOwner = (): boolean => {
    if (!hasHost.value || !hasCompParty.value) {
      return false
    }
    return true
  }

  const $reset = () => {
    hostOwners.value = []
  }

  return {
    hostOwners,
    hasHost,
    hasCoHost,
    hasPropertyManager,
    hasCompParty,
    addHostOwner,
    removeHostOwner,
    updateHostOwner,
    SetOwnerNameWithUserCreds,
    findByRole,
    findCompPartyIndex,
    getHostOwnerSchema,
    getNewHostOwner,
    validateOwner,
    $reset
  }
})