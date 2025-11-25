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
    <div class="demo-root">
        <div class="banner">example only – no HuggingFace endpoint configured yet</div>
        <div class="demo-grid">
            <div class="example-list">
                <div class="list-title">Examples</div>
                <div class="list-buttons">
                    <button
                        v-for="example in examples"
                        :key="example.name"
                        type="button"
                        class="list-button"
                        :class="{ active: example.name === selectedName }"
                        @click="setExample(example.name)"
                    >
                        {{ example.name }}
                    </button>
                </div>
            </div>
            <div class="example-detail" v-if="selectedExample">
                <div class="card">
                    <div class="card-header">Input</div>
                    <div class="card-body">
                        <div class="field">
                            <div class="field-label">Subject</div>
                            <div class="field-value">{{ selectedExample.subject }}</div>
                        </div>
                        <div class="field">
                            <div class="field-label">Body</div>
                            <div class="field-value">{{ selectedExample.body }}</div>
                        </div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">Predicted Tags</div>
                    <div class="tag-wrap">
                        <span class="tag-chip" v-for="tag in selectedExample.predictedTags" :key="tag">{{ tag }}</span>
                    </div>
                </div>
                <div class="card muted">
                    <div class="card-header">Your own text</div>
                    <div class="card-body">Live prediction coming soon</div>
                </div>
            </div>
        </div>

        <div class="tag-visuals">
            <div class="visual-card">
                <TagMindmap />
            </div>
            <div class="visual-card">
                <TagTree />
            </div>
        </div>
    </div>
</template>

<style scoped>
.demo-root {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.banner {
    background: var(--vp-c-warning-2);
    color: var(--vp-c-text-1);
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;
    font-weight: 600;
    text-align: center;
    border: 1px solid var(--vp-c-warning-3);
}

.demo-grid {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 1rem;
    align-items: start;
}

.example-list {
    background: var(--vp-c-bg-soft);
    border: 1px solid var(--vp-c-border);
    border-radius: 0.75rem;
    padding: 1rem;
    box-shadow: var(--vp-shadow-2);
}

.list-title {
    font-weight: 600;
    margin-bottom: 0.75rem;
}

.list-buttons {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.list-button {
    width: 100%;
    text-align: left;
    padding: 0.65rem 0.75rem;
    border-radius: 0.5rem;
    border: 1px solid var(--vp-c-border);
    background: var(--vp-c-bg);
    color: var(--vp-c-text-1);
    transition: background 0.2s ease, border-color 0.2s ease;
    cursor: pointer;
}

.list-button:hover {
    border-color: var(--vp-c-brand-2);
}

.list-button.active {
    border-color: var(--vp-c-brand-1);
    background: var(--vp-c-brand-soft);
}

.example-detail {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.card {
    background: var(--vp-c-bg);
    border: 1px solid var(--vp-c-border);
    border-radius: 0.75rem;
    box-shadow: var(--vp-shadow-2);
    overflow: hidden;
}

.card.muted {
    opacity: 0.7;
}

.card-header {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--vp-c-border);
    font-weight: 600;
}

.card-body {
    padding: 0.75rem 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.card-body.padded {
    gap: 1.25rem;
}

.field-label {
    font-weight: 600;
    margin-bottom: 0.25rem;
}

.field-value {
    white-space: pre-wrap;
    line-height: 1.5;
}

.tag-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    padding: 0.75rem 1rem 1rem;
}

.tag-chip {
    display: inline-flex;
    align-items: center;
    padding: 0.4rem 0.65rem;
    border-radius: 999px;
    background: var(--vp-c-bg-soft);
    color: var(--vp-c-text-1);
    border: 1px solid var(--vp-c-border);
    font-size: 0.95rem;
}

.tag-visuals {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 1rem;
    align-items: start;
}

.visual-card {
    background: var(--vp-c-bg);
    border: 1px solid var(--vp-c-border);
    border-radius: 0.9rem;
    box-shadow: var(--vp-shadow-2);
    padding: 1rem;
}

@media (max-width: 960px) {
    .demo-grid {
        grid-template-columns: 1fr;
    }
}
</style>
