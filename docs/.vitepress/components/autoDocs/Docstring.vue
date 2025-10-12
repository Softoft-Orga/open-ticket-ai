<template>
    <div v-if="doc" class="bg-vp-bg-soft rounded-lg text-vp-text text-md leading-relaxed">
        <!-- Short description formatted as inline markdown -->
        <div
            v-if="doc.short_description"
            class="text-md font-medium mb-4 text-vp-text"
            v-html="renderedShort"
        />

        <!-- Long description formatted as full markdown -->
        <div
            v-if="doc.long_description"
            class="text-vp-text-2 border-b border-vp-border pb-4 mb-4 prose prose-sm prose-dark"
            v-html="renderedLong"
        />

        <!-- Parameters section -->
        <section v-if="doc.params && doc.params.length" class="mt-6">
            <DocstringSection title="Parameters">
                <div v-for="param in doc.params" :key="param.name" class="flex flex-col">
                    <div class="flex items-center gap-2 flex-wrap">
                        <code class="font-semibold text-vp-brand">{{ param.name }}</code>
                        <span v-if="param.type" class="font-mono text-xs text-green-400">{{ param.type }}</span>
                        <span v-if="param.is_optional" class="text-xs text-vp-text-2 italic">(optional)</span>
                    </div>
                    <div
                        v-if="param.description"
                        class="text-vp-text-2 mt-1 prose prose-xs prose-dark"
                        v-html="renderMarkdown(param.description)"
                    />
                    <div v-if="param.default" class="text-sm text-vp-text-2 mt-2">
                        Default: <code class="bg-vp-bg border-vp-border px-1 py-0.5">{{ param.default }}</code>
                    </div>
                </div>
            </DocstringSection>
        </section>

        <!-- Returns section -->
        <section v-if="doc.returns" class="mt-6">
            <h4 class="text-sm font-semibold mb-3 uppercase tracking-wider text-vp-text-2">Returns</h4>
            <div class="flex flex-col gap-1">
        <span
            v-if="doc.returns.type"
            class="font-mono text-xs text-green-400"
        >
          {{ doc.returns.type }}
        </span>
                <div
                    v-if="doc.returns.description"
                    class="text-vp-text-2 prose prose-xs prose-dark"
                    v-html="renderMarkdown(doc.returns.description)"
                />
            </div>
        </section>

        <!-- Raises section -->
        <section v-if="doc.raises && doc.raises.length" class="mt-6">
            <h4 class="text-sm font-semibold mb-3 uppercase tracking-wider text-vp-text-2">Raises</h4>
            <div class="flex flex-col gap-4">
                <div v-for="err in doc.raises" :key="err.type" class="flex flex-col">
                    <code class="font-semibold text-red-400">{{ err.type }}</code>
                    <div
                        v-if="err.description"
                        class="text-vp-text-2 mt-1 prose prose-xs prose-dark"
                        v-html="renderMarkdown(err.description)"
                    />
                </div>
            </div>
        </section>
    </div>
</template>

<script lang="ts" setup>
import {computed} from 'vue'
import MarkdownIt from 'markdown-it'
import type {DocstringData} from '../../composables/useApiDocs'

const md = new MarkdownIt({html: true, linkify: true})

const props = withDefaults(defineProps<{ doc: DocstringData | null }>(), {doc: null})

const renderedShort = computed(() =>
    props.doc?.short_description
        ? md.renderInline(props.doc.short_description)
        : ''
)

const renderedLong = computed(() =>
    props.doc?.long_description
        ? md.render(props.doc.long_description)
        : ''
)

function renderMarkdown(input: string) {
    return md.render(input)
}
</script>
