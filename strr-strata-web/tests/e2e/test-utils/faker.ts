import { faker, fakerEN_CA as fakerCa } from '@faker-js/faker'

export function getFakeContactDetails (): StrrContact {
  const firstName = faker.person.firstName()
  const lastName = faker.person.lastName()
  return {
    position: faker.person.jobTitle(),
    firstName,
    middleName: faker.person.middleName(),
    lastName,
    preferredName: faker.person.firstName(),
    phone: {
      countryIso2: 'CA',
      countryCode: '1',
      number: faker.phone.number({ style: 'national' }),
      extension: faker.number.int({ min: 1, max: 1000 }).toString()
    },
    faxNumber: faker.phone.number({ style: 'national' }),
    emailAddress: faker.internet.email({ firstName, lastName })
  }
}

function getFakeAddress () {
  return {
    street: faker.location.streetAddress(),
    streetAdditional: '',
    city: fakerCa.location.city(),
    region: fakerCa.location.state(),
    postalCode: fakerCa.location.zipCode(),
    country: 'CA',
    locationDescription: faker.lorem.sentence(),
    streetName: faker.location.street(),
    streetNumber: faker.number.int({ min: 100, max: 7000 }).toString(),
    unitNumber: faker.number.int({ min: 1, max: 1000 }).toString()
  }
}

export function getFakeBusinessDetails (): StrrBusiness {
  const businessAddress = getFakeAddress()
  return {
    legalName: faker.company.name(),
    homeJurisdiction: businessAddress.region,
    businessNumber: faker.helpers.fromRegExp(/[0-9]{9}BC[0-9]{4}/),
    mailingAddress: businessAddress,
    hasRegOffAtt: true,
    regOfficeOrAtt: {
      attorneyName: faker.person.fullName(),
      sameAsMailAddress: false,
      mailingAddress: getFakeAddress()
    }
  }
}

export function getFakeStrataDetails (): StrataDetails {
  return {
    brand: {
      name: faker.company.name(),
      website: faker.internet.url()
    },
    buildings: [getFakeAddress(), getFakeAddress()],
    location: getFakeAddress(),
    numberOfUnits: faker.number.int({ min: 10, max: 5000 })
  }
}