import { defineCollection, z } from 'astro:content';
import { file } from 'astro/loaders';

// Navigation schema shared across collections
const navSchema = z.object({
  group: z.string().optional(),
  order: z.number().optional(),
  hidden: z.boolean().optional(),
}).optional();

// 1️⃣ docs collection - content collection (MD/MDX)
const docsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    lang: z.string().default('en'),
    nav: navSchema,
    draft: z.boolean().optional(),
  }),
});

// 2️⃣ blog collection - content collection (MD/MDX)
const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    lang: z.string().default('en'),
    nav: navSchema,
    draft: z.boolean().optional(),
    date: z.date(),
    tags: z.array(z.string()).optional(),
    category: z.string().optional(),
  }),
});

// 3️⃣ products collection - data collection (YAML)
const productsCollection = defineCollection({
  loader: file('src/content/products.yaml'),
  schema: z.object({
    slug: z.string(),
    title: z.string(),
    tagline: z.string().optional(),
    description: z.string().optional(),
    features: z.array(z.string()).optional(),
    tier: z.enum(['lite', 'pro', 'enterprise']).optional(),
    lang: z.string().default('en'),
    nav: navSchema,
    status: z.string().optional(),
    badges: z.array(z.string()).optional(),
    image: z.string().optional(),
    icon: z.string().optional(),
  }),
});

// 4️⃣ services collection - data collection (YAML)
const servicesCollection = defineCollection({
  loader: file("src/content/services.yaml"),
  schema: z.object({
    slug: z.string(),
    title: z.string(),
    oneLiner: z.string().optional(),
    description: z.string().optional(),
    outcomes: z.array(z.string()).optional(),
    startingPrice: z.number().optional(),
    lang: z.string().default('en'),
    serviceGroup: z.string(),
    serviceOrder: z.number().optional(),
    hidden: z.boolean().optional(),
  }),
});

// 5️⃣ site collection - data collection (YAML)
const siteCollection = defineCollection({
  loader: file("src/content/site.yml"),
  schema: z.object({
    slug: z.string(),
    meta: z.object({
      siteName: z.string(),
      tagline: z.string().optional(),
      logoUrl: z.string().optional(),
    }),
    nav: z.array(z.object({
      label: z.string(),
      url: z.string(),
    })),
    footer: z.object({
      sections: z.array(z.object({
        title: z.string(),
        links: z.array(z.object({
          label: z.string(),
          url: z.string(),
        })),
      })),
      social: z.array(z.object({
        platform: z.string(),
        url: z.string(),
        ariaLabel: z.string(),
      })),
      legal: z.array(z.object({
        label: z.string(),
        url: z.string(),
      })),
      copyright: z.string(),
    }),
  }),
});

// Export collections
export const collections = {
  docs: docsCollection,
  blog: blogCollection,
  products: productsCollection,
  services: servicesCollection,
  site: siteCollection,
};
