---
title: Agent Tools Reference
description: "Comprehensive reference of all MCP tools available to AI agents working on the Open Ticket AI repository"
nav:
  group: Developers
  order: 100
---

# Agent Tools Reference

This document provides a comprehensive reference of all MCP (Model Context Protocol) tools available to AI agents working on the Open Ticket AI repository. These tools enable agents to interact with GitHub, browse the web, manipulate files, search code, and perform security checks.

## GitHub Actions Tools

Tools for interacting with GitHub Actions workflows, runs, jobs, and artifacts.

### github-mcp-server-actions_list

List GitHub Actions resources including workflows, workflow runs, jobs, and artifacts.

**Methods:**
- `list_workflows` - List all workflows in a repository
- `list_workflow_runs` - List workflow runs (optionally filtered by workflow ID, branch, status, event, actor)
- `list_workflow_jobs` - List jobs for a specific workflow run
- `list_workflow_run_artifacts` - List artifacts for a specific workflow run

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name
- `method` (required) - The action to perform
- `resource_id` (optional) - Workflow ID or run ID depending on method
- `page` - Page number for pagination (default: 1)
- `per_page` - Results per page (default: 30, max: 100)

**When to use:** Investigating CI/CD pipelines, checking workflow status, debugging build failures.

### github-mcp-server-actions_get

Get details about specific GitHub Actions resources by their unique IDs.

**Methods:**
- `get_workflow` - Get workflow details by ID or filename
- `get_workflow_run` - Get workflow run details
- `get_workflow_job` - Get job details
- `download_workflow_run_artifact` - Download an artifact
- `get_workflow_run_usage` - Get usage metrics for a run
- `get_workflow_run_logs_url` - Get logs URL for a run

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name
- `method` (required) - The method to execute
- `resource_id` (required) - Workflow/run/job/artifact ID

**When to use:** Getting detailed information about specific workflows, runs, or jobs.

## GitHub Repository Tools

Tools for interacting with GitHub repositories, commits, issues, and pull requests.

### github-mcp-server-get_file_contents

Get the contents of a file or directory from a GitHub repository.

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name
- `path` - Path to file/directory (default: "/")
- `ref` - Git ref (branch, tag, or PR ref)
- `sha` - Commit SHA (overrides ref if specified)

**When to use:** Reading repository files, exploring directory structures, checking file content at specific commits.

### github-mcp-server-get_commit

Get details for a commit from a GitHub repository.

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name
- `sha` (required) - Commit SHA, branch name, or tag name
- `include_diff` - Include file diffs and stats (default: true)
- `page` - Page number for pagination
- `perPage` - Results per page (min 1, max 100)

**When to use:** Reviewing commit changes, understanding what was modified in a specific commit.

### github-mcp-server-list_commits

Get list of commits of a branch in a GitHub repository.

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name
- `sha` - Commit SHA, branch, or tag name (defaults to default branch)
- `author` - Filter by author username or email
- `page` - Page number for pagination
- `perPage` - Results per page (min 1, max 100)

**When to use:** Reviewing commit history, finding commits by author, tracking changes over time.

### github-mcp-server-list_branches

List branches in a GitHub repository.

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name
- `page` - Page number for pagination
- `perPage` - Results per page (min 1, max 100)

**When to use:** Discovering available branches, checking branch names.

### github-mcp-server-list_tags

List git tags in a GitHub repository.

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name
- `page` - Page number for pagination
- `perPage` - Results per page (min 1, max 100)

**When to use:** Finding release versions, checking available tags.

### github-mcp-server-get_tag

Get details about a specific git tag in a GitHub repository.

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name
- `tag` (required) - Tag name

**When to use:** Getting tag details, commit information for a specific release.

## GitHub Issues & Pull Requests

### github-mcp-server-list_issues

List issues in a GitHub repository with filtering and pagination.

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name
- `state` - Filter by state (OPEN, CLOSED)
- `labels` - Filter by labels (array)
- `since` - Filter by date (ISO 8601 timestamp)
- `orderBy` - Order issues by field (CREATED_AT, UPDATED_AT, COMMENTS)
- `direction` - Order direction (ASC, DESC)
- `after` - Cursor for pagination (use endCursor from previous response)
- `perPage` - Results per page (min 1, max 100)

**When to use:** Finding issues, filtering by labels or state, tracking open bugs.

### github-mcp-server-issue_read

Get information about a specific issue in a GitHub repository.

**Methods:**
- `get` - Get issue details
- `get_comments` - Get issue comments
- `get_sub_issues` - Get sub-issues
- `get_labels` - Get labels assigned to the issue

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name
- `method` (required) - The read operation to perform
- `issue_number` (required) - The issue number
- `page` - Page number for pagination
- `perPage` - Results per page (min 1, max 100)

**When to use:** Reading issue details, comments, or labels.

### github-mcp-server-list_pull_requests

List pull requests in a GitHub repository.

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name
- `state` - Filter by state (open, closed, all)
- `head` - Filter by head user/org and branch
- `base` - Filter by base branch
- `sort` - Sort by (created, updated, popularity, long-running)
- `direction` - Sort direction (asc, desc)
- `page` - Page number for pagination
- `perPage` - Results per page (min 1, max 100)

**When to use:** Listing PRs, finding PRs by branch or state.

### github-mcp-server-pull_request_read

Get information on a specific pull request.

**Methods:**
- `get` - Get PR details
- `get_diff` - Get the diff of a PR
- `get_status` - Get status of head commit (builds and checks)
- `get_files` - Get list of files changed
- `get_review_comments` - Get review threads with comments
- `get_reviews` - Get reviews on a PR
- `get_comments` - Get comments on a PR

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name
- `method` (required) - Action to specify what data to retrieve
- `pullNumber` (required) - Pull request number
- `page` - Page number for pagination
- `perPage` - Results per page (min 1, max 100)

**When to use:** Reviewing PR changes, checking PR status, reading review comments.

### github-mcp-server-search_pull_requests

Search for pull requests in GitHub repositories using issues search syntax scoped to `is:pr`.

**Parameters:**
- `query` (required) - Search query using GitHub PR search syntax
- `owner` - Optional repository owner (with repo, limits to specific repository)
- `repo` - Optional repository name (with owner, limits to specific repository)
- `sort` - Sort field (comments, reactions, created, updated, etc.)
- `order` - Sort order (asc, desc)
- `page` - Page number for pagination
- `perPage` - Results per page (min 1, max 100)

**When to use:** Searching PRs by author, content, or complex criteria.

### github-mcp-server-search_issues

Search for issues in GitHub repositories using issues search syntax scoped to `is:issue`.

**Parameters:**
- `query` (required) - Search query using GitHub issues search syntax
- `owner` - Optional repository owner
- `repo` - Optional repository name
- `sort` - Sort field (comments, reactions, created, updated, etc.)
- `order` - Sort order (asc, desc)
- `page` - Page number for pagination
- `perPage` - Results per page (min 1, max 100)

**When to use:** Searching issues across repositories, finding issues by complex criteria.

## GitHub Releases

### github-mcp-server-list_releases

List releases in a GitHub repository.

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name
- `page` - Page number for pagination
- `perPage` - Results per page (min 1, max 100)

**When to use:** Checking available releases, finding release notes.

### github-mcp-server-get_latest_release

Get the latest release in a GitHub repository.

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name

**When to use:** Checking the most recent release version.

### github-mcp-server-get_release_by_tag

Get a specific release by its tag name.

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name
- `tag` (required) - Tag name (e.g., 'v1.0.0')

**When to use:** Getting release details for a specific version.

## GitHub Search

### github-mcp-server-search_code

Fast and precise code search across ALL GitHub repositories using GitHub's native search engine.

**Parameters:**
- `query` (required) - Search query using GitHub's code search syntax
  - Examples: `content:Skill language:Java org:github`, `NOT is:archived language:Python OR language:go`
  - Supports exact matching, language filters, path filters, and more
- `sort` - Sort field ('indexed' only)
- `order` - Sort order (asc, desc)
- `page` - Page number for pagination
- `perPage` - Results per page (min 1, max 100)

**When to use:** Finding exact symbols, functions, classes, or specific code patterns across repositories.

### github-mcp-server-search_repositories

Find GitHub repositories by name, description, readme, topics, or other metadata.

**Parameters:**
- `query` (required) - Repository search query
  - Examples: `machine learning in:name stars:>1000 language:python`, `topic:react`, `user:facebook`
- `sort` - Sort by (stars, forks, help-wanted-issues, updated)
- `order` - Sort order (asc, desc)
- `minimal_output` - Return minimal info (default: true)
- `page` - Page number for pagination
- `perPage` - Results per page (min 1, max 100)

**When to use:** Discovering projects, finding examples, locating specific repositories.

### github-mcp-server-search_users

Find GitHub users by username, real name, or other profile information.

**Parameters:**
- `query` (required) - User search query
  - Examples: `john smith`, `location:seattle`, `followers:>100`
- `sort` - Sort by (followers, repositories, joined)
- `order` - Sort order (asc, desc)
- `page` - Page number for pagination
- `perPage` - Results per page (min 1, max 100)

**When to use:** Locating developers, contributors, or team members.

## GitHub Security

### github-mcp-server-list_code_scanning_alerts

List code scanning alerts in a GitHub repository.

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name
- `state` - Filter by state (open, closed, dismissed, fixed) - default: open
- `severity` - Filter by severity (critical, high, medium, low, warning, note, error)
- `ref` - Git reference for results
- `tool_name` - Name of the tool used for code scanning

**When to use:** Checking security vulnerabilities detected by code scanning.

### github-mcp-server-get_code_scanning_alert

Get details of a specific code scanning alert.

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name
- `alertNumber` (required) - The number of the alert

**When to use:** Investigating a specific security alert.

### github-mcp-server-list_secret_scanning_alerts

List secret scanning alerts in a GitHub repository.

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name
- `state` - Filter by state (open, resolved)
- `secret_type` - Filter by secret type (comma-separated)
- `resolution` - Filter by resolution (false_positive, wont_fix, revoked, pattern_edited, pattern_deleted, used_in_tests)

**When to use:** Checking for exposed secrets or credentials.

### github-mcp-server-get_secret_scanning_alert

Get details of a specific secret scanning alert.

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name
- `alertNumber` (required) - The number of the alert

**When to use:** Investigating a specific secret exposure.

## GitHub Actions Logs

### github-mcp-server-get_job_logs

Get logs for GitHub Actions workflow jobs.

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name
- `job_id` - The job ID (for single job logs)
- `run_id` - The workflow run ID (required when failed_only is true)
- `failed_only` - Get logs for all failed jobs (requires run_id)
- `return_content` - Return actual log content instead of URLs
- `tail_lines` - Number of lines from end of log (default: 500)

**When to use:** Debugging CI/CD failures, reviewing build logs.

### github-mcp-server-list_issue_types

List supported issue types for repository owner (organization).

**Parameters:**
- `owner` (required) - The organization owner of the repository

**When to use:** Understanding available issue types for an organization.

### github-mcp-server-get_label

Get a specific label from a repository.

**Parameters:**
- `owner` (required) - Repository owner
- `repo` (required) - Repository name
- `name` (required) - Label name

**When to use:** Checking label details, colors, or descriptions.

## Web & Browser Tools

### web_search

AI-powered web search to provide intelligent, contextual answers with citations.

**Parameters:**
- `query` (required) - A clear, specific question or prompt requiring up-to-date information

**When to use:**
- User's query pertains to recent events or frequently updated information
- User's query is about new developments, trends, or technologies
- User's query is extremely specific or pertains to niche subjects
- User explicitly requests a web search
- You need current, factual information with verifiable sources

**Examples:**
- "What are the latest features in React 19?"
- "What is the current status of the James Webb Space Telescope?"
- "Explain the recent developments in quantum computing?"

### web_fetch

Fetches a URL from the internet and returns the page as markdown or raw HTML.

**Parameters:**
- `url` (required) - The URL to fetch
- `raw` - If true, returns raw HTML; if false, converts to markdown (default: false)
- `max_length` - Maximum characters to return (default: 5000, max: 20000)
- `start_index` - Start index for pagination (default: 0)

**When to use:** Safely retrieving up-to-date information from HTML web pages, reading documentation.

## Playwright Browser Tools

Tools for browser automation, web scraping, and visual testing.

### playwright-browser_navigate

Navigate to a URL.

**Parameters:**
- `url` (required) - The URL to navigate to

### playwright-browser_navigate_back

Go back to the previous page.

### playwright-browser_snapshot

Capture accessibility snapshot of the current page (better than screenshot for analysis).

**When to use:** Analyzing page structure, checking accessibility, understanding DOM hierarchy.

### playwright-browser_take_screenshot

Take a screenshot of the current page.

**Parameters:**
- `element` - Human-readable element description (requires ref if provided)
- `ref` - Exact element reference from page snapshot
- `fullPage` - Capture full scrollable page (default: false)
- `type` - Image format (png, jpeg) - default: png
- `filename` - File name to save (defaults to `page-{timestamp}.{png|jpeg}`)

**When to use:** Visual documentation, capturing UI state, validating visual changes.

### playwright-browser_click

Perform click on a web page.

**Parameters:**
- `element` (required) - Human-readable element description
- `ref` (required) - Exact target element reference from page snapshot
- `button` - Button to click (left, right, middle) - default: left
- `doubleClick` - Perform double click
- `modifiers` - Modifier keys to press (Alt, Control, ControlOrMeta, Meta, Shift)

### playwright-browser_type

Type text into editable element.

**Parameters:**
- `element` (required) - Human-readable element description
- `ref` (required) - Exact target element reference
- `text` (required) - Text to type
- `slowly` - Type one character at a time (default: false)
- `submit` - Press Enter after typing

### playwright-browser_fill_form

Fill multiple form fields.

**Parameters:**
- `fields` (required) - Array of fields to fill
  - Each field: `name`, `type` (textbox, checkbox, radio, combobox, slider), `ref`, `value`

### playwright-browser_select_option

Select an option in a dropdown.

**Parameters:**
- `element` (required) - Human-readable element description
- `ref` (required) - Exact target element reference
- `values` (required) - Array of values to select

### playwright-browser_hover

Hover over element on page.

**Parameters:**
- `element` (required) - Human-readable element description
- `ref` (required) - Exact target element reference

### playwright-browser_drag

Perform drag and drop between two elements.

**Parameters:**
- `startElement` (required) - Source element description
- `startRef` (required) - Source element reference
- `endElement` (required) - Target element description
- `endRef` (required) - Target element reference

### playwright-browser_press_key

Press a key on the keyboard.

**Parameters:**
- `key` (required) - Key name (e.g., `ArrowLeft`, `a`)

### playwright-browser_evaluate

Evaluate JavaScript expression on page or element.

**Parameters:**
- `function` (required) - JavaScript function: `() => { /* code */ }` or `(element) => { /* code */ }`
- `element` - Human-readable element description (optional)
- `ref` - Exact element reference (optional)

### playwright-browser_wait_for

Wait for text to appear, disappear, or time to pass.

**Parameters:**
- `text` - Text to wait for to appear
- `textGone` - Text to wait for to disappear
- `time` - Time to wait in seconds

### playwright-browser_tabs

List, create, close, or select a browser tab.

**Parameters:**
- `action` (required) - Operation to perform (list, new, close, select)
- `index` - Tab index for close/select operations

### playwright-browser_resize

Resize the browser window.

**Parameters:**
- `width` (required) - Window width
- `height` (required) - Window height

### playwright-browser_close

Close the browser page.

### playwright-browser_console_messages

Returns all console messages from the page.

### playwright-browser_network_requests

Returns all network requests since loading the page.

### playwright-browser_handle_dialog

Handle a dialog (alert, confirm, prompt).

**Parameters:**
- `accept` (required) - Whether to accept the dialog
- `promptText` - Text for prompt dialog

### playwright-browser_file_upload

Upload one or multiple files.

**Parameters:**
- `paths` - Array of absolute file paths to upload (if omitted, file chooser is cancelled)

### playwright-browser_install

Install the browser specified in the config.

**When to use:** If you get an error about the browser not being installed.

## File Operations

### view

View files and directories.

**Parameters:**
- `path` (required) - Full absolute path to file or directory
- `view_range` - Optional line number range for files [start, end] (e.g., [11, 12] or [10, -1] for to end)
- `forceReadLargeFiles` - Skip large file check (default: false)

**Behavior:**
- Image files: Returns base64-encoded data with MIME type
- Other files: Displays content with line numbers
- Directories: Lists non-hidden files/directories up to 2 levels deep

**When to use:** Exploring repository structure, reading file contents, checking directory listings.

### create

Create new files.

**Parameters:**
- `path` (required) - Full absolute path to file to create
- `file_text` - The content of the file

**Important:**
- Cannot be used if file already exists
- Parent directories must exist
- Path must be absolute

### edit

Make string replacements in files.

**Parameters:**
- `path` (required) - Full absolute path to file to edit
- `old_str` (required) - The string to replace (must match exactly, preserve whitespace)
- `new_str` - The replacement string

**Important:**
- Replaces exactly one occurrence
- `old_str` must match EXACTLY (including whitespace)
- If not unique, replacement will not be performed
- Include enough context to make `old_str` unique
- Multiple edits in one response are applied sequentially
- Path must be absolute

**When to use:** Making precise, surgical code changes.

## Code Search Tools

### grep

Fast and precise code search using ripgrep. Search for patterns in file contents.

**Parameters:**
- `pattern` (required) - Regular expression pattern to search for
- `path` - File or directory to search (defaults to current working directory)
- `output_mode` - Output format (content, files_with_matches, count) - default: files_with_matches
- `type` - File type filter (js, py, rust, go, java, etc.)
- `glob` - Glob pattern to filter files (e.g., "*.js", "*.{ts,tsx}")
- `-i` - Case insensitive search
- `-n` - Show line numbers (requires output_mode: "content")
- `-A` - Lines of context after match (requires output_mode: "content")
- `-B` - Lines of context before match (requires output_mode: "content")
- `-C` - Lines of context before and after match (requires output_mode: "content")
- `multiline` - Enable multiline mode (default: false)
- `head_limit` - Limit output to first N results

**Important:**
- Literal braces need escaping: `interface\{\}` to find `interface{}`
- Default behavior matches within single lines only
- Use `multiline: true` for cross-line patterns
- Defaults to "files_with_matches" mode for efficiency

**When to use:** Finding code patterns, searching for specific strings, locating implementations.

### glob

Fast file pattern matching using glob patterns.

**Parameters:**
- `pattern` (required) - Glob pattern to match files
  - `*` matches any characters within a path segment
  - `**` matches any characters across multiple path segments
  - `?` matches a single character
  - `{a,b}` matches either a or b
- `path` - Directory to search in (defaults to current working directory)

**When to use:** Finding files by name patterns, discovering file types.

## Context7 Documentation Tools

### context7-resolve-library-id

Resolves a package/product name to a Context7-compatible library ID.

**Parameters:**
- `libraryName` (required) - Library name to search for
- `query` (required) - The user's original question or task (used for ranking results by relevance)

**Important:**
- MUST call this before `query-docs` to obtain valid library ID
- UNLESS user explicitly provides library ID in format `/org/project` or `/org/project/version`
- Do not call more than 3 times per question
- Do not include sensitive information in query

**When to use:** Before querying documentation, to find the correct library identifier.

### context7-query-docs

Retrieves and queries up-to-date documentation and code examples from Context7.

**Parameters:**
- `libraryId` (required) - Exact Context7-compatible library ID (from `resolve-library-id`)
- `query` (required) - Specific question or task

**Important:**
- Must call `resolve-library-id` first (unless user provides explicit library ID)
- Do not call more than 3 times per question
- Be specific in your query
- Do not include sensitive information

**When to use:** Getting current documentation, finding code examples, understanding library APIs.

## Bash & Terminal

### bash

Run a Bash command in an interactive Bash session.

**Parameters:**
- `command` (required) - The Bash command and arguments to run
- `description` (required) - Short human-readable description (max 100 chars)
- `sessionId` - Session identifier for persistent sessions (optional)
- `mode` - Execution mode (sync, async, detached) - default: sync
- `initial_wait` - Seconds to wait for initial output in sync mode (default: 10, range: 10-600)

**Modes:**
- `sync` - Runs synchronously, waits for completion
- `async` - Runs asynchronously in background attached to session
- `detached` - Runs asynchronously, persists after process shutdown

**Important:**
- No internet access via this tool
- Can run Python, Node.js, and Go code
- State is saved across calls with same sessionId
- Can install packages with `apt`, `pip`, `npm`, `go`
- For long-running commands, use appropriate `initial_wait`

**When to use:** Running tests, building code, linting, installing dependencies, executing scripts.

### write_bash

Send input to a running Bash command or session.

**Parameters:**
- `sessionId` (required) - Session ID from async bash command
- `delay` (required) - Seconds to wait before reading output
- `input` - Input to send (text, {up}, {down}, {left}, {right}, {enter}, {backspace})

**When to use:** Interacting with interactive tools, providing input to running processes.

### read_bash

Read output from a Bash command.

**Parameters:**
- `sessionId` (required) - Session ID from async bash command
- `delay` - Seconds to wait before reading output

**When to use:** Checking output from async commands, polling for completion.

### stop_bash

Stop a running Bash command by terminating the session.

**Parameters:**
- `sessionId` (required) - Session ID to terminate

**Important:**
- Terminates entire Bash session and process
- Environment variables will need to be redefined if reusing session ID

### list_bash

List all active Bash sessions.

**When to use:** Discovering active sessions, finding session IDs.

## Memory & Progress Tools

### store_memory

Store a fact about the codebase for future use.

**Parameters:**
- `subject` (required) - Topic of the memory (1-2 words, e.g., "naming conventions", "testing practices")
- `fact` (required) - Clear, short description (max 200 chars)
- `citations` (required) - Source of the fact (file:line or "User input: ...")
- `reason` (required) - Detailed explanation of why this is being stored (2-3+ sentences)
- `category` (required) - Type of memory:
  - `bootstrap_and_build` - How to bootstrap and build the project
  - `user_preferences` - Coding style, preferences, favorite libraries
  - `general` - File-independent facts
  - `file_specific` - Information about specific files

**When to use:**
- Storing important conventions or best practices
- Remembering build/test commands that have been verified
- Saving architectural patterns or design decisions
- Recording user preferences

**Examples:**
- "Use JWT for authentication."
- "Follow PEP 257 docstring conventions."
- "The code can be built with `npm run build`"

### report_progress

Report progress on the task and commit changes.

**Parameters:**
- `commitMessage` (required) - Short single line commit message
- `prDescription` (required) - Markdown checklist showing completed and remaining work

**Important:**
- Use only when you have meaningful progress to report
- Commits and pushes changes automatically
- Runs `git add .`, `git commit`, `git push`
- Use markdown checklists: `- [x]` completed, `- [ ]` pending
- Keep checklist structure consistent between updates
- Only include checklist in prDescription (no headers or summaries)

**When to use:**
- After completing a meaningful unit of work
- Before running security checks
- When you've made code changes to commit
- To update the plan in the PR description

## Security & Quality Tools

### code_review

Request automated code review for PR changes.

**Parameters:**
- `prTitle` (required) - Title for the pull request
- `prDescription` (required) - Description explaining the task and high-level changes

**Important:**
- Run BEFORE finalizing session and completing task
- Run BEFORE codeql_checker
- Review comments may be incorrect - use judgment
- If significant changes made after review, run again

**When to use:** Before finalizing any changes, even documentation-only changes.

### codeql_checker

Discover security vulnerabilities in code using CodeQL.

**Important:**
- MUST run after code_review completes
- MUST run when there are code changes
- Investigate all alerts discovered
- Fix any alert that requires only localized change
- Re-run after fixing to verify
- Include Security Summary when finalizing task

**When to use:** After code review, before finalizing changes.

### gh-advisory-database

Check GitHub advisory database for vulnerabilities in dependencies.

**Parameters:**
- `dependencies` (required) - Array of dependencies to check
  - Each: `ecosystem`, `name`, `version`

**Supported ecosystems:**
- actions, composer, erlang, go, maven, npm, nuget, other, pip, pub, rubygems, rust, swift

**Important:**
- Run ALWAYS before adding new dependencies from supported ecosystems
- DO NOT call for unsupported ecosystems
- Feedback MUST be incorporated
- Re-run as appropriate

**When to use:** Before adding or updating dependencies.

## Best Practices

### Parallel Tool Calling

When performing multiple independent operations, ALWAYS call tools simultaneously:

**Good examples:**
- Read multiple files in parallel
- Edit different files in parallel
- Run `git status` + `git diff` together
- Search multiple patterns concurrently

**Bad examples:**
- Reading files one by one when they could be read together
- Making sequential edits to different files

### Sequential Operations

Call tools sequentially when operations depend on previous results:

**Examples:**
- Reading shell output requires sessionID from previous bash command
- Using search results to decide which files to view
- Using file content to determine edit parameters

### Efficient Searching

1. Use `grep` for content search (faster, parallel-safe)
2. Use `glob` for file name search (faster than find/ls)
3. Call multiple searches in one response when possible

### Browser Automation

1. Use `browser_snapshot` for analysis (better than screenshot)
2. Use `browser_take_screenshot` for visual documentation
3. Always provide element descriptions for accessibility

### Memory Storage

Only store facts that:
- Have actionable implications for future tasks
- Are independent of current changes
- Are unlikely to change over time
- Can't always be inferred from limited code samples
- Contain no secrets or sensitive data

## Common Workflows

### Investigating CI Failures

1. `list_workflow_runs` - See recent workflow runs and status
2. `get_job_logs` - Get detailed failure logs
3. Fix the issues
4. `report_progress` - Commit changes

### Making Code Changes

1. `view` - Explore files and understand structure
2. `grep` or `glob` - Find relevant code
3. `edit` - Make precise changes
4. `bash` - Run tests/linters
5. `code_review` - Get automated review
6. Address review feedback
7. `codeql_checker` - Security scan
8. `report_progress` - Commit changes

### Adding Dependencies

1. `gh-advisory-database` - Check for vulnerabilities
2. `bash` - Install dependency (e.g., `npm install package`)
3. Test the changes
4. `report_progress` - Commit

### Researching Documentation

1. `context7-resolve-library-id` - Find library ID
2. `context7-query-docs` - Get documentation
3. Apply learnings to code

### Web Research

1. `web_search` - For recent information, trends, or specific questions
2. `web_fetch` - For reading specific web pages
3. Use information to inform decisions

## Limitations

- Cannot use `git` commands to commit/push directly (use `report_progress`)
- Cannot update issues, PR descriptions, or open new issues/PRs
- Cannot pull branches or fix merge conflicts
- Cannot clone repos
- Cannot use `git reset` or `git rebase` (force push not available)
- Cannot access files in `.github/agents/` directory
- Limited internet access (many domains blocked)
- Cannot share sensitive data with 3rd party systems
- Cannot commit secrets to source code
- Cannot introduce security vulnerabilities
