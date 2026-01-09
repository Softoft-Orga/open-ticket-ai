# Component Usage Guide

This guide provides examples for using the documentation and blog components in your pages.

## Documentation Components

### Alert

Display important information, warnings, tips, or success messages in documentation.

```vue
<!-- Info alert -->
<Alert type="info" title="Information">
  This is helpful context for the reader.
</Alert>

<!-- Success alert -->
<Alert type="success" title="Success">
  Your operation completed successfully!
</Alert>

<!-- Warning alert -->
<Alert type="warning" title="Warning">
  Please be careful when performing this operation.
</Alert>

<!-- Danger alert -->
<Alert type="danger" title="Danger">
  This action cannot be undone.
</Alert>

<!-- Tip alert -->
<Alert type="tip" title="Pro Tip">
  Use keyboard shortcuts to navigate faster!
</Alert>

<!-- Alert without title or icon -->
<Alert type="info" hideIcon>
  Simple message without icon.
</Alert>
```

### CodeBlock

Display code snippets with syntax highlighting and a copy button.

```vue
<!-- With language and title -->
<CodeBlock language="javascript" title="Example Script">
const greeting = 'Hello, World!';
console.log(greeting);
</CodeBlock>

<!-- Simple code block -->
<CodeBlock>
npm install open-ticket-ai
npm start
</CodeBlock>

<!-- Python example -->
<CodeBlock language="python">
def hello_world():
    print("Hello, World!")
</CodeBlock>
```

### CodeTabs

Display multiple code examples in different languages or formats using tabs.

```vue
<CodeTabs :tabs="['JavaScript', 'Python', 'Go']">
  <template #tab-0>
    <pre>const api = new OpenTicketAI({
  apiKey: 'your-api-key'
});</pre>
  </template>
  <template #tab-1>
    <pre>api = OpenTicketAI(api_key='your-api-key')</pre>
  </template>
  <template #tab-2>
    <pre>api := openticketai.New("your-api-key")</pre>
  </template>
</CodeTabs>
```

### StepIndicator

Show progress through multi-step processes or tutorials.

```vue
<StepIndicator 
  :steps="['Install', 'Configure', 'Deploy', 'Monitor']" 
  :currentStep="2" 
/>
```

### TableOfContents

Auto-generated table of contents with scroll tracking.

```vue
<TableOfContents 
  :headings="[
    { id: 'introduction', text: 'Introduction', level: 2 },
    { id: 'getting-started', text: 'Getting Started', level: 2 },
    { id: 'installation', text: 'Installation', level: 3 },
    { id: 'configuration', text: 'Configuration', level: 3 }
  ]" 
/>
```

## Blog Components

### AuthorBio

Display author information at the end of blog posts.

```vue
<AuthorBio
  name="Sarah Johnson"
  role="Senior AI Engineer"
  bio="Sarah is a passionate AI engineer with over 10 years of experience..."
  avatar="https://example.com/avatar.jpg"
  :social="{
    twitter: 'https://twitter.com/sarahjohnson',
    github: 'https://github.com/sarahjohnson',
    linkedin: 'https://linkedin.com/in/sarahjohnson'
  }"
/>
```

### ReadingTime

Show estimated reading time based on article content.

```vue
<ReadingTime :text="articleContent" />

<!-- Custom reading speed -->
<ReadingTime :text="articleContent" :wordsPerMinute="150" />
```

### ShareButtons

Enable readers to share articles on social media.

```vue
<ShareButtons 
  title="How to Build AI-Powered Support Automation"
  url="https://openticketai.com/blog/ai-support-automation"
/>

<!-- Uses current page URL if not specified -->
<ShareButtons title="My Article Title" />
```

### RelatedPosts

Display related articles at the end of blog posts.

```vue
<RelatedPosts 
  :posts="[
    {
      title: 'Getting Started with AI',
      description: 'Learn the basics...',
      category: 'Tutorial',
      date: 'Jan 5, 2024',
      image: 'https://example.com/image.jpg',
      href: '/blog/getting-started'
    },
    // More posts...
  ]"
/>
```

### TagFilter

Filter content by tags or categories.

```vue
<script setup>
import { ref } from 'vue'
const selectedTags = ref(['AI/ML', 'Automation'])
</script>

<TagFilter 
  :tags="['AI/ML', 'Automation', 'Support', 'Engineering']"
  v-model="selectedTags"
/>
```

## Using in Astro Pages

Import and use these components in your Astro pages:

```astro
---
import Alert from '../components/vue/docs/Alert.vue'
import CodeBlock from '../components/vue/docs/CodeBlock.vue'
import AuthorBio from '../components/vue/blog/AuthorBio.vue'
---

<Alert client:load type="info" title="Note">
  These components work seamlessly in Astro!
</Alert>

<CodeBlock client:load language="bash">
npm install
</CodeBlock>

<AuthorBio 
  client:load
  name="John Doe"
  bio="Content creator"
/>
```

## Using in MDX

You can also use these in MDX content files:

```mdx
import { Alert } from '@/components/vue/docs/Alert.vue'

# My Documentation

<Alert type="tip" title="Pro Tip">
  This is an inline alert in MDX!
</Alert>
```

## Styling

All components use the existing design system tokens:

- Colors: `primary`, `background-dark`, `surface-dark`, `text-dim`
- Border radius: `rounded-xl`, `rounded-2xl`
- Spacing: Consistent padding and margins
- Icons: Material Symbols

Components automatically adapt to the dark theme used throughout the site.
