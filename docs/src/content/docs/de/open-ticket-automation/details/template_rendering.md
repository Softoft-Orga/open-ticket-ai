---
title: Template Rendering
lang: en
nav:
  group: Details
  order: 2
---

# Template Rendering

Open Ticket AI verwendet Template Rendering, um Konfigurationen dynamisch und an verschiedene Umgebungen und Laufzeitbedingungen anpassbar zu machen. Dies ermöglicht es Ihnen, das Verhalten anzupassen, ohne Code zu ändern.

## Was ist Template Rendering?

Template Rendering verarbeitet spezielle Platzhalter in Ihren Konfigurationsdateien und ersetzt sie zur Laufzeit durch tatsächliche Werte. Dies ermöglicht:

- Die Verwendung von Umgebungsvariablen in Konfigurationen
- Das Referenzieren von Ergebnissen aus vorherigen Pipeline-Schritten
- Bedingte Logik basierend auf dem Kontext
- Dynamische Service-Konfigurationen

## Jinja2 Templates

Open Ticket AI verwendet [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/), eine leistungsstarke Template-Engine für Python. Jinja2 bietet:

- Variablenersetzung: `{{ variable }}`
- Bedingte Blöcke: `{% if condition %}...{% endif %}`
- Schleifen: `{% for item in list %}...{% endfor %}`
- Filter: `{{ value | filter }}`

Für die vollständige Jinja2-Dokumentation besuchen Sie die [offizielle Jinja2-Website](https://jinja.palletsprojects.com/en/3.1.x/).

## Benutzerdefinierte Template-Helfer

Zusätzlich zu den Standard-Jinja2-Funktionen stellt Open Ticket AI benutzerdefinierte Hilfsfunktionen bereit, die Laufzeitdaten für Templates verfügbar machen.

### `get_env(env_name)`

Liest den Wert einer Umgebungsvariable. Das Rendering schlägt fehl, wenn die Variable nicht definiert ist, um sicherzustellen, dass erforderliche Werte bereitgestellt werden.

```yaml
params:
  api_key: "{{ get_env('API_KEY') }}"
  timeout_seconds: "{{ get_env('TIMEOUT_SECONDS') | int }}"
```

### `get_pipe_result(pipe_id, data_key='value')`

Ruft einen Wert aus einem zuvor ausgeführten Pipe ab. Pipe-Ergebnisse werden als Dictionaries gespeichert; verwenden Sie `data_key`, um einen bestimmten Eintrag auszuwählen. Der Helfer löst einen Render-Fehler aus, wenn der Schlüssel nicht existiert.

```yaml
params:
  classification: "{{ get_pipe_result('classify') }}" # liest den Standardwert `value`
  confidence: "{{ get_pipe_result('classify', 'confidence') }}"
```

### `has_failed(pipe_id)`

Gibt `True` zurück, wenn der referenzierte Pipe die Ausführung erfolglos abgeschlossen hat (und nicht übersprungen wurde).

```yaml
if: "{{ not has_failed('fetch_ticket') }}"
```

### `at_path(data, path)`

Durchläuft verschachtelte Dictionaries oder Pydantic-Modelle mithilfe der Punktnotation.

```yaml
params:
  requester_email: "{{ at_path(ticket, 'metadata.requester.email') }}"
```

### `get_parent_param(param_key)`

Macht Parameter aus einem übergeordneten Kontext für verschachtelte (komposite) Pipes verfügbar. Wenn kein übergeordneter Parameter vorhanden ist oder der Schlüssel fehlt, schlägt das Rendering fehl, sodass Konfigurationsprobleme frühzeitig sichtbar werden.

```yaml
params:
  expression: "{{ get_parent_param('threshold') * 100 }}"
```

### `fail()`

Erzeugt eine spezielle Markierung, die vom Expression Pipe erkannt wird. Die Rückgabe dieser Markierung ermöglicht es einem Template-Ausdruck, einen Pipe explizit fehlschlagen zu lassen, anstatt eine Exception auszulösen.

```yaml
expression: '{{ fail() if confidence < 0.6 else result }}'
```

## Template-Kontext

Templates erhalten ein Kontext-Dictionary, das je nach Rendering-Stufe variiert. Die Schlüssel erscheinen direkt im Template (globale Objekte benötigen kein `context.`-Präfix).

### Globaler Kontext (immer verfügbar)

- Jinja-Helfer wie `get_env`, `get_pipe_result` und `at_path`
- Konfigurationswerte, die explizit im Render-Aufruf übergeben werden

### Pipeline-Kontext

Beim Rendering der Pipeline-Konfiguration:

- `params`: Pipeline-Parameter, definiert in `orchestrator.pipelines[].params`
- `pipe_results`: Historische Ausführungsergebnisse, nach Pipe-ID geordnet, sofern verfügbar

### Pipe-Kontext

Beim Rendering einzelner Pipes während der Ausführung:

- `params`: An den aktuellen Pipe übergebene Parameter
- `pipe_results`: Ergebnisse von zuvor ausgeführten Pipes in derselben Pipeline
- `parent_params`: Parameter vom übergeordneten Pipe (wenn der Pipe verschachtelt ist)

Übergeordnete Parameter werden jetzt automatisch für verschachtelte Pipelines befüllt, sodass komposite Pipes mit ihren untergeordneten Pipes mithilfe von `get_parent_param()` oder durch direktes Lesen aus `parent_params` koordinieren können. Service-Instanzen werden derzeit **nicht** in Templates injiziert. Wir planen, Service-Injection in Zukunft zu untersuchen, aber diese Dokumentation spiegelt das derzeit implementierte Verhalten wider.

## Wann Rendering stattfindet

Verschiedene Teile Ihrer Konfiguration werden zu unterschiedlichen Zeitpunkten gerendert:

### Service-Instanziierung

Services im Abschnitt `services` werden gerendert, wenn die Anwendung startet, bevor irgendwelche Pipelines ausgeführt werden. Sie haben nur Zugriff auf den globalen Kontext, der für die Service-Erstellung bereitgestellt wird.

### Pipeline-Erstellung

Pipeline-Definitionen werden gerendert, wenn Pipelines erstellt werden. Sie haben Zugriff auf den globalen Kontext, Pipeline-Parameter und (sofern verfügbar) vorherige Pipeline-Ergebnisse.

### Pipe-Ausführung

Einzelne Pipes werden kurz vor der Ausführung gerendert. Sie haben Zugriff auf globale Daten, Pipeline-Parameter, vorherige Pipe-Ergebnisse und übergeordnete Parameter, wenn der Pipe verschachtelt ist.

## Was gerendert wird

Template Rendering wird auf String-Werte in diesen Konfigurationsabschnitten angewendet:

### Services

- `params`-Werte
- `injects`-Schlüssel und -Werte

### Orchestrator

- `pipelines[].params`-Werte
- `pipelines[].pipes[].params`-Werte
- `pipelines[].pipes[].if`-Bedingungen
- `pipelines[].pipes[].depends_on`-Listen

### Pipes

- Alle Parameterwerte
- Bedingte Ausdrücke
- Abhängigkeitsspezifikationen

> Die Template-Renderer-Konfiguration selbst (`infrastructure.template_renderer_config`) wird niemals gerendert – sie wird als Roh-Eingabe verwendet, um das Rendering-System zu initialisieren. Das Rendering dieser Konfiguration würde eine zirkuläre Abhängigkeit erzeugen, da sie benötigt wird, um den Renderer selbst zu initialisieren.

## Beispiele

### Verwendung von Umgebungsvariablen

```yaml
services:
  - id: api_client
    use: 'mypackage:APIClient'
    params:
      base_url: "{{ get_env('API_BASE_URL') }}"
      api_key: "{{ get_env('API_KEY') }}"
```

### Pipeline-Parameter

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

### Pipe-Abhängigkeiten

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

### Verwendung übergeordneter Parameter in einem kompositen Pipe

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

### Explizites Fehlschlagen eines Pipes

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
- Vermeiden Sie komplexe Logik in Templates – bevorzugen Sie Konfiguration gegenüber Code