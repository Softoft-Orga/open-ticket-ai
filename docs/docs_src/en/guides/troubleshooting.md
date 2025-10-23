---
description: Troubleshooting guide for Open Ticket AI covering connection issues, configuration errors, pipeline problems, and common solutions.
---

# Troubleshooting Guide

Common issues and their solutions when working with Open Ticket AI.

## Connection Issues

### Cannot Connect to Ticket System

**Symptoms**:
```
Error: Failed to connect to https://tickets.example.com
ConnectionError: Connection refused
```

**Solutions**:

1. **Verify URL is correct**:
```bash
# Test connection
curl https://tickets.example.com

# Check if HTTPS is required
ping tickets.example.com
```

2. **Check network connectivity**:
```bash
# Test DNS resolution
nslookup tickets.example.com

# Test port access
telnet tickets.example.com 443
```

3. **Verify firewall rules**:
- Check outbound firewall rules
- Verify IP whitelisting
- Check proxy configuration

4. **SSL Certificate issues**:
```yaml
# Temporarily disable SSL verification
plugins:
  - name: otobo_znuny
    config:
      verify_ssl: false  # For testing only
```

### Timeout Errors

**Symptoms**:
```
TimeoutError: Request timed out after 30 seconds
```

**Solutions**:

1. **Increase timeout**:
```yaml
plugins:
  - name: otobo_znuny
    config:
      timeout: 60  # Increase to 60 seconds
```

2. **Reduce batch size**:
```yaml
pipes:
  - pipe_name: fetch_tickets
    search:
      limit: 25  # Reduce from 100
```

3. **Check server performance**:
- Monitor OTOBO/Znuny server load
- Check database performance
- Review server logs

## Authentication Issues

### 401 Unauthorized

**Symptoms**:
```
AuthenticationError: 401 Unauthorized
Invalid API token
```

**Solutions**:

1. **Verify token is set**:
```bash
echo $OTOBO_API_TOKEN
```

2. **Check token validity**:
- Log into OTOBO/Znuny
- Navigate to API token management
- Verify token exists and is active
- Check expiration date

3. **Verify permissions**:
- Ensure token has required permissions
- Check role assignments
- Verify access to queues

4. **Regenerate token**:
- Create new API token
- Update environment variable
- Restart application

### 403 Forbidden

**Symptoms**:
```
PermissionError: 403 Forbidden
Insufficient permissions
```

**Solutions**:

1. **Check user permissions**:
- Verify user has ticket read/write access
- Check queue permissions
- Verify role assignments

2. **Review required permissions**:
- Ticket read: Required for fetching
- Ticket write: Required for updates
- Note creation: Required for adding notes

## Configuration Issues

### Invalid Configuration

**Symptoms**:
```
ConfigurationError: Invalid configuration
Missing required field: 'orchestrator'
```

**Solutions**:

1. **Validate YAML syntax**:
```bash
# Use online YAML validator
# Or install yamllint
uv pip install yamllint
yamllint config.yml
```

2. **Check required fields**:
```yaml
# Minimum required configuration
orchestrator:
  pipelines:
    - name: my_pipeline
      run_every_milli_seconds: 60000
      pipes:
        - pipe_name: some_pipe
```

3. **Verify field types**:
```yaml
# Correct types
run_every_milli_seconds: 60000  # Number
name: "pipeline"  # String
StateType: "Open"  # String

# Wrong types
run_every_milli_seconds: "60000"  # Should be number
```

### Environment Variables Not Expanding

**Symptoms**:
```
Literal string "${OTOBO_API_TOKEN}" in configuration
Environment variable not expanded
```

**Solutions**:

1. **Check variable is set**:
```bash
echo $OTOBO_API_TOKEN
env | grep OTOBO
```

2. **Use correct syntax**:
```yaml
# Correct
api_token: "${OTOBO_API_TOKEN}"
api_token: ${OTOBO_API_TOKEN}

# Wrong - single quotes prevent expansion
api_token: '${OTOBO_API_TOKEN}'
```

3. **Load environment file**:
```bash
# Load .env file
source .env

# Or export directly
export OTOBO_API_TOKEN="your-token"
```

## Pipeline Execution Issues

### No Tickets Fetched

**Symptoms**:
```
INFO: Fetched 0 tickets
Pipeline completed with no results
```

**Solutions**:

1. **Verify search criteria**:
```yaml
# Check StateType is correct
search:
  StateType: "Open"  # Try "open" or other variants
```

2. **Test search manually**:
- Log into ticket system
- Use same search criteria
- Verify tickets exist

3. **Expand search**:
```yaml
# Remove restrictive filters
search:
  limit: 100  # Just limit, no other filters
```

4. **Check queue access**:
```yaml
# Try without queue filter
search:
  StateType: "Open"
  # QueueIDs: [1, 2, 3]  # Comment out temporarily
```

### Classification Fails

**Symptoms**:
```
ClassificationError: Model inference failed
CUDA out of memory
```

**Solutions**:

1. **Use CPU instead of GPU**:
```yaml
plugins:
  - name: hf_local
    config:
      device: "cpu"
```

2. **Reduce batch size**:
```yaml
pipes:
  - pipe_name: classify_queue
    batch_size: 1  # Process one at a time
```

3. **Use smaller model**:
```yaml
plugins:
  - name: hf_local
    config:
      model_name: "distilbert-base-uncased"  # Smaller variant
```

4. **Check model download**:
```bash
# Verify model cache
ls -la ~/.cache/huggingface/

# Clear cache if corrupted
rm -rf ~/.cache/huggingface/
```

### Updates Don't Apply

**Symptoms**:
```
Update succeeded but ticket unchanged
No error but no effect
```

**Solutions**:

1. **Verify field names**:
```yaml
# Correct field names
updates:
  QueueID: 2  # Not queue_id or queueId
  PriorityID: 3  # Not priority_id
```

2. **Check field values**:
```yaml
# Use valid IDs
updates:
  QueueID: 2  # Verify queue with ID 2 exists
  PriorityID: 3  # Verify priority with ID 3 exists
```

3. **Verify ticket is updateable**:
- Check ticket state allows updates
- Verify no locks on ticket
- Check ticket workflow rules

4. **Enable debug logging**:
```bash
open-ticket-ai run --config config.yml --log-level DEBUG
```

## Performance Issues

### Slow Execution

**Symptoms**:
```
Pipeline taking 5+ minutes to complete
High CPU/memory usage
```

**Solutions**:

1. **Reduce ticket limit**:
```yaml
search:
  limit: 25  # Start small, increase gradually
```

2. **Optimize search criteria**:
```yaml
# More specific = faster
search:
  StateType: "Open"
  QueueIDs: [1, 2]  # Specific queues
  create_time_after: "{{ now() - timedelta(hours=1) }}"
```

3. **Increase execution interval**:
```yaml
# Don't run too frequently
run_every_milli_seconds: 300000  # Every 5 minutes
```

4. **Use model caching**:
```yaml
plugins:
  - name: hf_local
    config:
      cache_models: true
```

### High Memory Usage

**Symptoms**:
```
MemoryError: Out of memory
Process killed by OOM killer
```

**Solutions**:

1. **Process smaller batches**:
```yaml
search:
  limit: 10  # Very small batches
```

2. **Use CPU instead of GPU**:
```yaml
plugins:
  - name: hf_local
    config:
      device: "cpu"
```

3. **Clear context between runs**:
```yaml
infrastructure:
  clear_context: true
```

## Debugging Techniques

### Enable Debug Logging

```bash
# Full debug output
open-ticket-ai run --config config.yml --log-level DEBUG

# Or in config
infrastructure:
  log_level: "DEBUG"
```

### Use Dry Run Mode

```bash
# Test without making changes
open-ticket-ai run --config config.yml --dry-run
```

### Validate Configuration

```bash
# Check configuration validity
open-ticket-ai validate --config config.yml
```

### Test Individual Pipes

```python
# Test pipe in isolation
from my_plugin.pipes import MyPipe

pipe = MyPipe()
context = PipelineContext()
result = pipe.execute(context)
print(result)
```

## Log Analysis

### Common Log Patterns

**Successful execution**:
```
[INFO] Pipeline started: my_pipeline
[INFO] Fetched 10 tickets
[INFO] Classified 10 tickets
[INFO] Updated 10 tickets
[INFO] Pipeline completed successfully
```

**Connection error**:
```
[ERROR] Failed to connect to ticket system
[ERROR] ConnectionError: [Errno 111] Connection refused
[DEBUG] Attempted URL: https://tickets.example.com/api/tickets
```

**Authentication error**:
```
[ERROR] Authentication failed
[ERROR] HTTPError: 401 Unauthorized
[DEBUG] Token: ${OTOBO_API_TOKEN} (not expanded!)
```

### Log Location

```bash
# Default log location
~/.local/share/open-ticket-ai/logs/

# Check current log
tail -f ~/.local/share/open-ticket-ai/logs/open-ticket-ai.log

# Search logs
grep ERROR ~/.local/share/open-ticket-ai/logs/open-ticket-ai.log
```

## Getting Help

### Before Asking for Help

1. **Check logs**:
```bash
tail -100 ~/.local/share/open-ticket-ai/logs/open-ticket-ai.log
```

2. **Gather system info**:
```bash
open-ticket-ai info
python --version
uv --version
```

3. **Test with minimal config**:
```yaml
# Simplest possible configuration
plugins:
  - name: otobo_znuny
    config:
      base_url: "${OTOBO_BASE_URL}"
      api_token: "${OTOBO_API_TOKEN}"

orchestrator:
  pipelines:
    - name: test
      run_every_milli_seconds: 60000
      pipes:
        - pipe_name: fetch_tickets
          search:
            limit: 1
```

4. **Create minimal reproduction**:
- Simplify configuration
- Remove unnecessary pipes
- Use test data

### Where to Get Help

- **Documentation**: Check relevant guides
- **GitHub Issues**: Search existing issues
- **GitHub Discussions**: Ask questions
- **Stack Overflow**: Tag with `open-ticket-ai`

### Creating Good Bug Reports

Include:
1. Open Ticket AI version
2. Python version
3. Operating system
4. Configuration (sanitized)
5. Error message/logs
6. Steps to reproduce
7. Expected vs actual behavior

## Related Documentation

- [Configuration Reference](../details/config_reference.md)
- [Testing Guide](../developers/testing.md)
- [Installation Guide](installation.md)
- [First Pipeline](first_pipeline.md)
