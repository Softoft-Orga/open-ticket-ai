<script setup lang='ts'>
import { computed, ref } from 'vue'
import type { PredictionExample } from '../data/PredictionDemo'
import { examples } from '../data/PredictionDemo'

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
    </div>
</template>

<style scoped>
.demo-root {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.banner {
    background: var(--vp-c-warning-1);
    color: var(--vp-c-text-1);
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;
    font-weight: 600;
    text-align: center;
    border: 1px solid var(--vp-c-warning-2);
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

@media (max-width: 960px) {
    .demo-grid {
        grid-template-columns: 1fr;
    }
}
</style>
