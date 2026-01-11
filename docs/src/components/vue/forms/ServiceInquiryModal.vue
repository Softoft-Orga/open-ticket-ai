<template>
  <TransitionRoot
    :show="modalOpen"
    as="template"
  >
    <Dialog
      as="div"
      class="relative z-50"
      @close="closeModal"
    >
      <TransitionChild
        as="template"
        enter="ease-out duration-300"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="ease-in duration-200"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black/80 backdrop-blur-sm" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
          <TransitionChild
            as="template"
            enter="ease-out duration-300"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel class="w-full max-w-2xl transform overflow-hidden rounded-3xl bg-[#1a101f] border border-primary/20 p-8 text-left align-middle shadow-xl transition-all">
              <div class="flex items-start justify-between mb-6">
                <DialogTitle
                  as="h3"
                  class="text-2xl font-bold text-white"
                >
                  Service Inquiry
                </DialogTitle>
                <button
                  type="button"
                  class="rounded-lg p-1 text-slate-400 hover:text-white hover:bg-white/10 transition-colors"
                  @click="closeModal"
                >
                  <XMarkIcon
                    class="w-6 h-6"
                    aria-hidden="true"
                  />
                </button>
              </div>

              <p class="text-slate-400 text-sm mb-8">
                Tell us about your helpdesk needs and we'll prepare a custom rollout plan.
              </p>

              <form
                v-if="!submitted"
                name="service-inquiry"
                method="POST"
                data-netlify="true"
                netlify-honeypot="bot-field"
                class="space-y-6"
                @submit.prevent="handleSubmit"
              >
                <input
                  type="hidden"
                  name="form-name"
                  value="service-inquiry"
                >
                <input
                  type="hidden"
                  name="bot-field"
                >

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label
                      for="fullName"
                      class="block text-xs font-bold text-slate-300 uppercase tracking-widest mb-2"
                    >
                      Full Name*
                    </label>
                    <input
                      id="fullName"
                      v-model="formData.fullName"
                      type="text"
                      name="fullName"
                      required
                      placeholder="Jane Doe"
                      class="w-full px-4 py-2.5 rounded-lg bg-black/40 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-primary/50 focus:ring-2 focus:ring-primary/20 transition-colors"
                    >
                  </div>

                  <div>
                    <label
                      for="email"
                      class="block text-xs font-bold text-slate-300 uppercase tracking-widest mb-2"
                    >
                      Email*
                    </label>
                    <input
                      id="email"
                      v-model="formData.email"
                      type="email"
                      name="email"
                      required
                      placeholder="jane@company.com"
                      class="w-full px-4 py-2.5 rounded-lg bg-black/40 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-primary/50 focus:ring-2 focus:ring-primary/20 transition-colors"
                    >
                  </div>
                </div>

                <div>
                  <label
                    for="company"
                    class="block text-xs font-bold text-slate-300 uppercase tracking-widest mb-2"
                  >
                    Company
                  </label>
                  <input
                    id="company"
                    v-model="formData.company"
                    type="text"
                    name="company"
                    placeholder="Enter company name"
                    class="w-full px-4 py-2.5 rounded-lg bg-black/40 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-primary/50 focus:ring-2 focus:ring-primary/20 transition-colors"
                  >
                </div>

                <div>
                  <label
                    for="service"
                    class="block text-xs font-bold text-slate-300 uppercase tracking-widest mb-2"
                  >
                    Service*
                  </label>
                  <div class="relative">
                    <select
                      id="service"
                      v-model="formData.service"
                      name="service"
                      required
                      class="w-full px-4 py-2.5 rounded-lg bg-black/40 border border-white/10 text-white appearance-none focus:outline-none focus:border-primary/50 focus:ring-2 focus:ring-primary/20 transition-colors cursor-pointer"
                    >
                      <option
                        value=""
                        disabled
                      >
                        Select a service
                      </option>
                      <option value="Evaluation Dataset Generation">
                        Evaluation Dataset Generation
                      </option>
                      <option value="Training Dataset Generation">
                        Training Dataset Generation
                      </option>
                      <option value="Enterprise Dataset Generation">
                        Enterprise Dataset Generation
                      </option>
                      <option value="Integration Package - Standard Stack">
                        Integration Package - Standard Stack
                      </option>
                      <option value="Integration Package - Enterprise/Custom">
                        Integration Package - Enterprise/Custom
                      </option>
                      <option value="OTA Automation Pack">
                        OTA Automation Pack
                      </option>
                      <option value="Custom Tags Model - Synthetic">
                        Custom Tags Model - Synthetic
                      </option>
                      <option value="Custom Tag Model - Real Data">
                        Custom Tag Model - Real Data
                      </option>
                      <option value="Custom Development">
                        Custom Development
                      </option>
                      <option value="Hourly Engineering">
                        Hourly Engineering
                      </option>
                      <option value="Ongoing Support Subscription">
                        Ongoing Support Subscription
                      </option>
                      <option value="Other">
                        Other
                      </option>
                    </select>
                    <ChevronDownIcon
                      class="w-5 h-5 text-slate-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none"
                      aria-hidden="true"
                    />
                  </div>
                </div>

                <div>
                  <label
                    for="ticketSystem"
                    class="block text-xs font-bold text-slate-300 uppercase tracking-widest mb-2"
                  >
                    Ticket System
                  </label>
                  <input
                    id="ticketSystem"
                    v-model="formData.ticketSystem"
                    type="text"
                    name="ticketSystem"
                    placeholder="e.g. OTOBO, Zammad, Zendesk..."
                    class="w-full px-4 py-2.5 rounded-lg bg-black/40 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-primary/50 focus:ring-2 focus:ring-primary/20 transition-colors"
                  >
                </div>

                <div>
                  <label
                    for="message"
                    class="block text-xs font-bold text-slate-300 uppercase tracking-widest mb-2"
                  >
                    Message*
                  </label>
                  <textarea
                    id="message"
                    v-model="formData.message"
                    name="message"
                    required
                    rows="4"
                    placeholder="How can we help?"
                    class="w-full px-4 py-2.5 rounded-lg bg-black/40 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-primary/50 focus:ring-2 focus:ring-primary/20 transition-colors resize-none"
                  />
                </div>

                <Button
                  type="submit"
                  variant="primary"
                  size="md"
                  class="w-full uppercase tracking-widest"
                >
                  Submit Inquiry
                </Button>
              </form>

              <div
                v-else
                class="text-center py-12"
              >
                <div class="mx-auto w-16 h-16 rounded-full bg-green-500/10 flex items-center justify-center mb-6">
                  <CheckCircleIcon
                    class="w-10 h-10 text-green-400"
                    aria-hidden="true"
                  />
                </div>
                <h3 class="text-2xl font-bold text-white mb-3">
                  Thank you!
                </h3>
                <p class="text-slate-400 mb-8">
                  We've received your inquiry and will get back to you within 1 business day.
                </p>
                <Button
                  type="button"
                  variant="outline"
                  size="md"
                  @click="closeModal"
                >
                  Close
                </Button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script lang="ts" setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { Dialog, DialogPanel, DialogTitle, TransitionRoot, TransitionChild } from '@headlessui/vue'
import { XMarkIcon, ChevronDownIcon, CheckCircleIcon } from '@heroicons/vue/24/outline'
import Button from '../core/basic/Button.vue'

const props = defineProps<{
  isOpen: boolean
  selectedService?: string
}>()

/* eslint-disable no-unused-vars */
const emit = defineEmits<{
  (e: 'close'): void
/* eslint-enable no-unused-vars */
}>()

const formData = ref({
  fullName: '',
  email: '',
  company: '',
  service: '',
  ticketSystem: '',
  message: ''
})

const submitted = ref(false)
const modalOpen = ref(false)

watch(() => props.selectedService, (newService) => {
  if (newService) {
    formData.value.service = newService
  }
}, { immediate: true })

watch(() => props.isOpen, (newValue) => {
  modalOpen.value = newValue
  if (!newValue) {
    setTimeout(() => {
      submitted.value = false
    }, 300)
  }
})

watch(modalOpen, (newValue) => {
  if (!newValue) {
    emit('close')
  }
})

function handleOpenModal(event: CustomEvent) {
  const service = event.detail?.service || ''
  if (service) {
    formData.value.service = service
  }
  modalOpen.value = true
}

function closeModal() {
  modalOpen.value = false
}

async function handleSubmit() {
  const form = new FormData()
  form.append('form-name', 'service-inquiry')
  form.append('fullName', formData.value.fullName)
  form.append('email', formData.value.email)
  form.append('company', formData.value.company)
  form.append('service', formData.value.service)
  form.append('ticketSystem', formData.value.ticketSystem)
  form.append('message', formData.value.message)

  try {
    await fetch('/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams(form as any).toString()
    })
    submitted.value = true
    formData.value = {
      fullName: '',
      email: '',
      company: '',
      service: '',
      ticketSystem: '',
      message: ''
    }
  } catch (error) {
    console.error('Form submission error:', error)
    alert('There was an error submitting the form. Please try again.')
  }
}

onMounted(() => {
  window.addEventListener('open-service-modal', handleOpenModal as EventListener)
})

onUnmounted(() => {
  window.removeEventListener('open-service-modal', handleOpenModal as EventListener)
})
</script>
