import { RoutesE } from '~/enums/routes'

export default defineAppConfig({
  connect: {
    core: {
      header: {
        options: {
          localeSelect: false
        }
      }
    }
  },
  strrBaseLayer: {
    page: {
      login: {
        redirectPath: RoutesE.DASHBOARD,
        options: {
          createAccount: false,
          idps: () => ['idir'] // function required to overwrite default value, will merge if no function
        }
      }
    }
  },
  ui: {}
})
