import { ApplicationStatusE, HostApplicationStatusE, ExaminerApplicationStatusE, AlertsFlavourE } from '#imports'

export const useChipFlavour = () => {
  const { t } = useTranslation()
  const { isExaminer } = useBcrosKeycloak()
  const tRegistryDashboardStatus = (translationKey: string) => t(`registryDashboard.statusChip.${translationKey}`)

  const statusMap = (flavour: AlertsFlavourE, translationKey: string) => ({
    alert: flavour,
    text: tRegistryDashboardStatus(translationKey)
  })

  const examinerOrHostStatusMap = (flavour: AlertsFlavourE, key: string) => ({
    alert: flavour,
    text: isExaminer
      ? tRegistryDashboardStatus(`examinerStatuses.${key}`)
      : tRegistryDashboardStatus(`hostStatuses.${key}`)
  })

  const getChipFlavour = (status: string): StatusChipFlavoursI['flavour'] => {
    switch (status) {
      case 'ACTIVE':
        return statusMap(AlertsFlavourE.SUCCESS, 'active')
      case 'DENIED':
        return statusMap(AlertsFlavourE.ALERT, 'denied')
      case 'APPROVED':
        return statusMap(AlertsFlavourE.SUCCESS, 'approved')
      case 'ISSUED':
        return statusMap(AlertsFlavourE.SUCCESS, 'issued')
      case 'REJECTED':
        return statusMap(AlertsFlavourE.ALERT, 'rejected')
      case 'PENDING':
        return statusMap(AlertsFlavourE.WARNING, 'pending')
      case 'UNDER_REVIEW':
        return statusMap(AlertsFlavourE.APPLIED, 'underReview')
      case 'SUBMITTED':
        return statusMap(AlertsFlavourE.APPLIED, 'submitted')
      case 'PAID':
      case HostApplicationStatusE.PAID:
      case ExaminerApplicationStatusE.PAID:
        return examinerOrHostStatusMap(AlertsFlavourE.APPLIED, 'paid')
      case ApplicationStatusE.DRAFT:
      case HostApplicationStatusE.DRAFT:
      case ExaminerApplicationStatusE.DRAFT:
        return examinerOrHostStatusMap(AlertsFlavourE.INFO, 'draft')
      case ApplicationStatusE.PAYMENT_DUE:
      case HostApplicationStatusE.PAYMENT_DUE:
      case ExaminerApplicationStatusE.PAYMENT_DUE:
        return examinerOrHostStatusMap(AlertsFlavourE.INFO, 'paymentDue')
      case ApplicationStatusE.AUTO_APPROVED:
      case HostApplicationStatusE.AUTO_APPROVED:
      case ExaminerApplicationStatusE.AUTO_APPROVED:
        return examinerOrHostStatusMap(AlertsFlavourE.SUCCESS, 'autoApproved')
      case ApplicationStatusE.PROVISIONALLY_APPROVED:
      case HostApplicationStatusE.PROVISIONALLY_APPROVED:
      case ExaminerApplicationStatusE.PROVISIONALLY_APPROVED:
        return examinerOrHostStatusMap(AlertsFlavourE.SUCCESS, 'provisionalApproved')
      case ApplicationStatusE.FULL_REVIEW_APPROVED:
      case HostApplicationStatusE.FULL_REVIEW_APPROVED:
      case ExaminerApplicationStatusE.FULL_REVIEW_APPROVED:
        return examinerOrHostStatusMap(AlertsFlavourE.SUCCESS, 'fullReviewApproved')
      case ApplicationStatusE.PROVISIONAL_REVIEW:
      case HostApplicationStatusE.PROVISIONAL_REVIEW:
      case ExaminerApplicationStatusE.PROVISIONAL_REVIEW:
        return examinerOrHostStatusMap(AlertsFlavourE.SUCCESS, 'provisionalReview')
      case ApplicationStatusE.FULL_REVIEW:
      case HostApplicationStatusE.FULL_REVIEW:
      case ExaminerApplicationStatusE.FULL_REVIEW:
        return examinerOrHostStatusMap(AlertsFlavourE.APPLIED, 'fullReview')
      case ApplicationStatusE.ADDITIONAL_INFO_REQUESTED:
        return statusMap(AlertsFlavourE.WARNING, 'additionalInfoRequested')
      case ApplicationStatusE.DECLINED:
      case HostApplicationStatusE.DECLINED:
      case ExaminerApplicationStatusE.DECLINED:
        return statusMap(AlertsFlavourE.ALERT, 'declined')
      case ApplicationStatusE.PROVISIONAL:
        return statusMap(AlertsFlavourE.APPLIED, 'provisional')
      default:
        return { alert: AlertsFlavourE.MESSAGE, text: '' }
    }
  }

  return { getChipFlavour }
}
