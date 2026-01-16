---
title: OTOBO / Znuny Setup Guide
---

# OTOBO / Znuny Setup Guide

Open Ticket AI verbindet sich mit OTOBO/Znuny über einen eingeschränkten WebService und einen dedizierten technischen Benutzer.
Folgen Sie diesen Schritten genau, um einen zuverlässigen und sicheren Betrieb der Automatisierung zu gewährleisten.

---

## 1. Benutzer `open_ticket_ai` erstellen

Dieser Benutzer wird ausschließlich von der Open Ticket AI Engine verwendet.
Er **darf keine** Admin-Berechtigungen haben.
Er muss **genau und nur die Berechtigungen** haben, die für Ihre Automatisierung erforderlich sind.

### Schritt 1: Gehen Sie zu Admin → Agents

Nutzen Sie die OTOBO Admin-Navigation:

![](/assets/otobo-admin.png)

---

### Schritt 2: Klicken Sie auf „Add Agent“

<img src="https://doc.otobo.org/manual/admin/10.0/en/_images/agent-add.png" alt="Add Agent" width="800" />

Füllen Sie aus:

| Feld          | Wert                         |
| ------------- | ---------------------------- |
| **Username**  | `open_ticket_ai`             |
| **Firstname** | Open                         |
| **Lastname**  | Ticket AI                    |
| **Email**     | (beliebig)                   |
| **Password**  | 16-stelliges Zufallspasswort |

### Ein sicheres Passwort generieren

:::code-group

```bash title="Linux/macOS"
openssl rand -base64 32 | cut -c1-16
```

```powershell title="Windows"
# PowerShell
-join ((33..126) | Get-Random -Count 16 | ForEach-Object {[char]$_})
```

:::

---

### Schritt 3: Passwort als Umgebungsvariable speichern

Setzen Sie das Passwort je nach Ihrer Deployment-Umgebung als Umgebungsvariable:

```
OTAI_ZNUNY_PASSWORD=your_generated_password_here
```

Sie können es anders benennen, aber es muss mit Ihrer Open Ticket AI Konfiguration übereinstimmen.
Speichern Sie dieses Passwort niemals in Git.
Verwenden Sie `.env` + Server-Geheimnisspeicher.

---

## 2. Berechtigungen zuweisen (Agents ↔ Groups oder Agents ↔ Roles)

Open Ticket AI kann nur Aktionen ausführen, die dem Benutzer erlaubt sind.

Je nach Automatisierungspipeline müssen Sie gewähren:

| Automatisierungstyp    | Erforderliche Berechtigungen                 |
| ---------------------- | -------------------------------------------- |
| Queue Classification   | **ro**, **move_into**                        |
| Priority Classification| **ro**, **priority**                         |
| Note creation          | **ro**, **note**                             |
| Ticket updates         | **ro**, **move_into**, **priority**, **note**|

---

### Option A — Über Gruppen zuweisen (empfohlen)

Gehen Sie zu:

**Admin → Agents ↔ Groups**

<img src="https://doc.otobo.org/manual/admin/10.0/en/_images/agent-group-management.png" alt="Agent Group Management" width="800" />

Wählen Sie den Agent **open_ticket_ai** und vergeben Sie Berechtigungen wie:

| Berechtigung | Bedeutung                   |
| ------------ | --------------------------- |
| ro           | Ticket lesen                |
| move_into    | Ticket in Queue verschieben |
| priority     | Priorität ändern            |
| note         | Interne Notizen hinzufügen  |

## rw, wenn Sie ein Ticket erstellen müssen.

## Option B — Über Rollen zuweisen (optional, aber skalierbar)

Wenn Ihr OTOBO Rollen → Gruppen-Mapping verwendet, weisen Sie zu:

**Admin → Agents ↔ Roles**

Stellen Sie dann sicher, dass die Rolle die erforderlichen Gruppenberechtigungen hat.

---

## 3. Sicherstellen, dass Queues, Prioritäten und Felder existieren

Ihre Automatisierungspipeline bezieht sich auf bestimmte Namen wie:

- Queues: _"IT"_, _"Real Estate"_, etc.
- Priorities: _"3 Mittel"_, _"5 Kritisch"_, etc.
- Types, Services (falls verwendet)

### Sie müssen manuell bestätigen:

✅ Jede Queue in Ihrer `config.yml` existiert
✅ Jede Priorität, die Ihr ML-Modell vorhersagt, existiert
✅ Wenn Sie "note"-Aktionen verwenden → Agent hat Berechtigung
✅ Ticket-Typen, auf die in der Automatisierung verwiesen wird, existieren

Wenn der Name falsch ist, schlägt das WebService-Update fehl.

---

## 4. WebService „OpenTicketAI“ erstellen

Gehen Sie zu:

**Admin → Web Services**

![](/assets/webservice_overview.png)

---

### Schritt 1: Klicken Sie auf „Add Web Service“

![](/assets/otobo_webservice_import.png)

Wählen Sie dann **Import Web Service**.

---

### Schritt 2: Webservice importieren

Verwenden Sie die mit Open Ticket AI mitgelieferte Vorlage:

[Open Ticket Ai yaml](https://raw.githubusercontent.com/Softoft-Orga/open-ticket-ai/refs/heads/dev/deployment/znuny_demo/OpenTicketAI.yml)

Laden Sie die Datei mit dem Button **Import web service** hoch.

Dies erstellt:

- `/ticket-get`
- `/ticket-update`
- `/ticket-search`
- `/ticket-create`

Alle sind so eingeschränkt, dass **nur der Benutzer `open_ticket_ai` sie verwenden darf**.

---

## 5. Warum der WebService eingeschränkt ist

Das importierte YAML enthält:

```yaml
ValueMap:
  UserLogin:
    ValueMapRegEx:
      .*: open_ticket_ai
```

Dies zwingt *jede* eingehende Anfrage, sich als `open_ticket_ai` zu authentifizieren
– selbst wenn ein Angreifer beliebige Benutzernamen sendet.

Dies verhindert:

- Passwort-Brute-Force-Angriffe
- API-Missbrauch
- Unautorisierte Ticket-Manipulation

Mit einem **16-stelligen Zufallspasswort** ist Brute-Force selbst unter extremer Last unmöglich.

---

## 6. Überprüfen, ob der WebService aktiv ist

Nach dem Import sollte Ihre Liste zeigen:

![](/assets/webservice_overview.png)

Prüfen Sie:

✅ Name: **OpenTicketAI**
✅ Provider Transport: **HTTP::REST**
✅ Validity: **valid**
✅ Eingeschränkt auf Benutzer `open_ticket_ai`

Wenn nicht gültig, bearbeiten → erneut speichern.