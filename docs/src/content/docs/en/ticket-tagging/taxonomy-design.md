---
title: Taxonomy Design
description: 'Design and structure your ticket classification taxonomy for effective automated tagging and categorization.'
lang: en
nav:
  group: Ticket Tagging
  order: 1
---

# Taxonomy Design

Learn how to design an effective taxonomy for automated ticket tagging and classification.

## Overview

A well-designed taxonomy is the foundation of successful automated ticket tagging. Your taxonomy should reflect your organization's structure, processes, and ticket handling requirements.

## Taxonomy Principles

### Keep It Simple

Start with a manageable number of categories:

- **Initial rollout**: 5-10 main categories
- **Mature system**: 15-25 categories maximum
- **Too many categories**: Reduces classification accuracy

### Make It Distinct

Categories should be clearly differentiated:

- Avoid overlapping definitions
- Use clear, descriptive names
- Define explicit scope for each category
- Document edge cases and boundary conditions

### Align with Business Processes

Your taxonomy should match how your organization works:

- Reflect existing team structures
- Map to support queues or departments
- Consider SLA requirements
- Account for escalation paths

## Taxonomy Structure

### Hierarchical Taxonomy

Organize categories in a tree structure:

```
IT Support
├── Hardware
│   ├── Desktop Issues
│   ├── Laptop Issues
│   └── Peripherals
├── Software
│   ├── Application Errors
│   ├── License Requests
│   └── Installation Support
└── Network
    ├── Connectivity Issues
    ├── VPN Access
    └── WiFi Problems
```

**Advantages**:

- Clear organization
- Supports multi-level classification
- Easy to understand and maintain

**Disadvantages**:

- More complex to implement
- Requires careful training data preparation
- May need multi-stage classification

### Flat Taxonomy

Single-level categories:

```
- Hardware Issues
- Software Errors
- Network Problems
- Access Requests
- Password Resets
- Account Management
- Email Issues
- Printer Support
```

**Advantages**:

- Simple to implement
- Easier to train models
- Faster classification

**Disadvantages**:

- Limited granularity
- May become unwieldy with many categories

## Defining Categories

### Category Definition Template

For each category, document:

```markdown
## Category Name: [Name]

**Description**: [Brief description of what belongs in this category]

**Scope**: [What is included]

**Examples**:

- Example ticket 1
- Example ticket 2
- Example ticket 3

**Exclusions**: [What is NOT included]

**Keywords**: [Common terms associated with this category]

**Priority**: [Typical priority level]

**Target Queue/Team**: [Where these tickets should be routed]
```

### Example Category Definition

```markdown
## Category Name: Password Reset

**Description**: Requests to reset forgotten passwords or unlock locked accounts

**Scope**:

- Forgotten password requests
- Account lockouts due to failed login attempts
- Password expiration issues

**Examples**:

- "I forgot my password and can't log in"
- "My account is locked after too many failed attempts"
- "I need to reset my password for the customer portal"

**Exclusions**:

- New account creation (→ Account Management)
- Permission/access level changes (→ Access Requests)
- Password policy questions (→ General IT Support)

**Keywords**: password, reset, locked, unlock, forgot, login, access

**Priority**: Medium (affects productivity)

**Target Queue/Team**: IT Help Desk
```

## Testing Your Taxonomy

### Manual Classification Test

Before automating, test your taxonomy manually:

1. **Sample Selection**: Select 100-200 recent tickets
2. **Multiple Reviewers**: Have 2-3 people classify the same tickets
3. **Measure Agreement**: Calculate inter-rater agreement
4. **Target Agreement**: Aim for >80% agreement between reviewers

### Common Issues

**Low Agreement** (<60%):

- Categories may overlap too much
- Definitions may be unclear
- Need better examples and documentation

**Medium Agreement** (60-80%):

- Some edge cases need clarification
- May need to merge similar categories
- Refinement of category boundaries needed

**High Agreement** (>80%):

- Taxonomy is ready for automation
- Proceed with model training

## Iteration and Refinement

### Start Small

Begin with core categories:

```
Phase 1 (Week 1-2):
- 5-7 most common ticket types
- Cover 60-70% of ticket volume

Phase 2 (Week 3-4):
- Add 5-7 more categories
- Target 80-90% coverage

Phase 3 (Month 2+):
- Fine-tune and add edge cases
- Achieve >90% coverage
```

### Monitor and Adjust

After deployment, continuously monitor:

- **Classification accuracy**: By category
- **Confidence scores**: Identify uncertain classifications
- **Misclassifications**: Look for patterns
- **New ticket types**: Identify gaps in taxonomy

### When to Split Categories

Consider splitting when:

- Category represents >20% of all tickets
- Clear subcategories exist
- Different handling processes needed
- SLA requirements differ

### When to Merge Categories

Consider merging when:

- Category has <2% of tickets
- Categories are frequently confused
- Similar handling processes
- Same team handles both

## Best Practices

### DO ✅

- Start with business-driven categories
- Document each category clearly
- Test manually before automating
- Iterate based on feedback
- Monitor performance continuously

### DON'T ❌

- Create too many categories initially
- Use vague or overlapping definitions
- Skip manual validation
- Set and forget - taxonomies evolve
- Ignore low-confidence predictions

## Tools and Resources

### Documentation Template

Use a shared document to define your taxonomy:

```
docs/
├── taxonomy/
│   ├── overview.md
│   ├── categories/
│   │   ├── hardware.md
│   │   ├── software.md
│   │   └── ...
│   └── changelog.md
```

### Review Schedule

- **Weekly**: Review misclassifications
- **Monthly**: Analyze category distribution
- **Quarterly**: Major taxonomy review
- **Annually**: Complete taxonomy redesign consideration

## Next Steps

After designing your taxonomy:

1. **Prepare Training Data**: Gather and label historical tickets
2. **Configure Model**: Set up classification model with your categories
3. **Test Classification**: Validate on hold-out data
4. **Monitor Performance**: Track accuracy and adjust as needed

## Related Documentation

- [Tag Mapping](tag-mapping.md) - Map classifications to ticket fields
- [Using Model](using-model.md) - Configure and use classification models
- [Hardware Sizing](hardware-sizing.md) - Infrastructure requirements for classification
