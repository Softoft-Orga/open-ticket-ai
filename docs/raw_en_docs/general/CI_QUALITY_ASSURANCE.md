# CI Quality Assurance and SonarCloud Integration

This document describes the automated quality assurance processes integrated into the CI/CD pipeline, including test coverage reporting, linting, and static type checking with SonarCloud.

## Overview

The repository uses SonarCloud for continuous code quality analysis. The QA workflow automatically generates and uploads reports from:

- **pytest** (test coverage)
- **ruff** (linting and code style)
- **mypy** (static type checking)

## Workflow: Quality Assurance SonarCloud

**File**: `.github/workflows/qa-tests.yml`

**Triggers**:
- Push to `dev` branch
- Pull requests (opened, synchronized, reopened)

### Workflow Steps

#### 1. Environment Setup
- Checkout repository with full git history (`fetch-depth: 0` for SonarCloud)
- Install `uv` package manager
- Set up Python 3.13
- Install all project dependencies with `uv sync --locked --all-extras`

#### 2. Test Coverage Generation

```bash
uv run pytest \
  --cov=src \
  --cov=packages/otai_hf_local/src \
  --cov=packages/otai_otobo_znuny/src \
  --cov-report=xml:coverage.xml \
  --cov-report=term
```

**Output**: `coverage.xml` (Cobertura format for SonarCloud)

**Coverage Paths**:
- `src/` - Core application source
- `packages/otai_hf_local/src/` - HuggingFace Local plugin
- `packages/otai_otobo_znuny/src/` - OTOBO/Znuny plugin

#### 3. Ruff Linting Report

```bash
uv run ruff check . --output-format=sarif > ruff-report.sarif
```

**Output**: `ruff-report.sarif` (SARIF format for SonarCloud external issues)

Ruff checks for:
- Code style violations
- Import sorting (I001)
- Potential bugs and anti-patterns
- Performance issues
- Code complexity

See `.pyproject.toml` for the complete ruff configuration.

#### 4. Mypy Type Checking

```bash
uv run mypy src packages/otai_hf_local/src packages/otai_otobo_znuny/src --no-error-summary > mypy-report.txt
```

**Output**: `mypy-report.txt` (text format for logging and artifact archival)

Mypy validates:
- Type annotations
- Function signatures
- Return types
- Module imports

#### 5. SonarCloud Scan

The workflow uses `SonarSource/sonarcloud-scan-action@v4` to upload all generated reports to SonarCloud.

**Required Secrets**:
- `SONAR_TOKEN` - SonarCloud authentication token
- `GITHUB_TOKEN` - Automatically provided by GitHub Actions

**SonarCloud Configuration**: See `sonar-project.properties`

#### 6. Artifact Upload

All reports are uploaded as GitHub Actions artifacts for review and debugging:

- `coverage-report` - Test coverage XML
- `ruff-report` - Linting issues in SARIF format
- `mypy-report` - Type checking errors

**Retention**: 30 days

## SonarCloud Configuration

**File**: `sonar-project.properties`

```properties
sonar.projectKey=Softoft-Orga_open-ticket-ai
sonar.organization=softoft-orga

# Source code paths (workspace structure)
sonar.sources=src,packages/otai_hf_local/src,packages/otai_otobo_znuny/src

# Test paths
sonar.tests=tests,packages/otai_hf_local/tests,packages/otai_otobo_znuny/tests

# Coverage report
sonar.python.coverage.reportPaths=coverage.xml

# Ruff linting report (SARIF format)
sonar.externalIssuesReportPaths=ruff-report.sarif
```

### Why Multiple Source Paths?

This project uses a **uv workspace** structure with:
- Core application in `src/open_ticket_ai/`
- Plugins as separate packages under `packages/*/src/`

SonarCloud must be configured with all source and test paths to provide complete coverage analysis.

## Viewing Results

### In Pull Requests

SonarCloud automatically comments on pull requests with:
- Quality Gate status (pass/fail)
- New issues introduced
- Coverage changes
- Code smells and duplications

### On SonarCloud Dashboard

Visit: https://sonarcloud.io/project/overview?id=Softoft-Orga_open-ticket-ai

The dashboard shows:
- Overall code quality metrics
- Coverage trends over time
- Technical debt
- Security vulnerabilities
- Bug and code smell reports

### In CI Artifacts

Each workflow run archives reports as artifacts. To download:

1. Go to the GitHub Actions run
2. Scroll to the "Artifacts" section
3. Download `coverage-report`, `ruff-report`, or `mypy-report`

## Local Testing

You can generate the same reports locally to preview quality metrics before pushing:

### Install Dependencies

```bash
uv sync --all-extras
```

### Generate Coverage Report

```bash
uv run pytest \
  --cov=src \
  --cov=packages/otai_hf_local/src \
  --cov=packages/otai_otobo_znuny/src \
  --cov-report=xml:coverage.xml \
  --cov-report=html
```

View HTML coverage report: `open htmlcov/index.html`

### Run Ruff Linting

```bash
uv run ruff check .
```

Fix auto-fixable issues:

```bash
uv run ruff check . --fix
```

Generate SARIF report:

```bash
uv run ruff check . --output-format=sarif > ruff-report.sarif
```

### Run Mypy Type Checking

```bash
uv run mypy src packages/otai_hf_local/src packages/otai_otobo_znuny/src
```

## Quality Standards

### Coverage Targets

- **Minimum**: 70% overall coverage
- **Goal**: 80%+ coverage for core modules
- **New code**: Should maintain or improve coverage

### Linting

- **Zero tolerance** for ruff errors in new code
- Existing code should be gradually improved
- All imports must be sorted (ruff I001)

### Type Checking

- All new functions must have type annotations
- Strict mode enabled for core modules
- Gradual typing for legacy code

## Troubleshooting

### Coverage Report Not Generated

**Symptom**: `coverage.xml` is missing or empty

**Causes**:
- Test collection failures
- No tests discovered
- Import errors in test files

**Solution**:
```bash
# Run pytest with verbose output to debug
uv run pytest -v
```

### Ruff SARIF Format Issues

**Symptom**: SonarCloud doesn't display ruff issues

**Cause**: SARIF file is malformed or has invalid paths

**Solution**:
```bash
# Validate SARIF locally
cat ruff-report.sarif | jq .
```

### SonarCloud Token Expired

**Symptom**: Authentication failure in workflow

**Solution**:
1. Generate a new token at https://sonarcloud.io/account/security
2. Update the `SONAR_TOKEN` secret in GitHub repository settings

## Related Documentation

- [Testing Strategy](../general/testing/) - Overview of test types
- [Contributing Guidelines](../general/CONTRIBUTING.md) - Code quality requirements
- [Release Process](../RELEASE.md) - How quality gates affect releases

## References

- [SonarCloud Documentation](https://docs.sonarcloud.io/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Mypy Documentation](https://mypy.readthedocs.io/)
