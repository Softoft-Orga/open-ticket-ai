<script setup lang='ts'>
import {computed, ref} from 'vue'
import TagMindmap from './TagMindmap.vue'
import TagTree from './TagTree.vue'

type PredictionExample = {
    name: string
    subject: string
    body: string
    predictedTags: string[]
}

const examples: PredictionExample[] = [
    {
        name: 'Drucker',
        subject: 'Drucker reagiert nicht auf Druckbefehle',
        body: `Hallo Support-Team,
mein Büro-Drucker HP OfficeJet Pro druckt seit dem jüngsten Firmware-Update gar nichts mehr.
Das Display bleibt dunkel und im System wird der Drucker als “Offline” angezeigt. Ich habe bereits Neustart,
zurücksetzen der Netzwerkeinstellungen und den Treiber-Neuinstallationsvorgang versucht – leider ohne Erfolg.
 Bitte um schnelle Hilfe, da wir dringend Dokumente ausdrucken müssen.`,
        predictedTags: [
            'intent/incident/performance_issue',
            'impact/high_critical/high',
            'urgency/low_normal/normal',
            'industry/tech_it/it_services/managed_services',
            'asset_kind/hardware/peripheral/printer',
            'failure_symptom/availability_performance/no_response_timeout/full_outage',
            'root_cause_hint/config_change/misconfiguration',
            'addressed_to/support_ops/technical_team',
            'formality/more_informal/informal',
            'user_role/end_user/business_user',
            'sentiment/negative/mildly_negative'
        ]
    },
    {
        name: 'Webinaranmeldung',
        subject: 'Anmeldung zum Webinar „Maschinelles Lernen für Einsteiger“',
        body: `Sehr geehrte Damen und Herren,
ich interessiere mich für Ihr kostenpflichtiges Webinar „Maschinelles Lernen für Einsteiger“ am 25.07.2025. Können Sie mir bitte folgende Informationen zukommen lassen: genaue Veranstaltungszeit, technische Voraussetzungen (z. B. Software, Browser-Version), Preis pro Teilnehmer und Zahlungsmodalitäten? Vielen Dank!`,
        predictedTags: [
            'intent/question/billing_pricing_question',
            'impact/low_normal/low',
            'urgency/low_normal/low',
            'industry/public_health_education_realestate/education/training_edtech',
            'asset_kind/service/business_service/customer_facing_service',
            'user_role/end_user/consumer_customer',
            'root_cause_hint/other',
            'addressed_to/business_functions/sales_account',
            'formality/more_formal/formal',
            'sentiment/neutral/purely_factual'
        ]
    },
    {
        name: 'Nest Learning Thermostat',
        subject: 'Nest Thermostat (3. Generation) verliert WLAN-Verbindung',
        body: `Liebes Google-Nest Team,

mein Nest Learning Thermostat der 3. Generation (Seriennummer 04-123-456-789) verbindet sich seit dem letzten Firmware-Update (v5.9.4-2) nicht mehr mit dem Heim-WLAN (Fritz!Box 7590). Es bleibt im Offline-Modus und reagiert nicht auf die App-Befehle. Bitte um kurzfristige Lösung, da die Temperatursteuerung aktuell fehlt.`,
        predictedTags: [
            'intent/incident/partial_degradation',
            'impact/low_normal/normal',
            'urgency/low_normal/normal',
            'industry/consumer_retail_hospitality/retail/specialty_retail',
            'asset_kind/hardware/specialized_device/iot_device',
            'failure_symptom/availability_performance/no_response_timeout/intermittent_outage',
            'root_cause_hint/infra_environment/network_issue',
            'addressed_to/support_ops/technical_team',
            'formality/more_informal/informal',
            'user_role/end_user/consumer_customer',
            'sentiment/negative/mildly_negative'
        ]
    },
    {
        name: 'Shopify Checkout: Zahlung',
        subject: '“Payment declined” beim Checkout auf my-shop.myshopify.com',
        body: `Liebes Shopify-Team,

mein Kunde versucht, im Shop my-shop.myshopify.com per Kreditkarte (Mastercard) zu zahlen. Die Fehlermeldung lautet “Payment declined: 2004”. In Stripe-Dashboard sehe ich keinen Eintrag. Bitte untersuchen Sie den Zahlungsfluss oder ob es ein Gateway-Problem gibt.`,
        predictedTags: [
            'intent/incident/outage_total',
            'impact/high_critical/critical',
            'urgency/high_critical/critical',
            'industry/consumer_retail_hospitality/ecommerce/online_retailer',
            'asset_kind/software/web_app/public_portal',
            'failure_symptom/behavior_functionality/workflow_blocked/cannot_complete_checkout_or_submission',
            'root_cause_hint/infra_environment/third_party_outage',
            'addressed_to/support_ops/technical_team',
            'formality/more_informal/informal',
            'user_role/admin/application_admin',
            'sentiment/negative/mildly_negative'
        ]
    },
    {
        name: 'Tesla Model 3',
        subject: 'Ladeport am Tesla Model 3 (VIN 5YJ3E1EA7LF000316) klemmt',
        body: `Guten Tag Tesla-Service,

bei meinem Model 3 Long Range (VIN 5YJ3E1EA7LF000316) klemmt seit gestern der Ladeport an der Rückseite. Der Ladeanschluss lässt sich nur mit Gewalt öffnen, und die Klappe rastet nicht automatisch ein. Das Auto ist 12 Monate alt. Bitte Termin in der Münchener Werkstatt vereinbaren oder Anweisungen zur temporären Reparatur senden.`,
        predictedTags: [
            'intent/incident/partial_degradation',
            'impact/high_critical/high',
            'urgency/low_normal/normal',
            'industry/industrial_logistics_energy/manufacturing/discrete_manufacturing',
            'asset_kind/other/generic_other',
            'failure_symptom/behavior_functionality/feature_problem/feature_not_available',
            'root_cause_hint/other',
            'addressed_to/support_ops/technical_team',
            'formality/more_formal/formal',
            'user_role/end_user/consumer_customer',
            'sentiment/negative/mildly_negative'
        ]
    }
]

const selectedName = ref(examples[0]?.name ?? '')
const selectedExample = computed<PredictionExample | undefined>(() =>
    examples.find(example => example.name === selectedName.value)
)

const setExample = (name: string) => {
    selectedName.value = name
}
</script>

<template>
    <div class="flex flex-col gap-4">
        <div class="bg-[var(--vp-c-warning-2)] text-[var(--vp-c-text-1)] py-3 px-4 rounded-lg font-semibold text-center border border-[var(--vp-c-warning-3)]">example only – no HuggingFace endpoint configured yet</div>
        <div class="grid grid-cols-[1fr_2fr] gap-4 items-start max-[960px]:grid-cols-1">
            <div class="bg-[var(--vp-c-bg-soft)] border border-[var(--vp-c-border)] rounded-xl p-4 shadow-[var(--vp-shadow-2)]">
                <div class="font-semibold mb-3">Examples</div>
                <div class="flex flex-col gap-2">
                    <button
                        v-for="example in examples"
                        :key="example.name"
                        type="button"
                        class="w-full text-left py-2.5 px-3 rounded-lg border border-[var(--vp-c-border)] bg-[var(--vp-c-bg)] text-[var(--vp-c-text-1)] transition-all duration-200 cursor-pointer hover:border-[var(--vp-c-brand-2)]"
                        :class="{ 'border-[var(--vp-c-brand-1)] bg-[var(--vp-c-brand-soft)]': example.name === selectedName }"
                        @click="setExample(example.name)"
                    >
                        {{ example.name }}
                    </button>
                </div>
            </div>
            <div class="flex flex-col gap-4" v-if="selectedExample">
                <div class="bg-[var(--vp-c-bg)] border border-[var(--vp-c-border)] rounded-xl shadow-[var(--vp-shadow-2)] overflow-hidden">
                    <div class="py-3 px-4 border-b border-[var(--vp-c-border)] font-semibold">Input</div>
                    <div class="py-3 px-4 flex flex-col gap-3">
                        <div>
                            <div class="font-semibold mb-1">Subject</div>
                            <div class="whitespace-pre-wrap leading-relaxed">{{ selectedExample.subject }}</div>
                        </div>
                        <div>
                            <div class="font-semibold mb-1">Body</div>
                            <div class="whitespace-pre-wrap leading-relaxed">{{ selectedExample.body }}</div>
                        </div>
                    </div>
                </div>
                <div class="bg-[var(--vp-c-bg)] border border-[var(--vp-c-border)] rounded-xl shadow-[var(--vp-shadow-2)] overflow-hidden">
                    <div class="py-3 px-4 border-b border-[var(--vp-c-border)] font-semibold">Predicted Tags</div>
                    <div class="flex flex-wrap gap-2 py-3 px-4 pb-4">
                        <span class="inline-flex items-center py-1.5 px-2.5 rounded-full bg-[var(--vp-c-bg-soft)] text-[var(--vp-c-text-1)] border border-[var(--vp-c-border)] text-sm" v-for="tag in selectedExample.predictedTags" :key="tag">{{ tag }}</span>
                    </div>
                </div>
                <div class="bg-[var(--vp-c-bg)] border border-[var(--vp-c-border)] rounded-xl shadow-[var(--vp-shadow-2)] overflow-hidden opacity-70">
                    <div class="py-3 px-4 border-b border-[var(--vp-c-border)] font-semibold">Your own text</div>
                    <div class="py-3 px-4">Live prediction coming soon</div>
                </div>
            </div>
        </div>
        <TagMindmap/>
        <TagTree/>
    </div>
</template>
