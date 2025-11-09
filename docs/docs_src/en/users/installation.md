---
description: Easy installation guide for Open Ticket AI using Docker Compose - the recommended method for production deployment with all plugins included.
---

# Installation Guide

This guide will help you install Open Ticket AI on your server. We recommend using Docker Compose
for the easiest and most reliable installation.

## Installation Overview

Most users should start with the **Docker Quick Start**. If Docker isn't installed yet, use the *
*per-OS tabs** below.

---

## 1) Ticket System Setup (OTOBO / Znuny)

Complete this **before** starting automation:

* Create user **`open_ticket_ai`** and store the password in `.env` as `OTAI_ZNUNY_PASSWORD`
* Import the provided webservice YAML:
  `deployment/ticket-systems/ticket_operations.yml`
* Ensure required Queues & Priorities exist
* Permissions needed: `ro`, `move_into`, `priority`, `note`

See **[OTOBO/Znuny Plugin Setup](./plugin-otobo-znuny/setup.md)** for details.


## 1) Check Hardware & OS

Ensure your system meets the minimum requirements:

- **RAM**: Minimum 512 MB (8 GB recommended for ML models)
- **free Disk Space**: Minimum 20 GB (50 GB recommended for ML models)
- **OS**: Linux (preferred), Windows 10/11, or macOS

## 2) Install Docker & Docker Compose

Command to find out your OS:

```bash
uname -a
```

Use the commands for your OS below to install Docker and Docker Compose.

::: code-group

```bash [Ubuntu / Debian]
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

```bash [RHEL / CentOS / Rocky / Alma]
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

```bash [Fedora]
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

```bash [openSUSE / SLES]
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

```bash [Arch Linux]
# Install Docker + Compose
sudo pacman -Syu --noconfirm docker docker-compose

# Enable & test
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
newgrp docker
docker --version
docker compose version
```

```bash [macOS]
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

```powershell [Windows 10/11]
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

## 3) Setup `config.yml` & `deployment/compose.yml`

Use these if you’re ready to place files under `/opt/open_ticket_ai` (Linux).

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

````bash
# Optional: keep secrets out of git
echo ".env" >> .gitignore
````

### Create /opt/open-ticket-ai/config.yml


::: warning
This is an example! Adjust according to your ticket system setup, queues, priorities, and
:::

:::details Example `config.yml`

```yaml
open_ticket_ai:
    api_version: ">=1.0.0"
    infrastructure:
        logging:
            level: "INFO"
            log_to_file: false
            log_file_path: null

    services:
        jinja_default:
            use: "base:JinjaRenderer"

        otobo_znuny:
            use: "otobo-znuny:OTOBOZnunyTicketSystemService"
            params:
                base_url: "http://host.docker.internal/znuny/nph-genericinterface.pl"
                password: "{{ get_env('OTAI_ZNUNY_PASSWORD') }}"

        hf_local:
            use: "hf-local:HFClassificationService"
            params:
                api_token: "{{ get_env('OTAI_HF_TOKEN') }}"

    orchestrator:
        use: "base:SimpleSequentialOrchestrator"
        params:
            orchestrator_sleep: "PT5S"
            steps:
                -   id: runner
                    use: "base:SimpleSequentialRunner"
                    params:
                        on:
                            id: "interval"
                            use: "base:IntervalTrigger"
                            params:
                                interval: "PT2S"
                        run:
                            id: "pipeline"
                            use: "base:CompositePipe"
                            params:
                                steps:
                                    -   id: fetch
                                        use: "base:FetchTicketsPipe"
                                        injects: { ticket_system: "otobo_znuny" }
                                        params:
                                            ticket_search_criteria:
                                                queue: { name: "Anfrage an die IT" }
                                                limit: 1
                                    -   id: ticket
                                        use: "base:ExpressionPipe"
                                        params:
                                            expression: "{{ get_pipe_result('fetch','fetched_tickets')[0] if (get_pipe_result('fetch','fetched_tickets')|length)>0 else fail() }}"
                                    -   id: cls_queue
                                        use: "base:ClassificationPipe"
                                        injects: { classification_service: "hf_local" }
                                        params:
                                            text: "{{ get_pipe_result('ticket')['subject'] }} {{ get_pipe_result('ticket')['body'] }}"
                                            model_name: "softoft/EHS_Queue_Prediction"
                                    -   id: queue_final
                                        use: "base:ExpressionPipe"
                                        params:
                                            expression: "{{ get_pipe_result('cls_queue','label') if get_pipe_result('cls_queue','confidence')>=0.8 else 'Unklassifiziert' }}"
                                    -   id: update_queue
                                        use: "base:UpdateTicketPipe"
                                        injects: { ticket_system: "otobo_znuny" }
                                        params:
                                            ticket_id: "{{ get_pipe_result('ticket')['id'] }}"
                                            updated_ticket:
                                                queue: { name: "{{ get_pipe_result('queue_final') }}" }
```
:::


For Testing set log level DEBUG and the interval to 5 seconds in production set interval to 10ms and
log level to INFO.

* Repo deployment directory:
  [https://github.com/Softoft-Orga/open-ticket-ai/tree/dev/deployment](https://github.com/Softoft-Orga/open-ticket-ai/tree/dev/deployment)
* Znuny demo `config.yml`:
  [https://github.com/Softoft-Orga/open-ticket-ai/blob/dev/deployment/znuny_demo/config.yml](https://github.com/Softoft-Orga/open-ticket-ai/blob/dev/deployment/znuny_demo/config.yml)
* Znuny demo `compose.yml`:
  [https://github.com/Softoft-Orga/open-ticket-ai/blob/dev/deployment/znuny_demo/compose.yml](https://github.com/Softoft-Orga/open-ticket-ai/blob/dev/deployment/znuny_demo/compose.yml)

### Create opt/open-ticket-ai/compose.yml
Check Versions on Github and Dockerhub
```yaml
services:
    open-ticket-ai:
        image: openticketai/engine:1.4.19
        restart: "always"
        volumes:
            - ./config.yml:/app/config.yml:ro
        extra_hosts:
            - "host.docker.internal:host-gateway"
        environment:
            - OTAI_HF_TOKEN
            - OTAI_ZNUNY_PASSWORD
            - HUGGING_FACE_HUB_TOKEN=${OTAI_HF_TOKEN}
            - HF_TOKEN=${OTAI_HF_TOKEN}
        logging:
            driver: json-file
            options:
                max-size: "50m"
                max-file: "3"
```

### Check Configuration

- Environment Vars are set and match compose.yml, config.yml, .env or .bashrc
- `config.yml` references correct ticket system, queues, priorities, types, services, slas, ...
- `compose.yml` uses correct image version
- Correct API Path "/znuny/nph-genericinterface.pl" in `config.yml` or /otobo/nph-genericinterface.pl or zammad ...
- Ticket system user `open_ticket_ai` exists with correct password
- Required Queues & Priorities, Types, Services, Users, ... exist in ticket system
- Permissions for user `open_ticket_ai`



### Start / Restart / Logs


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

### Extra Info for OTOBO / Znuny Setup

It seems like there are differences in Content Types between OTOBO Znuny Versions!
You might need to change your COntentType when ContentType invalid errors occur.
Therefore change the params of AddNotePipe in your config.yml like this:

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

---

## Verification Checklist

* `.env` contains `OTAI_HF_TOKEN` and `OTAI_ZNUNY_PASSWORD`
* `deployment/compose.yml` uses `image: openticketai/engine:1.4.19`
* OTOBO/Znuny webservice imported; user `open_ticket_ai` exists
* Queues & priorities present in the ticket system
* Run: `docker compose -f deployment/compose.yml up -d`
* Check logs: `docker compose -f deployment/compose.yml logs -f open-ticket-ai`
* Optionally: run `open-ticket-ai verify-connection` inside the container (if available)

### Getting Help

If you encounter issues:

1. Check the logs: `docker compose logs -f`
2. Verify your configuration file syntax
3. Review the [Configuration Reference](../details/_config_reference.md)
4. Visit our [GitHub Issues](https://github.com/Softoft-Orga/open-ticket-ai/issues)
5. Join our community discussions

## Next Steps

After installation:

1. **Configure your first pipeline** - See [First Pipeline Guide](first_pipeline.md)
2. **Connect to your ticket system** - See [OTOBO/Znuny Integration](../users/ticket_systems.md)
3. **Set up AI classification** - See [ML Model Configuration](../users/ml_models.md)
4. **Review security settings** - See [Security Best Practices](../users/security.md)

## Related Documentation

- [Quick Start Guide](quick_start.md) - Get started quickly
- [First Pipeline](first_pipeline.md) - Create your first automation
- [Configuration Reference](../details/_config_reference.md) - Complete config documentation
- [Plugin System](../users/plugins.md) - Understanding plugins
