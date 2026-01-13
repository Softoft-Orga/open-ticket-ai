<template>
  <div class="bg-gradient-to-br from-primary/10 to-cyan-glow/5 border border-primary/20 rounded-3xl p-12 text-center">
    <h2 class="text-3xl font-bold text-text-1 mb-6">
      Beyond Cost Savings
    </h2>
    <div class="grid md:grid-cols-3 gap-8 mb-8">
      <div>
        <div class="text-4xl mb-3">
          ⚡
        </div>
        <h3 class="text-lg font-bold text-text-1 mb-2">
          Faster Response Times
        </h3>
        <p class="text-sm text-text-2">
          Automated tagging enables instant routing and prioritization
        </p>
      </div>
      <div>
        <div class="text-4xl mb-3">
          📊
        </div>
        <h3 class="text-lg font-bold text-text-1 mb-2">
          Better Insights
        </h3>
        <p class="text-sm text-text-2">
          Consistent tagging improves analytics and reporting accuracy
        </p>
      </div>
      <div>
        <div class="text-4xl mb-3">
          😊
        </div>
        <h3 class="text-lg font-bold text-text-1 mb-2">
          Improved Satisfaction
        </h3>
        <p class="text-sm text-text-2">
          Faster resolution times lead to happier customers and agents
        </p>
      </div>
    </div>
    <Button
      tone="primary"
      size="lg"
      @click="openModal"
    >
      Contact Sales for Custom Analysis
    </Button>

    <!-- Modal with Netlify Form -->
    <Modal
      :open="isModalOpen"
      title="Request Custom ROI Analysis"
      size="md"
      @close="closeModal"
    >
      <form
        name="custom-roi-analysis"
        method="POST"
        data-netlify="true"
        netlify-honeypot="bot-field"
        action="/success/custom-roi-analysis"
        @submit="handleSubmit"
      >
        <input
          type="hidden"
          name="form-name"
          value="custom-roi-analysis"
        >
        <p class="hidden">
          <label>
            Don't fill this out if you're human: <input name="bot-field">
          </label>
        </p>

        <div class="space-y-4">
          <div>
            <label
              for="name"
              class="block text-sm font-medium text-text-1 mb-2"
            >
              Name *
            </label>
            <input
              id="name"
              type="text"
              name="name"
              required
              class="w-full px-4 py-2 bg-bg-2 border border-border-1 rounded-lg text-text-1 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            >
          </div>

          <div>
            <label
              for="email"
              class="block text-sm font-medium text-text-1 mb-2"
            >
              Email *
            </label>
            <input
              id="email"
              type="email"
              name="email"
              required
              class="w-full px-4 py-2 bg-bg-2 border border-border-1 rounded-lg text-text-1 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            >
          </div>

          <div>
            <label
              for="company"
              class="block text-sm font-medium text-text-1 mb-2"
            >
              Company *
            </label>
            <input
              id="company"
              type="text"
              name="company"
              required
              class="w-full px-4 py-2 bg-bg-2 border border-border-1 rounded-lg text-text-1 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            >
          </div>

          <div>
            <label
              for="tickets-per-day"
              class="block text-sm font-medium text-text-1 mb-2"
            >
              Approximate Daily Tickets *
            </label>
            <input
              id="tickets-per-day"
              type="number"
              name="tickets-per-day"
              required
              min="1"
              class="w-full px-4 py-2 bg-bg-2 border border-border-1 rounded-lg text-text-1 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            >
          </div>

          <div>
            <label
              for="message"
              class="block text-sm font-medium text-text-1 mb-2"
            >
              Additional Information
            </label>
            <textarea
              id="message"
              name="message"
              rows="4"
              class="w-full px-4 py-2 bg-bg-2 border border-border-1 rounded-lg text-text-1 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>
        </div>

        <div class="mt-6 flex gap-3 justify-end">
          <Button
            type="button"
            variant="subtle"
            tone="neutral"
            @click="closeModal"
          >
            Cancel
          </Button>
          <Button
            type="submit"
            tone="primary"
          >
            Submit Request
          </Button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import Button from '../core/basic/Button.vue'
import Modal from '../core/basic/Modal.vue'

const isModalOpen = ref(false)

const openModal = () => {
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
}

const handleSubmit = () => {
  // Let Netlify handle the form submission and redirect
  // The action attribute will handle the redirect to /success/custom-roi-analysis
}
</script>
