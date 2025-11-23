<script setup lang='ts'>
import { computed, ref } from 'vue'
import yaml from 'js-yaml'
import type { PredictionExample } from '../data/PredictionDemo'
import { examples } from '../data/PredictionDemo'
import tagYaml from '../.vitepress/data/tags.yml?raw'

const selectedName = ref(examples[0]?.name ?? '')
const selectedExample = computed<PredictionExample | undefined>(() =>
    examples.find(example => example.name === selectedName.value)
)

const topIcons = computed<Record<string, string>>(() => {
    const parsed = yaml.load(tagYaml)
    if (!parsed || typeof parsed !== 'object') return {}
    return Object.entries(parsed as Record<string, {icon?: string}>).reduce<Record<string, string>>(
        (acc, [key, value]) => {
            if (value?.icon) acc[key] = value.icon
            return acc
        },
        {},
    )
})

const stylizedTags = computed(() => {
    if (!selectedExample.value) return []
    return selectedExample.value.predictedTags.map(tag => {
        const parts = tag.split('/')
        const [first, second, ...rest] = parts
        const third = rest.length ? rest.join('/') : second ?? first
        return {
            key: tag,
            icon: (first && topIcons.value[first]) ? topIcons.value[first] : '📌',
            first,
            second,
            third,
        }
    })
})

const setExample = (name: string) => {
    selectedName.value = name
}
</script>

<template>
    <div class="flex flex-col gap-4 text-slate-100">
        <div class="rounded-lg border border-amber-700 bg-amber-900/60 px-4 py-3 text-center text-sm font-semibold shadow-lg shadow-amber-900/30">
            example only – no HuggingFace endpoint configured yet
        </div>
        <div class="grid grid-cols-1 gap-4 lg:grid-cols-[1fr,2fr]">
            <div class="rounded-xl border border-slate-800 bg-slate-900/70 p-4 shadow-xl shadow-black/40">
                <div class="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-300">Examples</div>
                <div class="flex flex-col gap-2">
                    <button
                        v-for="example in examples"
                        :key="example.name"
                        type="button"
                        class="w-full rounded-lg border border-slate-800 bg-slate-950/70 px-3 py-2 text-left text-slate-100 transition hover:border-indigo-600 hover:bg-slate-900/80"
                        :class="example.name === selectedName ? 'border-indigo-500/80 bg-indigo-950/60 text-indigo-100 shadow-lg shadow-indigo-900/40' : ''"
                        @click="setExample(example.name)"
                    >
                        {{ example.name }}
                    </button>
                </div>
            </div>
            <div v-if="selectedExample" class="flex flex-col gap-4">
                <div class="rounded-xl border border-slate-800 bg-slate-900/70 shadow-xl shadow-black/40">
                    <div class="border-b border-slate-800 px-4 py-3 text-sm font-semibold uppercase tracking-wide text-slate-300">Input</div>
                    <div class="flex flex-col gap-4 px-4 py-4">
                        <div class="flex flex-col gap-1">
                            <div class="text-sm font-semibold text-slate-300">Subject</div>
                            <div class="whitespace-pre-wrap text-base leading-relaxed text-slate-100">{{ selectedExample.subject }}</div>
                        </div>
                        <div class="flex flex-col gap-1">
                            <div class="text-sm font-semibold text-slate-300">Body</div>
                            <div class="whitespace-pre-wrap text-base leading-relaxed text-slate-100">{{ selectedExample.body }}</div>
                        </div>
                    </div>
                </div>
                <div class="rounded-xl border border-slate-800 bg-slate-900/70 shadow-xl shadow-black/40">
                    <div class="border-b border-slate-800 px-4 py-3 text-sm font-semibold uppercase tracking-wide text-slate-300">Predicted Tags</div>
                    <div class="flex flex-wrap gap-3 px-4 py-4">
                        <div
                            v-for="tag in stylizedTags"
                            :key="tag.key"
                            class="group flex items-center gap-3 rounded-2xl border border-indigo-800/60 bg-gradient-to-br from-slate-950/80 via-slate-900/80 to-indigo-950/60 px-4 py-3 shadow-lg shadow-black/40 ring-1 ring-indigo-900/50"
                        >
                            <div class="flex h-11 w-11 flex-shrink-0 items-center justify-center rounded-xl bg-indigo-900/60 text-2xl shadow-inner shadow-black/50">
                                {{ tag.icon }}
                            </div>
                            <div class="flex flex-col leading-tight text-indigo-50">
                                <span class="text-xs uppercase tracking-wide text-indigo-200/80">{{ tag.first }}</span>
                                <span class="text-[10px] font-semibold text-indigo-300/70">{{ tag.second }}</span>
                                <span class="text-2xl font-black text-indigo-50 drop-shadow-sm">{{ tag.third }}</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="rounded-xl border border-slate-800 bg-slate-950/50 shadow-inner shadow-black/40">
                    <div class="border-b border-slate-800 px-4 py-3 text-sm font-semibold uppercase tracking-wide text-slate-400">Your own text</div>
                    <div class="px-4 py-4 text-sm text-slate-400">Live prediction coming soon</div>
                </div>
            </div>
        </div>
    </div>
</template>
