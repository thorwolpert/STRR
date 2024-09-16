export default defineNuxtRouteMiddleware(() => {
  if (import.meta.server) { return }
  // check the user's acceptance of the Terms of Service
  useTermsOfService().checkTermsOfService()
})
