export enum ApplicationStatusE {
  DRAFT = 'DRAFT',
  PAYMENT_DUE = 'PAYMENT_DUE',
  PAID = 'PAID',
  AUTO_APPROVED = 'AUTO_APPROVED',
  PROVISIONALLY_APPROVED = 'PROVISIONALLY_APPROVED',
  FULL_REVIEW_APPROVED = 'FULL_REVIEW_APPROVED',
  PROVISIONAL_REVIEW = 'PROVISIONAL_REVIEW',
  ADDITIONAL_INFO_REQUESTED = 'ADDITIONAL_INFO_REQUESTED',
  FULL_REVIEW = 'FULL_REVIEW',
  DECLINED = 'DECLINED',
  PROVISIONAL = 'PROVISIONAL'
}

export enum HostApplicationStatusE {
  DRAFT = 'Draft',
  PAYMENT_DUE = 'Payment Due',
  PAID = 'Pending Review',
  AUTO_APPROVED = 'Approved',
  PROVISIONALLY_APPROVED = 'Provisionally Approved', // eslint-disable-next-line @typescript-eslint/no-duplicate-enum-values
  FULL_REVIEW_APPROVED = 'Approved', // eslint-disable-next-line @typescript-eslint/no-duplicate-enum-values
  PROVISIONAL_REVIEW = 'Provisionally Approved', // eslint-disable-next-line @typescript-eslint/no-duplicate-enum-values
  FULL_REVIEW = 'Pending Review',
  DECLINED = 'Declined'
}

export enum ExaminerApplicationStatusE {
  DRAFT = 'Draft',
  PAYMENT_DUE = 'Payment Due',
  PAID = 'Paid',
  AUTO_APPROVED = 'Automatic Approval',
  PROVISIONALLY_APPROVED = 'Provisional Approval',
  FULL_REVIEW_APPROVED = 'Full Review Approval',
  PROVISIONAL_REVIEW = 'Provisional Review',
  FULL_REVIEW = 'Full Review',
  DECLINED = 'Declined'
}
