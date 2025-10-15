# GitHub Actions Workflows

This directory contains the GitHub Actions workflows for the Open Ticket AI project.

## Workflows

### CI/CD Workflows

#### `ci-quality-assurance.yml`
Main CI workflow that runs on pushes and pull requests to `dev` and `main` branches.

**Triggers:** Push to dev/main, Pull Request (opened, synchronize, reopened)

**Steps:**
- Linting with ruff (auto-fix on push)
- Type checking with mypy
- Running all tests
- Validating test structure
- Generating coverage reports
- SonarCloud scanning

#### `copilot-pr-retry.yml` ⭐ NEW
Automatically handles Copilot-generated Pull Requests that fail checks.

**Triggers:** 
- Pull Request events (opened, synchronize, reopened)
- Workflow run completion (CI Quality Assurance, Trivy Security Scan)

**Behavior:**
- Detects PRs created by `github-copilot[bot]`
- Monitors check status for Copilot PRs
- On check failure:
  - Labels PR with `retry-needed` and `copilot-pr`
  - Posts detailed comment about failed checks
  - Closes the PR to allow Copilot to retry
- On check success:
  - Labels PR with `copilot-pr` for tracking
  - Logs success message

**Benefits:**
- Reduces manual intervention for failing Copilot PRs
- Enables Copilot to iterate quickly on solutions
- Does not affect manually created PRs
- Provides clear audit trail with labels and comments

**Configuration:**
The workflow runs automatically and requires no configuration. It respects these GitHub permissions:
- `contents: read` - Read repository content
- `pull-requests: write` - Update PR status and labels
- `issues: write` - Add comments and labels
- `checks: read` - Read check run status

#### `trivy-security.yml`
Security scanning workflow using Trivy.

**Triggers:** Push to main/dev, Pull Requests, Weekly schedule (Sunday)

**Steps:**
- Filesystem vulnerability scan
- Configuration scan
- Upload results to GitHub Security

### Deployment Workflows

#### `deploy-docker-image.yml`
Builds and publishes Docker images.

#### `publish-to-pypi.yml`
Publishes packages to PyPI.

#### `publish-open-ticket-ai.yml`
Publishes the main open-ticket-ai package.

#### `publish-otobo-znuny.yml`
Publishes the OTOBO/ZNUNY adapter package.

#### `publish-hf-local.yml`
Publishes the HuggingFace local package.

### Scheduled Workflows

#### `nightly-tests.yml`
Runs comprehensive tests on a nightly schedule.

## Labels Used

The workflows use the following labels:

- `copilot-pr` - Automatically added to all Copilot-generated PRs
- `retry-needed` - Added to Copilot PRs that have failed checks and need to be retried

## Security

All workflows follow security best practices:
- Use pinned versions of actions
- Minimal permission scopes
- Secrets are never logged
- SARIF reports uploaded to GitHub Security

## Testing Workflows Locally

To test workflow syntax:
```bash
# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/copilot-pr-retry.yml'))"
```

To test workflow logic:
1. Create a test PR from a Copilot bot account
2. Trigger failing checks
3. Verify the workflow properly labels, comments, and closes the PR

## Troubleshooting

### Copilot PR Retry Workflow

**Issue:** Workflow doesn't trigger for Copilot PRs
- Verify the PR author is `github-copilot[bot]`
- Check workflow run logs in the Actions tab
- Ensure required permissions are granted

**Issue:** PR isn't closed after failures
- Check if checks have completed (not pending)
- Verify the workflow has `pull-requests: write` permission
- Review workflow logs for error messages

**Issue:** Manual PRs are affected
- This should never happen - the workflow explicitly checks `github.actor == 'github-copilot[bot]'`
- If this occurs, it's a bug and should be reported immediately

## Contributing

When adding new workflows:
1. Follow the naming convention: `kebab-case.yml`
2. Add proper permissions (principle of least privilege)
3. Include clear step names and descriptions
4. Add documentation to this README
5. Test thoroughly before merging
