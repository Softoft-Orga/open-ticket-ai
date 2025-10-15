# Open Ticket AI

Open Ticket AI is an intelligent ticket classification and routing system that uses machine learning to automatically categorize and prioritize support tickets.

## CI/CD Automation

The repository includes automated workflows for handling Copilot-generated Pull Requests. When GitHub Copilot creates a PR that fails CI checks, the workflow automatically labels it with `retry-needed` and `copilot-pr`, posts a comment explaining the failures, and closes the PR to allow Copilot to retry with fixes. This automation only affects PRs created by `github-copilot[bot]` and has no impact on manually created PRs.
