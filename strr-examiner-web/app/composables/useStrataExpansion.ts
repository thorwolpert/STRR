import { StrataExpansionBusiness, StrataExpansionIndividuals, StrataExpansionBuildings } from '#components'

export const useStrataExpansion = (app: StrataApplicationResp) => {
  const exp = useStrrExpansion()

  const open = (component: any) => {
    exp.open(component, {
      application: app,
      onClose: exp.close
    })
  }

  const openBusiness = () => open(StrataExpansionBusiness)
  const openIndividuals = () => open(StrataExpansionIndividuals)
  const openAllBuildings = () => open(StrataExpansionBuildings)
  const close = () => exp.close()

  return {
    openBusiness,
    openIndividuals,
    openAllBuildings,
    close
  }
}
