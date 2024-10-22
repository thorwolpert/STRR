import type { Form } from '#ui/types'
import type { ZodSchema } from 'zod'

export const getOwnershipTypeDisplay = (ownershipType: string | null, t: (key: string) => string) => {
  switch (ownershipType) {
    case 'CO_OWN':
      return t('coOwner')
    case 'OWN':
      return t('owner')
    case 'RENT':
      return t('rent')
    default:
      return ownershipType ?? '-'
  }
}

export const hasFormErrors = (form: Form<any> | undefined, paths: string[]) => {
  for (const path of paths) {
    if (form && form.getErrors(path)?.length) {
      return true
    }
  }
  return false
}

export const validateSchemaAgainstState = (schema: ZodSchema<any>, state: any, formId: string) => {
  const result = schema.safeParse(state)

  if (result.success) {
    return {
      formId,
      success: true,
      errors: []
    }
  } else {
    return {
      formId,
      success: false,
      errors: result.error.issues
    }
  }
}
