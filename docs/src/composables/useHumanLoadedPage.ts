import {useDocumentVisibility, useEventListener} from '@vueuse/core'

export function useHumanLoadedPage(callback: () => void) {
    let triggered = false
    const run = () => {
        if (triggered) return
        triggered = true
        callback()
        cleanup()
    }

    const cleanupFns: (() => void)[] = []

    const add = (el: EventTarget, event: string) => {
        cleanupFns.push(useEventListener(el, event, run, {once: true, capture: true}))
    }

    const cleanup = () => cleanupFns.forEach(fn => fn())

    const visibility = useDocumentVisibility()
    if (visibility.value === 'visible') {
        add(document, 'pointerdown')
    }

    add(document, 'keydown')
    add(document, 'touchstart')

    cleanupFns.push(useEventListener(document, 'visibilitychange', () => {
        if (document.visibilityState === 'visible') add(document, 'pointerdown')
    }))
}
