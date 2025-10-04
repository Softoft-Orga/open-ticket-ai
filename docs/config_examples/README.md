# Open Ticket AI Configuration Examples

This directory contains example configurations demonstrating various use cases for Open Ticket AI.

> 📚 **Quick Reference**: See [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) for a comparison table and quick start guide.

## Available Examples

### 1. AI Adds Note to Ticket (`add_note_when_in_queue.yml`)

Demonstrates how to configure the AI to automatically add a note to tickets when they are in a specific queue. The AI
analyzes the ticket content and adds contextual information as a note.

**Use Case**: Automatically add analysis notes or suggestions to tickets in a "Review" queue.

### 2. Create Ticket in Specific Case (`create_ticket_on_condition.yml`)

Shows how to automatically create a new ticket when specific conditions are met, such as detecting certain keywords or
patterns in incoming tickets.

**Use Case**: Automatically create follow-up tickets for escalation or specialized handling.

### 3. Queue Classification (`queue_classification.yml`)

Demonstrates AI-powered queue classification where tickets are automatically routed to the appropriate queue based on
their content.

**Use Case**: Automatic ticket routing to departments like IT, HR, Finance, etc.

### 4. Priority Classification (`priority_classification.yml`)

Shows how to automatically set ticket priority based on AI analysis of urgency and importance.

**Use Case**: Ensure critical issues get immediate attention by automatic priority assignment.

### 5. Complete Workflow (`complete_workflow.yml`)

A comprehensive example combining multiple AI operations: classification, note addition, and conditional processing.

**Use Case**: Full automation pipeline with queue routing, priority setting, and contextual notes.

## Configuration Structure

All examples follow the Open Ticket AI configuration schema with these key sections:

- `system`: Ticket system adapter configuration (OTOBO/Znuny/OTRS)
- `general_config`: Logging and pipe class definitions
- `defs`: Reusable pipe definitions
- `orchestrator`: Pipeline orchestration and scheduling

## Using These Examples

1. Copy the relevant example to your `config.yml`
2. Update the environment variables (server addresses, credentials, API tokens)
3. Customize the models, queues, and conditions to match your setup
4. Test with a limited subset of tickets first

## Environment Variables Required

- `OTAI_OTOBO_ZNUNY_SERVER_ADDRESS`: Your ticket system server URL
- `OTAI_OTOBO_ZNUNY_PASSWORD`: Authentication password
- `OTAI_HUGGINGFACE_TOKEN`: HuggingFace API token for AI models (if using HuggingFace models)

## Further Resources

- [Developer Information](../vitepress_docs/docs_src/en/developers/developer-information.md)
- [Architecture Documentation](../vitepress_docs/docs_src/en/developers/architecture.md)
- [OTOBO/Znuny Integration Guide](../vitepress_docs/docs_src/en/guide/otobo-znuny-otrs-integration.md)
