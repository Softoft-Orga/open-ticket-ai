<!-- /components/TicketFlowTopDown.vue -->
<template>
    <ClientOnly>
        <div class="my-8">
            <h3 class="text-2xl font-bold mb-5 border-none p-0">
                {{ t('otai_animation.title') }}
            </h3>
            <svg
                ref="svgEl"
                :viewBox="`0 0 ${size.w} ${size.h}`"
                class="router-svg border rounded-lg border-gray-800"
            >
                <defs>
                    <symbol id="envelope" viewBox="-14 -12 28 24">
                        <rect
                            class="fill-gray-200 stroke-gray-200"
                            height="20"
                            rx="3"
                            stroke-width="2"
                            width="28"
                            x="-14"
                            y="-10"
                        />
                        <polyline
                            class="stroke-gray-400"
                            fill="none"
                            points="-14,-10 0,2 14,-10"
                            stroke-width="2"
                        />
                    </symbol>
                </defs>

                <g
                    id="button"
                    :key="'button'"
                    class="cursor-pointer hover:opacity-80"
                    role="button"
                    tabindex="0"
                    @click="handleClick"
                    @keydown.enter="handleClick"
                    @keydown.space.prevent="handleClick"
                >
                    <rect
                        :class="theme.strokeClass"
                        :height="nodeH"
                        :width="nodeW"
                        :x="0.5 * size.w - nodeW / 2"
                        :y="nodeH / 2 + padding - nodeH / 2"
                        class="fill-indigo-600 fill-opacity-35"
                        rx="6"
                    />
                    <text
                        :class="theme.textFillClass"
                        :font-size="Math.round(Math.min(26, Math.max(12, nodeH * 0.25)))"
                        :x="0.5 * size.w"
                        :y="nodeH / 2 + padding + 5"
                        class="select-none"
                        style="pointer-events:none"
                        text-anchor="middle"
                    >
                        {{ busy ? t('otai_animation.processingText') : t('otai_animation.startAnimationText') }}
                    </text>
                </g>

                <g
                    v-for="n in nodes"
                    :key="n.id"
                    :data-node="n.id"
                    class="cursor-pointer"
                >
                    <rect
                        :id="n.id"
                        :class="[n.tClass, n.alphaClass, theme.strokeClass]"
                        :height="nodeH"
                        :width="nodeW"
                        :x="n.x - nodeW / 2"
                        :y="n.y - nodeH / 2"
                        rx="6"
                    />
                    <text
                        :class="theme.textFillClass"
                        :font-size="Math.round(Math.min(26, Math.max(12, nodeH * 0.25)))"
                        :x="n.x"
                        :y="n.y + 5"
                        class="select-none"
                        style="pointer-events:none"
                        text-anchor="middle"
                    >
                        {{ n.label }}
                    </text>
                </g>

                <path id="inbox-otai" :d="mailD" fill="none" stroke="transparent"/>
                <path
                    v-for="e in outEdges"
                    :id="e.id"
                    :key="e.id"
                    :d="e.d"
                    fill="none"
                    stroke="transparent"
                />

                <g id="envelopes"/>
                <g id="tickets"/>
            </svg>
        </div>
    </ClientOnly>
</template>

<script lang="ts" setup>
import {ref, watch} from 'vue'
import {useI18n} from 'vue-i18n'
import {useElementVisibility} from '@vueuse/core'
import {useTicketFlow} from '../../composables/useTicketFlow'

const {t} = useI18n()
const svgEl = ref<SVGSVGElement | null>(null)

const {
    theme,
    size,
    nodeW,
    nodeH,
    nodes,
    mailD,
    outEdges,
    busy,
    play,
    getRandomQueueId,
    padding
} = useTicketFlow(svgEl)

function handleClick() {
    play(getRandomQueueId())
}

const visible = useElementVisibility(svgEl)
let started = false

watch(visible, v => {
    if (v && !started) {
        started = true
        handleClick()
    }
})
</script>

<style scoped>
svg.router-svg {
    width: 100%;
    height: auto;
    display: block;
}
</style>
