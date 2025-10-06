# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Plugin metadata interface with `get_metadata()` function
- Plugin hooks `register_pipes()` and `register_services()`
- Entry point registration in `open_ticket_ai.plugins` group

## [1.0.0rc1] - 2024-10-05

### Added
- Initial release candidate
- OTOBO/Znuny ticket system integration
- Support for ticket search, fetch, update, and note operations
- Unified ticket model conversion
- Configuration via Pydantic models

[Unreleased]: https://github.com/Softoft-Orga/open-ticket-ai/compare/v1.0.0rc1...HEAD
[1.0.0rc1]: https://github.com/Softoft-Orga/open-ticket-ai/releases/tag/v1.0.0rc1
