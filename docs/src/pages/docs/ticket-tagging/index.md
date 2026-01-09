---
layout: ../../../layouts/DocsLayout.astro

title: Ticket Tagging AI Documentation
description: "On-prem ticket classification. Tag schema, output format, multilingual behavior, backlog tagging, hardware sizing, and evaluation."
---

# Ticket Tagging AI Documentation

Welcome to the Ticket Tagging AI documentation. This guide covers on-premise ticket classification and automatic tagging using AI.

## What is Ticket Tagging AI?

Ticket Tagging AI is an intelligent classification system that automatically categorizes and tags support tickets. It provides:

- **Automatic Classification**: AI-powered categorization of tickets
- **Custom Tag Schemas**: Define your own classification categories
- **Multilingual Support**: Process tickets in multiple languages
- **On-Premise Deployment**: Keep your data secure within your infrastructure
- **Batch Processing**: Tag existing ticket backlogs efficiently

## Getting Started

### Quick Start

New to Ticket Tagging AI? Start here:

- [Quick Start Guide](/guides/quick_start/) - Get up and running in 5 minutes
- [Installation](/users/installation/) - Install the tagging AI components
- [Configuration](/details/config_reference/) - Set up your tag schema

### Prerequisites

Before using Ticket Tagging AI:

- Python 3.13+
- Sufficient hardware resources (see Hardware Sizing below)
- Open Ticket Automation installed and configured

## Key Features

### AI-Powered Classification

Leverage machine learning for ticket categorization:

- Pre-trained models for common ticket types
- Custom model training with your ticket data
- Multi-label classification support
- Confidence scoring for predictions

### Tag Schema Configuration

Define your classification system:

- Create custom tag categories
- Hierarchical tag structures
- Tag dependencies and rules
- Output format customization

### Multilingual Behavior

Process tickets in any language:

- Automatic language detection
- Language-specific models
- Cross-lingual classification
- Translation integration

### Backlog Processing

Handle existing tickets:

- Bulk tagging operations
- Progress tracking
- Error handling and retry logic
- Performance optimization

## Architecture

### Components

- **Classification Model**: ML model for ticket categorization
- **Tag Engine**: Applies tags based on predictions
- **Schema Manager**: Manages tag definitions and rules
- **Batch Processor**: Handles bulk operations

### Data Flow

1. Ticket content is preprocessed and normalized
2. AI model analyzes text and predicts categories
3. Tag engine applies tags based on schema rules
4. Results are written back to ticket system

## Tag Schema Design

### Best Practices

- Start with broad categories, refine over time
- Keep tag hierarchy shallow (2-3 levels max)
- Use consistent naming conventions
- Document tag meanings clearly
- Review and update schema regularly

### Example Schema

```yaml
tags:
  category:
    - Technical Issue
    - Billing Question
    - Feature Request
    - General Inquiry
  priority:
    - High
    - Medium
    - Low
  department:
    - IT Support
    - Sales
    - Customer Success
```

## Output Format

### Tag Metadata

Each classified ticket includes:

- Predicted tags with confidence scores
- Classification timestamp
- Model version used
- Processing metadata

### Integration

Tag results can be:

- Written to custom ticket fields
- Sent to external systems
- Stored in local database
- Exported for analysis

## Hardware Sizing

### Recommendations

**Small Deployment** (< 1000 tickets/day):
- 4 CPU cores
- 8GB RAM
- 20GB storage

**Medium Deployment** (1000-10,000 tickets/day):
- 8 CPU cores
- 16GB RAM
- 100GB storage
- GPU optional for faster processing

**Large Deployment** (> 10,000 tickets/day):
- 16+ CPU cores
- 32GB+ RAM
- 500GB+ storage
- GPU recommended

### GPU Acceleration

For improved performance:
- NVIDIA GPU with CUDA support
- 8GB+ VRAM recommended
- Compatible with PyTorch/TensorFlow

## Model Evaluation

### Performance Metrics

Track your model's accuracy:

- **Precision**: How many predicted tags are correct
- **Recall**: How many actual tags are found
- **F1 Score**: Balance between precision and recall
- **Confusion Matrix**: Detailed error analysis

### Continuous Improvement

1. Monitor classification accuracy
2. Collect feedback on predictions
3. Retrain models with corrected data
4. A/B test model versions
5. Update tag schema as needed

## Training Custom Models

### Data Requirements

For custom model training:

- Minimum 1000 labeled tickets per category
- Balanced distribution across categories
- Clean, representative data
- Consistent labeling

### Training Process

1. Prepare training dataset
2. Configure model parameters
3. Train model on your data
4. Evaluate on test set
5. Deploy to production

## Advanced Features

### Confidence Thresholds

Set minimum confidence levels:

- Require manual review for low confidence
- Auto-apply high-confidence tags
- Flag uncertain classifications

### Multi-Label Classification

Apply multiple tags per ticket:

- Category + priority + department
- Complex classification scenarios
- Tag correlation analysis

### Active Learning

Improve models over time:

- Flag uncertain predictions for review
- Learn from corrections
- Adaptive model updates

## Developer Resources

For developers working with Ticket Tagging AI:

- [Pipeline Code](/developers/pipeline_code/) - Integration with automation pipelines
- [Services](/developers/services/) - Core classification services
- [Testing](/developers/testing/) - Test your classification logic

## API Reference

### Classification Endpoints

- Classify single ticket
- Batch classification
- Model management
- Schema configuration

### Configuration Options

- Model selection
- Tag schema definition
- Output format
- Performance tuning

## Troubleshooting

### Common Issues

**Low Classification Accuracy**:
- Review training data quality
- Increase training dataset size
- Adjust model parameters
- Refine tag schema

**Performance Problems**:
- Enable GPU acceleration
- Optimize batch sizes
- Add more resources
- Cache model predictions

**Integration Issues**:
- Verify API connectivity
- Check authentication
- Review configuration
- Test with sample data

### Getting Help

- Check the [GitHub Issues](https://github.com/Softoft-Orga/open-ticket-ai/issues)
- Review documentation
- Join community discussions

## Next Steps

Ready to get started?

1. **Install Required Components**: Set up the AI infrastructure
2. **Define Your Tag Schema**: Design your classification system
3. **Test with Sample Data**: Validate on a small dataset
4. **Process Your Backlog**: Tag existing tickets
5. **Enable Real-Time Tagging**: Automate new ticket classification
6. **Monitor and Improve**: Track accuracy and refine models

---

For questions or feedback, please visit our [GitHub repository](https://github.com/Softoft-Orga/open-ticket-ai).
