import axios from 'axios'

/**
 * Composable to manage Terms of Service (ToS) checks and user acceptance.
 */
export const useTermsOfService = () => {
  const strrApiURL = useRuntimeConfig().public.strrApiURL
  const axiosInstance = addAxiosInterceptors(axios.create())
  const { tos, isTosAccepted } = storeToRefs(useBcrosAccount())

  async function checkTermsOfService () {
    // if ToS is already loaded, check acceptance status
    // this prevents multiple fetch calls to get ToS
    if (tos.value) {
      return handleTosAcceptance(tos.value.isTermsOfUseAccepted)
    }

    try {
      // fetch ToS data if not already loaded
      const { data } = await axiosInstance.get<TermsOfServiceI>(`${strrApiURL}/users/tos`)
      tos.value = data // Update the tos state

      // handle acceptance status after fetching
      return handleTosAcceptance(data.isTermsOfUseAccepted)
    } catch (error) {
      console.error('Error fetching Terms Of Service:', error)
    }
  }

  function handleTosAcceptance (isAccepted: boolean) {
    if (!isAccepted) {
      // if user has not accepted the terms, redirect to ToS page
      navigateTo('/terms-of-service')
    } else {
      // if user already accepted the terms, update the store and continue without redirect
      isTosAccepted.value = true
    }
  }

  async function acceptTermsOfService (acceptance: boolean, versionId: string): Promise<void> {
    try {
      await axiosInstance
        .patch<TermsOfServiceI>(`${strrApiURL}/users/tos`, {
          istermsaccepted: acceptance,
          termsversion: versionId
        })
      await useBcrosAccount().setAccountInfo()
      navigateTo(acceptance ? '/create-account' : '/')
    } catch (error) {
      console.error('Error accepting Terms Of Service:', error)
    }
  }

  return {
    checkTermsOfService,
    acceptTermsOfService
  }
}