#!/usr/bin/env python3

import importlib.metadata as md
import sys

PLUGIN_GROUP = "open_ticket_ai.plugins"
REQUIRED_CORE_API = "2.0"
REQUIRED_METADATA_FIELDS = {"name", "version", "core_api", "description"}
REQUIRED_HOOKS = {"register_pipes", "register_services"}


def validate_plugins():
    errors = []
    plugins_found = 0

    print(f"Validating plugins in group '{PLUGIN_GROUP}'...")
    print(f"Required core API: {REQUIRED_CORE_API}")
    print()

    try:
        entry_points = md.entry_points(group=PLUGIN_GROUP)
    except Exception as e:
        print(f"❌ Error loading entry points: {e}")
        return False

    if not entry_points:
        print(f"⚠️  No plugins found in entry point group '{PLUGIN_GROUP}'")
        return True

    for ep in entry_points:
        plugins_found += 1
        plugin_name = ep.name
        print(f"Checking plugin: {plugin_name}")

        try:
            plugin = ep.load()
        except Exception as e:
            errors.append(f"  ❌ Failed to load plugin '{plugin_name}': {e}")
            continue

        if not hasattr(plugin, "get_metadata"):
            errors.append(f"  ❌ Plugin '{plugin_name}' missing get_metadata() function")
            continue

        try:
            metadata = plugin.get_metadata()
        except Exception as e:
            errors.append(f"  ❌ Plugin '{plugin_name}' get_metadata() raised error: {e}")
            continue

        missing_fields = REQUIRED_METADATA_FIELDS - set(metadata.keys())
        if missing_fields:
            errors.append(f"  ❌ Plugin '{plugin_name}' metadata missing fields: {missing_fields}")

        if metadata.get("core_api") != REQUIRED_CORE_API:
            errors.append(
                f"  ❌ Plugin '{plugin_name}' has incompatible core_api: "
                f"{metadata.get('core_api')} (expected {REQUIRED_CORE_API})"
            )

        for hook in REQUIRED_HOOKS:
            if not hasattr(plugin, hook):
                errors.append(f"  ❌ Plugin '{plugin_name}' missing {hook}() function")
            else:
                try:
                    result = getattr(plugin, hook)()
                    if not isinstance(result, list):
                        errors.append(f"  ❌ Plugin '{plugin_name}' {hook}() must return list, got {type(result)}")
                except Exception as e:
                    errors.append(f"  ❌ Plugin '{plugin_name}' {hook}() raised error: {e}")

        if not errors or not any(plugin_name in err for err in errors):
            print(f"  ✅ Plugin '{plugin_name}' metadata: {metadata}")

    print()
    print(f"Found {plugins_found} plugin(s)")

    if errors:
        print()
        print("Validation errors:")
        for error in errors:
            print(error)
        return False

    print()
    print("✅ All plugins validated successfully!")
    return True


if __name__ == "__main__":
    success = validate_plugins()
    sys.exit(0 if success else 1)
