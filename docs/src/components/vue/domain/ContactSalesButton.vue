<template>
  <ModalTrigger :title="formTitle">
    <template #trigger="{ open }">
      <Button tone="primary" variant="surface" @click="open">
        <slot />
      </Button>
    </template>

    <form
      :action="successActionUrl"
      class="space-y-4"
      data-netlify="true"
      method="POST"
      name="contact-sales"
    >
      <input type="hidden" name="form-name" value="contact-sales" />

      <div>
        <label class="mb-2 block text-sm font-medium text-text-1" for="subject"> Subject </label>
        <input
          id="subject"
          :class="inputClasses"
          name="subject"
          required
          type="text"
          :value="formTitle"
        />
      </div>

      <div>
        <label class="mb-2 block text-sm font-medium text-text-1" for="email"> Email </label>
        <input
          id="email"
          :class="inputClasses"
          name="email"
          required
          type="email"
          placeholder="your@email.com"
        />
      </div>

      <div>
        <label class="mb-2 block text-sm font-medium text-text-1" for="message"> Message </label>
        <textarea
          id="message"
          :class="inputClasses"
          name="message"
          required
          rows="4"
          placeholder="How can we help you?"
        ></textarea>
      </div>

      <div class="pt-4">
        <Button tone="primary" variant="surface" size="md" radius="xl" :block="true" type="submit">
          Submit
        </Button>
      </div>
    </form>
  </ModalTrigger>
</template>

<script lang="ts" setup>
import { computed } from 'vue';
import Button from '../core/basic/Button.vue';
import ModalTrigger from '../core/basic/ModalTrigger.vue';
import { input } from '../core/design-system/recipes';

interface Props {
  formTitle: string;
  successActionUrl?: string;
}

withDefaults(defineProps<Props>(), {
  successActionUrl: '/success/contact-sales',
});

const inputClasses = computed(() => {
  return input({
    tone: 'neutral',
    size: 'md',
    radius: 'lg',
  });
});
</script>
