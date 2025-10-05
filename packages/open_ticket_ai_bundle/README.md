# Open Ticket AI Bundle

This is a meta-package that installs a tested, compatible set of Open Ticket AI packages.

## What's Included

- **open-ticket-ai** - Core package (1.0.0rc1)
- **open-ticket-ai-hf-local** - HuggingFace local inference plugin (1.0.0rc1)
- **open-ticket-ai-otobo-znuny-plugin** - OTOBO/Znuny integration plugin (1.0.0rc1)

## Installation

```bash
pip install open-ticket-ai-bundle
```

This is equivalent to:

```bash
pip install open-ticket-ai==1.0.0rc1 \
    open-ticket-ai-hf-local==1.0.0rc1 \
    open-ticket-ai-otobo-znuny-plugin==1.0.0rc1
```

## Why Use the Bundle?

The bundle provides:

1. **Guaranteed Compatibility**: All packages are tested together and known to work
2. **Simplified Installation**: One command installs everything
3. **Version Consistency**: Ensures compatible versions across the ecosystem

## Individual Installation

You can also install packages individually:

```bash
# Core only
pip install open-ticket-ai

# Core + specific plugins
pip install open-ticket-ai open-ticket-ai-hf-local
```

## Version Policy

The bundle version tracks the Core version and pins all plugins to tested versions. When the Core or plugins are updated, a new bundle version is released with the updated compatible set.

## License

LGPL-2.1-only

## Links

- **Homepage**: https://open-ticket-ai.com
- **Repository**: https://github.com/Softoft-Orga/open-ticket-ai
- **Documentation**: https://open-ticket-ai.com
