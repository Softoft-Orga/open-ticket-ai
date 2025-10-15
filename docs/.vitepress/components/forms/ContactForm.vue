<!-- components/ContactForm.vue -->
<template>
  <div class="w-100 pt-1 pb-5 lg:pb-10 px-5 lg:px-14 bg-gray-900 rounded-lg">
    <h2 class="!mt-1 !mb-6 w-full text-center text-vp-text border-0 !border-t-0">{{
        $t('otai_contact_form.title')
      }}</h2>


    <form
        action="https://formspree.io/f/movwyjqz"
        class="space-y-4"
        method="POST"
    >
      <!-- actual form fields (hidden) -->
      <input :value="email" name="email" type="hidden"/>
      <input :value="message" name="message" type="hidden"/>

      <div>
        <label class="block text-sm font-medium text-gray-200 mb-1" for="email">
          {{ $t('otai_contact_form.email_label') }}
        </label>
        <TextField
            id="email"
            v-model="email"
            placeholder="you@domain.com"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-200 mb-1" for="message">
          {{ $t('otai_contact_form.message_label') }}
        </label>
        <TextArea
            id="message"
            v-model="message"
            placeholder="How can we help you?"
            rows="5"
        />
      </div>

      <Button
          class="px-8 text-xl"
          type="submit"
          variant="primary"
      >
        {{ $t('otai_contact_form.submit_text') }}
      </Button>
    </form>
    <p class="text-sm text-gray-400">
      {{ $t('otai_contact_form.email_us_text') }}
      <a class="text-blue-400 hover:underline" href="mailto:sales@softoft.de">
        sales@softoft.de
      </a>
    </p>
  </div>
</template>

<script lang="ts" setup>
import {ref} from 'vue'
import TextField from '../core/forms/TextField.vue'
import TextArea from '../core/forms/TextArea.vue'
import Button from '../core/basic/Button.vue'

const email = ref('')
const message = ref('')

</script>
