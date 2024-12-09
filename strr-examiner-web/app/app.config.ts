export default defineAppConfig({
  strrBaseLayer: {
    page: {
      login: {
        redirectPath: '/dashboard',
        options: {
          createAccount: false,
          idps: () => ['idir'] // function required to overwrite default value, will merge if no function
        }
      }
    }
  },
  ui: {}
})
