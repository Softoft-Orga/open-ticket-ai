---
title: Hardware Sizing
description: "Hardware and infrastructure requirements for running ticket classification models at different scales."
lang: en
nav:
  group: Ticket Tagging
  order: 2
---
# Hardware Sizing

Understand the hardware requirements for running ticket classification models at different scales.

## Overview

Hardware requirements for ticket classification depend on several factors:

- Model size and complexity
- Number of tickets processed
- Classification frequency
- Response time requirements
- Budget constraints

## Quick Reference

| Scale | Tickets/Day | Min RAM | Min CPU | GPU | Model Type |
|-------|-------------|---------|---------|-----|------------|
| Small | <1,000 | 512 MB | 1 core | No | Simple ML |
| Medium | 1,000-10,000 | 2 GB | 2 cores | Optional | BERT-based |
| Large | 10,000-100,000 | 8 GB | 4 cores | Recommended | BERT/Large |
| Enterprise | >100,000 | 16+ GB | 8+ cores | Required | Custom/Fine-tuned |

## Deployment Models

### CPU-Only Deployment

**Best for**:
- Small to medium ticket volumes (<10,000/day)
- Budget-conscious deployments
- Simpler models (distilled BERT, small transformers)

**Recommended Specs**:

```yaml
Small Scale:
  CPU: 1-2 cores (2.0+ GHz)
  RAM: 512 MB - 2 GB
  Storage: 5 GB
  Network: Standard

Medium Scale:
  CPU: 2-4 cores (2.5+ GHz)
  RAM: 2-4 GB
  Storage: 10 GB
  Network: Standard
```

**Expected Performance**:
- Classification time: 200-500ms per ticket
- Throughput: 100-500 tickets/minute
- Model loading time: 5-30 seconds

### GPU-Accelerated Deployment

**Best for**:
- Large ticket volumes (>10,000/day)
- Real-time classification requirements
- Large transformer models
- Fine-tuning and retraining

**Recommended Specs**:

```yaml
Medium-Large Scale:
  CPU: 4-8 cores
  RAM: 8-16 GB
  GPU: NVIDIA T4 or better (16 GB VRAM)
  Storage: 20 GB SSD
  Network: High bandwidth

Enterprise Scale:
  CPU: 8-16 cores
  RAM: 16-32 GB
  GPU: NVIDIA A10/A100 (24-80 GB VRAM)
  Storage: 50+ GB NVMe SSD
  Network: High bandwidth, low latency
```

**Expected Performance**:
- Classification time: 10-50ms per ticket
- Throughput: 1,000-10,000 tickets/minute
- Model loading time: 2-10 seconds

## Model Size Impact

### Small Models (50-150 MB)

**Examples**:
- DistilBERT
- MiniLM
- TinyBERT

**Requirements**:
- RAM: 512 MB - 1 GB
- CPU: 1-2 cores sufficient
- GPU: Not required

**Use Cases**:
- Low-volume environments
- Cost-sensitive deployments
- Edge deployments

### Medium Models (300-500 MB)

**Examples**:
- BERT-base
- RoBERTa-base
- Custom fine-tuned models

**Requirements**:
- RAM: 2-4 GB
- CPU: 2-4 cores recommended
- GPU: Optional, improves performance 5-10x

**Use Cases**:
- Most production deployments
- Balanced accuracy/performance
- Standard ticket volumes

### Large Models (1-5 GB)

**Examples**:
- BERT-large
- RoBERTa-large
- GPT-based models
- Custom ensemble models

**Requirements**:
- RAM: 8-16 GB
- CPU: 4-8 cores minimum
- GPU: Highly recommended (T4 or better)

**Use Cases**:
- High-accuracy requirements
- Complex classification tasks
- Multi-label classification
- High-volume processing

## Containerized Deployments

### Docker Resource Limits

Configure appropriate resource limits:

```yaml
# docker-compose.yml
services:
  ticket-classifier:
    image: openticketai/engine:latest
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

### Kubernetes Pod Sizing

```yaml
# kubernetes-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: ticket-classifier
spec:
  containers:
  - name: classifier
    image: openticketai/engine:latest
    resources:
      requests:
        memory: "2Gi"
        cpu: "1000m"
      limits:
        memory: "4Gi"
        cpu: "2000m"
```

### Resource Monitoring

Monitor these metrics:

- **CPU Usage**: Should be <80% average
- **Memory Usage**: Should have 20% headroom
- **Classification Latency**: P95 latency under target
- **Queue Depth**: Tickets waiting for classification

## Scaling Strategies

### Vertical Scaling

Increase resources on a single instance:

```yaml
# Start
RAM: 2 GB, CPU: 2 cores

# Scale up
RAM: 4 GB, CPU: 4 cores

# Further scaling
RAM: 8 GB, CPU: 8 cores
```

**Pros**:
- Simple to implement
- No code changes required
- Easy to manage

**Cons**:
- Limited by hardware maximums
- Single point of failure
- Potentially expensive

### Horizontal Scaling

Deploy multiple instances:

```yaml
# Load balancer
└── Classifier Instance 1 (2 GB, 2 cores)
└── Classifier Instance 2 (2 GB, 2 cores)
└── Classifier Instance 3 (2 GB, 2 cores)
```

**Pros**:
- Better reliability
- Handles traffic spikes
- More cost-effective at scale

**Cons**:
- More complex setup
- Requires load balancer
- Shared state considerations

### Auto-Scaling

Dynamic scaling based on load:

```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ticket-classifier
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ticket-classifier
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Storage Requirements

### Model Storage

- **Base models**: 100 MB - 5 GB
- **Fine-tuned models**: +100-500 MB
- **Cache**: 1-5 GB
- **Logs**: 100 MB - 1 GB/day

### Recommended Setup

```
Disk Layout:
├── /models/ (10-20 GB, SSD)
├── /cache/ (5 GB, SSD)
├── /logs/ (rotating, 10 GB)
└── /data/ (variable, standard storage)
```

## Network Requirements

### Bandwidth

- **Model downloads**: Initial 1-5 GB, then minimal
- **API traffic**: 1-10 KB per ticket
- **Monitoring**: 1-5 MB/hour

### Latency

- **Internal**: <10ms ideal
- **External APIs**: <100ms acceptable
- **Model serving**: <50ms target

## Cost Optimization

### Development Environment

Minimal cost setup for testing:

```yaml
Cloud Instance:
  Type: t3.small (AWS) / e2-small (GCP)
  vCPU: 2
  RAM: 2 GB
  Cost: ~$15-20/month
```

### Production Small Scale

Cost-effective production:

```yaml
Cloud Instance:
  Type: t3.medium (AWS) / e2-medium (GCP)
  vCPU: 2
  RAM: 4 GB
  Cost: ~$30-40/month
```

### Production Large Scale

High-performance production:

```yaml
Cloud Instance:
  Type: c5.2xlarge (AWS) / c2-standard-8 (GCP)
  vCPU: 8
  RAM: 16 GB
  GPU: Optional T4
  Cost: ~$150-300/month (CPU) or ~$400-600/month (GPU)
```

## Performance Testing

### Benchmarking Your Setup

Test classification performance:

```bash
# Load test with 100 concurrent requests
ab -n 1000 -c 100 http://localhost:8080/classify

# Monitor during test
docker stats ticket-classifier

# Check response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8080/classify
```

### Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Latency P50 | <200ms | Median response time |
| Latency P95 | <500ms | 95th percentile |
| Latency P99 | <1000ms | 99th percentile |
| Throughput | >100/min | Tickets classified |
| CPU Usage | <80% | Average utilization |
| Memory Usage | <80% | Peak utilization |

## Troubleshooting

### Out of Memory Errors

**Symptoms**:
```
MemoryError: Unable to allocate array
Container killed (OOMKilled)
```

**Solutions**:
1. Increase memory allocation
2. Use smaller model variant
3. Reduce batch size
4. Enable model quantization

### Slow Classification

**Symptoms**:
- Latency >1 second per ticket
- Growing processing queue

**Solutions**:
1. Enable GPU acceleration
2. Use model distillation
3. Optimize batch processing
4. Add more replicas

### High CPU Usage

**Symptoms**:
- CPU constantly >90%
- Throttled performance

**Solutions**:
1. Add more CPU cores
2. Optimize model inference
3. Implement request queuing
4. Scale horizontally

## Best Practices

### DO ✅

- Start with CPU-only for testing
- Monitor resource usage continuously
- Set appropriate resource limits
- Plan for 2x current load
- Use caching where possible
- Implement health checks

### DON'T ❌

- Under-provision memory (causes OOM)
- Skip performance testing
- Ignore monitoring metrics
- Over-provision unnecessarily
- Mix production and development workloads

## Next Steps

After sizing your hardware:

1. **Deploy Infrastructure**: Set up servers/containers
2. **Install Model**: Download and configure classification model
3. **Performance Test**: Validate against your requirements
4. **Monitor**: Set up metrics and alerting

## Related Documentation

- [Using Model](using-model.md) - Configure and deploy classification models
- [Taxonomy Design](taxonomy-design.md) - Design your classification taxonomy
- [Tag Mapping](tag-mapping.md) - Map classifications to ticket fields
