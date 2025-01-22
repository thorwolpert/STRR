import { StrataExpansionBusiness, StrataExpansionIndividuals, StrataExpansionBuildings } from '#components'

export const useStrataExpansion = (app: StrataApplicationResp) => {
  const exp = useStrrExpansion()

  const open = (component: any) => {
    exp.open(component, {
      application: app,
      onClose: exp.close
    })
  }

  function openBusiness () {
    open(StrataExpansionBusiness)
  }

  function openIndividuals () {
    open(StrataExpansionIndividuals)
  }

  function openAllBuildings () {
    open(StrataExpansionBuildings)
  }

  function close () {
    exp.close()
  }

  return {
    openBusiness,
    openIndividuals,
    openAllBuildings,
    close
  }
}
