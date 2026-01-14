<template>
  <div>
    <slot
      name="trigger"
      :open="open"
    />

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
import { ref } from 'vue';
import Modal from './Modal.vue';
import type { Tone, Size } from '../design-system/tokens.ts';

interface Props {
  title?: string;
  tone?: Tone;
  size?: Size;
  closeOnOverlay?: boolean;
}

withDefaults(defineProps<Props>(), {
  title: undefined,
  tone: 'neutral',
  size: 'md',
  closeOnOverlay: true,
});

const isOpen = ref(false);

const open = () => {
  isOpen.value = true;
};

const close = () => {
  isOpen.value = false;
};
</script>
