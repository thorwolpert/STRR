import { RoutesE } from '~/enums/routes'

export default defineAppConfig({
  connect: {
    core: {
      login: {
        redirectPath: '',
        idps: () => ['idir']
      },
      header: {
        options: {
          localeSelect: false,
          unauthenticated: {
            whatsNew: false,
            loginMenu: false,
            createAccount: false
          },
          authenticated: {
            notifications: true,
            accountOptionsMenu: true
          }
        }
      },
      plugin: {
        authApi: {
          errorRedirect: {
            401: '/auth/login'
          }
        },
        payApi: {
          errorRedirect: {
            401: '/auth/login'
          }
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
