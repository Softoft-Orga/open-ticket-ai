<template>
  <div class="w-100 pt-3 bg-gray-900 rounded-lg">
    <div class="mx-auto max-w-screen-lg pb-5">
      <h2 class="!mt-1 !mb-6 w-full text-center text-vp-text border-0 !border-t-0">
        {{ $t('sdg_waitlist.title') }}
      </h2>

      <form
          class="space-y-5 max-w-64 mx-auto"
          name="synthetic-ticket-generator-waitlist"
          netlify
      >
        <div>
          <label class="block text-sm font-medium text-gray-200 mb-1" for="email">
            {{ $t('sdg_waitlist.email_label') }}
          </label>
          <TextField
              id="email"
              v-model="email"
              name="email"
              placeholder="you@domain.com"
              required
              type="email"
          />
        </div>

        <Button class="w-full justify-center">
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
import TextField from '../core/forms/TextField.vue'
import Button from '../core/basic/Button.vue'

const email = ref('')
</script>
