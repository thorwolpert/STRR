import {
  applicationDetailsBreadcrumb,
  breadcrumbs,
  examinerApplicationDetailsBreadcrumb
} from '~/page-data/breadcrumbs'

export const useBreadcrumb = () => {
  const route = useRoute()
  const strrStore = useStrrStore()
  const { getApplicationId, getApplicationNickname, getRegistrationNumber } = storeToRefs(strrStore)
  const { isExaminer } = useBcrosKeycloak()
  const { t } = useTranslation()

  const { setApplicationId, setApplicationNickname, setRegistrationNumber } = useStrrStore()

  const NO_BREADCRUMB_ROUTES = [
    RouteNamesE.TERMS_OF_SERVICE,
    RouteNamesE.FINALIZATION,
    RouteNamesE.ACCOUNT_SELECT,
    RouteNamesE.APPLICATION_SUBMITTED
  ]

  // set store values for breadcrumb
  const setupBreadcrumbData = (application: ApplicationI) => {
    setApplicationId(application?.header.id.toString())
    setApplicationNickname(application?.registration.unitAddress.nickname)
    setRegistrationNumber(application?.header.registrationNumber)
    console.log('finished setting up')
  }

  // Generate a breadcrumb array for Examiner role
  const getExaminerBreadcrumb = () => {
    const examinerBreadcrumb = [...examinerApplicationDetailsBreadcrumb]

    examinerBreadcrumb[1] = {
      label: `${getApplicationNickname.value ? `${getApplicationNickname.value}, ` : ''}Application #${
        getApplicationId.value
      }`,
      to: `/${RouteNamesE.APPLICATION_DETAILS}/${getApplicationId.value}`
    }

    return examinerBreadcrumb
  }

  // Remove '-id' suffix and language codes (e.g., '___en') from route names to match RouteNamesE enum values
  const cleanupRoute = (routeName: string) => {
    return routeName?.replace(/(-id|___\w{2}$)/g, '') as RouteNamesE
  }

  /**
   * Create breadcrumb links for the current route, including dynamic labels based on
   * application or registration details.
   *
   * @returns {BreadcrumbI[]} An array of breadcrumb objects for the current route
   */
  const getBreadcrumbLinks = computed((): BreadcrumbI[] => {
    const routeName = route.name?.toString()

    // cleanup route from locale and id suffix
    const currentRouteName = cleanupRoute(routeName as RouteNamesE)

    // set base breadcrumb
    let baseBreadcrumb = [...(breadcrumbs[currentRouteName as RouteNamesE] || applicationDetailsBreadcrumb)]

    // get nickname or set as empty string
    const nickname = getApplicationNickname.value ? `${getApplicationNickname.value}, ` : ''

    // ad custom Breadcrumb info based on route
    switch (currentRouteName) {
      case RouteNamesE.APPLICATION_DETAILS:
        if (isExaminer) {
          baseBreadcrumb = getExaminerBreadcrumb()
        }
        baseBreadcrumb[1] = {
          label: `${nickname}Application #${getApplicationId.value}`
        }
        break
      case RouteNamesE.APPLICATION_DETAILS_LTSA:
      case RouteNamesE.APPLICATION_DETAILS_AUTO_APPROVAL:
        if (isExaminer) {
          baseBreadcrumb = getExaminerBreadcrumb()
        }

        baseBreadcrumb[2] = {
          label:
            currentRouteName === RouteNamesE.APPLICATION_DETAILS_LTSA
              ? t('ltsa.ltsaDetails')
              : t('autoApproval.automaticDetails')
        }

        break
      case RouteNamesE.REGISTRATION_DETAILS:
        baseBreadcrumb[1] = {
          label: `${nickname}Registration #${getRegistrationNumber.value}`
        }
        break
      default:
        break
    }

    return baseBreadcrumb
  })

  // Disable Dashboard Back Button when already at top route (eg Dashboard route)
  const isDashboardButtonDisabled = computed((): boolean => {
    return [RouteNamesE.REGISTRY_DASHBOARD, RouteNamesE.APPLICATION_STATUS].includes(
      cleanupRoute(route.name?.toString() || '')
    )
  })

  // Check if breadcrumbs should be visible on certain routes
  const isBreadcrumbVisible = computed((): boolean =>
    NO_BREADCRUMB_ROUTES.every(routeName => !route.name?.toString().startsWith(routeName))
  )

  // Set the dashboard button link based on the role
  const dashboardButtonLink: string = isExaminer
    ? `/${RouteNamesE.REGISTRY_DASHBOARD}`
    : `/${RouteNamesE.APPLICATION_STATUS}`

  return {
    setupBreadcrumbData,
    getBreadcrumbLinks,
    isDashboardButtonDisabled,
    dashboardButtonLink,
    isBreadcrumbVisible
  }
}
