import axios from 'axios'
import { ApplicationI, ApplicationStatusE } from '#imports'

export const useApplications = () => {
  const apiURL = useRuntimeConfig().public.strrApiURL
  const axiosInstance = addAxiosInterceptors(axios.create())
  const { handlePaymentRedirect } = useFees()

  /**
   * Create a new STR Application and redirect user to the payment page.
   */
  const createApplication = async (
    userFirstName: string,
    userLastName: string,
    hasSecondaryContact: boolean,
    propertyType: string,
    ownershipType: string
  ) => {
    const formData: CreateAccountFormAPII = formStateToApi(
      formState,
      userFirstName,
      userLastName,
      hasSecondaryContact,
      propertyType,
      ownershipType
    )

    try {
      const response = await axiosInstance.post(`${apiURL}/applications`, { ...formData })
      const data = response?.data

      if (!data) {
        throw new Error('Invalid AUTH API response')
      }

      const { header } = data
      handlePaymentRedirect(header.paymentToken, header.id)

      return data
    } catch (error) {
      console.warn('Error creating account.')
      console.error(error)
    }
  }

  /**
   * Retrieves STR Application by Id.
   *
   * @param {string} id - The Id of the application to retrieve.
   */
  const getApplication = async (id: string): Promise<ApplicationI> => {
    const { data } = await axiosInstance.get(`${apiURL}/applications/${id}`)
    return data
  }

  /**
   * Get all STR Applications from the API and sorts them by status and city.
   * If no applications are found, the user is redirected to the create account page.
   */
  const getApplications = async (): Promise<PaginatedApplicationsI> => {
    const { data } = await axiosInstance.get<PaginatedApplicationsI>(`${apiURL}/applications`)
    return data
  }

  const getPaginatedApplications = async (paginationObject: SearchApplicationsI): Promise<PaginatedApplicationsI> => {
    // remove all empty params before constructing a query params
    const params = Object.entries(paginationObject).reduce((acc, [key, value]) => {
      if (value !== '') {
        acc[key as keyof SearchApplicationsI] = value
      }
      return acc
    }, {} as Partial<SearchApplicationsI>)

    const queryParams = new URLSearchParams(params as Record<string, string>)

    const { data } = await axiosInstance.get<PaginatedApplicationsI>(`${apiURL}/applications/search?${queryParams}`)
    return data
  }

  const getApplicationsByStatus = async (applicationStatus: ApplicationStatusE): Promise<PaginatedApplicationsI> => {
    const { data } = await axiosInstance.get<PaginatedApplicationsI>(`${apiURL}/applications/search`, {
      params: { status: applicationStatus }
    })
    return data
  }

  const getApplicationHistory = async (id: string): Promise<ApplicationHistoryEventI[]> => {
    const { data } = await axiosInstance.get(`${apiURL}/applications/${id}/events`)
    return data
  }

  // TODO: this will be replaced with documents data from GET /applications call
  const getDocumentsForApplication = async (id: string): Promise<ApplicationI[]> => {
    const res = await axiosInstance.get(`${apiURL}/applications/${id}/documents`)
    return res.data
  }

  const getFile = async (id: string, documentId: string): Promise<Blob> => {
    const response = await axiosInstance.get(`${apiURL}/applications/${id}/documents/${documentId}/file`, {
      responseType: 'blob'
    })
    return response.data
  }

  /**
   * Approve an Application by setting its status to APPROVED.
   * @param id - The id of the Application to approve.
   */
  const approveApplication = async (id: string) => {
    try {
      await updateApplicationStatus(id, ApplicationStatusE.APPROVED)
    } catch (error) {
      console.error(error)
    }
  }

  /**
   * Reject an application by setting its status to REJECTED.
   * @param id - The id of the Application to reject.
   */
  const rejectApplication = async (id: string) => {
    try {
      await updateApplicationStatus(id, ApplicationStatusE.REJECTED)
    } catch (error) {
      console.error(error)
    }
  }

  /**
   * Update the status of an application.
   * @param id - The id of the Application.
   * @param status - The status to set for the Application.
   */
  const updateApplicationStatus = async (id: string, status: ApplicationStatusE) => {
    await axiosInstance.put(`${apiURL}/applications/${id}/status`, { status: `${status}` })
    window.location.reload()
  }

  return {
    getApplication,
    getApplications,
    getApplicationsByStatus,
    getPaginatedApplications,
    createApplication,
    getApplicationHistory,
    getDocumentsForApplication,
    getFile,
    approveApplication,
    rejectApplication
  }
}
