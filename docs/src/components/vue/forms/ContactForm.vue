<!-- components/ContactForm.vue -->
<template>
  <div class="w-100 pt-1 pb-5 lg:pb-10 px-5 lg:px-14 bg-gray-900 rounded-lg">
    <h2 class="!mt-1 !mb-6 w-full text-center text-vp-text border-0 !border-t-0">
      {{
        $t('otai_contact_form.title')
      }}
    </h2>


    <form
      action="https://formspree.io/f/movwyjqz"
      class="space-y-4"
      method="POST"
    >
      <!-- actual form fields (hidden) -->
      <input
        :value="email"
        name="email"
        type="hidden"
      >
      <input
        :value="message"
        name="message"
        type="hidden"
      >

      <div>
        <label
          class="block text-sm font-medium text-gray-200 mb-1"
          for="email"
        >
          {{ $t('otai_contact_form.email_label') }}
        </label>
        <div class="relative w-full">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <EnvelopeIcon class="w-5 h-5 text-text-dim" />
          </div>
          <input
            id="email"
            v-model="email"
            class="w-full h-12 px-4 pl-10 text-base rounded-xl bg-surface-dark border border-primary/40 text-white placeholder:text-text-dim hover:border-primary/60 hover:shadow-[0_0_15px_rgba(166,13,242,0.2)] focus:ring-2 focus:ring-primary/50 focus:border-primary focus:outline-none active:border-primary active:ring-primary/60 shadow-sm transition-colors duration-200"
            placeholder="you@domain.com"
            type="email"
          >
        </div>
      </div>

      <div>
        <label
          class="block text-sm font-medium text-gray-200 mb-1"
          for="message"
        >
          {{ $t('otai_contact_form.message_label') }}
        </label>
        <div class="relative w-full">
          <div class="absolute top-3 left-4 pointer-events-none z-10">
            <ChatBubbleLeftRightIcon class="w-5 h-5 text-text-dim" />
          </div>
          <textarea
            id="message"
            v-model="message"
            class="w-full py-3 px-4 pl-11 pr-4 text-base rounded-xl min-h-[100px] border bg-surface-dark text-white placeholder-text-dim transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary/50 focus:shadow-[0_0_20px_rgba(166,13,242,0.2)] disabled:opacity-50 disabled:cursor-not-allowed border-border-dark hover:border-primary/30 resize-y"
            placeholder="How can we help you?"
            rows="5"
          />
        </div>
      </div>

      <Button
        class="px-8 text-xl"
        type="submit"
        variant="primary"
      >
        <PaperAirplaneIcon class="w-5 h-5 mr-2 -ml-1" />
        {{ $t('otai_contact_form.submit_text') }}
      </Button>
    </form>
    <p class="text-sm text-gray-400">
      {{ $t('otai_contact_form.email_us_text') }}
      <a
        class="text-blue-400 hover:underline"
        href="mailto:sales@softoft.de"
      >
        sales@softoft.de
      </a>
    </p>
  </div>
</template>

<script lang="ts" setup>
import {ref} from 'vue'
import Button from '../core/basic/Button.vue'
import { EnvelopeIcon, ChatBubbleLeftRightIcon, PaperAirplaneIcon } from '@heroicons/vue/24/outline'

const email = ref('')
const message = ref('')

</script>
