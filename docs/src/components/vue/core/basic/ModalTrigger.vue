<template>
  <div>
    <slot
      name="button"
      :open="open"
    >
      <Button
        :variant="buttonVariant"
        :tone="buttonTone"
        :size="buttonSize"
        @click="open"
      >
        {{ buttonText }}
      </Button>
    </slot>

    <Modal
      :open="isOpen"
      :title="title"
      :tone="tone"
      :size="size"
      :close-on-overlay="closeOnOverlay"
      @close="close"
    >
      <template
        v-if="$slots.title"
        #title
      >
        <slot name="title" />
      </template>

      <slot />

      <template
        v-if="$slots.footer"
        #footer
      >
        <slot name="footer" />
      </template>
    </Modal>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import Button from './Button.vue'
import Modal from './Modal.vue'
import type { Tone, Size, Variant } from '../design-system/tokens.ts'

interface Props {
  title?: string
  tone?: Tone
  size?: Size
  closeOnOverlay?: boolean
  buttonText?: string
  buttonVariant?: Variant
  buttonTone?: Tone
  buttonSize?: Size
}

withDefaults(defineProps<Props>(), {
  title: undefined,
  tone: 'neutral',
  size: 'md',
  closeOnOverlay: true,
  buttonText: 'Open',
  buttonVariant: 'surface',
  buttonTone: 'primary',
  buttonSize: 'md'
})

const isOpen = ref(false)

const open = () => {
  isOpen.value = true
}

const close = () => {
  isOpen.value = false
}
</script>
