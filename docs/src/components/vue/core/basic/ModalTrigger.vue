<template>
  <div>
    <Button
      :variant="buttonVariant"
      :tone="buttonTone"
      :size="buttonSize"
      :radius="buttonRadius"
      :disabled="buttonDisabled"
      :loading="buttonLoading"
      :block="buttonBlock"
      :to="buttonTo"
      :href="buttonHref"
      @click="open"
    >
      {{ buttonText }}
    </Button>

    <Modal
      :open="isOpen"
      :title="title"
      :tone="tone"
      :size="size"
      :close-on-overlay="closeOnOverlay"
      @close="close"
    >
      <template v-if="$slots.title" #title>
        <slot name="title" />
      </template>

      <slot />

      <template v-if="$slots.footer" #footer>
        <slot name="footer" />
      </template>
    </Modal>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import Modal from './Modal.vue';
import Button from './Button.vue';
import type { Tone, Size, Variant, Radius } from '../design-system/tokens.ts';

interface Props {
  title?: string;
  tone?: Tone;
  size?: Size;
  closeOnOverlay?: boolean;
  buttonText?: string;
  buttonVariant?: Variant;
  buttonTone?: Tone;
  buttonSize?: Size;
  buttonRadius?: Radius;
  buttonDisabled?: boolean;
  buttonLoading?: boolean;
  buttonBlock?: boolean;
  buttonTo?: string;
  buttonHref?: string;
}

withDefaults(defineProps<Props>(), {
  title: undefined,
  tone: 'neutral',
  size: 'md',
  closeOnOverlay: true,
  buttonText: 'Open Modal',
  buttonVariant: 'surface',
  buttonTone: 'primary',
  buttonSize: 'md',
  buttonRadius: 'xl',
  buttonDisabled: false,
  buttonLoading: false,
  buttonBlock: false,
  buttonTo: undefined,
  buttonHref: undefined,
});

const isOpen = ref(false);

const open = () => {
  isOpen.value = true;
};

const close = () => {
  isOpen.value = false;
};
</script>
