// /composables/useTicketFlow.ts
import {computed, ref, type Ref} from 'vue'
import * as d3 from 'd3'
import {breakpointsBootstrapV5, useBreakpoints, useWindowSize} from '@vueuse/core'

class XY {
    x: number
    y: number

    constructor(x: number, y: number) {
        this.x = x
        this.y = y
    }
}

class NodeModel extends XY {
    id: string
    label: string
    tClass: string
    alphaClass: string
    isQueue?: boolean

    constructor(p: {
        id: string
        label: string
        x: number
        y: number
        tClass: string
        alphaClass?: string
        isQueue?: boolean
    }) {
        super(p.x, p.y)
        this.id = p.id
        this.label = p.label
        this.tClass = p.tClass
        this.alphaClass = p.alphaClass ?? 'fill-opacity-35'
        this.isQueue = p.isQueue
    }
}

type Queue = { id: string; label: string; fillClass: string }

const theme = {
    strokeClass: 'stroke-gray-400',
    textFillClass: 'fill-gray-200'
}
const standardSize = {w: 1200, h: 400}
const allQueues: Queue[] = [
    {id: 'billing', label: 'Billing', fillClass: 'fill-amber-500'},
    {id: 'it', label: 'IT', fillClass: 'fill-cyan-500'},
    {id: 'hr', label: 'HR', fillClass: 'fill-violet-500'},
    {id: 'sales', label: 'Sales', fillClass: 'fill-rose-500'}
]

export function useTicketFlow(svgEl: Ref<SVGSVGElement | null>) {
    const {width: ww} = useWindowSize()
    const breakpoints = useBreakpoints(breakpointsBootstrapV5)
    const padding = 10

    const size = computed(() => ({
        w: Math.min(Math.max(ww.value * 0.8, 600), standardSize.w * 2),
        h: Math.min(Math.max(ww.value * 0.4, standardSize.h), standardSize.h * 2)
    }))

    const qCount = computed(() =>
        breakpoints.smaller('sm').value ? 2 : breakpoints.smaller('lg').value ? 3 : 4
    )

    const queues = computed(() => allQueues.slice(0, qCount.value))
    const queueFillClassById = computed<Record<string, string>>(() =>
        Object.fromEntries(queues.value.map(q => [q.id, q.fillClass]))
    )

    const nodeW = computed(() => {
        const qw = size.value.w / qCount.value
        if (breakpoints.smaller('sm').value) return qw * 0.7
        if (breakpoints.smaller('md').value) return qw * 0.65
        return qw * 0.6
    })
    const nodeH = computed(() => nodeW.value * 0.4)

    const dotScale = computed(() => Math.max(size.value.w / standardSize.w, 1))
    const envelopeScale = computed(() => Math.max(size.value.w / standardSize.w, 1))

    const scaleX = computed(() =>
        d3.scalePoint(
            queues.value.map(q => q.id),
            [padding + nodeW.value * 0.5, size.value.w - padding - nodeW.value * 0.5]
        )
    )

    const nodes = computed<NodeModel[]>(() => {
        const otai = new NodeModel({
            id: 'otai',
            label: 'Open Ticket AI',
            x: 0.5 * size.value.w,
            y: size.value.h * 0.5,
            tClass: 'fill-indigo-600'
        })
        const q = queues.value.map(
            q =>
                new NodeModel({
                    id: q.id,
                    label: q.label,
                    x: scaleX.value(q.id) ?? 0.5 * size.value.w,
                    y: size.value.h - nodeH.value * 0.5 - padding,
                    tClass: q.fillClass,
                    isQueue: true
                })
        )
        return [otai, ...q]
    })

    const nodesMap = computed<Record<string, NodeModel>>(
        () => Object.fromEntries(nodes.value.map(n => [n.id, n]))
    )

    const mailPos = computed(() => ({
        x: size.value.w * 0.5,
        y: -size.value.h * 0.1
    }))

    const quad = (a: XY, b: XY, lift = -60) => {
        console.log(a, b, lift)
        const mx = (a.x + b.x) / 2
        const my = (a.y + b.y) / 2 + lift
        return `M${a.x},${a.y} Q${mx},${my} ${b.x},${b.y}`
    }

    const mailD = computed(() => quad(mailPos.value, nodesMap.value.ai, -40))
    const outEdges = computed(() =>
        queues.value.map(q => ({
            id: `otai-${q.id}`,
            d: quad(nodesMap.value['otai'], nodesMap.value[q.id], -80)
        }))
    )

    const busy = ref(false)

    const alongPath = (path: SVGPathElement | null, scale = 1) => {
        if (!path) return () => ''
        const L = path.getTotalLength()
        const s = scale !== 1 ? ` scale(${scale})` : ''
        return (t: number) => {
            const p = path.getPointAtLength(t * L)
            return `translate(${p.x},${p.y})${s}`
        }
    }

    const animateAlong = (
        sel: d3.Selection<SVGGElement | SVGCircleElement, unknown, null, undefined>,
        path: SVGPathElement | null,
        ms: number,
        ease = d3.easeCubicInOut,
        scale = 1
    ) =>
        new Promise<void>(r =>
            sel
                .transition()
                .duration(ms)
                .ease(ease)
                .attrTween('transform', () => alongPath(path, scale))
                .on('end', () => r())
        )

    const blink = (
        s: d3.Selection<SVGElement, unknown, null, undefined>,
        prop = 'stroke-width',
        a = 6,
        b = 1,
        ms = 160
    ) =>
        new Promise<void>(r => {
            if (s.empty()) return r()
            s
                .transition()
                .duration(ms)
                .attr(prop, a)
                .transition()
                .duration(ms)
                .attr(prop, b)
                .on('end', () => r())
        })

    const play = async (destId: string) => {
        if (busy.value) return
        busy.value = true

        const svg = d3.select(svgEl.value)
        await blink(svg.select<SVGElement>('#button'))

        const envelope = svg
            .select('#envelopes')
            .append('use')
            .attr('href', '#envelope')
            .attr(
                'transform',
                `translate(${mailPos.value.x},${mailPos.value.y}) scale(${envelopeScale.value})`
            )

        const mailIn = svg.select<SVGPathElement>('#inbox-otai').node()
        await animateAlong(
            envelope as any,
            mailIn,
            1000,
            d3.easeCubicOut,
            envelopeScale.value
        )
        await blink(svg.select<SVGElement>('#otai'))
        envelope.remove()

        const fillClass = queueFillClassById.value[destId] || 'fill-gray-400'
        const dot = svg
            .select('#tickets')
            .append('circle')
            .attr('r', 7 * dotScale.value)
            .attr('class', fillClass)

        const path = svg.select<SVGPathElement>(`#otai-${destId}`).node()
        await animateAlong(dot as any, path, 1200, d3.easeCubicInOut)
        await blink(svg.select<SVGElement>(`#${destId}`))

        dot.remove()
        busy.value = false
    }

    const getRandomQueueId = () => {
        const qs = queues.value
        return qs[(Math.random() * qs.length) | 0].id
    }

    return {
        theme,
        size,
        nodeW,
        nodeH,
        dotScale,
        envelopeScale,
        queues,
        nodes,
        nodesMap,
        mailD,
        outEdges,
        busy,
        play,
        getRandomQueueId,
        padding
    }
}
