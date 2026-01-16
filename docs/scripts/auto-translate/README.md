# Auto-Translate Tool for Astro Docs

A Python tool that automatically translates Astro documentation trees (including `.astro`, `.yml/.yaml`, `.md`, `.mdx` files) into locale directories while preserving the relative structure.

## Features

- **Recursive translation**: Walks source directories and translates all supported files
- **Structure preservation**: Maintains exact relative paths in target directory
- **File type awareness**: Uses different translation prompts for Astro, YAML, Markdown, and MDX files
- **Concurrent processing**: Translates multiple files in parallel with configurable concurrency
- **Retry logic**: Exponential backoff for API failures
- **Smart skipping**: Skips existing files unless `--force` is used
- **Customizable prompts**: Uses Jinja2 templates for flexible prompt engineering

## Requirements

Dependencies (install via `pip` or `uv`):
- `openai` - OpenAI Python SDK for Chat Completions API
- `tenacity` - Retry library with exponential backoff
- `jinja2` - Template engine for prompts
- `pyyaml` - YAML configuration parser
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support (for tests only)

Install dependencies:
```bash
pip install openai tenacity jinja2 pyyaml pytest pytest-asyncio
```

## Usage

### Basic Usage

1. **Create a configuration file** (see `translate.config.yml` for example):

```yaml
mappings:
  - from_dir: /docs/src/pages/en
    to_dir: /docs/src/pages/de

include_ext:
  - .astro
  - .md
  - .yml

exclude_dir_names:
  - node_modules
  - .git

prompt_template_path: prompt.j2
base_language: English
target_language: German
model: gpt-4
temperature: 0.3
max_concurrency: 5
```

2. **Set your OpenAI API key** (or use `--api-key` flag):

```bash
export OPENAI_API_KEY="sk-..."
```

3. **Run the translator**:

```bash
python translate_tree.py --config translate.config.yml
```

### Command Line Options

```bash
python translate_tree.py --config CONFIG [--api-key KEY] [--base-url URL] [--force]
```

- `--config`: Path to configuration YAML file (required)
- `--api-key`: OpenAI API key (optional, uses `OPENAI_API_KEY` env var if not provided)
- `--base-url`: OpenAI base URL (optional, for using OpenRouter or custom endpoints)
- `--force`: Overwrite existing translated files

### Using with OpenRouter

To use OpenRouter instead of OpenAI:

```bash
export OPENAI_API_KEY="sk-or-v1-..."
export OPENAI_BASE_URL="https://openrouter.ai/api/v1"

python translate_tree.py --config translate.config.yml
```

Or use command line flags:

```bash
python translate_tree.py \
  --config translate.config.yml \
  --api-key "sk-or-v1-..." \
  --base-url "https://openrouter.ai/api/v1"
```

## Configuration

### Config File Structure

```yaml
# Directory mappings (source → target)
mappings:
  - from_dir: /path/to/source
    to_dir: /path/to/target

# File extensions to include
include_ext:
  - .astro
  - .yml
  - .yaml
  - .md
  - .mdx

# Directories to skip
exclude_dir_names:
  - node_modules
  - .git
  - dist
  - build

# Prompt template path (relative to config file)
prompt_template_path: prompt.j2

# Translation settings
base_language: English
target_language: German

# OpenAI API settings
model: gpt-4
temperature: 0.3

# Concurrency (parallel requests)
max_concurrency: 5
```

### Prompt Template

The `prompt.j2` file uses Jinja2 conditionals to customize instructions per file type:

```jinja2
{% if file_type == "astro" %}
Rules for Astro files:
- Preserve frontmatter and all code exactly
- Translate only visible text content
{% elif file_type == "yaml" %}
Rules for YAML files:
- Do NOT translate keys
- Translate only string values
{% endif %}
```

Variables available in template:
- `file_type`: "astro", "yaml", "markdown", or "mdx"
- `base_language`: Source language name
- `target_language`: Target language name

## Testing

Run tests with pytest:

```bash
pytest tests/
```

All tests use mocked OpenAI client and require no API keys. Tests verify:

1. **Relative path preservation**: Nested directory structure is maintained
2. **Force flag behavior**: Existing files are skipped unless `--force` is used
3. **Extension filtering**: Only supported file types are translated
4. **Directory exclusion**: Configured directories (e.g., `node_modules`) are skipped
5. **Prompt rendering**: Different prompts are used for different file types
6. **Concurrent execution**: Multiple files are processed in parallel
7. **Parent directory creation**: Missing directories are created automatically

## Architecture

### Class Design

**Config** (dataclass):
- Loads settings from YAML
- Validates paths and extensions
- Provides defaults

**TreeTranslator**:
- Accepts AsyncOpenAI client via dependency injection (for testing)
- Renders Jinja2 prompt template per file type
- Walks source directories with pathlib
- Filters files by extension and excluded directories
- Translates files concurrently with asyncio.Semaphore
- Retries API calls with tenacity
- Writes output preserving relative paths

### File Type Detection

Supported extensions map to file types:
- `.astro` → "astro"
- `.yml`, `.yaml` → "yaml"
- `.md` → "markdown"
- `.mdx` → "mdx"

Each file type receives a different system prompt via template conditionals.

## Translation Behavior

### Output Rules (enforced via prompt)

- **Astro files**: Preserve frontmatter and code; translate only visible text
- **YAML files**: Preserve keys and structure; translate only string values
- **Markdown files**: Preserve code blocks and syntax; translate prose only
- **MDX files**: Preserve JSX and code; translate text content

### Preserved Elements

Never translated:
- URLs and file paths
- Code blocks and inline code
- Variable names and identifiers
- HTML/JSX tags and attributes
- Configuration keys (YAML)

## Examples

### Example: Translate English docs to German

```bash
python translate_tree.py --config translate.config.yml
```

Before:
```
/docs/src/pages/en/
  ├── index.astro
  ├── docs/
  │   ├── guide.md
  │   └── config.yml
```

After:
```
/docs/src/pages/de/
  ├── index.astro       # Translated
  ├── docs/
  │   ├── guide.md      # Translated
  │   └── config.yml    # Translated
```

### Example: Translate with custom model

```yaml
model: gpt-3.5-turbo
temperature: 0.2
```

### Example: Multiple mappings

```yaml
mappings:
  - from_dir: /docs/src/pages/en
    to_dir: /docs/src/pages/de
  - from_dir: /docs/src/pages/en
    to_dir: /docs/src/pages/fr
  - from_dir: /docs/src/content/en
    to_dir: /docs/src/content/de
```

## License

Part of the Open Ticket AI project.
