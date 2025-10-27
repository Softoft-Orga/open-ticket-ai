import {computed, readonly} from 'vue'
import {data as blogPosts} from '../data/blogPosts.data.mts'

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

export const useNewsArticles = () => {
    const allArticles = computed(() => {
        return blogPosts
            .filter(post => post.date) // Filter out posts without a date
            .map(post => {
                const dateTime = new Date(post.date)
                return {
                    title: post.title,
                    description: post.description,
                    link: post.url,
                    date: post.date,
                    dateTime,
                    formattedDate: dateTime.toISOString().slice(0, 10),
                    image: post.image || '',
                    toastMessage: post.toast_message || '',
                    showOnNews: post['show-on-news'] || false
                }
            })
    })

    const newsArticles = computed(() =>
        allArticles.value.filter(article =>
            article.showOnNews && article.image && article.toastMessage && !isNaN(article.dateTime.getTime())
        )
    )

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

