<template>
  <TransitionRoot :show="isVisible" as="template">
    <div
      class="pointer-events-none fixed inset-x-0 bottom-0 z-50 px-4 pb-4 sm:px-6 sm:pb-6 md:px-8 md:pb-8"
    >
      <UiTransitionSlide direction="up">
        <div
          class="pointer-events-auto mx-auto max-w-4xl rounded-xl border border-neutral-200 bg-white p-6 shadow-lg sm:p-8 dark:border-neutral-700 dark:bg-neutral-900"
        >
          <div class="flex flex-col gap-6 sm:flex-row sm:items-start sm:gap-8">
            <div class="flex-1 space-y-3">
              <h3 class="text-lg font-semibold text-neutral-900 dark:text-neutral-50">
                {{ title }}
              </h3>
              <p class="text-sm text-neutral-600 dark:text-neutral-400">
                {{ description }}
                <a
                  :href="privacyPolicyUrl"
                  class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium underline"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {{ privacyPolicyText }}
                </a>
              </p>
            </div>
            <div class="flex flex-col gap-3 sm:flex-shrink-0 sm:flex-row">
              <Button variant="outline" tone="neutral" size="md" @click="handleDecline">
                {{ declineText }}
              </Button>
              <Button variant="solid" tone="primary" size="md" @click="handleAccept">
                {{ acceptText }}
              </Button>
            </div>
          </div>
        </div>
      </UiTransitionSlide>
    </div>
  </TransitionRoot>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { TransitionRoot } from '@headlessui/vue';
import Button from './Button.vue';
import UiTransitionSlide from '../transitions/UiTransitionSlide.vue';

interface Props {
  title: string;
  description: string;
  acceptText: string;
  declineText: string;
  privacyPolicyText: string;
  privacyPolicyUrl: string;
  storageKey?: string;
}

const props = withDefaults(defineProps<Props>(), {
  storageKey: 'cookie-consent',
});

const emit = defineEmits<{
  accept: [];
  decline: [];
}>();

const isVisible = ref(false);

const CONSENT_ACCEPTED = 'accepted';
const CONSENT_DECLINED = 'declined';

const getConsent = (): string | null => {
  if (typeof window === 'undefined') return null;
  try {
    return localStorage.getItem(props.storageKey);
  } catch {
    return null;
  }
};

const setConsent = (value: string): void => {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(props.storageKey, value);
    window.dispatchEvent(
      new CustomEvent('cookie-consent-changed', {
        detail: { consent: value },
      })
    );
  } catch (error) {
    console.error('Failed to save cookie consent:', error);
  }
};

const handleAccept = () => {
  setConsent(CONSENT_ACCEPTED);
  isVisible.value = false;
  emit('accept');
};

const handleDecline = () => {
  setConsent(CONSENT_DECLINED);
  isVisible.value = false;
  emit('decline');
};

onMounted(() => {
  const consent = getConsent();
  if (!consent) {
    setTimeout(() => {
      isVisible.value = true;
    }, 1000);
  }
});

defineExpose({
  getConsent,
  CONSENT_ACCEPTED,
  CONSENT_DECLINED,
});
</script>
