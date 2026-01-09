// Mock blog posts data for Storybook
export interface BlogPost {
    title: string
    description: string
    url: string
    date: string
    image?: string
    toast_message?: string
    'show-on-news'?: boolean
}

export const data: BlogPost[] = []

export default data
