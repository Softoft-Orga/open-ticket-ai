import {createContentLoader} from 'vitepress'

export interface BlogPostData {
    title: string
    description: string
    date: string
    url: string
    image?: string
    toast_message?: string
    'show-on-news'?: boolean
}

declare const data: BlogPostData[]
export {data}

export default createContentLoader('docs_src/en/blog/**/*.md', {
    transform(raw): BlogPostData[] {
        return raw
            .map(({url, frontmatter}) => ({
                title: frontmatter.title || '',
                description: frontmatter.description || '',
                date: frontmatter.date || '',
                url,
                image: frontmatter.image,
                toast_message: frontmatter.toast_message,
                'show-on-news': frontmatter['show-on-news']
            }))
            .filter(post => post.title && post.description && post.date)
            .sort((a, b) => +new Date(b.date) - +new Date(a.date))
    }
})

