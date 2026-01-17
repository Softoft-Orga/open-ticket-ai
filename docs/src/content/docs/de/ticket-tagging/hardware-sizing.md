---
title: Hardware-Größenbestimmung
description: 'Hardware- und Infrastruktur-Anforderungen für den Betrieb von Ticket‑Klassifizierungs‑Modellen in verschiedenen Skalierungen.'
lang: en
nav:
  group: Ticket Tagging
  order: 2
---

# Hardware-Größenbestimmung

Verstehen Sie die Hardware‑Anforderungen für den Betrieb von Ticket‑Klassifizierungs‑Modellen in verschiedenen Skalierungen.

## Überblick

Hardware‑Anforderungen für die Ticket‑Klassifizierung hängen von mehreren Faktoren ab:

- Modellgröße und -komplexität
- Anzahl der zu verarbeitenden Tickets
- Klassifizierungs‑Frequenz
- Anforderungen an die Reaktionszeit
- Budget‑Beschränkungen

## Schnellreferenz

| Skala      | Tickets/Tag    | Min RAM | Min CPU  | GPU         | Model Type        |
| ---------- | -------------- | ------- | -------- | ----------- | ----------------- |
| Klein      | <1.000         | 512 MB  | 1 Kern   | Nein        | Simple ML         |
| Mittel     | 1.000‑10.000   | 2 GB    | 2 Kerne  | Optional    | BERT-based        |
| Groß       | 10.000‑100.000 | 8 GB    | 4 Kerne  | Empfohlen   | BERT/Large        |
| Enterprise | >100.000       | 16+ GB  | 8+ Kerne | Erforderlich| Custom/Fine-tuned |

## Bereitstellungs‑Modelle

### CPU‑Only‑Bereitstellung

**Am besten für**:

- Kleine bis mittlere Ticket‑Volumina (<10.000/Tag)
- Budget‑bewusste Deployments
- Einfachere Modelle (distilled BERT, kleine Transformer)

**Empfohlene Specs**:

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

**Erwartete Leistung**:

- Klassifizierungszeit: 200‑500 ms pro Ticket
- Durchsatz: 100‑500 Tickets/Minute
- Modell‑Ladezeit: 5‑30 Sekunden

### GPU‑Beschleunigte Bereitstellung

**Am besten für**:

- Große Ticket‑Volumina (>10.000/Tag)
- Echtzeit‑Klassifizierungs‑Anforderungen
- Große Transformer‑Modelle
- Fine‑Tuning und Retraining

**Empfohlene Specs**:

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

**Erwartete Leistung**:

- Klassifizierungszeit: 10‑50 ms pro Ticket
- Durchsatz: 1.000‑10.000 Tickets/Minute
- Modell‑Ladezeit: 2‑10 Sekunden

## Einfluss der Modellgröße

### Kleine Modelle (50‑150 MB)

**Beispiele**:

- DistilBERT
- MiniLM
- TinyBERT

**Anforderungen**:

- RAM: 512 MB ‑ 1 GB
- CPU: 1‑2 Kerne ausreichend
- GPU: Nicht erforderlich

**Anwendungsfälle**:

- Niedrig‑Volumen‑Umgebungen
- Kosten‑sensitives Deployment
- Edge‑Deployments

### Mittlere Modelle (300‑500 MB)

**Beispiele**:

- BERT-base
- RoBERTa-base
- Custom fine‑tuned models

**Anforderungen**:

- RAM: 2‑4 GB
- CPU: 2‑4 Kerne empfohlen
- GPU: Optional, verbessert die Leistung 5‑10×

**Anwendungsfälle**:

- Die meisten Produktions‑Deployments
- Ausgewogenes Verhältnis von Genauigkeit und Performance
- Standard‑Ticket‑Volumina

### Große Modelle (1‑5 GB)

**Beispiele**:

- BERT-large
- RoBERTa-large
- GPT‑basierte Modelle
- Custom ensemble models

**Anforderungen**:

- RAM: 8‑16 GB
- CPU: 4‑8 Kerne mindestens
- GPU: Sehr empfehlenswert (T4 oder besser)

**Anwendungsfälle**:

- Hohe Genauigkeits‑Anforderungen
- Komplexe Klassifizierungs‑Aufgaben
- Multi‑Label‑Klassifizierung
- Hoch‑Volumen‑Verarbeitung

## Containerisierte Deployments

### Docker‑Ressourcen‑Limits

Konfigurieren Sie passende Ressourcen‑Limits:

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

### Kubernetes‑Pod‑Größenbestimmung

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
          memory: '2Gi'
          cpu: '1000m'
        limits:
          memory: '4Gi'
          cpu: '2000m'
```

### Ressourcen‑Monitoring

Überwachen Sie diese Metriken:

- **CPU‑Auslastung**: Sollte im Durchschnitt <80 % liegen
- **Speicherauslastung**: Sollte 20 % Puffer haben
- **Klassifizierungs‑Latenz**: P95‑Latenz unter dem Zielwert
- **Warteschlangen‑Tiefe**: Tickets, die auf Klassifizierung warten

## Skalierungs‑Strategien

### Vertikale Skalierung

Ressourcen auf einer einzelnen Instanz erhöhen:

```yaml
# Start
RAM: 2 GB, CPU: 2 cores

# Scale up
RAM: 4 GB, CPU: 4 cores

# Further scaling
RAM: 8 GB, CPU: 8 cores
```

**Vorteile**:

- Einfach zu implementieren
- Keine Code‑Änderungen nötig
- Leicht zu verwalten

**Nachteile**:

- Durch Hardware‑Grenzwerte begrenzt
- Einzelner Ausfallpunkt
- Potenziell teuer

### Horizontale Skalierung

Mehrere Instanzen bereitstellen:

```yaml
# Load balancer
└── Classifier Instance 1 (2 GB, 2 cores)
└── Classifier Instance 2 (2 GB, 2 cores)
└── Classifier Instance 3 (2 GB, 2 cores)
```

**Vorteile**:

- Bessere Zuverlässigkeit
- Bewältigt Traffic‑Spitzen
- Kosteneffizienter im großen Maßstab

**Nachteile**:

- Komplexere Einrichtung
- Benötigt Load Balancer
- Gemeinsame Zustands‑Überlegungen

### Auto‑Scaling

Dynamische Skalierung basierend auf Last:

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

## Speicher‑Anforderungen

### Modell‑Speicher

- **Basis‑Modelle**: 100 MB ‑ 5 GB
- **Fine‑tuned Modelle**: +100‑500 MB
- **Cache**: 1‑5 GB
- **Logs**: 100 MB ‑ 1 GB/Tag

### Empfohlene Einrichtung

```
Disk Layout:
├── /models/ (10‑20 GB, SSD)
├── /cache/ (5 GB, SSD)
├── /logs/ (rotierend, 10 GB)
└── /data/ (variabel, Standard‑Speicher)
```

## Netzwerk‑Anforderungen

### Bandbreite

- **Modell‑Downloads**: Initial 1‑5 GB, danach minimal
- **API‑Traffic**: 1‑10 KB pro Ticket
- **Monitoring**: 1‑5 MB/Stunde

### Latenz

- **Intern**: <10 ms ideal
- **Externe APIs**: <100 ms akzeptabel
- **Model‑Serving**: <50 ms Zielwert

## Kosten‑Optimierung

### Entwicklungs‑Umgebung

Minimal‑Kosten‑Setup für Tests:

```yaml
Cloud Instance:
  Type: t3.small (AWS) / e2-small (GCP)
  vCPU: 2
  RAM: 2 GB
  Cost: ~$15-20/month
```

### Produktion – Kleine Skalierung

Kosten‑effiziente Produktion:

```yaml
Cloud Instance:
  Type: t3.medium (AWS) / e2-medium (GCP)
  vCPU: 2
  RAM: 4 GB
  Cost: ~$30-40/month
```

### Produktion – Große Skalierung

Leistungsstarke Produktion:

```yaml
Cloud Instance:
  Type: c5.2xlarge (AWS) / c2-standard-8 (GCP)
  vCPU: 8
  RAM: 16 GB
  GPU: Optional T4
  Cost: ~$150-300/month (CPU) or ~$400-600/month (GPU)
```

## Performance‑Testing

### Benchmark Ihres Setups

Testen Sie die Klassifizierungs‑Performance:

```bash
# Load test with 100 concurrent requests
ab -n 1000 -c 100 http://localhost:8080/classify

# Monitor during test
docker stats ticket-classifier

# Check response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8080/classify
```

### Performance‑Ziele

| Metrik          | Ziel          | Messung                |
| --------------- | ------------- | ---------------------- |
| Latency P50    | <200 ms       | Median response time  |
| Latency P95    | <500 ms       | 95. Perzentil          |
| Latency P99    | <1000 ms      | 99. Perzentil          |
| Throughput     | >100/min      | Tickets klassifiziert |
| CPU‑Usage      | <80 %         | Durchschnittliche Nutzung |
| Memory‑Usage   | <80 %         | Spitzen‑Nutzung        |

## Fehlersuche

### Out of Memory Errors

**Symptome**:

```
MemoryError: Unable to allocate array
Container killed (OOMKilled)
```

**Lösungen**:

1. Speicherzuweisung erhöhen
2. Kleinere Modell‑Variante verwenden
3. Batch‑Größe reduzieren
4. Modell‑Quantisierung aktivieren

### Langsame Klassifizierung

**Symptome**:

- Latenz >1 Sekunde pro Ticket
- Wachsender Verarbeitungs‑Queue

**Lösungen**:

1. GPU‑Beschleunigung aktivieren
2. Modell‑Distillation einsetzen
3. Batch‑Verarbeitung optimieren
4. Mehr Replicas hinzufügen

### Hohe CPU‑Auslastung

**Symptome**:

- CPU konstant >90 %
- Gedrosselte Performance

**Lösungen**:

1. Mehr CPU‑Kerne hinzufügen
2. Modell‑Inference optimieren
3. Request‑Queueing implementieren
4. Horizontal skalieren

## Best Practices

### DO ✅

- Mit CPU‑Only für Tests starten
- Ressourcen‑Nutzung kontinuierlich überwachen
- Angemessene Ressourcen‑Limits setzen
- Für das 2‑fache aktuelle Load planen
- Caching wo möglich einsetzen
- Health‑Checks implementieren

### DON'T ❌

- Speicher zu knapp provisionieren (führt zu OOM)
- Performance‑Tests überspringen
- Monitoring‑Metriken ignorieren
- Unnötig über‑provisionieren
- Produktions‑ und Entwicklungs‑Workloads mischen

## Nächste Schritte

Nach der Größenbestimmung Ihrer Hardware:

1. **Infrastructure Deploy**: Server/Container einrichten
2. **Model Install**: Klassifizierungs‑Modell herunterladen und konfigurieren
3. **Performance Test**: Gegen Ihre Anforderungen validieren
4. **Monitor**: Metriken und Alerting einrichten

## Verwandte Dokumentation

- [Using Model](using-model.md) - Configure and deploy classification models
- [Taxonomy Design](taxonomy-design.md) - Design your classification taxonomy
- [Tag Mapping](tag-mapping.md) - Map classifications to ticket fields