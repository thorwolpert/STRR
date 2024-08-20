import { ApplicationStatusE } from '#imports'

export interface PaginatedApplicationsI {
  applications: ApplicationI[],
  limit: number,
  page: number,
  total: number
}

export interface SearchApplicationsI {
  status: ApplicationStatusE,
  text: String,
  limit: number,
  page: number
}
