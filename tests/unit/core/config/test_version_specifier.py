import pytest
from packaging.specifiers import InvalidSpecifier, SpecifierSet
from pydantic import ValidationError


class TestVersionSpecifierFormats:
    """Test various version specifier formats with packaging.specifiers.SpecifierSet."""

    @pytest.mark.parametrize(
        "spec,expected_valid,expected_normalized",
        [
            ("^1.4.0", False, None),
            ("1", False, None),
            (">=1.4.0,<2.0.0", True, "<2.0.0,>=1.4.0"),
            ("~=1.4.0", True, "~=1.4.0"),
            ("==1.4.0", True, "==1.4.0"),
            (">=1.0.0", True, ">=1.0.0"),
            ("!=1.4.0", True, "!=1.4.0"),
            ("==1.*", True, "==1.*"),
        ],
    )
    def test_version_specifier_validation(self, spec: str, expected_valid: bool, expected_normalized: str | None):
        if expected_valid:
            result = SpecifierSet(spec)
            assert str(result) == expected_normalized
        else:
            with pytest.raises(InvalidSpecifier):
                SpecifierSet(spec)


class TestVersionSpecifierUsageInConfig:
    """Test that api_version field handles version specifiers correctly."""

    def test_valid_specifier_in_config(self):
        from open_ticket_ai.core.config.config_models import OpenTicketAIConfig

        config = OpenTicketAIConfig(api_version=">=1.4.0")
        assert str(config.api_version) == ">=1.4.0"

    def test_invalid_npm_style_specifier_raises_error(self):
        from open_ticket_ai.core.config.config_models import OpenTicketAIConfig

        with pytest.raises(ValidationError, match="Invalid specifier"):
            OpenTicketAIConfig(api_version="^1.4.0")

    def test_invalid_plain_version_raises_error(self):
        from open_ticket_ai.core.config.config_models import OpenTicketAIConfig

        with pytest.raises(ValidationError, match="Invalid specifier"):
            OpenTicketAIConfig(api_version="1")

    def test_exact_version_specifier(self):
        from open_ticket_ai.core.config.config_models import OpenTicketAIConfig

        config = OpenTicketAIConfig(api_version="==1.4.0")
        assert str(config.api_version) == "==1.4.0"

    def test_compatible_release_specifier(self):
        from open_ticket_ai.core.config.config_models import OpenTicketAIConfig

        config = OpenTicketAIConfig(api_version="~=1.4.0")
        assert str(config.api_version) == "~=1.4.0"

    def test_default_api_version_is_semver(self):
        from open_ticket_ai.core.config.config_models import OpenTicketAIConfig

        config = OpenTicketAIConfig()
        assert str(config.api_version) == ">=1.0.0"
