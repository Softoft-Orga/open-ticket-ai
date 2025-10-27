import {computed, readonly} from 'vue'

export interface NewsArticle {
    title: string
    description: string
    link: string
    date: string
    dateTime: Date
    formattedDate: string
    image: string
    toastMessage: string
    showOnNews: boolean
}

type MarkdownModule = {
    frontmatter?: Record<string, unknown>
}

const blogModules = import.meta.glob('../docs_src/en/blog/**/*.md', {eager: true}) as Record<string, MarkdownModule>

const parseArticle = (path: string, mod: MarkdownModule): NewsArticle | null => {
    const frontmatter = mod.frontmatter ?? {}
    const title = typeof frontmatter.title === 'string' ? frontmatter.title.trim() : ''
    const description = typeof frontmatter.description === 'string' ? frontmatter.description.trim() : ''
    const dateValue = typeof frontmatter.date === 'string' ? frontmatter.date.trim() : ''
    const image = typeof frontmatter.image === 'string' ? frontmatter.image.trim() : ''
    const toastMessage = typeof frontmatter.toast_message === 'string' ? frontmatter.toast_message.trim() : ''
    const showOnNews = Boolean(frontmatter['show-on-news'])

    if (!title || !description || !dateValue) {
        return null
    }

    const parsedDate = new Date(dateValue)
    if (Number.isNaN(parsedDate.getTime())) {
        return null
    }

    const link = path.replace('../docs_src', '').replace(/\.md$/, '')

    return {
        title,
        description,
        link,
        date: dateValue,
        dateTime: parsedDate,
        formattedDate: parsedDate.toISOString().slice(0, 10),
        image,
        toastMessage,
        showOnNews
    }
}

export const useNewsArticles = () => {
    const allArticles = computed(() => {
        const articles: NewsArticle[] = []
        for (const [path, mod] of Object.entries(blogModules)) {
            const article = parseArticle(path, mod)
            if (article) {
                articles.push(article)
            }
        }
        return articles.sort((a, b) => b.dateTime.getTime() - a.dateTime.getTime())
    })

    const newsArticles = computed(() => allArticles.value.filter(article => article.showOnNews && article.image && article.toastMessage))

    const mostRecentNewsArticle = computed(() => newsArticles.value.at(0) ?? null)

    const isMostRecentNewsRecentlyPublished = computed(() => {
        const article = mostRecentNewsArticle.value
        if (!article) {
            return false
        }
        const now = Date.now()
        const articleTime = article.dateTime.getTime()
        if (articleTime > now) {
            return false
        }
        const fourteenDaysMs = 1000 * 60 * 60 * 24 * 14
        return now - articleTime <= fourteenDaysMs
    })

    return {
        allArticles: readonly(allArticles),
        newsArticles: readonly(newsArticles),
        mostRecentNewsArticle,
        isMostRecentNewsRecentlyPublished
    }
}
