import importlib
import importlib.metadata
import logging
import re
from typing import Any, Dict, List, Optional

from packaging import specifiers, version


class PluginLoader:
    """Handles dynamic loading and version validation of plugins."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._loaded_plugins: Dict[str, Any] = {}
    
    def parse_plugin_spec(self, plugin_spec: str) -> tuple[str, Optional[str]]:
        """Parse plugin specification like 'package_name ~= 1.0.0' into name and version spec."""
        # Split on whitespace to separate package name from version spec
        parts = plugin_spec.strip().split()
        if len(parts) == 1:
            return parts[0], None
        elif len(parts) >= 3:
            # Rejoin version spec parts (e.g., "~= 1.0.0")
            return parts[0], " ".join(parts[1:])
        else:
            return parts[0], parts[1] if len(parts) > 1 else None
    
    def check_plugin_version(self, package_name: str, version_spec: Optional[str]) -> bool:
        """Check if the installed version of a package matches the required version spec."""
        if not version_spec:
            # No version requirement, just check if package is installed
            try:
                importlib.metadata.version(package_name)
                return True
            except importlib.metadata.PackageNotFoundError:
                return False
        
        try:
            installed_version = importlib.metadata.version(package_name)
            spec_set = specifiers.SpecifierSet(version_spec)
            return spec_set.contains(installed_version)
        except importlib.metadata.PackageNotFoundError:
            self.logger.error(f"Plugin package '{package_name}' is not installed")
            return False
        except Exception as e:
            self.logger.error(f"Error checking version for '{package_name}': {e}")
            return False
    
    def load_plugin(self, plugin_spec: str) -> Optional[Any]:
        """Load a plugin after validating its version."""
        package_name, version_spec = self.parse_plugin_spec(plugin_spec)
        
        # Check if already loaded
        if package_name in self._loaded_plugins:
            return self._loaded_plugins[package_name]
        
        # Check version compatibility
        if not self.check_plugin_version(package_name, version_spec):
            if version_spec:
                self.logger.error(
                    f"Plugin '{package_name}' version does not match requirement '{version_spec}'"
                )
            else:
                self.logger.error(f"Plugin '{package_name}' is not installed")
            return None
        
        try:
            # Import the plugin module
            plugin_module = importlib.import_module(package_name)
            self._loaded_plugins[package_name] = plugin_module
            
            # Check if the plugin has a register function and call it
            if hasattr(plugin_module, 'register_plugin'):
                plugin_module.register_plugin()
                self.logger.info(f"Registered plugin '{package_name}' successfully")
            else:
                self.logger.info(f"Loaded plugin '{package_name}' (no register_plugin function found)")
            
            return plugin_module
            
        except ImportError as e:
            self.logger.error(f"Failed to import plugin '{package_name}': {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error loading plugin '{package_name}': {e}")
            return None
    
    def load_plugins(self, plugin_specs: List[str]) -> Dict[str, Any]:
        """Load multiple plugins from a list of specifications."""
        loaded = {}
        
        for plugin_spec in plugin_specs:
            plugin_module = self.load_plugin(plugin_spec)
            if plugin_module:
                package_name, _ = self.parse_plugin_spec(plugin_spec)
                loaded[package_name] = plugin_module
        
        self.logger.info(f"Successfully loaded {len(loaded)} out of {len(plugin_specs)} plugins")
        return loaded
    
    def get_loaded_plugins(self) -> Dict[str, Any]:
        """Get all currently loaded plugins."""
        return self._loaded_plugins.copy()
