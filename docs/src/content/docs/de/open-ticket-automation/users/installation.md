---
title: Installationsanleitung
description: 'Vollständige Anleitung zur Installation von Open Ticket AI mit Docker, OTOBO/Znuny-Setup und Konfiguration.'
lang: en
nav:
  group: Users
  order: 1
---

# Installationsanleitung

Dieser Leitfaden hilft Ihnen, Open Ticket AI auf Ihrem Server zu installieren. Wir empfehlen die Verwendung von Docker Compose für die einfachste und zuverlässigste Installation.

## Installationsübersicht

Die meisten Benutzer sollten mit dem **Docker Quick Start** beginnen. Wenn Docker noch nicht installiert ist, verwenden Sie die **per-OS Tabs** unten.

---

## 1) Ticket-System-Setup (OTOBO / Znuny)

Führen Sie dies **vor** dem Start der Automatisierung aus:

- Erstellen Sie den Benutzer **`open_ticket_ai`** und speichern Sie das Passwort in `.env` als `OTAI_ZNUNY_PASSWORD`
- Importieren Sie das bereitgestellte Webservice-YAML: `deployment/ticket-systems/ticket_operations.yml`
- Stellen Sie sicher, dass die erforderlichen Queues & Priorities vorhanden sind
- Benötigte Berechtigungen: `ro`, `move_into`, `priority`, `note`

Siehe **[OTOBO/Znuny Plugin Setup](otobo-znuny-plugin-setup.md)** für Details.

## 1) Hardware & OS prüfen

Stellen Sie sicher, dass Ihr System die Mindestanforderungen erfüllt:

- **RAM**: Minimum 512 MB (8 GB empfohlen für ML-Modelle)
- **freier Festplattenspeicher**: Minimum 20 GB (50 GB empfohlen für ML-Modelle)
- **OS**: Linux (bevorzugt), Windows 10/11 oder macOS

## 2) Docker & Docker Compose installieren

Befehl, um Ihr OS herauszufinden:

```bash
uname -a
```

Verwenden Sie die untenstehenden Befehle für Ihr OS, um Docker und Docker Compose zu installieren.

:::code-group

```bash title="Ubuntu / Debian"
# Install Docker Engine + Compose plugin
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt-get update
sudo apt-get install -y docker-compose-plugin

# Enable & test
sudo usermod -aG docker "$USER"
newgrp docker
docker --version
docker compose version
```

```bash title="RHEL / CentOS / Rocky / Alma"
# Prereqs
sudo dnf -y install dnf-plugins-core

# Docker CE repo
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Install Engine + Compose plugin
sudo dnf -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Enable & test
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
newgrp docker
docker --version
docker compose version
```

```bash title="Fedora"
# Install Engine + Compose plugin
sudo dnf -y install dnf-plugins-core
sudo dnf -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Enable & test
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
newgrp docker
docker --version
docker compose version
```

```bash title="openSUSE / SLES"
# Install Docker
sudo zypper refresh
sudo zypper install -y docker docker-compose

# Enable & test
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
newgrp docker
docker --version
docker compose version
```

```bash title="Arch Linux"
# Install Docker + Compose
sudo pacman -Syu --noconfirm docker docker-compose

# Enable & test
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
newgrp docker
docker --version
docker compose version
```

```bash title="macOS"
# Option A: Docker Desktop (GUI)
# Download: https://www.docker.com/products/docker-desktop/
# Then verify:
docker --version
docker compose version

# Option B: Homebrew (installs Desktop app)
brew install --cask docker
open -a Docker
docker --version
docker compose version
```

```powershell title="Windows 10/11"
# Option A: Docker Desktop (recommended)
winget install -e --id Docker.DockerDesktop

# Option B: Ensure WSL2 is enabled (if prompted by Docker Desktop)
wsl --install
wsl --set-default-version 2

# Verify in a new PowerShell
docker --version
docker compose version
```

:::

---

## 3) `config.yml` & `deployment/compose.yml` einrichten

Verwenden Sie diese, wenn Sie bereit sind, Dateien unter `/opt/open_ticket_ai` (Linux) abzulegen.

```bash
sudo mkdir -p /opt/open_ticket_ai
sudo chown "$USER":"$USER" /opt/open_ticket_ai -R
cd /opt/open_ticket_ai
```

```bash
cat > .env <<'EOF'
OTAI_HF_TOKEN=your_hf_token_here
OTAI_ZNUNY_PASSWORD=your_secure_password_here
EOF
```

```bash
# Optional: keep secrets out of git
echo ".env" >> .gitignore
```

### /opt/open-ticket-ai/config.yml erstellen

:::caution
Dies ist ein Beispiel! Passen Sie es an Ihr Ticket-System-Setup, Queues, Priorities und 
:::

<details>
<summary>Beispiel <code>config.yml</code></summary>

```yaml
open_ticket_ai:
  api_version: '>=1.0.0'
  infrastructure:
    logging:
      level: 'INFO'
      log_to_file: false
      log_file_path: null

  services:
    jinja_default:
      use: 'base:JinjaRenderer'

    otobo_znuny:
      use: 'otobo-znuny:OTOBOZnunyTicketSystemService'
      params:
        base_url: 'http://host.docker.internal/znuny/nph-genericinterface.pl'
        password: "{{ get_env('OTAI_ZNUNY_PASSWORD') }}"

    hf_local:
      use: 'hf-local:HFClassificationService'
      params:
        api_token: "{{ get_env('OTAI_HF_TOKEN') }}"

  orchestrator:
    use: 'base:SimpleSequentialOrchestrator'
    params:
      orchestrator_sleep: 'PT5S'
      steps:
        - id: runner
          use: 'base:SimpleSequentialRunner'
          params:
            on:
              id: 'interval'
              use: 'base:IntervalTrigger'
              params:
                interval: 'PT2S'
            run:
              id: 'pipeline'
              use: 'base:CompositePipe'
              params:
                steps:
                  - id: fetch
                    use: 'base:FetchTicketsPipe'
                    injects: { ticket_system: 'otobo_znuny' }
                    params:
                      ticket_search_criteria:
                        queue: { name: 'Anfrage an die IT' }
                        limit: 1
                  - id: ticket
                    use: 'base:ExpressionPipe'
                    params:
                      expression: "{{ get_pipe_result('fetch','fetched_tickets')[0] if (get_pipe_result('fetch','fetched_tickets')|length)>0 else fail() }}"
                  - id: cls_queue
                    use: 'base:ClassificationPipe'
                    injects: { classification_service: 'hf_local' }
                    params:
                      text: "{{ get_pipe_result('ticket')['subject'] }} {{ get_pipe_result('ticket')['body'] }}"
                      model_name: 'softoft/EHS_Queue_Prediction'
                  - id: queue_final
                    use: 'base:ExpressionPipe'
                    params:
                      expression: "{{ get_pipe_result('cls_queue','label') if get_pipe_result('cls_queue','confidence')>=0.8 else 'Unklassifiziert' }}"
                  - id: update_queue
                    use: 'base:UpdateTicketPipe'
                    injects: { ticket_system: 'otobo_znuny' }
                    params:
                      ticket_id: "{{ get_pipe_result('ticket')['id'] }}"
                      updated_ticket:
                        queue: { name: "{{ get_pipe_result('queue_final') }}" }
```

</details>

Zum Testen setzen Sie das Log-Level auf DEBUG und das Intervall auf 5 Sekunden; in der Produktion setzen Sie das Intervall auf 10 ms und das Log-Level auf INFO.

- Repo-Deploymentsverzeichnis:
  [https://github.com/Softoft-Orga/open-ticket-ai/tree/dev/deployment](https://github.com/Softoft-Orga/open-ticket-ai/tree/dev/deployment)
- Znuny-Demo `config.yml`:
  [https://github.com/Softoft-Orga/open-ticket-ai/blob/dev/deployment/znuny_demo/config.yml](https://github.com/Softoft-Orga/open-ticket-ai/blob/dev/deployment/znuny_demo/config.yml)
- Znuny-Demo `compose.yml`:
  [https://github.com/Softoft-Orga/open-ticket-ai/blob/dev/deployment/znuny_demo/compose.yml](https://github.com/Softoft-Orga/open-ticket-ai/blob/dev/deployment/znuny_demo/compose.yml)

### opt/open-ticket-ai/compose.yml erstellen

Versionen auf Github und Dockerhub prüfen

```yaml
services:
  open-ticket-ai:
    image: openticketai/engine:1.4.19
    restart: 'always'
    volumes:
      - ./config.yml:/app/config.yml:ro
    extra_hosts:
      - 'host.docker.internal:host-gateway'
    environment:
      - OTAI_HF_TOKEN
      - OTAI_ZNUNY_PASSWORD
      - HUGGING_FACE_HUB_TOKEN=${OTAI_HF_TOKEN}
      - HF_TOKEN=${OTAI_HF_TOKEN}
    logging:
      driver: json-file
      options:
        max-size: '50m'
        max-file: '3'
```

### Konfiguration prüfen

- Umgebungsvariablen sind gesetzt und stimmen mit compose.yml, config.yml, .env oder .bashrc überein
- `config.yml` verweist auf das korrekte Ticket-System, Queues, Priorities, Types, Services, SLAs, ...
- `compose.yml` verwendet die korrekte Image-Version
- Korrekter API-Pfad "/znuny/nph-genericinterface.pl" in `config.yml` oder /otobo/nph-genericinterface.pl oder zammad ...
- Ticket-System-Benutzer `open_ticket_ai` existiert mit dem korrekten Passwort
- Erforderliche Queues & Priorities, Types, Services, Users, ... existieren im Ticket-System
- Berechtigungen für Benutzer `open_ticket_ai`

### Start / Neustart / Logs

```bash
docker compose  up -d
```

```bash
docker compose  restart
```

```bash
docker compose logs -f open-ticket-ai
```

---

### Zusätzliche Informationen für OTOBO / Znuny Setup

Es scheint Unterschiede bei den Content Types zwischen OTOBO- und Znuny-Versionen zu geben! Möglicherweise müssen Sie Ihren ContentType ändern, wenn ungültige ContentType-Fehler auftreten. Ändern Sie daher die Parameter von AddNotePipe in Ihrer config.yml wie folgt:

```yaml
-   id: add_note
    use: "base:AddNotePipe"
    injects: { ticket_system: "otobo_znuny" }
    params:
        ticket_id: "{{ get_pipe_result('ticket')['id'] }}"
        note:
            subject: "This is a note added by Open Ticket AI."
            body: "Automated note content."
            content_type: "text/plain; charset=utf8"
```

---

## Verifizierungs-Checkliste

* `.env` enthält `OTAI_HF_TOKEN` und `OTAI_ZNUNY_PASSWORD`
* `deployment/compose.yml` verwendet `image: openticketai/engine:1.4.19`
* OTOBO/Znuny-Webservice importiert; Benutzer `open_ticket_ai` existiert
* Queues & Priorities im Ticket-System vorhanden
* Ausführen: `docker compose -f deployment/compose.yml up -d`
* Logs prüfen: `docker compose -f deployment/compose.yml logs -f open-ticket-ai`
* Optional: `open-ticket-ai verify-connection` im Container ausführen (falls verfügbar)

### Hilfe erhalten

Wenn Sie auf Probleme stoßen:

1. Logs prüfen: `docker compose logs -f`
2. Syntax Ihrer Konfigurationsdatei überprüfen
3. Die [Configuration Reference](../details/config_reference.md) prüfen
4. Besuchen Sie unsere [GitHub Issues](https://github.com/Softoft-Orga/open-ticket-ai/issues)
5. Nehmen Sie an unseren Community-Diskussionen teil

## Nächste Schritte

Nach der Installation:

1. **Ihre erste Pipeline konfigurieren** - Siehe [First Pipeline Guide](first_pipeline.md)
2. **Mit Ihrem Ticket-System verbinden** - Siehe [OTOBO/Znuny Integration](../users/ticket_systems.md)
3. **KI-Klassifizierung einrichten** - Siehe [ML Model Configuration](../users/ml_models.md)
4. **Sicherheitseinstellungen überprüfen** - Siehe [Security Best Practices](../users/security.md)

## Verwandte Dokumentation

- [Quick Start Guide](quick_start.md) - Schnell starten
- [First Pipeline](first_pipeline.md) - Erstellen Sie Ihre erste Automation
- [Configuration Reference](../details/config_reference.md) - Vollständige Konfigurationsdokumentation
- [Plugin System](../users/plugins.mdx) - Verständnis von Plugins