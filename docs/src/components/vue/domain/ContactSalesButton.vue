<template>
  <div>
    <Button
      variant="surface"
      tone="primary"
      @click="isOpen = true"
    >
      {{ buttonText }}
    </Button>

    <TransitionRoot
      :show="isOpen"
      as="template"
    >
      <Dialog
        as="div"
        class="relative z-50"
        @close="isOpen = false"
      >
        <TransitionChild
          v-bind="fade"
          as="template"
        >
          <div class="fixed inset-0 bg-black/80 backdrop-blur-sm" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4">
            <TransitionChild
              v-bind="fadeScaleSm"
              as="template"
            >
              <DialogPanel :class="panelClasses">
                <div class="flex items-start justify-between mb-6">
                  <DialogTitle
                    as="h3"
                    class="text-2xl font-bold text-white"
                  >
                    {{ formTitle }}
                  </DialogTitle>
                  <button
                    type="button"
                    :class="closeButtonClasses"
                    @click="isOpen = false"
                  >
                    <XMarkIcon
                      class="w-6 h-6"
                      aria-hidden="true"
                    />
                  </button>
                </div>

                <form
                  name="contact-sales"
                  method="POST"
                  action="/success/contact-sales"
                  data-netlify="true"
                  netlify-honeypot="bot-field"
                  class="space-y-4"
                >
                  <input
                    type="hidden"
                    name="form-name"
                    value="contact-sales"
                  >
                  <input
                    type="hidden"
                    name="bot-field"
                  >

                  <div>
                    <label
                      for="subject"
                      class="block text-sm font-medium text-text-1 mb-2"
                    >
                      Subject
                    </label>
                    <input
                      id="subject"
                      v-model="formData.subject"
                      type="text"
                      name="subject"
                      required
                      :class="inputClasses"
                    >
                  </div>

                  <div>
                    <label
                      for="email"
                      class="block text-sm font-medium text-text-1 mb-2"
                    >
                      Email
                    </label>
                    <input
                      id="email"
                      v-model="formData.email"
                      type="email"
                      name="email"
                      required
                      :class="inputClasses"
                    >
                  </div>

                  <div>
                    <label
                      for="message"
                      class="block text-sm font-medium text-text-1 mb-2"
                    >
                      Message
                    </label>
                    <textarea
                      id="message"
                      v-model="formData.message"
                      name="message"
                      rows="4"
                      required
                      :class="inputClasses"
                    />
                  </div>

                  <div class="flex gap-3 pt-4">
                    <Button
                      type="submit"
                      variant="surface"
                      tone="primary"
                      class="flex-1"
                    >
                      Submit
                    </Button>
                    <Button
                      type="button"
                      variant="outline"
                      tone="neutral"
                      class="flex-1"
                      @click="handleCancel"
                    >
                      Cancel
                    </Button>
                  </div>
                </form>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { Dialog, DialogPanel, DialogTitle, TransitionRoot, TransitionChild } from '@headlessui/vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'
import Button from '../core/basic/Button.vue'
import { surface } from '../../../design-system/recipes/surface'
import { button } from '../../../design-system/recipes/button'
import { input } from '../../../design-system/recipes/input'
import { fade, fadeScaleSm } from '../core/transitions/presets'

interface Props {
  buttonText: string
  formTitle: string
}

const props = defineProps<Props>()

const isOpen = ref(false)
const formData = ref({
  subject: props.formTitle,
  email: '',
  message: ''
})

const handleCancel = () => {
  isOpen.value = false
  formData.value = {
    subject: props.formTitle,
    email: '',
    message: ''
  }
}

const panelClasses = computed(() => {
  return [
    'w-full max-w-2xl transform overflow-hidden text-left align-middle transition-all',
    surface({
      variant: 'surface',
      tone: 'neutral',
      radius: '2xl',
      elevation: 'lg'
    }),
    'p-8'
  ].join(' ')
})

const closeButtonClasses = computed(() => {
  return button({
    variant: 'subtle',
    tone: 'neutral',
    size: 'sm',
    radius: 'lg'
  })
})

const inputClasses = computed(() => {
  return input({
    tone: 'neutral',
    size: 'md',
    radius: 'lg'
  })
})
</script>
