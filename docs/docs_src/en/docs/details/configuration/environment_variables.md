# Environment Variables Reference

Complete reference for environment variables used in Open Ticket AI configuration.

## Environment Variable Syntax

Use environment variables in YAML configuration:

```yaml
# Required variable
api_token: "${OTOBO_API_TOKEN}"

# Optional with default value
base_url: "${OTOBO_BASE_URL:-https://default.example.com}"

# Nested in templates
note: "User: ${USER}, Time: {{ now() }}"
```

## Required Variables

These variables must be set for the application to work:

### Ticket System Integration

**OTOBO_API_TOKEN** or **OTOBO_USERNAME** and **OTOBO_PASSWORD**
- Authentication credentials for OTOBO/Znuny
- Set one of: API token (recommended) or username/password
- Example: `export OTOBO_API_TOKEN="abc123..."`

**OTOBO_BASE_URL**
- Base URL of your OTOBO/Znuny instance
- Must include protocol (http/https)
- Example: `export OTOBO_BASE_URL="https://tickets.example.com"`

### Machine Learning (if using HF Local plugin)

**HF_MODEL_NAME** (optional)
- HuggingFace model identifier
- Can be specified in config instead
- Example: `export HF_MODEL_NAME="bert-base-uncased"`

**HF_HOME** (optional)
- HuggingFace cache directory
- Defaults to `~/.cache/huggingface`
- Example: `export HF_HOME="/data/models"`

## Optional Configuration Overrides

### Application Settings

**LOG_LEVEL**
- Logging verbosity: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Default: INFO
- Example: `export LOG_LEVEL="DEBUG"`

**LOG_IMPL**
- Logging implementation: stdlib, structlog
- Default: stdlib
- Example: `export LOG_IMPL="structlog"`

**ENVIRONMENT**
- Deployment environment: development, staging, production
- Affects logging and error handling
- Example: `export ENVIRONMENT="production"`

**CONFIG_PATH**
- Path to configuration file
- Default: `./config.yml`
- Example: `export CONFIG_PATH="/etc/open-ticket-ai/config.yml"`

### Performance Settings

**MAX_WORKERS**
- Number of worker threads
- Default: Number of CPU cores
- Example: `export MAX_WORKERS="4"`

**BATCH_SIZE**
- Batch size for processing
- Default: 10
- Example: `export BATCH_SIZE="50"`

### Integration Settings

**OTOBO_VERIFY_SSL**
- Enable/disable SSL certificate verification
- Default: true
- Example: `export OTOBO_VERIFY_SSL="false"`

**OTOBO_TIMEOUT**
- Request timeout in seconds
- Default: 30
- Example: `export OTOBO_TIMEOUT="60"`

**OTOBO_MAX_RETRIES**
- Maximum retry attempts for failed requests
- Default: 3
- Example: `export OTOBO_MAX_RETRIES="5"`

## Security Best Practices

### 1. Never Commit Secrets

```bash
# BAD: Don't do this
api_token: "hardcoded-secret-123"

# GOOD: Use environment variables
api_token: "${OTOBO_API_TOKEN}"
```

### 2. Use .env Files Locally

Create `.env` file for local development:

```bash
# .env (add to .gitignore!)
OTOBO_API_TOKEN="your-token-here"
OTOBO_BASE_URL="https://dev.example.com"
LOG_LEVEL="DEBUG"
```

Load with:
```bash
source .env
# or
export $(cat .env | xargs)
```

### 3. Use Secret Management in Production

Production secrets should be managed securely:
- Kubernetes Secrets
- AWS Secrets Manager
- Azure Key Vault
- HashiCorp Vault

### 4. Principle of Least Privilege

- Create service accounts with minimum required permissions
- Use read-only tokens where possible
- Rotate credentials regularly

### 5. Environment-Specific Values

```bash
# Development
export OTOBO_BASE_URL="https://dev.tickets.example.com"
export LOG_LEVEL="DEBUG"

# Production
export OTOBO_BASE_URL="https://tickets.example.com"
export LOG_LEVEL="WARNING"
```

## Setting Environment Variables

### Linux/macOS

```bash
# Current session
export OTOBO_API_TOKEN="your-token"

# Persistent (add to ~/.bashrc or ~/.zshrc)
echo 'export OTOBO_API_TOKEN="your-token"' >> ~/.bashrc
source ~/.bashrc
```

### Windows

```powershell
# Current session
$env:OTOBO_API_TOKEN="your-token"

# Persistent (PowerShell)
[System.Environment]::SetEnvironmentVariable('OTOBO_API_TOKEN', 'your-token', 'User')

# Persistent (Command Prompt)
setx OTOBO_API_TOKEN "your-token"
```

### Docker

```bash
# Command line
docker run -e OTOBO_API_TOKEN="your-token" open-ticket-ai

# Docker Compose
services:
  app:
    environment:
      - OTOBO_API_TOKEN=${OTOBO_API_TOKEN}
    env_file:
      - .env
```

### Kubernetes

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: open-ticket-ai-secrets
type: Opaque
data:
  otobo-api-token: <base64-encoded-token>
---
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: app
      env:
        - name: OTOBO_API_TOKEN
          valueFrom:
            secretKeyRef:
              name: open-ticket-ai-secrets
              key: otobo-api-token
```

## Validation

Environment variables are validated on startup:
- Required variables must be set
- URLs must be valid
- Numeric values must be in valid ranges
- Enum values must match allowed options

## Troubleshooting

### Variable Not Expanding

```yaml
# Wrong: quotes prevent expansion
api_token: '${OTOBO_API_TOKEN}'  # Treated as literal string

# Correct: no quotes or double quotes
api_token: "${OTOBO_API_TOKEN}"
api_token: ${OTOBO_API_TOKEN}
```

### Variable Not Set

Check if variable is set:
```bash
echo $OTOBO_API_TOKEN
env | grep OTOBO
```

### Default Values Not Working

```yaml
# Syntax: ${VAR:-default}
base_url: "${OTOBO_URL:-https://default.com}"
```

## Related Documentation

- [Configuration Reference](../config_reference.md)
- [Configuration Structure](config_structure.md)
- [Installation Guide](../../guides/installation.md)
