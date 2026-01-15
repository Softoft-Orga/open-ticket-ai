import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Navigation schema shared across collections
const navSchema = z
  .object({
    group: z.string().optional(),
    order: z.number().optional(),
    hidden: z.boolean().optional(),
  })
  .optional();

// 1️⃣ docs collection - content collection (MD/MDX)
const docs = defineCollection({
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
// noinspection TypeScriptUnresolvedReference
const blog = defineCollection({
  type: 'content',
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      description: z.string().optional(),
      lang: z.string().default('en'),
      nav: navSchema,
      draft: z.boolean().optional(),
      date: z.date(),
      tags: z.array(z.string()).optional(),
      category: z.string().optional(),
      image: image().optional(),
    }),
});

// 3️⃣ products collection - data collection (YAML)
const products = defineCollection({
  loader: glob({
    base: './src/content/products',
    pattern: '*/products.{yml,yaml}',
  }),
  schema: z.array(
    z.object({
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
    })
  ),
});

// 4️⃣ services collection - data collection (YAML)
const services = defineCollection({
  loader: glob({
    base: './src/content/services',
    pattern: '*/services.{yml,yaml}',
  }),
  schema: z.array(
    z.object({
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
    })
  ),
});

// 5️⃣ site collection - data collection (YAML)
const site = defineCollection({
  loader: glob({
    base: './src/content/site',
    pattern: '*/*.{yml,yaml}',
  }),
  schema: z.object({
    slug: z.string().optional(),
    meta: z.object({
      siteName: z.string(),
      tagline: z.string().optional(),
      logoUrl: z.string().optional(),
    }),
    nav: z.array(
      z.object({
        label: z.string(),
        url: z.string(),
      })
    ),
    footer: z.object({
      brandName: z.string(),
      brandTagline: z.string(),
      socialHeading: z.string(),
      sections: z.array(
        z.object({
          title: z.string(),
          links: z.array(
            z.object({
              label: z.string(),
              url: z.string(),
            })
          ),
        })
      ),
      social: z.array(
        z.object({
          platform: z.string(),
          url: z.string(),
          ariaLabel: z.string(),
        })
      ),
      copyright: z.string(),
    }),
    popularResources: z
      .object({
        title: z.string(),
        groups: z.array(
          z.object({
            title: z.string(),
            basePath: z.string(),
            items: z.array(
              z.object({
                docId: z.string(),
                icon: z.string(),
                label: z.string().optional(),
              })
            ),
          })
        ),
      })
      .optional(),
    legalInfo: z
      .object({
        companyName: z.string(),
        ceo: z.string(),
        address: z.object({
          street: z.string(),
          city: z.string(),
          zip: z.string(),
          country: z.string(),
        }),
        legalForm: z.string(),
        vatId: z.string(),
        registerInfo: z.string(),
        email: z.string(),
        phone: z.string(),
      })
      .optional(),
    team: z
      .array(
        z.object({
          name: z.string().optional(),
          role: z.string().optional(),
          pictureUrl: z.string().optional(),
          email: z.string().optional(),
          phoneNumber: z.string().optional(),
        })
      )
      .optional(),
    dataPrivacy: z
      .object({
        introduction: z.string(),
        controller: z.object({
          title: z.string(),
          content: z.string(),
        }),
        dataProcessing: z.object({
          title: z.string(),
          categories: z.array(
            z.object({
              title: z.string(),
              description: z.string(),
              legalBasis: z.string().optional(),
            })
          ),
        }),
        yourRights: z.object({
          title: z.string(),
          rights: z.array(
            z.object({
              title: z.string(),
              description: z.string(),
            })
          ),
        }),
        dataSecurity: z.object({
          title: z.string(),
          content: z.string(),
        }),
        thirdPartyServices: z
          .object({
            title: z.string(),
            services: z.array(
              z.object({
                name: z.string(),
                purpose: z.string(),
                provider: z.string().optional(),
                privacyPolicy: z.string().optional(),
              })
            ),
          })
          .optional(),
        contact: z.object({
          title: z.string(),
          content: z.string(),
        }),
        lastUpdated: z.string(),
      })
      .optional(),
  }),
});

// Export collections
export const collections = {
  docs,
  blog,
  services,
  products,
  site,
};
