<template>
  <div class="w-100 pt-3 bg-gray-900 rounded-lg">
    <div class="mx-auto max-w-screen-lg pb-5">
      <h2 class="!mt-1 !mb-6 w-full text-center text-vp-text border-0 !border-t-0">
        {{ $t('sdg_waitlist.title') }}
      </h2>

      <form
        class="space-y-5 max-w-64 mx-auto"
        name="synthetic-ticket-generator-waitlist"
        action="https://formspree.io/f/xjkjkzdo"
        method="POST"
      >
        <div>
          <label
            class="block text-sm font-medium text-gray-200 mb-1"
            for="email"
          >
            {{ $t('sdg_waitlist.email_label') }}
          </label>
          <div class="relative w-full">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <EnvelopeIcon class="w-5 h-5 text-text-dim" />
            </div>
            <input
              id="email"
              v-model="email"
              name="email"
              type="email"
              placeholder="you@domain.com"
              required
              class="w-full h-12 px-4 pl-10 text-base rounded-xl bg-surface-dark border border-primary/40 text-white placeholder:text-text-dim hover:border-primary/60 hover:shadow-[0_0_15px_rgba(166,13,242,0.2)] focus:ring-2 focus:ring-primary/50 focus:border-primary focus:outline-none active:border-primary active:ring-primary/60 shadow-sm transition-colors duration-200"
            >
          </div>
        </div>

        <Button class="w-full justify-center">
          <UserPlusIcon class="w-5 h-5 mr-2 -ml-1" />
          {{ $t('sdg_waitlist.submit_text') }}
        </Button>
      </form>
    </div>
    <p class="w-full text-xs text-center leading-3 text-gray-400">
      {{
        $t('sdg_waitlist.privacy_note')
      }}
    </p>
  </div>
</template>

<script lang="ts" setup>
import {ref} from 'vue'
import Button from '../core/basic/Button.vue'
import { EnvelopeIcon, UserPlusIcon } from '@heroicons/vue/24/outline'

const email = ref('')
</script>
