import { vi } from 'vitest'

vi.mock('vue-i18n', async (importOriginal) => {
  const actual = await importOriginal()
  return {
    ...(actual as any),
    useI18n: () => ({
      t: (key: string) => key
    })
  }
})

import { config } from '@vue/test-utils'
import { dataTestId } from './plugins/data-test-id'

config.global.plugins.push(dataTestId)
