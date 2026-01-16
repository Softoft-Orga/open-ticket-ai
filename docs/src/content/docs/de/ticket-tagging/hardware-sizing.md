---
title: Hardware Sizing
description: 'Hardware- und Infrastrukturanforderungen für den Betrieb von Ticket-Klassifizierungsmodellen in verschiedenen Größenordnungen.'
lang: en
nav:
  group: Ticket Tagging
  order: 2
---

# Hardware Sizing

Verstehen Sie die Hardware-Anforderungen für den Betrieb von Ticket-Klassifizierungsmodellen in verschiedenen Größenordnungen.

## Überblick

Die Hardware-Anforderungen für die Ticket-Klassifizierung hängen von mehreren Faktoren ab:

- Modellgröße und -komplexität
- Anzahl der verarbeiteten Tickets
- Klassifizierungshäufigkeit
- Antwortzeit-Anforderungen
- Budgetbeschränkungen

## Schnellreferenz

| Skalierung | Tickets/Tag    | Min. RAM | Min. CPU | GPU          | Modelltyp         |
| ---------- | -------------- | -------- | -------- | ------------ | ----------------- |
| Klein      | <1.000         | 512 MB   | 1 Kern   | Nein         | Simple ML         |
| Mittel     | 1.000-10.000   | 2 GB     | 2 Kerne  | Optional     | BERT-basiert      |
| Groß       | 10.000-100.000 | 8 GB     | 4 Kerne  | Empfohlen    | BERT/Large        |
| Enterprise | >100.000       | 16+ GB   | 8+ Kerne | Erforderlich | Custom/Fine-tuned |

## Bereitstellungsmodelle

### Nur-CPU-Bereitstellung

**Am besten geeignet für**:

- Kleine bis mittlere Ticketvolumen (<10.000/Tag)
- Budgetbewusste Bereitstellungen
- Einfachere Modelle (distilled BERT, kleine Transformer)

**Empfohlene Spezifikationen**:

```yaml
Small Scale:
  CPU: 1-2 Kerne (2.0+ GHz)
  RAM: 512 MB - 2 GB
  Storage: 5 GB
  Network: Standard

Medium Scale:
  CPU: 2-4 Kerne (2.5+ GHz)
  RAM: 2-4 GB
  Storage: 10 GB
  Network: Standard
```

**Erwartete Leistung**:

- Klassifizierungszeit: 200-500ms pro Ticket
- Durchsatz: 100-500 Tickets/Minute
- Modell-Ladezeit: 5-30 Sekunden

### GPU-beschleunigte Bereitstellung

**Am besten geeignet für**:

- Große Ticketvolumen (>10.000/Tag)
- Echtzeit-Klassifizierungsanforderungen
- Große Transformer-Modelle
- Fine-tuning und Retraining

**Empfohlene Spezifikationen**:

```yaml
Medium-Large Scale:
  CPU: 4-8 Kerne
  RAM: 8-16 GB
  GPU: NVIDIA T4 oder besser (16 GB VRAM)
  Storage: 20 GB SSD
  Network: Hohe Bandbreite

Enterprise Scale:
  CPU: 8-16 Kerne
  RAM: 16-32 GB
  GPU: NVIDIA A10/A100 (24-80 GB VRAM)
  Storage: 50+ GB NVMe SSD
  Network: Hohe Bandbreite, niedrige Latenz
```

**Erwartete Leistung**:

- Klassifizierungszeit: 10-50ms pro Ticket
- Durchsatz: 1.000-10.000 Tickets/Minute
- Modell-Ladezeit: 2-10 Sekunden

## Auswirkung der Modellgröße

### Kleine Modelle (50-150 MB)

**Beispiele**:

- DistilBERT
- MiniLM
- TinyBERT

**Anforderungen**:

- RAM: 512 MB - 1 GB
- CPU: 1-2 Kerne ausreichend
- GPU: Nicht erforderlich

**Anwendungsfälle**:

- Umgebungen mit geringem Volumen
- Kostenbewusste Bereitstellungen
- Edge-Bereitstellungen

### Mittlere Modelle (300-500 MB)

**Beispiele**:

- BERT-base
- RoBERTa-base
- Custom fine-tuned models

**Anforderungen**:

- RAM: 2-4 GB
- CPU: 2-4 Kerne empfohlen
- GPU: Optional, verbessert Leistung um das 5-10-fache

**Anwendungsfälle**:

- Die meisten Produktionsbereitstellungen
- Ausgewogenes Verhältnis Genauigkeit/Leistung
- Standard-Ticketvolumen

### Große Modelle (1-5 GB)

**Beispiele**:

- BERT-large
- RoBERTa-large
- GPT-basierte Modelle
- Custom ensemble models

**Anforderungen**:

- RAM: 8-16 GB
- CPU: 4-8 Kerne Minimum
- GPU: Sehr empfohlen (T4 oder besser)

**Anwendungsfälle**:

- Hohe Genauigkeitsanforderungen
- Komplexe Klassifizierungsaufgaben
- Multi-Label-Klassifizierung
- Hochvolumige Verarbeitung

## Containerisierte Bereitstellungen

### Docker-Ressourcenlimits

Konfigurieren Sie angemessene Ressourcenlimits:

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

### Kubernetes-Pod-Dimensionierung

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

### Ressourcenüberwachung

Überwachen Sie diese Metriken:

- **CPU-Auslastung**: Sollte im Durchschnitt <80% sein
- **Speicherauslastung**: Sollte 20% Puffer haben
- **Klassifizierungslatenz**: P95-Latenz unter Zielwert
- **Warteschlangentiefe**: Tickets, die auf Klassifizierung warten

## Skalierungsstrategien

### Vertikale Skalierung

Ressourcen auf einer einzelnen Instanz erhöhen:

```yaml
# Start
RAM: 2 GB, CPU: 2 Kerne

# Hochskalieren
RAM: 4 GB, CPU: 4 Kerne

# Weitere Skalierung
RAM: 8 GB, CPU: 8 Kerne
```

**Vorteile**:

- Einfach zu implementieren
- Keine Code-Änderungen erforderlich
- Einfach zu verwalten

**Nachteile**:

- Durch Hardware-Maxima begrenzt
- Single Point of Failure
- Potenziell teuer

### Horizontale Skalierung

Mehrere Instanzen bereitstellen:

```yaml
# Load Balancer
└── Classifier Instance 1 (2 GB, 2 Kerne)
└── Classifier Instance 2 (2 GB, 2 Kerne)
└── Classifier Instance 3 (2 GB, 2 Kerne)
```

**Vorteile**:

- Bessere Zuverlässigkeit
- Bewältigt Verkehrsspitzen
- Kosteneffektiver bei Skalierung

**Nachteile**:

- Komplexerer Aufbau
- Erfordert Load Balancer
- Überlegungen zum gemeinsamen Zustand

### Auto-Scaling

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

## Speicheranforderungen

### Modellspeicher

- **Basismodelle**: 100 MB - 5 GB
- **Fine-tuned models**: +100-500 MB
- **Cache**: 1-5 GB
- **Logs**: 100 MB - 1 GB/Tag

### Empfohlene Einrichtung

```
Disk Layout:
├── /models/ (10-20 GB, SSD)
├── /cache/ (5 GB, SSD)
├── /logs/ (rotierend, 10 GB)
└── /data/ (variabel, Standard-Speicher)
```

## Netzwerkanforderungen

### Bandbreite

- **Modelldownloads**: Anfänglich 1-5 GB, dann minimal
- **API-Verkehr**: 1-10 KB pro Ticket
- **Monitoring**: 1-5 MB/Stunde

### Latenz

- **Intern**: <10ms ideal
- **Externe APIs**: <100ms akzeptabel
- **Model Serving**: <50ms Ziel

## Kostenoptimierung

### Entwicklungsumgebung

Minimale Kosten-Einrichtung für Tests:

```yaml
Cloud Instance:
  Type: t3.small (AWS) / e2-small (GCP)
  vCPU: 2
  RAM: 2 GB
  Cost: ~$15-20/month
```

### Produktion Kleine Skalierung

Kosteneffektive Produktion:

```yaml
Cloud Instance:
  Type: t3.medium (AWS) / e2-medium (GCP)
  vCPU: 2
  RAM: 4 GB
  Cost: ~$30-40/month
```

### Produktion Große Skalierung

Hochleistungs-Produktion:

```yaml
Cloud Instance:
  Type: c5.2xlarge (AWS) / c2-standard-8 (GCP)
  vCPU: 8
  RAM: 16 GB
  GPU: Optional T4
  Cost: ~$150-300/month (CPU) or ~$400-600/month (GPU)
```

## Leistungstests

### Benchmarking Ihrer Einrichtung

Testen Sie die Klassifizierungsleistung:

```bash
# Lasttest mit 100 gleichzeitigen Anfragen
ab -n 1000 -c 100 http://localhost:8080/classify

# Während des Tests überwachen
docker stats ticket-classifier

# Antwortzeiten prüfen
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8080/classify
```

### Leistungsziele

| Metrik             | Ziel     | Messung                      |
| ------------------ | -------- | ---------------------------- |
| Latenz P50         | <200ms   | Median-Antwortzeit           |
| Latenz P95         | <500ms   | 95. Perzentil                |
| Latenz P99         | <1000ms  | 99. Perzentil                |
| Durchsatz          | >100/min | Klassifizierte Tickets       |
| CPU-Auslastung     | <80%     | Durchschnittliche Auslastung |
| Speicherauslastung | <80%     | Spitzenauslastung            |

## Fehlerbehebung

### Out-of-Memory-Fehler

**Symptome**:

```
MemoryError: Unable to allocate array
Container killed (OOMKilled)
```

**Lösungen**:

1. Speicherzuweisung erhöhen
2. Kleinere Modellvariante verwenden
3. Batch-Größe reduzieren
4. Modellquantisierung aktivieren

### Langsame Klassifizierung

**Symptome**:

- Latenz >1 Sekunde pro Ticket
- Wachsende Verarbeitungswarteschlange

**Lösungen**:

1. GPU-Beschleunigung aktivieren
2. Modelldistillation verwenden
3. Batch-Verarbeitung optimieren
4. Mehr Replikate hinzufügen

### Hohe CPU-Auslastung

**Symptome**:

- CPU konstant >90%
- Gedrosselte Leistung

**Lösungen**:

1. Mehr CPU-Kerne hinzufügen
2. Modellinferenz optimieren
3. Request-Queuing implementieren
4. Horizontal skalieren

## Best Practices

### DO ✅

- Beginnen Sie mit Nur-CPU für Tests
- Überwachen Sie die Ressourcennutzung kontinuierlich
- Legen Sie angemessene Ressourcenlimits fest
- Planen Sie für die 2-fache aktuelle Last
- Verwenden Sie Caching, wo möglich
- Implementieren Sie Health Checks

### DON'T ❌

- Speicher unterdimensionieren (verursacht OOM)
- Leistungstests überspringen
- Monitoring-Metriken ignorieren
- Unnötig überdimensionieren
- Produktions- und Entwicklungslasten vermischen

## Nächste Schritte

Nach der Dimensionierung Ihrer Hardware:

1. **Infrastruktur bereitstellen**: Server/Container einrichten
2. **Modell installieren**: Klassifizierungsmodell herunterladen und konfigurieren
3. **Leistungstest**: Gegen Ihre Anforderungen validieren
4. **Überwachen**: Metriken und Alerting einrichten

## Verwandte Dokumentation

- [Using Model](using-model.md) - Klassifizierungsmodelle konfigurieren und bereitstellen
- [Taxonomy Design](taxonomy-design.md) - Ihre Klassifizierungstaxonomie entwerfen
- [Tag Mapping](tag-mapping.md) - Klassifizierungen auf Ticket-Felder abbilden
