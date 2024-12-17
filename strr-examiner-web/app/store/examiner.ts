export const useExaminerStore = defineStore('strr/examiner-store', () => {
  const { getAccountApplications } = useStrrApi()

  const { $strrApi } = useNuxtApp()

  const getAllApplications = async () => {
    return await getAccountApplications()
  }

  const getApplication = async (applicationNumber: string): Promise<ApiApplicationResp> => {
    return (await getAccountApplications(applicationNumber)) as ApiApplicationResp
  }

  const approveApplication = async (applicationNumber: string): Promise<void> => {
    await $strrApi(`/applications/${applicationNumber}/status`, {
      method: 'PUT',
      body: { status: ApplicationStatus.FULL_REVIEW_APPROVED }
    })
  }

  const rejectApplication = async (applicationNumber: string): Promise<void> => {
    await $strrApi(`/applications/${applicationNumber}/status`, {
      method: 'PUT',
      body: { status: ApplicationStatus.DECLINED }
    })
  }

  return {
    getAllApplications,
    getApplication,
    approveApplication,
    rejectApplication
  }
})
