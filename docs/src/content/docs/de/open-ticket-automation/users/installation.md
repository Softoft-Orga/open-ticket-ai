---
title: Installationsanleitung
description: 'Vollständige Anleitung zur Installation von Open Ticket AI mit Docker, OTOBO/Znuny-Einrichtung und Konfiguration.'
lang: de
nav:
  group: Benutzer
  order: 1
---

# Installationsanleitung

Diese Anleitung hilft Ihnen, Open Ticket AI auf Ihrem Server zu installieren. Wir empfehlen die Verwendung von Docker Compose für die einfachste und zuverlässigste Installation.

## Installationsübersicht

Die meisten Benutzer sollten mit dem **Docker Quick Start** beginnen. Wenn Docker noch nicht installiert ist, verwenden Sie die **\* \*pro-OS-Tabs\*\*** unten.

---

## 1) Ticket-System-Einrichtung (OTOBO / Znuny)

Führen Sie dies **vor** dem Start der Automatisierung durch:

- Erstellen Sie den Benutzer **`open_ticket_ai`** und speichern Sie das Passwort in `.env` als `OTAI_ZNUNY_PASSWORD`
- Importieren Sie die bereitgestellte Webservice-YAML:
  `deployment/ticket-systems/ticket_operations.yml`
- Stellen Sie sicher, dass die erforderlichen Queues & Prioritäten existieren
- Erforderliche Berechtigungen: `ro`, `move_into`, `priority`, `note`

Details finden Sie unter **[OTOBO/Znuny Plugin Setup](otobo-znuny-plugin-setup.md)**.

## 1) Hardware & OS prüfen

Stellen Sie sicher, dass Ihr System die Mindestanforderungen erfüllt:

- **RAM**: Mindestens 512 MB (8 GB empfohlen für ML-Modelle)
- **Freier Festplattenspeicher**: Mindestens 20 GB (50 GB empfohlen für ML-Modelle)
- **OS**: Linux (bevorzugt), Windows 10/11 oder macOS

## 2) Docker & Docker Compose installieren

Befehl, um Ihr OS herauszufinden:

```bash
uname -a
```

Verwenden Sie die Befehle für Ihr OS unten, um Docker und Docker Compose zu installieren.

:::code-group

```bash title="Ubuntu / Debian"
# Docker Engine + Compose Plugin installieren
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt-get update
sudo apt-get install -y docker-compose-plugin

# Aktivieren & testen
sudo usermod -aG docker "$USER"
newgrp docker
docker --version
docker compose version
```

```bash title="RHEL / CentOS / Rocky / Alma"
# Voraussetzungen
sudo dnf -y install dnf-plugins-core

# Docker CE Repo
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Engine + Compose Plugin installieren
sudo dnf -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Aktivieren & testen
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
newgrp docker
docker --version
docker compose version
```

```bash title="Fedora"
# Engine + Compose Plugin installieren
sudo dnf -y install dnf-plugins-core
sudo dnf -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Aktivieren & testen
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
newgrp docker
docker --version
docker compose version
```

```bash title="openSUSE / SLES"
# Docker installieren
sudo zypper refresh
sudo zypper install -y docker docker-compose

# Aktivieren & testen
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
newgrp docker
docker --version
docker compose version
```

```bash title="Arch Linux"
# Docker + Compose installieren
sudo pacman -Syu --noconfirm docker docker-compose

# Aktivieren & testen
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
newgrp docker
docker --version
docker compose version
```

```bash title="macOS"
# Option A: Docker Desktop (GUI)
# Download: https://www.docker.com/products/docker-desktop/
# Dann verifizieren:
docker --version
docker compose version

# Option B: Homebrew (installiert Desktop-App)
brew install --cask docker
open -a Docker
docker --version
docker compose version
```

```powershell title="Windows 10/11"
# Option A: Docker Desktop (empfohlen)
winget install -e --id Docker.DockerDesktop

# Option B: WSL2 aktivieren (falls von Docker Desktop gefordert)
wsl --install
wsl --set-default-version 2

# In einer neuen PowerShell verifizieren
docker --version
docker compose version
```

:::

---

## 3) `config.yml` & `deployment/compose.yml` einrichten

Verwenden Sie diese Befehle, wenn Sie bereit sind, Dateien unter `/opt/open_ticket_ai` (Linux) abzulegen.

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
# Optional: Secrets aus Git fernhalten
echo ".env" >> .gitignore
```

### /opt/open-ticket-ai/config.yml erstellen

:::caution
Dies ist ein Beispiel! Passen Sie es an Ihre Ticket-System-Einrichtung, Queues, Prioritäten und
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

Zum Testen log level auf DEBUG und das Intervall auf 5 Sekunden setzen. In der Produktion Intervall auf 10ms und log level auf INFO setzen.

- Repo deployment Verzeichnis:
  [https://github.com/Softoft-Orga/open-ticket-ai/tree/dev/deployment](https://github.com/Softoft-Orga/open-ticket-ai/tree/dev/deployment)
- Znuny Demo `config.yml`:
  [https://github.com/Softoft-Orga/open-ticket-ai/blob/dev/deployment/znuny_demo/config.yml](https://github.com/Softoft-Orga/open-ticket-ai/blob/dev/deployment/znuny_demo/config.yml)
- Znuny Demo `compose.yml`:
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
- `config.yml` verweist auf korrektes Ticket-System, Queues, Prioritäten, Typen, Services, SLAs, ...
- `compose.yml` verwendet korrekte Image-Version
- Korrekter API-Pfad "/znuny/nph-genericinterface.pl" in `config.yml` oder /otobo/nph-genericinterface.pl oder zammad ...
- Ticket-System-Benutzer `open_ticket_ai` existiert mit korrektem Passwort
- Erforderliche Queues & Prioritäten, Typen, Services, Benutzer, ... existieren im Ticket-System
- Berechtigungen für Benutzer `open_ticket_ai`

### Starten / Neustarten / Logs

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

### Zusatzinfo für OTOBO / Znuny Setup

Es scheint Unterschiede in den Content Types zwischen OTOBO Znuny Versionen zu geben!
Möglicherweise müssen Sie Ihren ContentType ändern, wenn ContentType invalid Fehler auftreten.
Ändern Sie daher die params des AddNotePipe in Ihrer config.yml wie folgt:

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

## Verifikations-Checkliste

* `.env` enthält `OTAI_HF_TOKEN` und `OTAI_ZNUNY_PASSWORD`
* `deployment/compose.yml` verwendet `image: openticketai/engine:1.4.19`
* OTOBO/Znuny-Webservice importiert; Benutzer `open_ticket_ai` existiert
* Queues & Prioritäten im Ticket-System vorhanden
* Ausführen: `docker compose -f deployment/compose.yml up -d`
* Logs prüfen: `docker compose -f deployment/compose.yml logs -f open-ticket-ai`
* Optional: `open-ticket-ai verify-connection` im Container ausführen (falls verfügbar)

### Hilfe erhalten

Wenn Probleme auftreten:

1. Prüfen Sie die Logs: `docker compose logs -f`
2. Überprüfen Sie die Syntax Ihrer Konfigurationsdatei
3. Lesen Sie die [Configuration Reference](../details/config_reference.md)
4. Besuchen Sie unsere [GitHub Issues](https://github.com/Softoft-Orga/open-ticket-ai/issues)
5. Nehmen Sie an unseren Community-Diskussionen teil

## Nächste Schritte

Nach der Installation:

1. **Ihre erste Pipeline konfigurieren** - Siehe [First Pipeline Guide](first_pipeline.md)
2. **Mit Ihrem Ticket-System verbinden** - Siehe [OTOBO/Znuny Integration](../users/ticket_systems.md)
3. **AI-Klassifizierung einrichten** - Siehe [ML Model Configuration](../users/ml_models.md)
4. **Sicherheitseinstellungen überprüfen** - Siehe [Security Best Practices](../users/security.md)

## Verwandte Dokumentation

- [Quick Start Guide](quick_start.md) - Schnellstart
- [First Pipeline](first_pipeline.md) - Erstellen Sie Ihre erste Automatisierung
- [Configuration Reference](../details/config_reference.md) - Vollständige Konfigurationsdokumentation
- [Plugin System](../users/plugins.mdx) - Plugins verstehen