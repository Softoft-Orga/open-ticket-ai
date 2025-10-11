export interface Feature {
    text: string
    icon: string
}

export interface Product {
    name: string
    price: number
    pricePeriod?: string
    description: string
    features: Feature[]
}
