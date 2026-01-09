// Mock blog posts data for Storybook
// This is a placeholder to satisfy imports in the useNewsArticles composable
// In production, this data is typically populated from your CMS or data source
export interface BlogPost {
    title: string
    description: string
    url: string
    date: string
    image?: string
    toast_message?: string
    'show-on-news'?: boolean
}

// Empty array - add sample blog posts here if needed for Storybook stories
export const data: BlogPost[] = []

export default data
