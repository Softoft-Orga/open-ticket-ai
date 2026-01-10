import type { Meta, StoryObj } from '@storybook/vue3'
import { ref } from 'vue'
import { TransitionRoot } from '@headlessui/vue'
import UiTransitionFade from '../src/components/vue/core/transitions/UiTransitionFade.vue'
import UiTransitionFadeScale from '../src/components/vue/core/transitions/UiTransitionFadeScale.vue'
import UiTransitionSlide from '../src/components/vue/core/transitions/UiTransitionSlide.vue'
import Button from '../src/components/vue/core/basic/Button.vue'

const meta: Meta = {
  title: 'Core/Transitions',
  parameters: {
    backgrounds: {
      default: 'dark',
      values: [
        { name: 'dark', value: '#0f0814' }
      ]
    }
  }
}
export default meta

type Story = StoryObj<typeof meta>

export const Fade: Story = {
  render: () => ({
    components: { TransitionRoot, UiTransitionFade, Button },
    setup() {
      const isOpen = ref(false)
      return { isOpen }
    },
    template: `
      <div class="p-8">
        <Button @click="isOpen = !isOpen" variant="primary">
          {{ isOpen ? 'Hide' : 'Show' }} Content
        </Button>
        
        <div class="mt-8 relative min-h-[200px]">
          <TransitionRoot :show="isOpen" as="template">
            <UiTransitionFade>
              <div class="bg-surface-dark border border-border-dark rounded-xl p-6 text-slate-200">
                <h3 class="text-lg font-semibold mb-2">Fade Transition</h3>
                <p class="text-slate-400">
                  This content fades in and out smoothly. Perfect for backdrops and overlays.
                </p>
              </div>
            </UiTransitionFade>
          </TransitionRoot>
        </div>
      </div>
    `
  })
}

export const FadeScaleSm: Story = {
  render: () => ({
    components: { TransitionRoot, UiTransitionFadeScale, Button },
    setup() {
      const isOpen = ref(false)
      return { isOpen }
    },
    template: `
      <div class="p-8">
        <Button @click="isOpen = !isOpen" variant="primary">
          {{ isOpen ? 'Hide' : 'Show' }} Content
        </Button>
        
        <div class="mt-8 relative min-h-[200px]">
          <TransitionRoot :show="isOpen" as="template">
            <UiTransitionFadeScale strength="sm">
              <div class="bg-surface-dark border border-border-dark rounded-xl p-6 text-slate-200">
                <h3 class="text-lg font-semibold mb-2">Fade + Scale (Small)</h3>
                <p class="text-slate-400">
                  The default choice for Dialog/Modal panels and Popover content.
                  Scales from 95% to 100% with a fade effect.
                </p>
              </div>
            </UiTransitionFadeScale>
          </TransitionRoot>
        </div>
      </div>
    `
  })
}

export const FadeScaleMd: Story = {
  render: () => ({
    components: { TransitionRoot, UiTransitionFadeScale, Button },
    setup() {
      const isOpen = ref(false)
      return { isOpen }
    },
    template: `
      <div class="p-8">
        <Button @click="isOpen = !isOpen" variant="primary">
          {{ isOpen ? 'Hide' : 'Show' }} Content
        </Button>
        
        <div class="mt-8 relative min-h-[200px]">
          <TransitionRoot :show="isOpen" as="template">
            <UiTransitionFadeScale strength="md">
              <div class="bg-surface-dark border border-border-dark rounded-xl p-6 text-slate-200">
                <h3 class="text-lg font-semibold mb-2">Fade + Scale (Medium)</h3>
                <p class="text-slate-400">
                  A stronger scale effect (90% to 100%) for emphasis.
                  Use for special modals or attention-grabbing animations.
                </p>
              </div>
            </UiTransitionFadeScale>
          </TransitionRoot>
        </div>
      </div>
    `
  })
}

export const SlideDown: Story = {
  render: () => ({
    components: { TransitionRoot, UiTransitionSlide, Button },
    setup() {
      const isOpen = ref(false)
      return { isOpen }
    },
    template: `
      <div class="p-8">
        <Button @click="isOpen = !isOpen" variant="primary">
          {{ isOpen ? 'Hide' : 'Show' }} Content
        </Button>
        
        <div class="mt-8 relative min-h-[200px]">
          <TransitionRoot :show="isOpen" as="template">
            <UiTransitionSlide direction="down">
              <div class="bg-surface-dark border border-border-dark rounded-xl p-6 text-slate-200">
                <h3 class="text-lg font-semibold mb-2">Slide Down</h3>
                <p class="text-slate-400">
                  Slides down from the top. Perfect for dropdown menus and select options.
                </p>
              </div>
            </UiTransitionSlide>
          </TransitionRoot>
        </div>
      </div>
    `
  })
}

export const SlideUp: Story = {
  render: () => ({
    components: { TransitionRoot, UiTransitionSlide, Button },
    setup() {
      const isOpen = ref(false)
      return { isOpen }
    },
    template: `
      <div class="p-8">
        <Button @click="isOpen = !isOpen" variant="primary">
          {{ isOpen ? 'Hide' : 'Show' }} Content
        </Button>
        
        <div class="mt-8 relative min-h-[200px]">
          <TransitionRoot :show="isOpen" as="template">
            <UiTransitionSlide direction="up">
              <div class="bg-surface-dark border border-border-dark rounded-xl p-6 text-slate-200">
                <h3 class="text-lg font-semibold mb-2">Slide Up</h3>
                <p class="text-slate-400">
                  Slides up from the bottom. Ideal for toasts, notifications, and bottom sheets.
                </p>
              </div>
            </UiTransitionSlide>
          </TransitionRoot>
        </div>
      </div>
    `
  })
}

export const SlideLeft: Story = {
  render: () => ({
    components: { TransitionRoot, UiTransitionSlide, Button },
    setup() {
      const isOpen = ref(false)
      return { isOpen }
    },
    template: `
      <div class="p-8">
        <Button @click="isOpen = !isOpen" variant="primary">
          {{ isOpen ? 'Hide' : 'Show' }} Content
        </Button>
        
        <div class="mt-8 relative min-h-[200px]">
          <TransitionRoot :show="isOpen" as="template">
            <UiTransitionSlide direction="left">
              <div class="bg-surface-dark border border-border-dark rounded-xl p-6 text-slate-200">
                <h3 class="text-lg font-semibold mb-2">Slide Left</h3>
                <p class="text-slate-400">
                  Slides in from the left. Great for slide-over panels from the left edge.
                </p>
              </div>
            </UiTransitionSlide>
          </TransitionRoot>
        </div>
      </div>
    `
  })
}

export const SlideRight: Story = {
  render: () => ({
    components: { TransitionRoot, UiTransitionSlide, Button },
    setup() {
      const isOpen = ref(false)
      return { isOpen }
    },
    template: `
      <div class="p-8">
        <Button @click="isOpen = !isOpen" variant="primary">
          {{ isOpen ? 'Hide' : 'Show' }} Content
        </Button>
        
        <div class="mt-8 relative min-h-[200px]">
          <TransitionRoot :show="isOpen" as="template">
            <UiTransitionSlide direction="right">
              <div class="bg-surface-dark border border-border-dark rounded-xl p-6 text-slate-200">
                <h3 class="text-lg font-semibold mb-2">Slide Right</h3>
                <p class="text-slate-400">
                  Slides in from the right. Perfect for slide-over panels from the right edge.
                </p>
              </div>
            </UiTransitionSlide>
          </TransitionRoot>
        </div>
      </div>
    `
  })
}

export const DialogExample: Story = {
  render: () => ({
    components: { TransitionRoot, UiTransitionFade, UiTransitionFadeScale, Button },
    setup() {
      const isOpen = ref(false)
      return { isOpen }
    },
    template: `
      <div class="p-8">
        <Button @click="isOpen = !isOpen" variant="primary">
          Open Dialog
        </Button>
        
        <TransitionRoot :show="isOpen" as="template">
          <div class="fixed inset-0 z-50 overflow-y-auto">
            <!-- Backdrop -->
            <UiTransitionFade>
              <div class="fixed inset-0 bg-black/80 backdrop-blur-sm" @click="isOpen = false" />
            </UiTransitionFade>
            
            <!-- Panel -->
            <div class="flex min-h-full items-center justify-center p-4">
              <UiTransitionFadeScale strength="sm">
                <div class="relative bg-surface-dark border border-border-dark rounded-2xl p-8 text-slate-200 max-w-md w-full shadow-xl">
                  <h3 class="text-2xl font-bold mb-4">Example Dialog</h3>
                  <p class="text-slate-400 mb-6">
                    This demonstrates a typical modal pattern using UiTransitionFade for the backdrop
                    and UiTransitionFadeScale for the panel.
                  </p>
                  <div class="flex gap-3">
                    <Button variant="primary" @click="isOpen = false">Confirm</Button>
                    <Button variant="outline" @click="isOpen = false">Cancel</Button>
                  </div>
                </div>
              </UiTransitionFadeScale>
            </div>
          </div>
        </TransitionRoot>
      </div>
    `
  })
}
