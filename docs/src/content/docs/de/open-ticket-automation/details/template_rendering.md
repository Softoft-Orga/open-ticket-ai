---
title: Template Rendering
lang: en
nav:
  group: Details
  order: 2
---

# Template Rendering

Open Ticket AI verwendet Template Rendering, um Konfigurationen dynamisch und an verschiedene Umgebungen sowie Laufzeitbedingungen anpassbar zu machen. Dadurch können Sie das Verhalten anpassen, ohne Code zu ändern.

## Was ist Template Rendering?

Template Rendering verarbeitet spezielle Platzhalter in Ihren Konfigurationsdateien und ersetzt sie zur Laufzeit durch tatsächliche Werte. Das ermöglicht:

- Verwendung von Umgebungsvariablen in Konfigurationen
- Referenzieren von Ergebnissen vorheriger Pipeline-Schritte
- Bedingte Logik basierend auf dem Kontext
- Dynamische Service-Konfigurationen

## Jinja2 Templates

Open Ticket AI verwendet [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/), eine leistungsstarke Templating-Engine für Python. Jinja2 bietet:

- Variablenersetzung: `{{ variable }}`
- Bedingte Blöcke: `{% if condition %}...{% endif %}`
- Schleifen: `{% for item in list %}...{% endfor %}`
- Filter: `{{ value | filter }}`

Für die vollständige Jinja2-Dokumentation besuchen Sie die [offizielle Jinja2-Website](https://jinja.palletsprojects.com/en/3.1.x/).

## Custom Template Helpers

Zusätzlich zu den Standard‑Jinja2‑Funktionen stellt Open Ticket AI benutzerdefinierte Hilfsfunktionen bereit, die Laufzeitdaten für Templates zugänglich machen.

### `get_env(env_name)`

Liest den Wert einer Umgebungsvariablen. Das Rendering schlägt fehl, wenn die Variable nicht definiert ist, wodurch sichergestellt wird, dass erforderliche Werte bereitgestellt werden.

```yaml
params:
  api_key: "{{ get_env('API_KEY') }}"
  timeout_seconds: "{{ get_env('TIMEOUT_SECONDS') | int }}"
```

### `get_pipe_result(pipe_id, data_key='value')`

Ruft einen Wert aus einer zuvor ausgeführten Pipe ab. Pipe‑Ergebnisse werden als Dictionaries gespeichert; verwenden Sie `data_key`, um einen bestimmten Eintrag auszuwählen. Die Hilfsfunktion löst einen Render‑Fehler aus, wenn der Schlüssel nicht existiert.

```yaml
params:
  classification: "{{ get_pipe_result('classify') }}" # reads the default `value`
  confidence: "{{ get_pipe_result('classify', 'confidence') }}"
```

### `has_failed(pipe_id)`

Gibt `True` zurück, wenn die referenzierte Pipe die Ausführung erfolglos abgeschlossen hat (und nicht übersprungen wurde).

```yaml
if: "{{ not has_failed('fetch_ticket') }}"
```

### `at_path(data, path)`

Durchläuft verschachtelte Dictionaries oder Pydantic‑Modelle mittels Punktnotation.

```yaml
params:
  requester_email: "{{ at_path(ticket, 'metadata.requester.email') }}"
```

### `get_parent_param(param_key)`

Stellt Parameter aus einem übergeordneten Kontext für verschachtelte (komposite) Pipes bereit. Wenn kein übergeordneter Parameter vorhanden ist oder der Schlüssel fehlt, schlägt das Rendering fehl, sodass Konfigurationsprobleme frühzeitig sichtbar werden.

```yaml
params:
  expression: "{{ get_parent_param('threshold') * 100 }}"
```

### `fail()`

Erstellt ein spezielles Marker‑Objekt, das von der Expression‑Pipe erkannt wird. Die Rückgabe dieses Markers ermöglicht es einem Template‑Ausdruck, eine Pipe explizit fehlschlagen zu lassen, anstatt eine Ausnahme zu werfen.

```yaml
expression: '{{ fail() if confidence < 0.6 else result }}'
```

## Template Context

Templates erhalten ein Kontext‑Dictionary, das je nach Rendering‑Phase variiert. Die Schlüssel erscheinen direkt im Template (globale Objekte benötigen kein `context.`‑Präfix).

### Global Context (Always Available)

- Jinja‑Hilfsfunktionen wie `get_env`, `get_pipe_result` und `at_path`
- Konfigurationswerte, die explizit im Render‑Aufruf übergeben werden

### Pipeline Context

Beim Rendering von pipeline‑bezogenen Konfigurationen:

- `params`: Pipeline‑Parameter, definiert in `orchestrator.pipelines[].params`
- `pipe_results`: Historische Ausführungsergebnisse, nach Pipe‑ID indiziert, sofern verfügbar

### Pipe Context

Beim Rendering einzelner Pipes während der Ausführung:

- `params`: Parameter, die an die aktuelle Pipe übergeben werden
- `pipe_results`: Ergebnisse zuvor ausgeführter Pipes in derselben Pipeline
- `parent_params`: Parameter der übergeordneten Pipe (falls die Pipe verschachtelt ist)

Eltern‑Parameter werden jetzt für verschachtelte Pipelines automatisch bereitgestellt, sodass komposite Pipes mit ihren Kind‑Pipes über `get_parent_param()` oder durch direktes Auslesen von `parent_params` koordinieren können. Service‑Instanzen werden zu diesem Zeitpunkt **nicht** in Templates injiziert. Wir planen, Service‑Injection in Zukunft zu untersuchen, aber diese Dokumentation spiegelt das derzeit implementierte Verhalten wider.

## When Rendering Happens

Verschiedene Teile Ihrer Konfiguration werden zu unterschiedlichen Zeitpunkten gerendert:

### Service Instantiation

Services im Abschnitt `services` werden gerendert, wenn die Anwendung startet, bevor irgendeine Pipeline ausgeführt wird. Sie haben nur Zugriff auf den globalen Kontext, der für die Service‑Erstellung bereitgestellt wird.

### Pipeline Creation

Pipeline‑Definitionen werden gerendert, wenn Pipelines erstellt werden. Sie haben Zugriff auf den globalen Kontext, Pipeline‑Parameter und (sofern verfügbar) vorherige Pipeline‑Ergebnisse.

### Pipe Execution

Einzelne Pipes werden unmittelbar vor ihrer Ausführung gerendert. Sie haben Zugriff auf globale Daten, pipeline‑bezogene Parameter, vorherige Pipe‑Ergebnisse und Eltern‑Parameter, falls die Pipe verschachtelt ist.

## What Gets Rendered

Template Rendering wird auf Zeichenkettenwerte in den folgenden Konfigurationsabschnitten angewendet:

### Services

- `params`‑Werte
- `injects`‑Schlüssel und -Werte

### Orchestrator

- `pipelines[].params`‑Werte
- `pipelines[].pipes[].params`‑Werte
- `pipelines[].pipes[].if`‑Bedingungen
- `pipelines[].pipes[].depends_on`‑Listen

### Pipes

- Alle Parameter‑Werte
- Bedingte Ausdrücke
- Abhängigkeits‑Spezifikationen

> Die Template‑Renderer‑Konfiguration selbst (`infrastructure.template_renderer_config`) wird niemals gerendert – sie wird als Roh‑Input verwendet, um das Rendering‑System zu bootstrappen. Das Rendern dieser Konfiguration würde eine zirkuläre Abhängigkeit erzeugen, da sie zum Initialisieren des Renderers selbst benötigt wird.

## Examples

### Using Environment Variables

```yaml
services:
  - id: api_client
    use: 'mypackage:APIClient'
    params:
      base_url: "{{ get_env('API_BASE_URL') }}"
      api_key: "{{ get_env('API_KEY') }}"
```

### Pipeline Parameters

```yaml
orchestrator:
  pipelines:
    - name: process_tickets
      params:
        threshold: 0.8
      pipes:
        - id: classify
          use: 'mypackage:Classifier'
          params:
            confidence_threshold: '{{ params.threshold }}'
```

### Pipe Dependencies

```yaml
pipes:
  - id: fetch_data
    use: 'mypackage:Fetcher'

  - id: process_data
    use: 'mypackage:Processor'
    params:
      input: "{{ get_pipe_result('fetch_data') }}"
    depends_on: [fetch_data]
    if: "{{ not has_failed('fetch_data') }}"
```

### Using Parent Parameters in a Composite Pipe

```yaml
pipes:
  - id: composite
    use: 'mypackage:Composite'
    params:
      threshold: 0.75
    steps:
      - id: evaluate
        use: 'mypackage:Expression'
        params:
          expression: "{{ get_parent_param('threshold') > 0.7 }}"
```

### Explicitly Failing a Pipe

```yaml
pipes:
  - id: evaluate
    use: 'mypackage:Expression'
    params:
      expression: "{{ fail() if get_pipe_result('validate', 'score') < 0.5 else 'ok' }}"
```

## Best Practices

- Verwenden Sie Umgebungsvariablen für Secrets und umgebungsspezifische Werte
- Bevorzugen Sie `get_env()` gegenüber dem direkten Lesen von `os.environ` für bessere Fehlermeldungen
- Halten Sie Templates einfach und lesbar
- Testen Sie Ihre Templates mit verschiedenen Kontextwerten
- Vermeiden Sie komplexe Logik in Templates – bevorzugen Sie Konfiguration statt Code