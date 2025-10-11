# VitePress Documentation Setup

**Note**: This project uses **VitePress**, not Jekyll, for its documentation website.

## Overview

Open Ticket AI uses VitePress as its static site generator for documentation. VitePress is a modern, fast, and Vue-powered static site generator designed for technical documentation.

## Documentation Structure

### Primary Documentation Source

- **Location**: `docs/raw_en_docs/`
- **Purpose**: Authoritative English documentation in Markdown format
- **Content**: User guides, configuration examples, API references

### VitePress Website

- **Location**: `docs/vitepress_docs/`
- **Purpose**: Multi-lingual documentation website
- **Deployment**: Hosted at https://open-ticket-ai.com via Netlify

## Directory Layout

```
docs/
├── raw_en_docs/               # Primary English documentation source
│   ├── README.md              # Main project README
│   ├── config_examples/       # YAML configuration examples
│   ├── general/               # General guides and setup
│   └── ...                    # Other documentation sections
│
└── vitepress_docs/            # VitePress website source
    ├── .vitepress/            # VitePress configuration
    │   ├── config.mts         # Main VitePress config
    │   ├── theme/             # Custom theme components
    │   └── components/        # Vue components
    ├── docs_src/              # Multi-lingual content
    │   ├── en/                # English (primary)
    │   ├── de/                # German
    │   ├── es/                # Spanish
    │   └── fr/                # French
    ├── package.json           # Node.js dependencies
    └── netlify.toml           # Netlify deployment config
```

## Local Development

### Prerequisites

- Node.js 18+ (recommended: Node.js 20)
- npm or yarn package manager

### Setup Instructions

1. **Navigate to the VitePress directory**:
   ```bash
   cd docs/vitepress_docs
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run docs:dev
   ```

4. **Access the local site**:
   Open your browser to `http://localhost:5173`

### Development Commands

```bash
# Start dev server with hot reload
npm run docs:dev

# Build for production
npm run docs:build

# Preview production build locally
npm run docs:preview

# Run Storybook for component development
npm run storybook

# Build Storybook
npm run build-storybook
```

## Configuration

### Main Configuration File

**Location**: `docs/vitepress_docs/.vitepress/config.mts`

Key configuration options:

```typescript
export default defineConfig({
  title: 'Open Ticket AI',
  srcDir: './docs_src',
  appearance: 'force-dark',
  
  locales: {
    root: {
      label: 'English',
      lang: 'en',
      link: '/en/',
      // ...theme config
    },
    de: { /* German config */ },
    es: { /* Spanish config */ },
    fr: { /* French config */ }
  },
  
  // SEO and site metadata
  sitemap: {
    hostname: 'https://open-ticket-ai.com',
  }
})
```

### Theme Configuration

The VitePress theme uses:
- **Dark mode**: Force dark appearance
- **Custom components**: Vue components in `.vitepress/components/`
- **Tailwind CSS**: For styling (configured in `tailwind.config.cjs`)
- **Mermaid diagrams**: For flowcharts and diagrams

### Navigation Generation

Navigation is auto-generated using a custom NavGenerator utility:

```typescript
const navGenerator = new NavGenerator(navGeneratorOptions);

// Generates navbar and sidebar from directory structure
nav: navGenerator.generateNavbar('en'),
sidebar: navGenerator.generateSidebar("en")
```

## Multi-Language Support

### Supported Languages

- **English (EN)**: Primary language, located at `/en/`
- **German (DE)**: Located at `/de/`
- **Spanish (ES)**: Located at `/es/`
- **French (FR)**: Located at `/fr/`

### Adding Content in Multiple Languages

1. **Edit English version first**: `docs_src/en/your-page.md`
2. **Translate to other languages**: 
   - `docs_src/de/your-page.md`
   - `docs_src/es/your-page.md`
   - `docs_src/fr/your-page.md`
3. **Update i18n messages**: Edit `messages.ts` files in each language directory

### Language Switching

The site includes an automatic language switcher. Users are redirected to their preferred language based on browser settings (configured in `netlify.toml`).

## Deployment

### Netlify Deployment

The documentation is automatically deployed to Netlify when changes are pushed to the repository.

**Configuration**: `netlify.toml` (root of repository)

```toml
[build]
base = "docs/vitepress_docs"
command = "npm run docs:build"
publish = ".vitepress/dist"
```

### Build Process

1. **Trigger**: Push to main/dev branch
2. **Build**: Netlify runs `npm run docs:build`
3. **Output**: Static files generated in `.vitepress/dist`
4. **Deploy**: Files published to https://open-ticket-ai.com

### Environment Variables

No special environment variables are required for basic deployment. The site uses:
- Google Analytics tracking ID (embedded in config)
- Netlify Functions for API endpoints (optional)

## Content Guidelines

### Creating New Pages

1. **Choose the appropriate directory**:
   - User guides → `docs_src/en/guide/`
   - Developer docs → `docs_src/en/developers/`
   - Blog posts → `docs_src/en/blog/`

2. **Create Markdown file**:
   ```markdown
   ---
   title: Your Page Title
   description: Brief description for SEO
   ---
   
   # Your Page Title
   
   Content goes here...
   ```

3. **Add to navigation** (if using manual nav):
   Edit `.vitepress/config.mts` or rely on auto-generation

### Markdown Features

VitePress supports:
- **Standard Markdown**: Headings, lists, code blocks, links
- **Vue components**: Embed custom components in Markdown
- **Code highlighting**: Syntax highlighting for 100+ languages
- **Mermaid diagrams**: Flowcharts, sequence diagrams, etc.
- **Custom containers**: Info, warning, danger, tip boxes

Example with custom container:
```markdown
::: tip
This is a helpful tip for users.
:::

::: warning
This is a warning about potential issues.
:::
```

### Code Examples

Use fenced code blocks with language specification:

```yaml
# Configuration example
orchestrator:
  pipelines:
    - name: classify_tickets
      run_every_milli_seconds: 60000
```

## Syncing Documentation

### From raw_en_docs to VitePress

When updating documentation:

1. **Edit source**: Make changes in `docs/raw_en_docs/`
2. **Sync to VitePress**: Copy/adapt content to `docs/vitepress_docs/docs_src/en/`
3. **Maintain consistency**: Ensure both sources are aligned

### Configuration Examples

Configuration examples in `docs/raw_en_docs/config_examples/` can be referenced or imported into VitePress pages:

```markdown
<<< @/../../raw_en_docs/config_examples/queue_classification.yml
```

## Troubleshooting

### Build Failures

**Issue**: Build fails with module errors
- **Solution**: Run `npm install` to ensure all dependencies are installed

**Issue**: Outdated dependencies
- **Solution**: Run `npm update` or update `package.json`

### Development Server Issues

**Issue**: Port 5173 already in use
- **Solution**: Kill the process using the port or use a different port:
  ```bash
  npm run docs:dev -- --port 5174
  ```

**Issue**: Hot reload not working
- **Solution**: Restart the dev server or clear VitePress cache:
  ```bash
  rm -rf docs/vitepress_docs/.vitepress/cache
  ```

### Navigation Not Updating

**Issue**: New pages don't appear in sidebar
- **Solution**: 
  - Check file naming matches NavGenerator patterns
  - Restart dev server
  - Verify file is in correct language directory

## Advanced Topics

### Custom Components

Add Vue components to `.vitepress/components/` and use them in Markdown:

```vue
<!-- .vitepress/components/MyComponent.vue -->
<template>
  <div class="my-component">
    <slot />
  </div>
</template>
```

Use in Markdown:
```markdown
<MyComponent>
  Custom content here
</MyComponent>
```

### Theme Customization

Customize the theme by editing files in `.vitepress/theme/`:
- `Layout.vue`: Main layout component
- `style.css`: Global styles
- `index.ts`: Theme configuration

### Analytics

Google Analytics is configured in `.vitepress/config.mts`:
- Main tracking: Google Tag Manager (AW-474755810)
- Analytics: GA4 (G-FBWC3JDZJ4)

## Resources

- **VitePress Documentation**: https://vitepress.dev/
- **Vue.js**: https://vuejs.org/
- **Tailwind CSS**: https://tailwindcss.com/
- **Mermaid**: https://mermaid.js.org/

## Getting Help

- **Documentation Issues**: Open an issue on GitHub
- **VitePress Questions**: See VitePress official docs
- **Project Questions**: Check `docs/AGENTS.md` for AI agent guidelines

## Migration Notes

**Previous Documentation System**: This project previously did not use any static site generator. VitePress was chosen for its:
- Modern, fast build system
- Excellent Vue integration
- Multi-language support
- Developer-friendly experience
- Great documentation and community

**Note**: This project has **never used Jekyll**. If you encounter references to Jekyll in old issues or documentation, they are incorrect or outdated.
