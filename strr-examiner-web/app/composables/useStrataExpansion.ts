// https://ui.nuxt.com/components/modal#control-programmatically

import { StrataExpansionBusiness } from '#components'

export const useStrataExpansion = () => {
  const exp = useStrrExpansion()

  function openBusiness (
    application: StrataApplicationResp
  ) {
    exp.open(StrataExpansionBusiness, {
      application,
      onClose () {
        exp.close()
      }
    })
  }

  function close () {
    exp.close()
  }

  return {
    openBusiness,
    close
  }
}
