<template>
  <div class="min-h-screen bg-background-dark">
    <!-- Hero Section -->
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-24">
      <div class="mb-12">
        <div class="inline-block mb-6">
          <Badge type="primary">
            🔒 ON-PREMISE ONLY (0.5B PARAMETERS)
          </Badge>
        </div>
        <h1 class="text-5xl md:text-7xl font-black text-white mb-8">
          Tagging AI <span class="text-primary-light">Lite Free.</span>
        </h1>
        <p class="text-xl text-text-dim max-w-3xl leading-relaxed mb-12">
          Small-footprint classification. Optimized for edge deployment and privacy-focused evaluation. 
          Supports the full OTA taxonomy tree.
        </p>
        <Button
          variant="secondary"
          size="lg"
        >
          DOWNLOAD CONTAINER
        </Button>
      </div>

      <!-- Performance Metrics -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-20">
        <Card
          background="surface-dark"
          padding="default"
          hoverable
        >
          <div class="text-sm text-text-dim mb-2 font-semibold uppercase tracking-wider">
            MODEL SIZE
          </div>
          <div class="text-2xl font-bold text-white">
            500M Params
          </div>
        </Card>
        <Card
          background="surface-dark"
          padding="default"
          hoverable
        >
          <div class="text-sm text-text-dim mb-2 font-semibold uppercase tracking-wider">
            VRAM REQUIREMENT
          </div>
          <div class="text-2xl font-bold text-white">
            &lt;1GB
          </div>
        </Card>
        <Card
          background="surface-dark"
          padding="default"
          hoverable
        >
          <div class="text-sm text-text-dim mb-2 font-semibold uppercase tracking-wider">
            AVERAGE ACCURACY
          </div>
          <div class="text-2xl font-bold text-white">
            ~82%
          </div>
        </Card>
        <Card
          background="surface-dark"
          padding="default"
          hoverable
        >
          <div class="text-sm text-text-dim mb-2 font-semibold uppercase tracking-wider">
            LANGUAGE SUPPORT
          </div>
          <div class="text-2xl font-bold text-white">
            Global / Multilingual
          </div>
        </Card>
      </div>

      <!-- Interactive Tags Tree Section -->
      <div class="mb-20">
        <div class="text-center mb-12">
          <h2 class="text-4xl md:text-5xl font-bold text-white mb-4">
            INTERACTIVE TAGS TREE
          </h2>
          <p class="text-text-dim text-lg italic">
            example predictions - full model deployment coming soon
          </p>
        </div>

        <div class="grid lg:grid-cols-3 gap-8">
          <!-- Test Examples Sidebar -->
          <div class="lg:col-span-1">
            <Card
              background="surface-dark"
              padding="default"
            >
              <template #header>
                <h3 class="text-sm font-bold text-text-dim uppercase tracking-wider">
                  TEST EXAMPLES
                </h3>
              </template>
              <div class="space-y-2">
                <Button
                  v-for="(example, index) in examples"
                  :key="index"
                  :variant="activeExample === index ? 'primary' : 'ghost'"
                  class="w-full !justify-start"
                  @click="activeExample = index"
                >
                  {{ example.name }}
                </Button>
              </div>
            </Card>
          </div>

          <!-- Helpdesk Input & AI Classification Result -->
          <div class="lg:col-span-2 space-y-6">
            <!-- Helpdesk Input Card -->
            <Card
              background="surface-dark"
              padding="lg"
            >
              <template #header>
                <h3 class="text-sm font-bold text-cyan-glow uppercase tracking-wider">
                  HELPDESK INPUT
                </h3>
              </template>
              <div class="mb-4">
                <div class="text-xs text-text-dim mb-2">
                  Subj:
                </div>
                <div class="text-white font-medium">
                  {{ examples[activeExample].subject }}
                </div>
              </div>
              <div>
                <div class="text-white leading-relaxed">
                  {{ examples[activeExample].body }}
                </div>
              </div>
            </Card>

            <!-- AI Classification Result -->
            <Card
              background="surface-dark"
              padding="lg"
            >
              <template #header>
                <h3 class="text-sm font-bold text-primary-light uppercase tracking-wider">
                  AI CLASSIFICATION RESULT
                </h3>
              </template>
              <div class="flex flex-wrap gap-2">
                <Badge
                  v-for="tag in examples[activeExample].tags"
                  :key="tag"
                  type="primary"
                  class="!px-3 !py-1.5 !font-mono"
                >
                  {{ tag }}
                </Badge>
              </div>
            </Card>
          </div>
        </div>
      </div>

      <!-- Engine Taxonomy Section -->
      <div>
        <div class="text-center mb-12">
          <h2 class="text-4xl md:text-5xl font-bold text-white mb-4">
            ENGINE TAXONOMY
          </h2>
        </div>
        
        <div class="grid md:grid-cols-3 gap-6">
          <Card
            background="surface-dark"
            padding="lg"
            hoverable
          >
            <template #title>
              <div class="text-white font-bold text-xl uppercase tracking-wide">
                INDUSTRY
              </div>
            </template>
            <p class="text-text-dim text-sm mb-6">
              Domain of the customer's business
            </p>
            <ul class="space-y-2">
              <li
                v-for="item in [
                  'TECH_IT',
                  'FINANCE_SERVICES',
                  'CONSUMER_RETAIL',
                  'PUBLIC_HEALTH',
                  'INDUSTRIAL'
                ]"
                :key="item"
                class="flex items-center gap-3"
              >
                <div class="w-2 h-2 rounded-full bg-primary-light" />
                <span class="text-white text-sm font-medium">{{ item }}</span>
              </li>
            </ul>
          </Card>
          <Card
            background="surface-dark"
            padding="lg"
            hoverable
          >
            <template #title>
              <div class="text-white font-bold text-xl uppercase tracking-wide">
                INTENT
              </div>
            </template>
            <p class="text-text-dim text-sm mb-6">
              What the user wants to achieve
            </p>
            <ul class="space-y-2">
              <li
                v-for="item in [
                  'INCIDENT',
                  'SERVICE_REQUEST',
                  'QUESTION',
                  'COMPLAINT',
                  'CHANGE_REQUEST'
                ]"
                :key="item"
                class="flex items-center gap-3"
              >
                <div class="w-2 h-2 rounded-full bg-primary-light" />
                <span class="text-white text-sm font-medium">{{ item }}</span>
              </li>
            </ul>
          </Card>
          <Card
            background="surface-dark"
            padding="lg"
            hoverable
          >
            <template #title>
              <div class="text-white font-bold text-xl uppercase tracking-wide">
                FAILURE SYMPTOM
              </div>
            </template>
            <p class="text-text-dim text-sm mb-6">
              Manifestation of the problem
            </p>
            <ul class="space-y-2">
              <li
                v-for="item in [
                  'AVAILABILITY',
                  'PERFORMANCE',
                  'FUNCTIONALITY',
                  'AUTHENTICATION',
                  'INTEGRATION'
                ]"
                :key="item"
                class="flex items-center gap-3"
              >
                <div class="w-2 h-2 rounded-full bg-primary-light" />
                <span class="text-white text-sm font-medium">{{ item }}</span>
              </li>
            </ul>
          </Card>
          <Card
            background="surface-dark"
            padding="lg"
            hoverable
          >
            <template #title>
              <div class="text-white font-bold text-xl uppercase tracking-wide">
                SENTIMENT
              </div>
            </template>
            <p class="text-text-dim text-sm mb-6">
              Emotional tone of the text
            </p>
            <ul class="space-y-2">
              <li
                v-for="item in [
                  'NEGATIVE (FRUSTRATED/ANGRY)',
                  'NEUTRAL (FACTUAL)',
                  'POSITIVE (GRATEFUL)'
                ]"
                :key="item"
                class="flex items-center gap-3"
              >
                <div class="w-2 h-2 rounded-full bg-primary-light" />
                <span class="text-white text-sm font-medium">{{ item }}</span>
              </li>
            </ul>
          </Card>
          <Card
            background="surface-dark"
            padding="lg"
            hoverable
          >
            <template #title>
              <div class="text-white font-bold text-xl uppercase tracking-wide">
                FORMALITY
              </div>
            </template>
            <p class="text-text-dim text-sm mb-6">
              Writing style level
            </p>
            <ul class="space-y-2">
              <li
                v-for="item in [
                  'MORE_FORMAL',
                  'NEUTRAL',
                  'MORE_INFORMAL'
                ]"
                :key="item"
                class="flex items-center gap-3"
              >
                <div class="w-2 h-2 rounded-full bg-primary-light" />
                <span class="text-white text-sm font-medium">{{ item }}</span>
              </li>
            </ul>
          </Card>
          <Card
            background="surface-dark"
            padding="lg"
            hoverable
          >
            <template #title>
              <div class="text-white font-bold text-xl uppercase tracking-wide">
                ADDRESSED_TO
              </div>
            </template>
            <p class="text-text-dim text-sm mb-6">
              Explicitly mentioned recipient
            </p>
            <ul class="space-y-2">
              <li
                v-for="item in [
                  'SUPPORT_OPS',
                  'BUSINESS_FUNCTIONS',
                  'LEADERSHIP',
                  'NAMED_PERSON'
                ]"
                :key="item"
                class="flex items-center gap-3"
              >
                <div class="w-2 h-2 rounded-full bg-primary-light" />
                <span class="text-white text-sm font-medium">{{ item }}</span>
              </li>
            </ul>
          </Card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import Button from '../core/basic/Button.vue';
import Card from '../core/basic/Card.vue';
import Badge from '../core/basic/Badge.vue';

interface Example {
  name: string;
  subject: string;
  body: string;
  tags: string[];
}

const activeExample = ref(0);

const examples: Example[] = [
  {
    name: "Drucker",
    subject: "Drucker reagiert nicht auf Druckbefehle",
    body: "Hallo Support-Team, mein Büro-Drucker HP OfficeJet Pro druckt seit dem jüngsten Firmware-Update gar nichts mehr. Das Display bleibt dunkel und im System wird der Drucker als \"Offline\" angezeigt. Ich habe bereits Neustart, zurücksetzen der Netzwerkeinstellungen und den Treiber-Neuinstallationsvorgang versucht – leider ohne Erfolg. Bitte um schnelle Hilfe, da wir dringend Dokumente ausdrucken müssen.",
    tags: ["intent/incident/performance_issue", "impact/high_critical/high", "urgency/low_normal/normal", "industry/tech_it/it_services/managed_services", "asset_kind/hardware/peripheral/printer", "failure_symptom/availability_performance/no_response_timeout/full_outage", "root_cause_hint/config_change/misconfiguration", "addressed_to/support_ops/technical_team", "formality/more_informal/informal", "user_role/end_user/business_user", "sentiment/negative/mildly_negative"]
  },
  {
    name: "Webinaranmeldung",
    subject: "Registrierung für das Automatisierungs-Webinar",
    body: "Guten Tag, ich möchte mich für das Webinar anmelden, aber der Bestätigungsbutton ist ausgegraut. Ich habe meine Firmendaten bereits korrekt eingegeben.",
    tags: ["intent/service_request/new_service_onboarding", "industry/public_health_education_realestate/education/training_edtech", "failure_symptom/behavior_functionality/workflow_blocked", "user_role/end_user/consumer_customer", "sentiment/neutral/purely_factual"]
  },
  {
    name: "Nest Thermostat",
    subject: "Nest Learning Thermostat showing Error W5",
    body: "My thermostat disconnected from WiFi and shows error W5. I've tried resetting the router but the thermostat still won't find any networks.",
    tags: ["intent/incident/partial_degradation", "asset_kind/hardware/specialized_device/iot_device", "failure_symptom/availability_performance/no_response_timeout", "root_cause_hint/infra_environment/network_issue", "sentiment/negative/mildly_negative"]
  },
  {
    name: "Shopify Checkout",
    subject: "Payment failed during checkout: Credit Card error",
    body: "I am trying to finish my purchase but my Visa card is being rejected with a generic 'System Error'. My bank says the card is fine.",
    tags: ["intent/incident/performance_issue", "industry/consumer_retail_hospitality/ecommerce/online_retailer", "failure_symptom/behavior_functionality/wrong_or_unexpected_result", "asset_kind/service/external_api/payment_gateway_api", "user_role/end_user/consumer_customer"]
  },
  {
    name: "Tesla Model 3",
    subject: "Supercharger connection issue",
    body: "Charging won't start at the Berlin Supercharger. Tried two different stalls. The car says 'Ready to charge' but no current is flowing.",
    tags: ["intent/incident/outage_total", "industry/industrial_logistics_energy/manufacturing/discrete_manufacturing", "asset_kind/hardware/specialized_device/iot_device", "urgency/high_critical/high", "sentiment/negative/frustrated"]
  }
];
</script>

<style scoped>
.glow-text {
  text-shadow: 0 0 20px rgba(100, 108, 255, 0.3);
}
</style>
