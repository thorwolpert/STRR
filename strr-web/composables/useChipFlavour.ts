import { HostApplicationStatusE, ExaminerApplicationStatusE } from '#imports'

export const useChipFlavour = () => {
  const { t } = useTranslation()
  const { isExaminer } = useBcrosKeycloak()
  const tRegistryDashboardStatus = (translationKey: string) => t(`registryDashboard.statusChip.${translationKey}`)

  const getChipFlavour = (status: string): StatusChipFlavoursI['flavour'] => {
    switch (status) {
      case 'ACTIVE':
        return {
          text: tRegistryDashboardStatus('active'),
          alert: AlertsFlavourE.SUCCESS
        }
      case 'DENIED':
        return {
          text: tRegistryDashboardStatus('denied'),
          alert: AlertsFlavourE.ALERT
        }
      case 'APPROVED':
        return {
          alert: AlertsFlavourE.SUCCESS,
          text: tRegistryDashboardStatus('approved')
        }
      case 'ISSUED':
        return {
          alert: AlertsFlavourE.SUCCESS,
          text: tRegistryDashboardStatus('issued')
        }
      case 'REJECTED':
        return {
          alert: AlertsFlavourE.ALERT,
          text: tRegistryDashboardStatus('rejected')
        }
      case 'PENDING':
        return {
          alert: AlertsFlavourE.WARNING,
          text: tRegistryDashboardStatus('pending')
        }
      case 'UNDER_REVIEW':
        return {
          alert: AlertsFlavourE.APPLIED,
          text: tRegistryDashboardStatus('underReview')
        }
      case 'SUBMITTED':
        return {
          alert: AlertsFlavourE.APPLIED,
          text: tRegistryDashboardStatus('submitted')
        }
      case 'PAID':
      case HostApplicationStatusE.PAID:
      case ExaminerApplicationStatusE.PAID:
        return {
          alert: AlertsFlavourE.APPLIED,
          text: isExaminer ? tRegistryDashboardStatus('paidExaminer') : tRegistryDashboardStatus('paidHost')
        }
      case ApplicationStatusE.DRAFT:
      case HostApplicationStatusE.DRAFT:
      case ExaminerApplicationStatusE.DRAFT:
        return {
          alert: AlertsFlavourE.INFO,
          text: tRegistryDashboardStatus('draft')
        }
      case ApplicationStatusE.PAYMENT_DUE:
      case HostApplicationStatusE.PAYMENT_DUE:
      case ExaminerApplicationStatusE.PAYMENT_DUE:
        return {
          alert: AlertsFlavourE.INFO,
          text: tRegistryDashboardStatus('paymentDue')
        }
      case ApplicationStatusE.AUTO_APPROVED:
      case HostApplicationStatusE.AUTO_APPROVED:
      case ExaminerApplicationStatusE.AUTO_APPROVED:
        return {
          alert: AlertsFlavourE.SUCCESS,
          text: isExaminer
            ? tRegistryDashboardStatus('autoApprovedExaminer')
            : tRegistryDashboardStatus('autoApprovedHost')
        }
      case ApplicationStatusE.PROVISIONALLY_APPROVED:
      case HostApplicationStatusE.PROVISIONALLY_APPROVED:
      case ExaminerApplicationStatusE.PROVISIONALLY_APPROVED:
        return {
          alert: AlertsFlavourE.SUCCESS,
          text: isExaminer
            ? tRegistryDashboardStatus('provisionalApprovedExaminer')
            : tRegistryDashboardStatus('provisionalApprovedHost')
        }
      case ApplicationStatusE.FULL_REVIEW_APPROVED:
      case HostApplicationStatusE.FULL_REVIEW_APPROVED:
      case ExaminerApplicationStatusE.FULL_REVIEW_APPROVED:
        return {
          alert: AlertsFlavourE.SUCCESS,
          text: isExaminer
            ? tRegistryDashboardStatus('fullReviewApprovedExaminer')
            : tRegistryDashboardStatus('fullReviewApprovedHost')
        }
      case ApplicationStatusE.PROVISIONAL_REVIEW:
      case HostApplicationStatusE.PROVISIONAL_REVIEW:
      case ExaminerApplicationStatusE.PROVISIONAL_REVIEW:
        return {
          alert: AlertsFlavourE.SUCCESS,
          text: isExaminer
            ? tRegistryDashboardStatus('provisionalReviewExaminer')
            : tRegistryDashboardStatus('provisionalReviewHost')
        }
      case ApplicationStatusE.FULL_REVIEW:
      case HostApplicationStatusE.FULL_REVIEW:
      case ExaminerApplicationStatusE.FULL_REVIEW:
        return {
          alert: AlertsFlavourE.APPLIED,
          text: isExaminer
            ? tRegistryDashboardStatus('fullReviewExaminer')
            : tRegistryDashboardStatus('fullReviewHost')
        }
      case ApplicationStatusE.ADDITIONAL_INFO_REQUESTED:
        return {
          alert: AlertsFlavourE.WARNING,
          text: tRegistryDashboardStatus('additionalInfoRequested')
        }
      case ApplicationStatusE.DECLINED:
      case HostApplicationStatusE.DECLINED:
      case ExaminerApplicationStatusE.DECLINED:
        return {
          alert: AlertsFlavourE.ALERT,
          text: tRegistryDashboardStatus('declined')
        }
      case ApplicationStatusE.PROVISIONAL:
        return {
          alert: AlertsFlavourE.APPLIED,
          text: tRegistryDashboardStatus('provisional')
        }
      default:
        return {
          alert: AlertsFlavourE.MESSAGE,
          text: ''
        }
    }
  }

  return { getChipFlavour }
}
