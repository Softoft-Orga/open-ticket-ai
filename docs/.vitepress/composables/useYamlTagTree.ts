import {computed, isRef, ref, watch} from 'vue'
import yaml from 'js-yaml'

export type RawTagNode = {
    description?: string
    required?: boolean
    default?: string
    children?: Record<string, RawTagNode>
}

export type TagNode = {
    key: string
    path: string
    description?: string
    required?: boolean
    default?: string
    children: TagNode[]
}

export function useYamlTagTree(source: string) {
    const raw = ref<Record<string, RawTagNode> | null>(null)
    const error = ref<string | null>(null)


    const parse = () => {
        try {
            error.value = null
            const data = yaml.load(source)
            if (data && typeof data === 'object') {
                raw.value = data as Record<string, RawTagNode>
            } else {
                raw.value = null
            }
        } catch (e: any) {
            raw.value = null
            error.value = e?.message ?? 'Invalid YAML'
        }
    }

    if (isRef(source)) {
        watch(source, parse, {immediate: true})
    } else {
        parse()
    }

    const buildTree = (obj: Record<string, RawTagNode>, prefix = ''): TagNode[] =>
        Object.entries(obj).map(([key, value]) => {
            const path = prefix ? `${prefix}/${key}` : key
            const childrenObj = value.children ?? {}
            return {
                key,
                path,
                description: value.description,
                required: value.required,
                default: value.default,
                children: buildTree(childrenObj, path),
            }
        })

    const tree = computed<TagNode[]>(() => {
        if (!raw.value) return []
        return buildTree(raw.value)
    })

    return {
        tree,
        error,
    }
}
