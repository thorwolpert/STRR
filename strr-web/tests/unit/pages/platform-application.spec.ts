import { mount } from '@vue/test-utils'
import PlatformApplication from '@/pages/platform-application.vue'
import { BcrosStepper } from '#components'

describe('Platform Application tests', () => {
  it('renders page and components correctly', () => {
    const wrapper = mount(PlatformApplication)
    expect(wrapper.exists()).toBe(true)

    expect(wrapper.find('h1').exists()).toBe(true)

    const stepper = wrapper.findComponent(BcrosStepper)
    expect(stepper.exists()).toBe(true)
    expect(stepper.vm.steps.length).toBe(4)
  })
})
