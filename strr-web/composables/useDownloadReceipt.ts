export const useDownloadReceipt = () => {
  const { t } = useTranslation()
  const tRegistrationStatus = (translationKey: string) => t(`registrationStatus.${translationKey}`)
  const { getReceipt } = useApplications()

  const downloadReceipt = async (appNum: string) => {
    const pdfBlob = await getReceipt(appNum)
    const link = document.createElement('a')
    link.href = window.URL.createObjectURL(pdfBlob)
    link.target = '_blank'
    link.download = `${tRegistrationStatus('strrReceipt')}.pdf`
    document.body.appendChild(link)
    link.click()
    URL.revokeObjectURL(link.href)
  }

  return {
    downloadReceipt
  }
}
