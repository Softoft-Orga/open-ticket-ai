# Copilot PR Retry Workflow - Test Scenarios

This document describes test scenarios for the Copilot PR Retry workflow.

## Test Scenario 1: Copilot PR with Passing Checks

**Setup:**
1. Create a PR from `github-copilot[bot]` account
2. Ensure all CI checks pass

**Expected Behavior:**
- Workflow detects it's a Copilot PR
- Monitors check status
- Adds `copilot-pr` label
- Logs success message
- PR remains open for review

**Verification:**
- Check workflow logs show "Copilot PR #X has passing checks ✓"
- PR has `copilot-pr` label
- PR is still open
- No retry-needed label

## Test Scenario 2: Copilot PR with Failing Checks

**Setup:**
1. Create a PR from `github-copilot[bot]` account
2. Introduce a change that causes CI to fail (e.g., syntax error, failing test)

**Expected Behavior:**
- Workflow detects it's a Copilot PR
- Monitors check status and detects failures
- Adds both `copilot-pr` and `retry-needed` labels
- Posts a comment with details of failed checks
- Closes the PR to allow Copilot to retry

**Verification:**
- Check workflow logs show failed checks detected
- PR has both `copilot-pr` and `retry-needed` labels
- Comment exists on PR explaining the failures
- PR is closed (not merged)
- Workflow logs show "Closed PR #X due to failed checks"

## Test Scenario 3: Manual PR with Failing Checks

**Setup:**
1. Create a PR from a regular user account (not Copilot bot)
2. Introduce a change that causes CI to fail

**Expected Behavior:**
- Workflow runs but skips all Copilot-specific actions
- PR is NOT closed
- No labels are added
- No comments are posted

**Verification:**
- Check workflow logs show it detected this is not a Copilot PR
- PR remains open regardless of check status
- No `copilot-pr` or `retry-needed` labels
- No automated comments from the retry handler

## Test Scenario 4: Copilot PR with Mixed Check Status

**Setup:**
1. Create a PR from `github-copilot[bot]` account
2. Some checks pass, some fail

**Expected Behavior:**
- Workflow detects failures (even if some checks pass)
- Treats the PR as failed
- Follows same behavior as Scenario 2

**Verification:**
- PR is closed
- Both labels are added
- Comment lists only the failed checks

## Test Scenario 5: Workflow Run Trigger

**Setup:**
1. Create a Copilot PR
2. Wait for CI workflow to complete with failures

**Expected Behavior:**
- Copilot retry workflow triggers via `workflow_run` event
- Detects the PR associated with the workflow run
- Processes it according to check status

**Verification:**
- Workflow triggers after CI completion
- Correctly identifies the associated PR
- Takes appropriate action based on results

## Test Scenario 6: PR Updated After Initial Failure

**Setup:**
1. Create a Copilot PR that initially fails
2. Copilot pushes a fix to the same PR

**Expected Behavior:**
- First push: PR gets labeled, commented, and closed
- If Copilot creates a new PR: treated as new scenario
- If Copilot updates the same PR: workflow re-evaluates

**Verification:**
- Each push triggers re-evaluation
- Labels and comments reflect current state
- Workflow doesn't duplicate comments

## Running the Tests

### Manual Testing

1. Fork the repository to a test environment
2. Create test PRs using a bot account or GitHub Copilot
3. Manually trigger failures by introducing errors
4. Verify workflow behavior matches expected outcomes

### Automated Testing

Currently, the workflow is designed to be tested in a live environment. Future improvements could include:
- Unit tests for the GitHub API interaction logic
- Mock GitHub API responses for edge cases
- Integration tests with a test repository

## Known Limitations

1. **Workflow Run Association**: The workflow_run trigger may not always correctly associate with a PR if multiple PRs share the same branch name
2. **Rate Limiting**: Multiple rapid PR updates could hit GitHub API rate limits
3. **Label Creation**: The workflow assumes labels can be created; if they don't exist and can't be auto-created, labeling will fail (but workflow continues)
4. **Comment Duplication**: If the workflow runs multiple times quickly, it may create duplicate comments

## Troubleshooting Guide

### Workflow doesn't trigger
- Verify the actor is exactly `github-copilot[bot]`
- Check workflow permissions are granted
- Review repository settings for workflow restrictions

### PR not closed despite failures
- Check if checks have actually completed (not just failed)
- Verify `pull-requests: write` permission is granted
- Review workflow logs for error messages

### Manual PRs affected
- This should never happen due to the actor check
- If it does, immediately report as a critical bug
- Check workflow condition logic for errors
