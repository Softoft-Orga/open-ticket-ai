<template>

    <section class="w-100 pt-1 pb-5 lg:pb-10 px-5 lg:px-14 bg-gray-900 rounded-lg">
        <h2 class="!mt-1 !mb-6 w-full text-center text-vp-text border-0 !border-t-0">{{
                t('otai_prediction_demo_component.title')
            }}</h2>
        <div class="mb-3">
            <SelectComponent
                v-model="selected"
                :label="t('otai_prediction_demo_component.pickExampleText')"
                :options="exampleOptions"
                :placeholder="t('otai_prediction_demo_component.exampleSelectDefault')"
                @update:modelValue="applyExample"
            >
            </SelectComponent>
        </div>

        <div class="mb-3">
            <label class="block mb-1 font-bold" for="demo-subject">{{
                    t('otai_prediction_demo_component.subjectLabel')
                }}</label>
            <TextField
                id="demo-subject"
                v-model="subject"
                :placeholder="t('otai_prediction_demo_component.subjectPlaceholder')"
                type="text"
            />
        </div>

        <div class="mb-3">
            <label class="block mb-1 font-bold" for="demo-body">{{
                    t('otai_prediction_demo_component.messageLabel')
                }}</label>
            <TextArea
                id="demo-body"
                v-model="body"
                :placeholder="t('otai_prediction_demo_component.messagePlaceholder')"
                class="min-h-40"
            ></TextArea>
        </div>

        <Button
            :disabled="loading"
            class="px-4 py-2 mt-1 mb-4 bg-vp-brand-1 text-white hover:bg-vp-brand-light disabled:opacity-50"
            @click="predict"
        >
                    <span v-if="loading" aria-hidden="true"
                          class="animate-spin h-4 w-4 mr-1 border-2 border-white border-t-transparent rounded-full">

                    </span>
            <span v-if="loading"
                  role="status">{{ t('otai_prediction_demo_component.loadingText') }}</span>
            <span v-else
                  class="text-white">{{ t('otai_prediction_demo_component.submitButtonText') }}</span>
        </Button>

        <Callout v-if="errorMessage" type="danger">
            {{ errorMessage }}
        </Callout>

        <ResultTable v-if="queueResult && prioResult" :prio-result="prioResult" :queue-result="queueResult"/>
        <p>{{ t('otai_prediction_demo_component.apiText') }}<span v-if="apiLink != ''">:</span> <a v-if="apiLink != ''"
                                                                                                   :href="apiLink">German
            Ticket Classification API</a></p>

    </section>
</template>

<script lang="ts" setup>

import {onMounted, ref} from 'vue'
import Button from '../core/basic/Button.vue'
import {examples} from "./demoExamples";
import {useI18n} from 'vue-i18n'
import ResultTable from "./ResultTable.vue";
import SelectComponent from "../core/forms/SelectComponent.vue";
import TextField from "../core/forms/TextField.vue";
import TextArea from "../core/forms/TextArea.vue";
import Callout from "../core/basic/Callout.vue";
import {useHumanLoadedPage} from "../../composables/useHumanLoadedPage";

const {apiLink = ''} = defineProps<{
    apiLink?: string
}>()
const {t} = useI18n()
const QUEUE_EP = 'https://uwlzdugezcmrk5vk.eu-west-1.aws.endpoints.huggingface.cloud'
const PRIORITY_EP = 'https://rxnypflnfgdbgoxr.us-east-1.aws.endpoints.huggingface.cloud'


const exampleOptions = examples.map(ex => ({
    value: ex.name,
    label: ex.name,
    subject: ex.subject,
    body: ex.body
}))

async function query(endpoint: string, payload: any) {
    const res = await fetch(endpoint, {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`)
    return res.json()
}

function constructModelInput(subject: string, body: string) {
    return {
        inputs: (subject + ' ').repeat(2) + body,
        parameters: {}
    }
}


async function predictQueue(subject: string, body: string) {
    return query(QUEUE_EP, constructModelInput(subject, body))
}

async function predictPriority(subject: string, body: string) {
    return query(PRIORITY_EP, constructModelInput(subject, body))
}


// form state
const subject = ref('')
const body = ref('')
const loading = ref(false)
const errorMessage = ref<string | null>(null)

// API results
const queueResult = ref<any>(null)
const prioResult = ref<any>(null)

// select logic
const selected = ref('')

function applyExample() {
    const selectedOption = exampleOptions.find(opt => opt.value === selected.value)
    subject.value = selectedOption.subject
    body.value = selectedOption.body
    queueResult.value = null
    prioResult.value = null
    errorMessage.value = null
}

async function warmupHuggingfaceEndpoints() {
    // Warmup the endpoints to avoid cold start issues
    try {
        await Promise.all([
            predictQueue('Warmup', 'This is a warmup message'),
            predictPriority('Warmup', 'This is a warmup message')
        ])
        console.log('Endpoints warmed up successfully')
    } catch (e) {
        console.error('Error during warmup:', e)
    }
}

// retry+backoff prediction
async function predict(attempt = 1) {
    const maxAttempts = 8

    loading.value = true
    errorMessage.value = null
    queueResult.value = null

    prioResult.value = null

    try {
        const [q, p] = await Promise.all([
            predictQueue(subject.value, body.value),
            predictPriority(subject.value, body.value)
        ])
        queueResult.value = q
        prioResult.value = p
        loading.value = false
    } catch (e) {
        console.error(`Attempt ${attempt} failed`, e)
        if (attempt >= maxAttempts) {
            errorMessage.value = t('otai_prediction_demo_component.predictionError')
            loading.value = false
        } else {
            const delay = 500 * Math.pow(2, attempt - 1)
            await new Promise(res => setTimeout(res, delay))
            return predict(attempt + 1)
        }
    }
}

onMounted(() => {
    useHumanLoadedPage(() => {
        warmupHuggingfaceEndpoints().then(() => {
            console.log('Warmup complete')
        }).catch(err => {
            console.error('Warmup failed:', err)
        })
    })
})


</script>
