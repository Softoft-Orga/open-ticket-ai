<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-white mb-4">
        Pricing Simulator.
      </h1>
      <p class="text-gray-400 text-lg">
        Select a predefined scenario or customize values to see how automated
        tagging scales for your specific helpdesk environment.
      </p>
    </div>

    <!-- Scenario Selection -->
    <div class="mb-8">
      <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">
        Choose a Preset Scenario
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card
          v-for="scenario in scenarios"
          :key="scenario.id"
          :class="[
            'relative cursor-pointer transition-all duration-300 text-left',
            activeScenario === scenario.id
              ? 'border-primary border-2 !bg-gradient-to-br from-primary/30 via-primary/15 to-surface-dark shadow-[0_0_40px_rgba(166,13,242,0.5)] ring-2 ring-primary/40 scale-[1.02]'
              : 'border-border-dark hover:border-primary/60 hover:shadow-[0_0_20px_rgba(166,13,242,0.25)] hover:scale-[1.01] hover:bg-surface-lighter'
          ]"
          background="surface-dark"
          @click="applyScenario(scenario.id)"
        >
          <!-- Check icon for selected scenario -->
          <div
            v-if="activeScenario === scenario.id"
            class="absolute top-3 right-3"
          >
            <div class="w-6 h-6 bg-primary rounded-full flex items-center justify-center">
              <component
                :is="CheckIcon"
                class="w-4 h-4 text-white"
              />
            </div>
          </div>
          
          <div class="flex items-start mb-3">
            <component
              :is="scenario.icon"
              class="w-6 h-6 mr-3 flex-shrink-0"
              :class="scenario.iconColor"
            />
            <h3 class="text-lg font-bold text-white">
              {{ scenario.name }}
            </h3>
          </div>
          <p class="text-sm text-gray-400">
            {{ scenario.description }}
          </p>
        </Card>
      </div>
    </div>

    <!-- Main Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
      <!-- Left Column: Customer Context -->
      <Card background="surface-dark">
        <div class="flex items-center mb-4">
          <component
            :is="ChartBarIcon"
            class="w-5 h-5 mr-2 text-primary"
          />
          <h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wider">
            Customer Context
          </h3>
        </div>

        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">
              Daily Tickets
            </label>
            <input
              v-model="ticketsStr"
              type="number"
              class="w-full h-12 px-4 text-base rounded-xl bg-surface-dark border border-primary/40 text-white placeholder:text-text-dim hover:border-primary/60 hover:shadow-[0_0_15px_rgba(166,13,242,0.2)] focus:ring-2 focus:ring-primary/50 focus:border-primary focus:outline-none active:border-primary active:ring-primary/60 shadow-sm transition-colors duration-200"
            >
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">
                Manual Cost/Ticket (€)
              </label>
              <input
                v-model="manualCostStr"
                type="number"
                class="w-full h-12 px-4 text-base rounded-xl bg-surface-dark border border-primary/40 text-white placeholder:text-text-dim hover:border-primary/60 hover:shadow-[0_0_15px_rgba(166,13,242,0.2)] focus:ring-2 focus:ring-primary/50 focus:border-primary focus:outline-none active:border-primary active:ring-primary/60 shadow-sm transition-colors duration-200"
              >
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">
                Cost Per Error (€)
              </label>
              <input
                v-model="errorCostStr"
                type="number"
                class="w-full h-12 px-4 text-base rounded-xl bg-surface-dark border border-primary/40 text-white placeholder:text-text-dim hover:border-primary/60 hover:shadow-[0_0_15px_rgba(166,13,242,0.2)] focus:ring-2 focus:ring-primary/50 focus:border-primary focus:outline-none active:border-primary active:ring-primary/60 shadow-sm transition-colors duration-200"
              >
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">
                Human Acc (%)
              </label>
              <input
                v-model="humanAccStr"
                type="number"
                class="w-full h-12 px-4 text-base rounded-xl bg-surface-dark border border-primary/40 text-white placeholder:text-text-dim hover:border-primary/60 hover:shadow-[0_0_15px_rgba(166,13,242,0.2)] focus:ring-2 focus:ring-primary/50 focus:border-primary focus:outline-none active:border-primary active:ring-primary/60 shadow-sm transition-colors duration-200"
              >
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">
                Amortization (Mo)
              </label>
              <input
                v-model="monthsStr"
                type="number"
                class="w-full h-12 px-4 text-base rounded-xl bg-surface-dark border border-primary/40 text-white placeholder:text-text-dim hover:border-primary/60 hover:shadow-[0_0_15px_rgba(166,13,242,0.2)] focus:ring-2 focus:ring-primary/50 focus:border-primary focus:outline-none active:border-primary active:ring-primary/60 shadow-sm transition-colors duration-200"
              >
            </div>
          </div>
        </div>
      </Card>

      <!-- Middle Column: Stats Cards -->
      <div class="space-y-4">
        <Transition
          enter-active-class="transition-all duration-150 ease-out"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="transition-all duration-100 ease-in"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
          appear
        >
          <Card 
            key="stat1" 
            background="surface-dark"
            class="transition-all duration-300 hover:shadow-[0_0_25px_rgba(166,13,242,0.2)] hover:scale-[1.02]"
          >
            <div class="text-sm text-gray-400 uppercase tracking-wider mb-1">
              Manual Base (Inc. Errors)
            </div>
            <div class="text-3xl font-bold text-white">
              {{ formatCurrency(stats.manualTotal) }}
            </div>
            <div class="text-xs text-gray-500 mt-1">
              Monthly Baseline
            </div>
          </Card>
        </Transition>

        <Transition
          enter-active-class="transition-all duration-150 ease-out"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="transition-all duration-100 ease-in"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
          appear
        >
          <Card 
            key="stat2" 
            background="surface-dark"
            class="transition-all duration-300 hover:shadow-[0_0_30px_rgba(166,13,242,0.4)] hover:scale-[1.02]"
          >
            <div class="text-sm text-gray-400 uppercase tracking-wider mb-1">
              Lite Pro TCO
            </div>
            <div class="text-3xl font-bold text-primary">
              {{ formatCurrency(stats.proTotal) }}
            </div>
            <div class="text-xs text-gray-500 mt-1">
              Inc. Fixed HW
            </div>
          </Card>
        </Transition>

        <Transition
          enter-active-class="transition-all duration-150 ease-out"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="transition-all duration-100 ease-in"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
          appear
        >
          <Card 
            key="stat3" 
            background="surface-dark"
            class="transition-all duration-300 hover:shadow-[0_0_25px_rgba(34,211,238,0.3)] hover:scale-[1.02]"
          >
            <div class="text-sm text-gray-400 uppercase tracking-wider mb-1">
              Break-Even
            </div>
            <div class="text-3xl font-bold text-cyan-glow">
              {{ stats.beProFree }}
            </div>
            <div class="text-xs text-gray-500 mt-1">
              Pro vs Free (TIX/Day)
            </div>
          </Card>
        </Transition>
      </div>

      <!-- Right Column: Lite Pro Config -->
      <Card background="surface-dark">
        <div class="mb-4">
          <Badge type="primary">
            <component
              :is="SparklesIcon"
              class="w-4 h-4"
            />
            Lite Pro (4B)
          </Badge>
          <div class="mt-2 text-sm text-primary font-medium">
            RECOMMENDED
          </div>
        </div>

        <div class="space-y-4">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">
                License (€)
              </label>
              <input
                v-model="proLicenseStr"
                type="number"
                class="w-full h-12 px-4 text-base rounded-xl bg-surface-dark border border-primary/40 text-white placeholder:text-text-dim hover:border-primary/60 hover:shadow-[0_0_15px_rgba(166,13,242,0.2)] focus:ring-2 focus:ring-primary/50 focus:border-primary focus:outline-none active:border-primary active:ring-primary/60 shadow-sm transition-colors duration-200"
              >
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">
                AI Accuracy (%)
              </label>
              <input
                v-model="proAccStr"
                type="number"
                class="w-full h-12 px-4 text-base rounded-xl bg-surface-dark border border-primary/40 text-white placeholder:text-text-dim hover:border-primary/60 hover:shadow-[0_0_15px_rgba(166,13,242,0.2)] focus:ring-2 focus:ring-primary/50 focus:border-primary focus:outline-none active:border-primary active:ring-primary/60 shadow-sm transition-colors duration-200"
              >
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">
                Maint/Mo (€)
              </label>
              <input
                v-model="proMaintStr"
                type="number"
                class="w-full h-12 px-4 text-base rounded-xl bg-surface-dark border border-primary/40 text-white placeholder:text-text-dim hover:border-primary/60 hover:shadow-[0_0_15px_rgba(166,13,242,0.2)] focus:ring-2 focus:ring-primary/50 focus:border-primary focus:outline-none active:border-primary active:ring-primary/60 shadow-sm transition-colors duration-200"
              >
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">
                Hardware/Mo (€)
              </label>
              <input
                :value="String(proHw)"
                type="number"
                disabled
                class="w-full h-12 px-4 text-base rounded-xl bg-surface-dark border border-primary/40 text-white placeholder:text-text-dim hover:border-primary/60 hover:shadow-[0_0_15px_rgba(166,13,242,0.2)] focus:ring-2 focus:ring-primary/50 focus:border-primary focus:outline-none active:border-primary active:ring-primary/60 shadow-sm transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
              <span class="text-xs text-gray-500">(Auto)</span>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">
              Inherent Setup Estimate (€)
            </label>
            <input
              v-model="proSetupStr"
              type="number"
              class="w-full h-12 px-4 text-base rounded-xl bg-surface-dark border border-primary/40 text-white placeholder:text-text-dim hover:border-primary/60 hover:shadow-[0_0_15px_rgba(166,13,242,0.2)] focus:ring-2 focus:ring-primary/50 focus:border-primary focus:outline-none active:border-primary active:ring-primary/60 shadow-sm transition-colors duration-200"
            >
          </div>
        </div>
      </Card>
    </div>

    <!-- Lite Free Config -->
    <Card
      background="surface-dark"
      class="mb-8"
    >
      <div class="mb-4">
        <Badge type="secondary">
          <component
            :is="BeakerIcon"
            class="w-4 h-4"
          />
          Lite Free (0.6B)
        </Badge>
      </div>

      <div class="grid grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">
            Inherent Setup (€)
          </label>
          <input
            v-model="freeSetupStr"
            type="number"
            class="w-full h-12 px-4 text-base rounded-xl bg-surface-dark border border-primary/40 text-white placeholder:text-text-dim hover:border-primary/60 hover:shadow-[0_0_15px_rgba(166,13,242,0.2)] focus:ring-2 focus:ring-primary/50 focus:border-primary focus:outline-none active:border-primary active:ring-primary/60 shadow-sm transition-colors duration-200"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">
            Accuracy (%)
          </label>
          <input
            v-model="freeAccStr"
            type="number"
            class="w-full h-12 px-4 text-base rounded-xl bg-surface-dark border border-primary/40 text-white placeholder:text-text-dim hover:border-primary/60 hover:shadow-[0_0_15px_rgba(166,13,242,0.2)] focus:ring-2 focus:ring-primary/50 focus:border-primary focus:outline-none active:border-primary active:ring-primary/60 shadow-sm transition-colors duration-200"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">
            Maint/Mo (€)
          </label>
          <input
            v-model="freeMaintStr"
            type="number"
            class="w-full h-12 px-4 text-base rounded-xl bg-surface-dark border border-primary/40 text-white placeholder:text-text-dim hover:border-primary/60 hover:shadow-[0_0_15px_rgba(166,13,242,0.2)] focus:ring-2 focus:ring-primary/50 focus:border-primary focus:outline-none active:border-primary active:ring-primary/60 shadow-sm transition-colors duration-200"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">
            Hardware/Mo (€)
          </label>
          <input
            :value="String(freeHw)"
            type="number"
            disabled
            class="w-full h-12 px-4 text-base rounded-xl bg-surface-dark border border-primary/40 text-white placeholder:text-text-dim hover:border-primary/60 hover:shadow-[0_0_15px_rgba(166,13,242,0.2)] focus:ring-2 focus:ring-primary/50 focus:border-primary focus:outline-none active:border-primary active:ring-primary/60 shadow-sm transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
          <span class="text-xs text-gray-500">(Auto)</span>
        </div>
      </div>
    </Card>

    <!-- Charts Row -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      <!-- TCO Projection Chart -->
      <Card background="surface-dark">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-white">
            TCO Projection (Monthly)
          </h3>
          <div class="flex items-center space-x-3 text-xs">
            <div class="flex items-center">
              <div class="w-3 h-0.5 bg-red-500 mr-2" />
              <span class="text-gray-400">Manual</span>
            </div>
            <div class="flex items-center">
              <div class="w-3 h-0.5 border-t-2 border-dashed border-gray-400 mr-2" />
              <span class="text-gray-400">Free</span>
            </div>
            <div class="flex items-center">
              <div class="w-3 h-0.5 bg-primary mr-2" />
              <span class="text-gray-400">Pro</span>
            </div>
          </div>
        </div>
        <div class="h-80">
          <canvas ref="tcoChartRef" />
        </div>
      </Card>

      <!-- Monthly Cost Breakdown Chart -->
      <Card background="surface-dark">
        <h3 class="text-lg font-semibold text-white mb-4">
          Monthly Cost Breakdown
        </h3>
        <div class="h-80">
          <canvas ref="roiChartRef" />
        </div>
      </Card>
    </div>

    <!-- Simulated Savings -->
    <Transition
      enter-active-class="transition-all duration-200 ease-out motion-reduce:transition-none motion-reduce:transform-none"
      enter-from-class="opacity-0 scale-90"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition-all duration-150 ease-in motion-reduce:transition-none motion-reduce:transform-none"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-90"
      appear
    >
      <Card 
        key="savings"
        background="custom"
        custom-bg="bg-gradient-to-br from-primary/10 to-surface-dark"
        class="border-primary/30 transition-all duration-500 hover:shadow-[0_0_40px_rgba(166,13,242,0.3)] hover:border-primary/50"
      >
        <h3 class="text-lg font-semibold text-white mb-2">
          Simulated Savings
        </h3>
        <div class="text-5xl font-bold text-primary mb-3">
          {{ formatCurrency(stats.savings) }}
        </div>
        <p class="text-gray-400">
          By switching from manual classification to Lite Pro, your organization could save approximately
          <span class="text-primary font-semibold">{{ formatCurrency(stats.savings) }}</span> every month.
        </p>
      </Card>
    </Transition>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { Chart, registerables } from 'chart.js'
import {
  ChartBarIcon,
  SparklesIcon,
  BeakerIcon,
  ServerIcon,
  ChartPieIcon,
  ExclamationTriangleIcon,
  CheckIcon
} from '@heroicons/vue/24/outline'
import Card from '../core/basic/Card.vue'
import Badge from '../core/basic/Badge.vue'

Chart.register(...registerables)

type Scenario = 'conservative' | 'realistic' | 'critical'

interface ScenarioConfig {
  id: Scenario
  name: string
  description: string
  icon: any
  iconColor: string
}

const scenarios: ScenarioConfig[] = [
  {
    id: 'conservative',
    name: 'Conservative',
    description: 'Low volume, high manual precision. Focus on small deployments with strict oversight.',
    icon: ServerIcon,
    iconColor: 'text-blue-400'
  },
  {
    id: 'realistic',
    name: 'Realistic',
    description: 'Medium volume with typical operational churn. Based on average enterprise rollout metrics.',
    icon: ChartPieIcon,
    iconColor: 'text-primary'
  },
  {
    id: 'critical',
    name: 'SLA / Critical',
    description: 'High volume, high cost of failure. Strict SLAs where every classification error is expensive.',
    icon: ExclamationTriangleIcon,
    iconColor: 'text-red-400'
  }
]

// Global Simulation Inputs
const tickets = ref(100)
const manualCost = ref(1.0)
const errorCost = ref(2.0)
const months = ref(24)
const humanAcc = ref(95)

// Lite Free (0.6B) Configuration
const freeSetup = ref(1500)
const freeAcc = ref(82)
const freeMaint = ref(50)
const freeHw = ref(20)

// Lite Pro (4B) Configuration
const proLicense = ref(2500)
const proSetup = ref(2000)
const proAcc = ref(90)
const proMaint = ref(50)
const proHw = ref(100)

const activeScenario = ref<Scenario>('realistic')

const tcoChartRef = ref<HTMLCanvasElement | null>(null)
const roiChartRef = ref<HTMLCanvasElement | null>(null)
let tcoInstance: Chart | null = null
let roiInstance: Chart | null = null

// Computed string properties for input v-model bindings
const ticketsStr = computed({
  get: () => String(tickets.value),
  set: (val) => { tickets.value = Number(val) || 0 }
})

const manualCostStr = computed({
  get: () => String(manualCost.value),
  set: (val) => { manualCost.value = Number(val) || 0 }
})

const errorCostStr = computed({
  get: () => String(errorCost.value),
  set: (val) => { errorCost.value = Number(val) || 0 }
})

const humanAccStr = computed({
  get: () => String(humanAcc.value),
  set: (val) => { humanAcc.value = Number(val) || 0 }
})

const monthsStr = computed({
  get: () => String(months.value),
  set: (val) => { months.value = Number(val) || 0 }
})

const freeSetupStr = computed({
  get: () => String(freeSetup.value),
  set: (val) => { freeSetup.value = Number(val) || 0 }
})

const freeAccStr = computed({
  get: () => String(freeAcc.value),
  set: (val) => { freeAcc.value = Number(val) || 0 }
})

const freeMaintStr = computed({
  get: () => String(freeMaint.value),
  set: (val) => { freeMaint.value = Number(val) || 0 }
})

const proLicenseStr = computed({
  get: () => String(proLicense.value),
  set: (val) => { proLicense.value = Number(val) || 0 }
})

const proSetupStr = computed({
  get: () => String(proSetup.value),
  set: (val) => { proSetup.value = Number(val) || 0 }
})

const proAccStr = computed({
  get: () => String(proAcc.value),
  set: (val) => { proAcc.value = Number(val) || 0 }
})

const proMaintStr = computed({
  get: () => String(proMaint.value),
  set: (val) => { proMaint.value = Number(val) || 0 }
})

const applyScenario = (scenario: Scenario) => {
  activeScenario.value = scenario
  switch (scenario) {
    case 'conservative':
      tickets.value = 50
      manualCost.value = 1.5
      errorCost.value = 5.0
      humanAcc.value = 98
      proAcc.value = 88
      freeAcc.value = 80
      break
    case 'realistic':
      tickets.value = 200
      manualCost.value = 1.0
      errorCost.value = 2.0
      humanAcc.value = 95
      proAcc.value = 90
      freeAcc.value = 82
      break
    case 'critical':
      tickets.value = 500
      manualCost.value = 0.8
      errorCost.value = 15.0
      humanAcc.value = 92
      proAcc.value = 94
      freeAcc.value = 85
      break
  }
}

// Calculations
const stats = computed(() => {
  const days = 22
  const manualWageTotal = tickets.value * days * manualCost.value
  const humanErrors = (1 - humanAcc.value / 100) * tickets.value * days
  const manualTotal = manualWageTotal + humanErrors * errorCost.value

  const freeFixed = freeSetup.value / months.value + freeHw.value + freeMaint.value
  const freeErrors = (1 - freeAcc.value / 100) * tickets.value * days
  const freeTotal = freeFixed + freeErrors * errorCost.value

  const proFixed = (proSetup.value + proLicense.value) / months.value + proHw.value + proMaint.value
  const proErrors = (1 - proAcc.value / 100) * tickets.value * days
  const proTotal = proFixed + proErrors * errorCost.value

  const fixedDiff = proFixed - freeFixed
  const accDiff = (proAcc.value - freeAcc.value) / 100
  let beProFree: string | number = 'Never'
  if (accDiff > 0) {
    beProFree = Math.round(fixedDiff / (days * errorCost.value * accDiff))
    if (beProFree < 0) beProFree = 0
  }

  return {
    manualTotal,
    freeTotal,
    proTotal,
    savings: manualTotal - proTotal,
    beProFree
  }
})

const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('de-DE', { maximumFractionDigits: 0 }).format(value) + ' €'
}

const updateCharts = () => {
  const steps = [10, 50, 100, 250, 500, 750, 1000]
  const days = 22

  if (tcoInstance) {
    tcoInstance.data.labels = steps
    tcoInstance.data.datasets[0].data = steps.map(
      (t) =>
        t * days * manualCost.value +
        (1 - humanAcc.value / 100) * t * days * errorCost.value
    )
    tcoInstance.data.datasets[1].data = steps.map((t) => {
      const fixed = freeSetup.value / months.value + freeHw.value + freeMaint.value
      const errs = (1 - freeAcc.value / 100) * t * days
      return fixed + errs * errorCost.value
    })
    tcoInstance.data.datasets[2].data = steps.map((t) => {
      const fixed =
        (proSetup.value + proLicense.value) / months.value + proHw.value + proMaint.value
      const errs = (1 - proAcc.value / 100) * t * days
      return fixed + errs * errorCost.value
    })
    tcoInstance.update()
  }

  if (roiInstance) {
    roiInstance.data.datasets[0].data = [
      stats.value.manualTotal,
      stats.value.freeTotal,
      stats.value.proTotal
    ]
    roiInstance.update()
  }
}

onMounted(() => {
  if (tcoChartRef.value) {
    tcoInstance = new Chart(tcoChartRef.value, {
      type: 'line',
      data: {
        labels: [],
        datasets: [
          {
            label: 'Manual (Inc. Errors)',
            data: [],
            borderColor: '#ef4444',
            borderWidth: 2,
            pointRadius: 0,
            tension: 0.1
          },
          {
            label: 'Lite Free TCO',
            data: [],
            borderColor: '#94a3b8',
            borderWidth: 2,
            borderDash: [5, 5],
            pointRadius: 0,
            tension: 0.1
          },
          {
            label: 'Lite Pro TCO',
            data: [],
            borderColor: '#a60df2',
            borderWidth: 2,
            pointRadius: 0,
            tension: 0.1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#1d1023',
            titleColor: '#fff',
            bodyColor: '#cbd5e1',
            borderColor: 'rgba(255,255,255,0.1)',
            borderWidth: 1,
            padding: 12,
            cornerRadius: 8
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255,255,255,0.05)' },
            ticks: { color: '#64748b' }
          },
          y: {
            grid: { color: 'rgba(255,255,255,0.05)' },
            ticks: { color: '#64748b' }
          }
        }
      }
    })
  }

  if (roiChartRef.value) {
    roiInstance = new Chart(roiChartRef.value, {
      type: 'bar',
      data: {
        labels: ['Manual', 'Lite Free', 'Lite Pro'],
        datasets: [
          {
            data: [],
            backgroundColor: ['#ef4444', '#475569', '#a60df2'],
            borderRadius: 8
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: {
            grid: { color: 'rgba(255,255,255,0.05)' },
            ticks: { color: '#64748b' }
          },
          x: {
            ticks: { color: '#fff' }
          }
        }
      }
    })
  }

  updateCharts()
})

onUnmounted(() => {
  if (tcoInstance) {
    tcoInstance.destroy()
    tcoInstance = null
  }
  if (roiInstance) {
    roiInstance.destroy()
    roiInstance = null
  }
})

// Watch for changes and update charts
watch(
  () => [
    tickets.value,
    manualCost.value,
    errorCost.value,
    months.value,
    humanAcc.value,
    freeSetup.value,
    freeAcc.value,
    freeMaint.value,
    proLicense.value,
    proSetup.value,
    proAcc.value,
    proMaint.value
  ],
  () => {
    updateCharts()
  }
)
</script>

<style scoped>
/* Motion reduce support - handled by transition presets */
</style>
