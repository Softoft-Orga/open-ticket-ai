<template>
  <div>
    <Button tone="primary" variant="surface" @click="isOpen = true">
      <slot />
    </Button>

    <Modal :open="isOpen" :title="formTitle" @close="isOpen = false">
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
            v-model="formData.subject"
            :class="inputClasses"
            name="subject"
            required
            type="text"
          />
        </div>

        <div>
          <label class="mb-2 block text-sm font-medium text-text-1" for="email"> Email </label>
          <input
            id="email"
            v-model="formData.email"
            :class="inputClasses"
            name="email"
            required
            type="email"
          />
        </div>

        <div>
          <label class="mb-2 block text-sm font-medium text-text-1" for="message"> Message </label>
          <textarea
            id="message"
            v-model="formData.message"
            :class="inputClasses"
            name="message"
            required
            rows="4"
          />
        </div>

        <div class="flex gap-3 pt-4">
          <Button class="flex-1" tone="primary" type="submit" variant="surface"> Submit </Button>
          <Button
            class="flex-1"
            tone="neutral"
            type="button"
            variant="outline"
            @click="handleCancel"
          >
            Cancel
          </Button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue';
import Button from '../core/basic/Button.vue';
import Modal from '../core/basic/Modal.vue';
import { input } from '../core/design-system/recipes';

interface Props {
  formTitle: string;
  successActionUrl?: string;
}

const props = withDefaults(defineProps<Props>(), {
  successActionUrl: '/success/contact-sales',
});

const isOpen = ref(false);
const formData = ref({
  subject: props.formTitle,
  email: '',
  message: '',
});

const handleCancel = () => {
  isOpen.value = false;
  formData.value = {
    subject: props.formTitle,
    email: '',
    message: '',
  };
};

const inputClasses = computed(() => {
  return input({
    tone: 'neutral',
    size: 'md',
    radius: 'lg',
  });
});
</script>
