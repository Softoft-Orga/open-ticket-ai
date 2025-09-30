# Configuration Examples Quick Reference

This quick reference guide helps you choose the right configuration example for your use case.

## Use Case Comparison

| Example File | Primary Purpose | Key Features | Complexity | Best For |
|--------------|----------------|--------------|------------|----------|
| `add_note_when_in_queue.yml` | Add AI notes to tickets | - Ticket analysis<br>- Sentiment detection<br>- Contextual notes | ⭐⭐ Medium | Teams wanting to add AI insights to specific queues |
| `create_ticket_on_condition.yml` | Auto-create escalation tickets | - Conditional ticket creation<br>- Urgency detection<br>- Automated escalation | ⭐⭐⭐ Advanced | Organizations needing automated escalation workflows |
| `queue_classification.yml` | Route tickets to queues | - AI queue classification<br>- Confidence thresholds<br>- Fallback handling | ⭐⭐ Medium | Standard ticket routing automation |
| `priority_classification.yml` | Set ticket priorities | - Priority prediction<br>- Urgency analysis<br>- SLA optimization | ⭐⭐ Medium | Teams optimizing response times by priority |
| `complete_workflow.yml` | Full automation pipeline | - Queue + Priority classification<br>- Notes for all actions<br>- Error handling<br>- Production-ready | ⭐⭐⭐⭐ Complex | Production deployments needing comprehensive automation |

## Quick Start Guide

### 1. First-time users
**Start with**: `queue_classification.yml` or `priority_classification.yml`
- Simple single-purpose workflows
- Easy to understand and customize
- Good for learning the system

### 2. Want to add AI insights
**Start with**: `add_note_when_in_queue.yml`
- Demonstrates AI analysis without modifying tickets
- Safe to deploy alongside existing processes
- Provides value without disrupting workflows

### 3. Need escalation automation
**Start with**: `create_ticket_on_condition.yml`
- Shows conditional logic and ticket creation
- Useful for complex business rules
- Demonstrates multi-step workflows

### 4. Production deployment
**Start with**: `complete_workflow.yml`
- Full-featured production example
- Includes error handling and fallbacks
- Combines multiple AI operations

## Common Customization Points

### All Examples
```yaml
# Update these in every example:
server_address: "{{ env.OTAI_OTOBO_ZNUNY_SERVER_ADDRESS }}"  # Your server URL
password: "{{ env.OTAI_OTOBO_ZNUNY_PASSWORD }}"              # Your password
token: "{{ env.OTAI_HUGGINGFACE_TOKEN }}"                    # Your HuggingFace token

# Adjust timing (in milliseconds):
run_every_milli_seconds: 60000  # 60 seconds
```

### Queue Names
```yaml
# Replace with your actual queue names:
queue.name: "Incoming"        # Source queue
target_queue: "IT Support"    # Destination queue
```

### AI Models
```yaml
# Update to use your trained models or preferred public models:
model: "open-ticket-ai/queue-classification-german-bert"
model: "open-ticket-ai/priority-classification-german-bert"
```

### Confidence Thresholds
```yaml
# Adjust based on your accuracy requirements:
min_confidence: 0.8           # Higher = more conservative
min_queue_confidence: 0.8
min_priority_confidence: 0.75
```

## Feature Matrix

| Feature | add_note | create_ticket | queue_class | priority_class | complete |
|---------|----------|---------------|-------------|----------------|----------|
| Fetch tickets | ✅ | ✅ | ✅ | ✅ | ✅ |
| AI classification | ✅ | ✅ | ✅ | ✅ | ✅ |
| Update queue | ❌ | ❌ | ✅ | ❌ | ✅ |
| Update priority | ❌ | ❌ | ❌ | ✅ | ✅ |
| Add notes | ✅ | ✅ | ✅ | ✅ | ✅ |
| Create new tickets | ❌ | ✅ | ❌ | ❌ | ❌ |
| Conditional logic | ✅ | ✅ | ✅ | ✅ | ✅ |
| Error handling | ❌ | ❌ | ❌ | ❌ | ✅ |
| Fallback queues | ❌ | ❌ | ✅ | ❌ | ✅ |

## Environment Variables Required

All examples require these environment variables:

```bash
# Required for all examples
export OTAI_OTOBO_ZNUNY_SERVER_ADDRESS="https://your-server.example.com"
export OTAI_OTOBO_ZNUNY_PASSWORD="your_secure_password"

# Required when using AI models from HuggingFace
export OTAI_HUGGINGFACE_TOKEN="hf_your_token_here"
```

## Testing Your Configuration

Before deploying to production:

1. **Validate YAML syntax**:
   ```bash
   python -c "import yaml; yaml.safe_load(open('config.yml'))"
   ```

2. **Start with limited tickets**:
   - Set `limit: 1` in ticket_search_criteria
   - Monitor logs carefully
   - Verify results before scaling up

3. **Test in a non-production environment first**:
   - Use a test queue
   - Create test tickets
   - Verify AI classifications are correct

4. **Monitor performance**:
   - Check execution time
   - Monitor API rate limits
   - Adjust run_every_milli_seconds as needed

## Getting Help

- **Documentation**: See [docs/vitepress_docs/docs_src/en/developers/developer-information.md](../vitepress_docs/docs_src/en/developers/developer-information.md)
- **Integration Guide**: See [docs/vitepress_docs/docs_src/en/guide/otobo-znuny-otrs-integration.md](../vitepress_docs/docs_src/en/guide/otobo-znuny-otrs-integration.md)
- **Issues**: Report problems on GitHub

## Next Steps

1. Choose an example that matches your use case
2. Copy it to your `config.yml`
3. Update environment variables
4. Customize queue names and models
5. Test with `limit: 1`
6. Monitor and adjust
7. Scale up gradually
