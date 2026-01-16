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
- Anforderungen an die Antwortzeit
- Budgetbeschränkungen

## Schnellreferenz

| Skalierung  | Tickets/Tag     | Min. RAM | Min. CPU | GPU         | Modelltyp         |
| ----------- | --------------- | -------- | -------- | ----------- | ----------------- |
| Klein       | <1.000          | 512 MB   | 1 Kern   | Nein        | Einfaches ML      |
| Mittel      | 1.000-10.000    | 2 GB     | 2 Kerne  | Optional    | BERT-basiert      |
| Groß        | 10.000-100.000  | 8 GB     | 4 Kerne  | Empfohlen   | BERT/Large        |
| Enterprise  | >100.000        | 16+ GB   | 8+ Kerne | Erforderlich| Benutzerdefiniert/Feinabgestimmt |

## Bereitstellungsmodelle

### Nur-CPU-Bereitstellung

**Am besten geeignet für**:

- Kleine bis mittlere Ticketvolumen (<10.000/Tag)
- Budgetbewusste Bereitstellungen
- Einfachere Modelle (distilled BERT, kleine Transformer)

**Empfohlene Spezifikationen**:

```yaml
Kleine Skalierung:
  CPU: 1-2 Kerne (2.0+ GHz)
  RAM: 512 MB - 2 GB
  Speicher: 5 GB
  Netzwerk: Standard

Mittlere Skalierung:
  CPU: 2-4 Kerne (2.5+ GHz)
  RAM: 2-4 GB
  Speicher: 10 GB
  Netzwerk: Standard
```

**Erwartete Leistung**:

- Klassifizierungszeit: 200-500ms pro Ticket
- Durchsatz: 100-500 Tickets/Minute
- Modellladezeit: 5-30 Sekunden

### GPU-beschleunigte Bereitstellung

**Am besten geeignet für**:

- Große Ticketvolumen (>10.000/Tag)
- Echtzeit-Klassifizierungsanforderungen
- Große Transformer-Modelle
- Feinabstimmung und erneutes Training

**Empfohlene Spezifikationen**:

```yaml
Mittel-Große Skalierung:
  CPU: 4-8 Kerne
  RAM: 8-16 GB
  GPU: NVIDIA T4 oder besser (16 GB VRAM)
  Speicher: 20 GB SSD
  Netzwerk: Hohe Bandbreite

Enterprise-Skalierung:
  CPU: 8-16 Kerne
  RAM: 16-32 GB
  GPU: NVIDIA A10/A100 (24-80 GB VRAM)
  Speicher: 50+ GB NVMe SSD
  Netzwerk: Hohe Bandbreite, niedrige Latenz
```

**Erwartete Leistung**:

- Klassifizierungszeit: 10-50ms pro Ticket
- Durchsatz: 1.000-10.000 Tickets/Minute
- Modellladezeit: 2-10 Sekunden

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
- Benutzerdefinierte feinabgestimmte Modelle

**Anforderungen**:

- RAM: 2-4 GB
- CPU: 2-4 Kerne empfohlen
- GPU: Optional, verbessert Leistung um das 5-10-fache

**Anwendungsfälle**:

- Die meisten Produktionsbereitstellungen
- Ausgewogene Genauigkeit/Leistung
- Standard-Ticketvolumen

### Große Modelle (1-5 GB)

**Beispiele**:

- BERT-large
- RoBERTa-large
- GPT-basierte Modelle
- Benutzerdefinierte Ensemble-Modelle

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
- **Speicherauslastung**: Sollte 20% Spielraum haben
- **Klassifizierungslatenz**: P95-Latenz unter dem Zielwert
- **Warteschlangentiefe**: Tickets, die auf Klassifizierung warten

## Skalierungsstrategien

### Vertikale Skalierung

Erhöhen Sie die Ressourcen auf einer einzelnen Instanz:

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
- Keine Codeänderungen erforderlich
- Einfach zu verwalten

**Nachteile**:

- Begrenzt durch Hardware-Maxima
- Single Point of Failure
- Möglicherweise teuer

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

### Automatische Skalierung

Dynamische Skalierung basierend auf der Last:

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
- **Feinabgestimmte Modelle**: +100-500 MB
- **Cache**: 1-5 GB
- **Logs**: 100 MB - 1 GB/Tag

### Empfohlene Einrichtung

```
Festplattenlayout:
├── /models/ (10-20 GB, SSD)
├── /cache/ (5 GB, SSD)
├── /logs/ (rotierend, 10 GB)
└── /data/ (variabel, Standard-Speicher)
```

## Netzwerkanforderungen

### Bandbreite

- **Modell-Downloads**: Anfänglich 1-5 GB, dann minimal
- **API-Verkehr**: 1-10 KB pro Ticket
- **Überwachung**: 1-5 MB/Stunde

### Latenz

- **Intern**: <10ms ideal
- **Externe APIs**: <100ms akzeptabel
- **Modellbereitstellung**: <50ms Ziel

## Kostenoptimierung

### Entwicklungsumgebung

Minimale Kosten-Einrichtung für Tests:

```yaml
Cloud-Instanz:
  Typ: t3.small (AWS) / e2-small (GCP)
  vCPU: 2
  RAM: 2 GB
  Kosten: ~$15-20/Monat
```

### Produktion Kleine Skalierung

Kosteneffektive Produktion:

```yaml
Cloud-Instanz:
  Typ: t3.medium (AWS) / e2-medium (GCP)
  vCPU: 2
  RAM: 4 GB
  Kosten: ~$30-40/Monat
```

### Produktion Große Skalierung

Hochleistungs-Produktion:

```yaml
Cloud-Instanz:
  Typ: c5.2xlarge (AWS) / c2-standard-8 (GCP)
  vCPU: 8
  RAM: 16 GB
  GPU: Optional T4
  Kosten: ~$150-300/Monat (CPU) oder ~$400-600/Monat (GPU)
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

| Metrik       | Ziel     | Messung               |
| ------------ | -------- | --------------------- |
| Latenz P50   | <200ms   | Median-Antwortzeit    |
| Latenz P95   | <500ms   | 95. Perzentil         |
| Latenz P99   | <1000ms  | 99. Perzentil         |
| Durchsatz    | >100/min | Klassifizierte Tickets|
| CPU-Auslastung | <80%   | Durchschnittliche Auslastung |
| Speicherauslastung | <80% | Spitzenauslastung     |

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
2. Modell-Distillation verwenden
3. Batch-Verarbeitung optimieren
4. Mehr Replikate hinzufügen

### Hohe CPU-Auslastung

**Symptome**:

- CPU konstant >90%
- Gedrosselte Leistung

**Lösungen**:

1. Mehr CPU-Kerne hinzufügen
2. Modell-Inferenz optimieren
3. Request-Queuing implementieren
4. Horizontal skalieren

## Best Practices

### DO ✅

- Beginnen Sie mit Nur-CPU für Tests
- Ressourcennutzung kontinuierlich überwachen
- Angemessene Ressourcenlimits setzen
- Für die 2-fache aktuelle Last planen
- Caching wo möglich nutzen
- Health Checks implementieren

### DON'T ❌

- Speicher unterdimensionieren (verursacht OOM)
- Leistungstests überspringen
- Überwachungsmetriken ignorieren
- Unnötig überdimensionieren
- Produktions- und Entwicklungslasten vermischen

## Nächste Schritte

Nach der Dimensionierung Ihrer Hardware:

1. **Infrastruktur bereitstellen**: Server/Container einrichten
2. **Modell installieren**: Klassifizierungsmodell herunterladen und konfigurieren
3. **Leistungstest**: Gegen Ihre Anforderungen validieren
4. **Überwachen**: Metriken und Alarmierung einrichten

## Verwandte Dokumentation

- [Using Model](using-model.md) - Klassifizierungsmodelle konfigurieren und bereitstellen
- [Taxonomy Design](taxonomy-design.md) - Ihre Klassifizierungstaxonomie entwerfen
- [Tag Mapping](tag-mapping.md) - Klassifizierungen auf Ticket-Felder abbilden