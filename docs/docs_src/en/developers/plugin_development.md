---
description: Complete guide to developing custom plugins for Open Ticket AI including project structure, entry points, and best practices.
---

# Plugin Development Guide

Learn how to create custom plugins to extend Open Ticket AI functionality.

<InlineExample slug="basics-minimal" />

## Packaging & Naming Requirements

Open Ticket AI discovers plugins by their Python package name and project metadata.

- **Distribution/project name**: must start with `otai-`. This matches the
  `AppConfig.PLUGIN_NAME_PREFIX` (`otai-`) that the runtime uses when computing registry keys.
- **Python package name**: use the same words as the distribution name but with underscores (
  `otai_my_plugin`). The loader converts the top-level module name to kebab-case automatically, so
  `otai_my_plugin` becomes `otai-my-plugin` internally.
- **Registry prefix**: when a plugin registers injectables it strips the global prefix (`otai-`) and
  keeps the remainder (e.g. `otai-my-plugin` → `my-plugin`). That portion becomes the registry key
  prefix when combined with the injectable name, such as `my-plugin:MyPipe`.

## Recommended Project Layout

```
otai-my-plugin/
├── pyproject.toml
├── src/
│   └── otai_my_plugin/
│       ├── __init__.py
│       ├── pipes/
│       │   └── my_pipe.py
│       ├── services/
│       │   └── my_service.py
│       └── plugin_factory.py
└── tests/
    └── unit/
        └── test_my_plugin.py
```

## Entry Point Contract

Open Ticket AI loads plugins via the `open_ticket_ai.plugins` entry-point group. The entry point
must resolve to a callable that accepts an `AppConfig` instance and returns a `Plugin`. Subclassing
`Plugin` already satisfies that contract, so expose your subclass directly.

```toml
[project.entry-points."open_ticket_ai.plugins"]
my_plugin = "otai_my_plugin.plugin_factory:PluginFactory"
```

### Why reference the class?

- The loader invokes the target like a factory. Referencing the subclass keeps the wiring
  declarative—no wrapper function required.
- The class name clarifies that instantiating the plugin may involve dependency wiring (for example,
  constructor parameters beyond `AppConfig` can be injected by the IoC container).

## Implementing the PluginFactory Class

All plugins inherit from `open_ticket_ai.core.plugins.plugin.Plugin`. The base class:

1. Accepts `AppConfig` (injected by the loader) in its constructor.
2. Uses the top-level module name to infer the plugin name and registry prefix.
3. Calls `_get_all_injectables()` during `on_load` and registers each `Injectable` automatically
   with the `ComponentRegistry` using the pattern `<plugin-prefix>:<injectable-registry-name>`.

The separator between the prefix and the injectable name is
`AppConfig.REGISTRY_IDENTIFIER_SEPERATOR`, which defaults to `:`.

Override `_get_all_injectables()` to return every injectable you want to expose. You should **not**
call `registry.register(...)` yourself inside `on_load`; the base class does it for you.

```python
# src/otai_my_plugin/plugin_factory.py

from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.plugins.plugin import Plugin

from otai_my_plugin.pipes.my_pipe import MyPipe
from otai_my_plugin.services.my_service import MyService


class PluginFactory(Plugin):
    """Create the plugin instance and declare exported injectables."""

    def _get_all_injectables(self) -> list[type[Injectable]]:
        return [
            MyPipe,
            MyService,
        ]
```

When the loader instantiates `PluginFactory`, the base implementation will:

1. Compute the registry prefix (`my-plugin` in this example).
2. Call `MyPipe.get_registry_name()` and `MyService.get_registry_name()`.
3. Register each injectable as `my-plugin:<registry-name>` with the shared `ComponentRegistry`.

### Returning Injectables vs Manual Registration

Prior implementations required a `setup(registry)` helper that performed manual registration. With
the factory pattern above you simply return the list of injectables and let the base class handle
the rest. This keeps registration consistent and ensures registry names follow the
`prefix:Injectable` convention automatically.

If you do need to opt out of the automatic behaviour—for example, to register additional aliases—you
can still access the registry inside `_get_all_injectables()` by overriding `on_load`. For typical
use cases, returning the list is sufficient and preferred.

## pyproject.toml Essentials

Ensure the metadata aligns with the naming rules and entry-point contract:

```toml
[project]
name = "otai-my-plugin"
version = "0.1.0"
description = "Custom plugin for Open Ticket AI"
requires-python = ">=3.13"
dependencies = [
    "open-ticket-ai>=1.0.0,<2.0.0",
]

[project.entry-points."open_ticket_ai.plugins"]
my_plugin = "otai_my_plugin.plugin_factory:PluginFactory"
```

Use the distribution name (`otai-my-plugin`) to derive both the module prefix (`otai_my_plugin`) and
registry prefix (`my-plugin`). Keeping these consistent ensures the loader resolves entry points
correctly and produces predictable registry keys.

## Packaging, Distribution & Testing

```
uv build
uv publish
```

Install your plugin into an Open Ticket AI environment with:

```
uv pip install otai-my-plugin
```

Write unit tests alongside your plugin code under `tests/unit/` and run them with
`uv run -m pytest`.

## Commercial Plugins & Monetization

Open Ticket AI fully supports **commercial plugin development** with complete licensing freedom. You
can create and sell plugins with no restrictions from the core project.

### Developer Freedom

- **Choose your license**: MIT, GPL, proprietary—your choice
- **Set your pricing**: Free, paid, subscription, one-time—you decide
- **Support model**: Community support, commercial support, or both
- **No revenue sharing**: Keep 100% of your plugin sales
- **No marketplace fees**: Currently no official marketplace (coming soon)

### Current Status & Future Plans

- **Plugin Listings**: Available on the documentation site
- **No Marketplace Yet**: There is currently no official plugin marketplace or store
- **Future Plans**: A dedicated plugins showcase page is planned with search, categories, and
  community ratings

### Monetization Strategies

#### Strategy 1: Private PyPI + License Keys

Host your commercial plugin on a private PyPI server (DevPI, Gemfury, AWS CodeArtifact) that
customers access with authentication tokens. Implement license validation in your plugin's
initialization:

```python
import os
from open_ticket_ai.core.plugins.plugin import Plugin
from open_ticket_ai.core.injectables.injectable import Injectable


class LicenseError(Exception):
    """Raised when license validation fails."""
    pass


class MyCommercialPlugin(Plugin):
    """Commercial plugin with license validation."""

    def __init__(self, config):
        # Validate license before plugin initialization
        license_key = os.getenv('MY_PLUGIN_LICENSE_KEY')
        if not license_key or not self._validate_license(license_key):
            raise LicenseError(
                "Valid license key required. "
                "Visit https://myplugin.com for licensing."
            )
        super().__init__(config)

    def _validate_license(self, key: str) -> bool:
        """
        Implement your license validation logic.
        Examples:
        - API call to license server
        - Signature verification
        - Offline validation with cryptographic signatures
        """
        # Your validation logic here
        return self._verify_with_license_server(key)

    def _verify_with_license_server(self, key: str) -> bool:
        """Validate license key against remote server."""
        # Example implementation
        import requests
        try:
            response = requests.post(
                'https://api.myplugin.com/validate',
                json={'license_key': key},
                timeout=5
            )
            return response.status_code == 200 and response.json().get('valid')
        except Exception:
            # Consider grace period for network failures
            return False

    def _get_all_injectables(self) -> list[type[Injectable]]:
        return [MyService, MyPipe]
```

**Benefits:**

- Full control over distribution
- Secure plugin delivery
- Customer-specific authentication
- Private code repository

**Drawbacks:**

- Requires maintaining private PyPI infrastructure
- More complex installation for customers
- Less discoverable

#### Strategy 2: Public PyPI + Runtime License Enforcement

Publish your plugin to public PyPI for easy discovery, but implement runtime license validation.
Installation is free, but usage requires a valid license:

```python
import os
from open_ticket_ai.core.plugins.plugin import Plugin
from open_ticket_ai.core.injectables.injectable import Injectable


class LicenseError(Exception):
    """Raised when license validation fails."""
    pass


class PublicCommercialPlugin(Plugin):
    """Publicly available plugin with runtime license enforcement."""

    def _get_all_injectables(self) -> list[type[Injectable]]:
        """Validate license before exposing injectables."""
        license_key = os.getenv('MY_PLUGIN_LICENSE_KEY')

        if not license_key:
            raise LicenseError(
                "License key required to use this plugin.\n"
                "Set the MY_PLUGIN_LICENSE_KEY environment variable.\n"
                "Purchase a license at https://myplugin.com"
            )

        if not self._verify_license(license_key):
            raise LicenseError(
                "Invalid or expired license key.\n"
                "Visit https://myplugin.com to renew or purchase a license."
            )

        return [MyService, MyPipe]

    def _verify_license(self, key: str) -> bool:
        """Your license verification logic."""
        # Example: Check license format, expiration, signature
        return self._check_license_signature(key)

    def _check_license_signature(self, key: str) -> bool:
        """Verify license key signature (example)."""
        # Implement cryptographic signature verification
        # This allows offline validation
        return True  # Replace with actual verification
```

**Benefits:**

- Easy installation via `uv add otai-my-plugin`
- Public discovery on PyPI
- Simple customer onboarding
- Trial versions possible (e.g., time-limited grace period)

**Drawbacks:**

- Plugin code is publicly visible
- Potential for license bypass attempts
- Requires robust license validation

#### Strategy 3: Freemium Model

Offer a free tier with basic features and charge for premium functionality:

```python
import os
from open_ticket_ai.core.plugins.plugin import Plugin
from open_ticket_ai.core.injectables.injectable import Injectable


class FreemiumPlugin(Plugin):
    """Plugin with free and premium features."""

    def _get_all_injectables(self) -> list[type[Injectable]]:
        """Return free injectables always, premium only with license."""
        injectables = [
            # Always available
            BasicPipe,
            BasicService,
        ]

        # Add premium features if licensed
        license_key = os.getenv('MY_PLUGIN_LICENSE_KEY')
        if license_key and self._verify_license(license_key):
            injectables.extend([
                PremiumPipe,
                AdvancedService,
            ])

        return injectables

    def _verify_license(self, key: str) -> bool:
        """Verify premium license."""
        return True  # Your validation logic
```

### License Validation Best Practices

#### 1. Environment Variables

Use environment variables for license keys to keep them out of configuration files:

```python
license_key = os.getenv('MY_PLUGIN_LICENSE_KEY')
```

Users set it in their environment:

```bash
export MY_PLUGIN_LICENSE_KEY="your-license-key-here"
```

#### 2. Clear Error Messages

Provide actionable error messages that guide users to purchase licenses:

```python
if not license_key:
    raise LicenseError(
        "Missing license key for my-plugin.\n"
        "\n"
        "To use this commercial plugin:\n"
        "1. Purchase a license at https://myplugin.com\n"
        "2. Set the environment variable: MY_PLUGIN_LICENSE_KEY=<your-key>\n"
        "3. Restart Open Ticket AI\n"
        "\n"
        "For questions, contact support@myplugin.com"
    )
```

#### 3. Fail Fast

Validate licenses during plugin initialization, not at pipe execution time:

```python
# Good: Fails immediately on startup
class MyPlugin(Plugin):
    def __init__(self, config):
        self._validate_license()
        super().__init__(config)


# Bad: Fails when pipe is executed
class BadPipe(Pipe):
    def run(self, context):
        self._validate_license()  # Too late!
```

#### 4. Offline Support

Consider cached validation for intermittent connectivity:

```python
import time
import json
from pathlib import Path


def _verify_license(self, key: str) -> bool:
    """Verify license with grace period for offline scenarios."""
    cache_file = Path.home() / '.my_plugin_license_cache'

    # Try online validation first
    if self._online_validation(key):
        # Cache successful validation
        cache_file.write_text(json.dumps({
            'validated_at': time.time(),
            'key_hash': hashlib.sha256(key.encode()).hexdigest()
        }))
        return True

    # Fall back to cached validation (24-hour grace period)
    if cache_file.exists():
        cache = json.loads(cache_file.read_text())
        age = time.time() - cache['validated_at']
        if age < 86400:  # 24 hours
            return True

    return False
```

#### 5. Grace Periods & Trials

Allow reasonable trial periods or grace windows:

```python
def _verify_license(self, key: str) -> bool:
    """Allow 14-day trial period."""
    if key.startswith('TRIAL-'):
        # Extract trial start date from key
        trial_start = self._parse_trial_date(key)
        days_elapsed = (datetime.now() - trial_start).days

        if days_elapsed <= 14:
            print(f"Trial mode: {14 - days_elapsed} days remaining")
            return True
        else:
            raise LicenseError(
                "Trial period expired. Purchase a license at https://myplugin.com"
            )

    return self._verify_paid_license(key)
```

### Getting Your Plugin Listed

To have your plugin listed on the official plugins page:

1. **Publish to PyPI** with the `otai-` prefix (e.g., `otai-my-plugin`)
2. **Create documentation** describing features, installation, and configuration
3. **Submit a PR** to the Open Ticket AI documentation repository with:
    - Plugin name and description
    - Installation instructions
    - Pricing model (free, commercial, freemium)
    - Link to documentation
    - Support contact information
4. **Specify licensing** clearly in your plugin's README and PyPI metadata

### Example: Complete Commercial Plugin Structure

```
otai-my-commercial-plugin/
├── pyproject.toml              # Project metadata & dependencies
├── LICENSE                     # Your chosen license (proprietary, etc.)
├── README.md                   # Installation & purchase info
├── src/
│   └── otai_my_commercial_plugin/
│       ├── __init__.py
│       ├── plugin_factory.py   # Plugin with license validation
│       ├── licensing.py        # License validation logic
│       ├── pipes/
│       │   └── my_pipe.py
│       └── services/
│           └── my_service.py
├── tests/
│   └── unit/
│       ├── test_licensing.py   # Test license validation
│       └── test_plugin.py
└── docs/
    ├── installation.md         # How to install & license
    ├── configuration.md        # How to configure
    └── pricing.md             # Pricing & licensing options
```

### Support & Maintenance

As a commercial plugin developer, consider:

- **Documentation**: Comprehensive guides for installation, configuration, troubleshooting
- **Support Channels**: Email, issue tracker, Discord/Slack community
- **Updates**: Regular releases for bug fixes and new features
- **Compatibility**: Test against new Open Ticket AI versions
- **Migration Guides**: Help users upgrade between versions

### Legal Considerations

- **License Agreement**: Provide clear terms of use
- **Privacy Policy**: If collecting any data (license validation calls, analytics)
- **Compliance**: Ensure your plugin complies with relevant regulations (GDPR, etc.)
- **Intellectual Property**: Protect your code and trademarks appropriately

## Additional Resources

- [Plugin System](../plugins/plugin_system.md)
- [Dependency Injection](dependency_injection.md)
- [Services](services.md)
- [Pipeline Architecture](../users/pipeline-architecture.md)
- [Hugging Face Local plugin example](../plugins/hf_local.md)
