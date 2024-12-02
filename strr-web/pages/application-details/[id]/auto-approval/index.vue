<template>
  <div>
    <div>
      <BcrosBanner>
        <div class="flex flex-col m:justify-between">
          <BcrosTypographyH1
            :text="tAutoApproval('autoApprovalDetails')"
            class="mobile:text-6 mb-4"
            no-spacing
          />
          <p class="flex-shrink-0">
            {{ headerLabel }}
          </p>
        </div>
      </BcrosBanner>
    </div>
    <div class="mt-[104px] m:mt-[200px]">
      <div>
        <BcrosTypographyH2
          class="mobile:mx-2"
          :text="tAutoApproval('automaticLogic')"
        />
        <div class="bg-white py-[22px] px-[30px] mobile:px-2">
          <div class="flex flex-col justify-between w-full mobile:flex-col">
            <UTable :rows="automaticRows" />
          </div>
        </div>
      </div>
      <div class="mt-10">
        <div>
          <BcrosTypographyH2
            class="mobile:mx-2"
            :text="tAutoApproval('provisionalLogic')"
          />
          <div class="bg-white py-[22px] px-[30px] mobile:px-2">
            <div class="flex flex-col justify-between w-full mobile:flex-col">
              <UTable :rows="provisionalRows" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { AutoApprovalDataI } from '~/interfaces/auto-approval-data-i'

const route = useRoute()
const { t } = useTranslation()
const tAutoApproval = (translationKey: string) => t(`autoApproval.${translationKey}`)
const automaticRows = ref<{ [key: string]: string }[]>([])
const provisionalRows = ref<{ [key: string]: string }[]>([])

const { getAutoApproval } = useApplications()
const { setupBreadcrumbData } = useBreadcrumb()

const registrationId = parseInt(route.params.id.toString())

// Fetch applications and find application number based on registration id from params
const { applications } = await useApplications().getApplications()

const application = applications.find(app => app.header.registrationId === registrationId)

const applicationNumber = application?.header.applicationNumber

const data: AutoApprovalDataI[] = await getAutoApproval(applicationNumber || '') || {} as AutoApprovalDataI[]
const applicationDetails = application?.registration as HostApplicationDetailsI

setupBreadcrumbData(application || {} as ApplicationI)

const buildAutomaticRows = (rowsData: AutoApprovalDataI[]) => {
  if (!rowsData.length || !rowsData[0].record) {
    return
  }
  if (rowsData[0].record.renting !== null) {
    automaticRows.value.push({
      criteria: tAutoApproval('renting'),
      outcome: rowsData[0].record.renting ? tAutoApproval('yes') : tAutoApproval('no')
    })
  }
  if (rowsData[0].record.serviceProvider !== null) {
    automaticRows.value.push({
      criteria: tAutoApproval('accommodationSelected'),
      outcome: rowsData[0].record.serviceProvider ? tAutoApproval('yes') : tAutoApproval('no')
    })
  }
  if (rowsData[0].record.prExempt !== null) {
    automaticRows.value.push({
      criteria: tAutoApproval('prExempt'),
      outcome: rowsData[0].record.prExempt
        ? tAutoApproval('exempt')
        : rowsData[0].record.prExempt === false
          ? tAutoApproval('notExempt')
          : tAutoApproval('lookupFailed')
    })
  }
}

const buildProvisionalRows = (rowsData: AutoApprovalDataI[]) => {
  if (!rowsData.length || !rowsData[0].record) {
    return
  }
  if (rowsData[0].record.addressMatch !== null) {
    provisionalRows.value.push({
      criteria: tAutoApproval('addrMatchQuestion'),
      outcome: rowsData[0].record.addressMatch ? tAutoApproval('addrDoMatch') : tAutoApproval('addrDoNotMatch')
    })
  }

  const licenseNull =
    rowsData[0].record.businessLicenseRequired === null &&
    rowsData[0].record.businessLicenseProvided === null

  if (!licenseNull) {
    provisionalRows.value.push({
      criteria: tAutoApproval('businessLicenseReq'),
      outcome: rowsData[0].record.businessLicenseRequired
        ? rowsData[0].record.businessLicenseProvided
          ? tAutoApproval('requiredProvided')
          : tAutoApproval('requiredNotProvided')
        : tAutoApproval('notRequired')
    })
  }
  if (rowsData[0].record.titleCheck !== null) {
    provisionalRows.value.push({
      criteria: tAutoApproval('titleCheck'),
      outcome: rowsData[0].record.titleCheck ? tAutoApproval('ltsaPassed') : tAutoApproval('ltsaNotPassed')
    })
  }
}

buildAutomaticRows(data)
buildProvisionalRows(data)

const headerLabel =
  `${
    applicationDetails.unitAddress.nickname
      ? applicationDetails.unitAddress.nickname + ','
      : ''
  }` +
  `${applicationDetails.unitAddress.streetNumber} ` +
  `${applicationDetails.unitAddress.streetName}` +
  `${applicationDetails.unitAddress.unitNumber
    ? `, ${applicationDetails.unitAddress.unitNumber}`
    : ''}` +
  `${
    applicationDetails.unitAddress.addressLineTwo
      ? ' ' + applicationDetails.unitAddress.addressLineTwo
      : ''
  }, ` +
  `${applicationDetails.unitAddress.city} ` +
  `${applicationDetails.unitAddress.province} ` +
  `${applicationDetails.unitAddress.postalCode}` +
  `, Application #${applicationNumber}`

</script>
