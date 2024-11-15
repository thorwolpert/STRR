import { reactive } from 'vue'
import { z } from 'zod'
import type {
  CreateAccountFormStateI,
  OrgI,
  PrimaryContactInformationI,
  SecondaryContactInformationI
} from '~/interfaces/account-i'
import type { PropertyManagerI } from '~/interfaces/property-manager-i'
import { RegistrationTypeE } from '#imports'
import { HostContactTypeE } from '~/enums/host-contact-type-e'
import { PropertyTypeE } from '~/enums/property-type-e'

const numbersRegex = /^\d+$/
// matches chars 123456789 ()
const httpRegex = /^(https?:\/\/)?([\w-]+(\.[\w-]+)+\.?(:\d+)?(\/.*)?)$/i // https is optional
const html5EmailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/
const html5PhoneRegex = /^(\+\d{1,3}[-\s.]?)?(\(?\d{3}\)?[-\s.]?\d{3}[-\s.]?\d{4,6})$/
const pidRegex = /^\d{3}(-)\d{3}(-)\d{3}$/

// not allowed: all 0s, starting with 8, letters; allowed: 111 222 333 or 111222333
const sinRegex = /^(?!00000000|000 000 000)(?!8)(?:\d{9}|\d{3} \d{3} \d{3})$/
const craBusinessNumberRegex = /^\d{9}$/
const phoneError = { message: 'Please enter a valid phone number' }
const emailError = { message: 'Please enter a valid email' }

const requiredPhone = z
  .string()
  .min(1, { message: 'Required' })
  .regex(html5PhoneRegex, phoneError)

const optionalPhone = z.string().regex(html5PhoneRegex, phoneError).optional().or(z.literal(''))
const requiredEmail = z.string().regex(html5EmailRegex, emailError)
const requiredNumber = z.string()
  .min(1, { message: 'Required' })
  .regex(numbersRegex, { message: 'Must be a number' })
const optionalNumber = z
  .string()
  .refine(val => val === '' || numbersRegex.test(val), { message: 'Must be a number' })
  .optional()
const optionalPID = z
  .string()
  .refine(val => val === '' || pidRegex.test(val), {
    message: 'If provided this value must be in the format 111-111-111'
  })
  .optional()
const requiredSin = z
  .string()
  .regex(sinRegex, { message: 'Please enter a valid Social Insurance Number' })

const optionalSin = requiredSin.or(z.literal(''))

const optionalCRABusinessNumber = z
  .string()
  .refine(val => val === '' || craBusinessNumberRegex.test(val), {
    message: 'CRA Business Number must be a 9-digit number'
  })
  .optional()
const optionalExtension = optionalNumber
const optionalOrEmptyString = z
  .string()
  .optional()
  .transform(e => (e === '' ? undefined : e))
const optionalOrEmptyString15 = z
  .string()
  .max(15, { message: 'Maximum length is 15 characters' })
  .optional()
  .transform(e => (e === '' ? undefined : e))
const optionalOrEmptyString50 = z
  .string()
  .max(50, { message: 'Maximum length is 50 characters' })
  .optional()
  .transform(e => (e === '' ? undefined : e))
const requiredNonEmptyString = z
  .string()
  .min(1, { message: 'Required' })
  // .refine(e => e !== '', 'Field cannot be empty')
const requiredNonEmptyString15 = z
  .string()
  .min(1, { message: 'Required' })
  .max(15, { message: 'Maximum length is 15 characters' })
  // .refine(e => e !== '', 'Field cannot be empty')
const requiredNonEmptyString100 = z
  .string()
  .min(1, { message: 'Required' })
  .max(100, { message: 'Maximum length is 100 characters' })
  // .refine(e => e !== '', 'Field cannot be empty')
const requiredNonEmptyString50 = z
  .string()
  .min(1, { message: 'Required' })
  .max(50, { message: 'Maximum length is 50 characters' })
  // .refine(s => !s.includes(' '), 'Spaces not allowed')

export const finalizationSchema = z.object({
  phone: requiredPhone,
  phoneExtension: optionalExtension,
  email: requiredEmail,
  name: requiredNonEmptyString
})

export const propertyManagerSchema = z.object({
  businessLegalName: optionalOrEmptyString50,
  businessNumber: optionalCRABusinessNumber,
  address: requiredNonEmptyString,
  addressLineTwo: optionalOrEmptyString,
  city: requiredNonEmptyString100,
  postalCode: requiredNonEmptyString15,
  province: requiredNonEmptyString,
  country: requiredNonEmptyString,
  firstName: requiredNonEmptyString50,
  middleName: optionalOrEmptyString50,
  lastName: requiredNonEmptyString50,
  preferredName: optionalOrEmptyString50,
  phoneNumber: requiredPhone,
  extension: optionalOrEmptyString15,
  faxNumber: optionalPhone,
  emailAddress: requiredEmail
})

const primaryContact: PrimaryContactInformationI = {
  preferredName: '',
  phoneNumber: undefined,
  extension: '',
  faxNumber: '',
  emailAddress: undefined,
  address: undefined,
  country: undefined,
  addressLineTwo: undefined,
  city: undefined,
  province: undefined,
  postalCode: undefined,
  birthDay: undefined,
  birthMonth: undefined,
  birthYear: undefined,
  socialInsuranceNumber: '',
  businessNumber: '',
  firstName: '',
  middleName: '',
  lastName: '',
  businessLegalName: '',
  contactType: HostContactTypeE.INDIVIDUAL
}

export const propertyManager: PropertyManagerI = {
  initiatedByPropertyManager: undefined,
  businessLegalName: '',
  businessNumber: '',
  businessMailingAddress: {
    address: '',
    addressLineTwo: '',
    city: '',
    postalCode: '',
    province: '',
    country: ''
  },
  contact: {
    firstName: '',
    middleName: '',
    lastName: '',
    preferredName: '',
    phoneNumber: '',
    extension: '',
    faxNumber: '',
    emailAddress: ''
  }
}

const secondaryContact: SecondaryContactInformationI = {
  firstName: '',
  lastName: '',
  middleName: '',
  preferredName: '',
  phoneNumber: '',
  businessNumber: '',
  socialInsuranceNumber: '',
  extension: '',
  faxNumber: '',
  emailAddress: undefined,
  address: undefined,
  country: undefined,
  addressLineTwo: undefined,
  city: undefined,
  province: undefined,
  postalCode: undefined,
  birthDay: undefined,
  birthMonth: undefined,
  birthYear: undefined
}

// If any listing details exist must follow httpRegex otherwise can be blank
const listingDetailsSchema = z.array(
  z.object({
    url: z
      .string()
      .regex(httpRegex, { message: 'Invalid URL format' })
      .optional()
      .or(z.literal(''))
  })
)

const basePropertyDetailsSchema = z.object({
  streetNumber: requiredNonEmptyString,
  streetName: requiredNonEmptyString,
  addressLineTwo: optionalOrEmptyString,
  city: requiredNonEmptyString,
  country: requiredNonEmptyString,
  listingDetails: listingDetailsSchema,
  nickname: optionalOrEmptyString,
  ownershipType: requiredNonEmptyString,
  parcelIdentifier: optionalPID,
  postalCode: requiredNonEmptyString,
  propertyType: requiredNonEmptyString,
  rentalUnitSpaceType: requiredNonEmptyString,
  isUnitOnPrincipalResidenceProperty: z.boolean(),
  numberOfRoomsForRent: z.number().min(1),
  province: requiredNonEmptyString.refine(province => province === 'BC', { message: 'Province must be set to BC' })
})

const withPrincipalResidenceSchema = z.object({
  isUnitOnPrincipalResidenceProperty: z.literal(true),
  hostResidence: requiredNonEmptyString
})

const withoutPrincipalResidenceSchema = z.object({
  isUnitOnPrincipalResidenceProperty: z.literal(false),
  hostResidence: z.string().nullable()
})

const unitNumberRequiredPropertyDetailsSchema = z.object({
  propertyType: z.enum([
    PropertyTypeE.CONDO_OR_APT,
    PropertyTypeE.STRATA_HOTEL,
    PropertyTypeE.SECONDARY_SUITE,
    PropertyTypeE.ACCESSORY_DWELLING,
    PropertyTypeE.TOWN_HOME,
    PropertyTypeE.MULTI_UNIT_HOUSING
  ]),
  unitNumber: requiredNonEmptyString
})

const unitNumberOptionalPropertyDetailsSchema = z.object({
  propertyType: z.enum([
    PropertyTypeE.SINGLE_FAMILY_HOME,
    PropertyTypeE.RECREATIONAL,
    PropertyTypeE.BED_AND_BREAKFAST,
    PropertyTypeE.FLOAT_HOME
  ]),
  unitNumber: optionalOrEmptyString
})

const businessLicensePropertyDetailsSchema = z.object({
  businessLicense: optionalOrEmptyString,
  businessLicenseExpiryDate: optionalOrEmptyString
}).superRefine((data, ctx) => {
  const hasLicense = data.businessLicense?.trim()
  const hasExpiryDate = data.businessLicenseExpiryDate?.trim()
  if (hasLicense && !hasExpiryDate) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: 'Business License Expiry Date is required',
      path: ['businessLicenseExpiryDate']
    })
  }
})

export const propertyDetailsSchema = z.preprocess(
  data => data,
  basePropertyDetailsSchema
    .and(businessLicensePropertyDetailsSchema)
    .and(
      z.discriminatedUnion('propertyType', [
        unitNumberRequiredPropertyDetailsSchema,
        unitNumberOptionalPropertyDetailsSchema
      ])
    )
    .and(
      z.discriminatedUnion('isUnitOnPrincipalResidenceProperty', [
        withPrincipalResidenceSchema,
        withoutPrincipalResidenceSchema
      ])
    )
)

export const formState: CreateAccountFormStateI = reactive({
  primaryContact,
  secondaryContact,
  isPropertyManagerRole: false,
  hasPropertyManager: true,
  propertyManager,
  propertyDetails: {
    parcelIdentifier: undefined,
    businessLicense: undefined,
    businessLicenseExpiryDate: undefined,
    propertyType: undefined,
    ownershipType: undefined,
    primaryResidence: undefined,
    whichPlatform: undefined,
    nickname: '',
    country: 'CA',
    streetNumber: undefined,
    streetName: undefined,
    unitNumber: undefined,
    addressLineTwo: undefined,
    city: undefined,
    province: 'BC',
    postalCode: undefined,
    listingDetails: [{ url: '' }],
    numberOfRoomsForRent: 1,
    rentalUnitSpaceType: '',
    isUnitOnPrincipalResidenceProperty: null,
    hostResidence: undefined
  },
  selectedAccount: {} as OrgI,
  principal: {
    isPrincipalResidence: undefined,
    agreedToRentalAct: false,
    agreedToSubmit: false,
    nonPrincipalOption: undefined,
    specifiedServiceProvider: undefined
  },
  supportingDocuments: [],
  hasHostAuthorization: false // if Property Manager is authorized by Host
})

const primaryContactAPI: ContactAPII = {
  name: {
    firstName: '',
    middleName: '',
    lastName: ''
  },
  dateOfBirth: '',
  details: {
    preferredName: '',
    phoneNumber: '',
    extension: '',
    faxNumber: '',
    emailAddress: ''
  },
  mailingAddress: {
    address: '',
    addressLineTwo: '',
    city: '',
    postalCode: '',
    province: '',
    country: ''
  },
  socialInsuranceNumber: '',
  businessNumber: '',
  businessLegalName: '',
  contactType: HostContactTypeE.INDIVIDUAL
}

const secondaryContactAPI: ContactAPII = {
  name: {
    firstName: '',
    middleName: '',
    lastName: ''
  },
  dateOfBirth: '',
  details: {
    preferredName: '',
    phoneNumber: '',
    extension: '',
    faxNumber: '',
    emailAddress: ''
  },
  mailingAddress: {
    address: '',
    addressLineTwo: '',
    city: '',
    postalCode: '',
    province: '',
    country: ''
  },
  socialInsuranceNumber: '',
  businessNumber: '',
  businessLegalName: '',
  contactType: HostContactTypeE.INDIVIDUAL
}

export const formDataForAPI: CreateAccountFormAPII = {
  registration: {
    primaryContact: primaryContactAPI,
    secondaryContact: secondaryContactAPI,
    propertyManager: undefined,
    unitAddress: {
      streetNumber: '',
      streetName: '',
      unitNumber: '',
      addressLineTwo: '',
      city: '',
      postalCode: '',
      province: '',
      country: '',
      nickname: ''
    },
    unitDetails: {
      parcelIdentifier: '',
      businessLicense: '',
      propertyType: '',
      ownershipType: '',
      rentalUnitSpaceType: '',
      isUnitOnPrincipalResidenceProperty: false,
      hostResidence: '',
      numberOfRoomsForRent: 1
    },
    principalResidence: {
      isPrincipalResidence: false,
      agreedToRentalAct: false,
      nonPrincipalOption: '',
      specifiedServiceProvider: '',
      agreedToSubmit: false
    },
    registrationType: RegistrationTypeE.HOST
  }
}

// validation schema for Individual Host Type
const primaryContactIndividual = z.object({
  contactType: z.literal(HostContactTypeE.INDIVIDUAL),
  firstName: requiredNonEmptyString50,
  lastName: requiredNonEmptyString50,
  middleName: optionalOrEmptyString,
  preferredName: optionalOrEmptyString,
  socialInsuranceNumber: requiredSin,
  businessLegalName: optionalOrEmptyString,
  businessNumber: optionalOrEmptyString,
  phoneNumber: requiredPhone,
  extension: optionalOrEmptyString15,
  faxNumber: optionalPhone,
  emailAddress: requiredEmail,
  address: requiredNonEmptyString,
  addressLineTwo: optionalOrEmptyString,
  country: requiredNonEmptyString,
  city: requiredNonEmptyString100,
  province: requiredNonEmptyString,
  postalCode: requiredNonEmptyString15,
  birthDay: requiredNumber
    .refine(day => day.length <= 2, 'Incorrect Date')
    .refine(day => Number(day) <= 31, 'Date must be less than or equal to 31')
    .refine(day => Number(day) > 0, 'Date must be less greater to 0'),
  birthMonth: requiredNonEmptyString,
  birthYear: requiredNumber
    .refine(year => Number(year) <= new Date().getFullYear(), 'Year must be in the past')
    .refine(year => year.length === 4, 'Year must be four digits')
    .refine(day => Number(day) > 0, 'Year must be greater than 0')
})

// validation schema for Business Host Type
const primaryContactBusiness = primaryContactIndividual.extend({
  contactType: z.literal(HostContactTypeE.BUSINESS),
  businessLegalName: requiredNonEmptyString50,
  socialInsuranceNumber: optionalOrEmptyString,
  birthDay: optionalOrEmptyString,
  birthMonth: optionalOrEmptyString,
  birthYear: optionalOrEmptyString
})

export const secondaryContactSchema = z.object({
  firstName: requiredNonEmptyString50,
  lastName: requiredNonEmptyString50,
  middleName: optionalOrEmptyString50,
  socialInsuranceNumber: optionalSin,
  businessNumber: optionalOrEmptyString,
  preferredName: optionalOrEmptyString,
  phoneNumber: requiredPhone,
  extension: optionalOrEmptyString15,
  faxNumber: optionalPhone,
  emailAddress: requiredEmail,
  address: requiredNonEmptyString,
  country: requiredNonEmptyString,
  addressLineTwo: optionalOrEmptyString,
  city: requiredNonEmptyString100,
  province: requiredNonEmptyString,
  postalCode: requiredNonEmptyString15,
  birthDay: optionalNumber
    .refine(day => Number(day) <= 31, 'Must be less than or equal to 31')
    .optional(),
  birthMonth: optionalOrEmptyString,
  birthYear: optionalNumber
    .refine(year => Number(year) <= new Date().getFullYear(), 'Year must be in the past')
    .refine(year => year?.length === 4, 'Year must be four digits')
    .optional()
    .or(z.literal(''))
})

// main Primary Contact Schema will selected based on contactType prop
export const primaryContactSchema = z.discriminatedUnion('contactType', [
  primaryContactIndividual,
  primaryContactBusiness
])
