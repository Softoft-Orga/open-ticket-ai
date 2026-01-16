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

Die meisten Benutzer sollten mit dem **Docker Quick Start** beginnen. Wenn Docker noch nicht installiert ist, verwenden Sie die **\* \*OS-spezifischen Tabs\*\*** unten.

---

## 1) Ticket-System-Einrichtung (OTOBO / Znuny)

Führen Sie dies **vor** dem Start der Automatisierung durch:

- Erstellen Sie den Benutzer **`open_ticket_ai`** und speichern Sie das Passwort in `.env` als `OTAI_ZNUNY_PASSWORD`
- Importieren Sie den bereitgestellten Webservice-YAML:
  `deployment/ticket-systems/ticket_operations.yml`
- Stellen Sie sicher, dass die erforderlichen Queues & Prioritäten existieren
- Benötigte Berechtigungen: `ro`, `move_into`, `priority`, `note`

Details finden Sie unter **[OTOBO/Znuny Plugin Setup](otobo-znuny-plugin-setup.md)**.

## 1) Hardware & OS prüfen

Stellen Sie sicher, dass Ihr System die Mindestanforderungen erfüllt:

- **RAM**: Mindestens 512 MB (8 GB empfohlen für ML-Modelle)
- **Freier Speicherplatz**: Mindestens 20 GB (50 GB empfohlen für ML-Modelle)
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

Verwenden Sie diese, wenn Sie bereit sind, Dateien unter `/opt/open_ticket_ai` (Linux) abzulegen.

```bash
sudo mkdir -p /opt/open_ticket_ai
sudo chown "$USER":"
```
