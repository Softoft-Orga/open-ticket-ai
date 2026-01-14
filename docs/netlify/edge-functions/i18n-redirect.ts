export default async (request: Request) => {
    const url = new URL(request.url)
    const path = url.pathname

    const supported = ['de', 'en'] as const
    const defaultLocale = 'de'

    const hasLocale = supported.some(l => path === `/${l}` || path.startsWith(`/${l}/`))
    if (hasLocale) return fetch(request)

    const header = request.headers.get('accept-language') || ''
    const pick = pickLocaleFromAcceptLanguage(header, [...supported], defaultLocale)

    url.pathname = `/${pick}${path}`
    return Response.redirect(url.toString(), 302)
}

function pickLocaleFromAcceptLanguage(
    header: string,
    supported: string[],
    fallback: string
): string {
    const prefs = header
        .split(',')
        .map(part => part.trim())
        .filter(Boolean)
        .map(part => {
            const [tagRaw, ...params] = part.split(';').map(s => s.trim())
            const tag = (tagRaw || '').toLowerCase()
            let q = 1
            for (const p of params) {
                const m = /^q=([0-9.]+)$/i.exec(p)
                if (m) {
                    const v = Number(m[1])
                    if (Number.isFinite(v)) q = v
                }
            }
            const base = tag.split('-')[0] || ''
            return {tag, base, q}
        })
        .sort((a, b) => b.q - a.q)

    for (const p of prefs) {
        if (supported.includes(p.tag)) return p.tag
        if (supported.includes(p.base)) return p.base
    }
    return fallback
}
