import { createContentLoader } from 'vitepress'

export interface BlogPostData {
    url: string
    title: string
    description: string
    date: string
    image?: string
    toast_message?: string
    'show-on-news'?: boolean
}

declare const data: BlogPostData[]
export { data }

export default createContentLoader('en/blog/**/*.md', {
    transform(raw): BlogPostData[] {
        return raw
            .map(({ url, frontmatter }) => ({
                url,
                title: frontmatter.title || '',
                description: frontmatter.description || '',
                date: frontmatter.date || '',
                image: frontmatter.image,
                toast_message: frontmatter.toast_message,
                'show-on-news': frontmatter['show-on-news']
            }))
            .sort((a, b) => {
                const dateA = new Date(a.date).getTime()
                const dateB = new Date(b.date).getTime()
                // Handle invalid dates by treating them as oldest
                if (isNaN(dateA) && isNaN(dateB)) return 0
                if (isNaN(dateA)) return 1
                if (isNaN(dateB)) return -1
                return dateB - dateA
            })
    }
})
