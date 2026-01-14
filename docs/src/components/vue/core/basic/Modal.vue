<template>
  <TransitionRoot
    :show="open"
    as="template"
  >
    <Dialog
      as="div"
      class="relative z-50"
      @close="handleClose"
    >
      <!-- Backdrop -->
      <TransitionChild
        v-bind="fade"
        as="template"
      >
        <div class="fixed inset-0 bg-black/80 backdrop-blur-sm" />
      </TransitionChild>

      <!-- Modal container -->
      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
          <TransitionChild
            v-bind="fadeScaleSm"
            as="template"
          >
            <DialogPanel :class="panelClasses">
              <!-- Header -->
              <div
                v-if="title || $slots.title"
                class="flex items-start justify-between mb-6"
              >
                <DialogTitle
                  v-if="!$slots.title"
                  as="h3"
                  class="text-2xl font-bold text-white"
                >
                  {{ title }}
                </DialogTitle>
                <slot
                  v-else
                  name="title"
                />
                <button
                  type="button"
                  :class="closeButtonClasses"
                  @click="handleClose"
                >
                  <XMarkIcon
                    class="w-6 h-6"
                    aria-hidden="true"
                  />
                </button>
              </div>

              <!-- Body -->
              <div class="text-slate-300">
                <slot />
              </div>

              <!-- Footer -->
              <div
                v-if="$slots.footer"
                class="mt-6 pt-6 border-t border-border-dark/40"
              >
                <slot name="footer" />
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { Dialog, DialogPanel, DialogTitle, TransitionRoot, TransitionChild } from '@headlessui/vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'
import { surface } from '../design-system/recipes/surface'
import { button } from '../design-system/recipes/button'
import { fade, fadeScaleSm } from '../transitions/presets'
import type { Tone, Size } from '../design-system/tokens.ts'

interface Props {
  open: boolean
  title?: string
  tone?: Tone
  size?: Size
  closeOnOverlay?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  title: undefined,
  tone: 'neutral',
  size: 'md',
  closeOnOverlay: true
})

const emit = defineEmits<{
  close: []
}>()

const handleClose = () => {
  if (props.closeOnOverlay) {
    emit('close')
  }
}

const panelClasses = computed(() => {
  const sizeClasses = {
    sm: 'max-w-md',
    md: 'max-w-2xl',
    lg: 'max-w-4xl'
  }

  return [
    'w-full transform overflow-hidden text-left align-middle transition-all',
    sizeClasses[props.size],
    surface({
      variant: 'surface',
      tone: props.tone,
      radius: '2xl',
      elevation: 'lg',
      intensity: props.tone !== 'neutral' ? 'soft' : 'none'
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
</script>
