export const useExaminerStore = defineStore('strr/examiner-store', () => {
  const { getAccountApplications } = useStrrApi()

  const { $strrApi } = useNuxtApp()

  const getAllApplications = async () => {
    return await getAccountApplications()
  }

  const getApplication = async (applicationNumber: string): Promise<ApiApplicationResp> => {
    return (await getAccountApplications(applicationNumber)) as ApiApplicationResp
  }

  // Fetch next Application to examiner when navigating to Examiner tab
  const getNextApplication = async (): Promise<string> => {
    const applications = await getAccountApplications(undefined, ApplicationType.HOST) as ApiApplicationBaseResp[]
    // for now just get the first available Host Application
    return applications[0].header.applicationNumber
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
    rejectApplication,
    getNextApplication
  }
})
