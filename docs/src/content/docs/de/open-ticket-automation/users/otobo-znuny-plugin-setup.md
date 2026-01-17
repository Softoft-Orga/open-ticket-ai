---
title: OTOBO / Znuny Einrichtungsanleitung
---

# OTOBO / Znuny Einrichtungsanleitung

Open Ticket AI verbindet sich mit OTOBO/Znuny über einen eingeschränkten WebService und einen dedizierten technischen Benutzer. Befolgen Sie diese Schritte exakt, um sicherzustellen, dass die Automatisierung zuverlässig und sicher funktioniert.

---

## 1. Erstellen Sie den Benutzer `open_ticket_ai`

Dieser Benutzer wird ausschließlich von der Open Ticket AI Engine verwendet. Er **darf** keine Administrator‑Rechte haben. Er muss **genau die erforderlichen Berechtigungen** für Ihre Automatisierung besitzen.

### Schritt 1: Gehen Sie zu Admin → Agents

Verwenden Sie die OTOBO Admin Navigation:

![](/assets/otobo-admin.png)

---

### Schritt 2: Klicken Sie auf “Add Agent”

<img src="https://doc.otobo.org/manual/admin/10.0/en/_images/agent-add.png" alt="Add Agent" width="800" />

Füllen Sie aus:

| Field         | Value                        |
| ------------- | ---------------------------- |
| **Username**  | `open_ticket_ai`             |
| **Firstname** | Open                         |
| **Lastname**  | Ticket AI                    |
| **Email**     | (anything)                   |
| **Password**  | 16-character random password |

### Generieren Sie ein sicheres Passwort

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

### Schritt 3: Speichern Sie das Passwort als Umgebungsvariable

Abhängig von Ihrer Bereitstellung setzen Sie das Passwort als Umgebungsvariable:

```
OTAI_ZNUNY_PASSWORD=your_generated_password_here
```

Sie können ihm einen anderen Namen geben, aber er muss zu Ihrer Open Ticket AI‑Konfiguration machth. Speichern Sie dieses Passwort niemals im Git. Verwenden Sie `.env` + Server‑Geheimnisspeicherung.

---

## 2. Berechtigungen zuweisen (Agents ↔ Groups oder Agents ↔ Roles)

Open Ticket AI kann nur Aktionen ausführen, die dem Benutzer erlaubt sind.

Abhängig von Ihrer Automatisierungspipeline müssen Sie gewähren:

| Automation Type         | Required Permissions                          |
| ----------------------- | --------------------------------------------- |
| Queue Classification    | **ro**, **move_into**                         |
| Priority Classification | **ro**, **priority**                          |
| Note creation           | **ro**, **note**                              |
| Ticket updates          | **ro**, **move_into**, **priority**, **note** |

### Option A — Zuweisung über Groups (empfohlen)

Gehen Sie zu:

**Admin → Agents ↔ Groups**

<img src="https://doc.otobo.org/manual/admin/10.0/en/_images/agent-group-management.png" alt="Agent Group Management" width="800" />

Wählen Sie den Agenten **open_ticket_ai** aus und vergeben Sie Berechtigungen wie:

| Permission | Meaning                |
| ---------- | ---------------------- |
| ro         | Read ticket            |
| move_into  | Move ticket into queue |
| priority   | Change priority        |
| note       | Add internal notes     |

## rw falls Sie ein Ticket erstellen müssen.

## Option B — Zuweisung über Roles (optional aber skalierbar)

Wenn Ihr OTOBO Roles → Groups‑Mapping verwendet, weisen Sie zu:

**Admin → Agents ↔ Roles**

Dann stellen Sie sicher, dass die Role die erforderlichen Gruppen‑Berechtigungen hat.

---

## 3. Stellen Sie sicher, dass Queues, Priorities und Fields existieren

Ihre Automatisierungspipeline bezieht sich auf spezifische Namen wie:

- Queues: _“IT”_, _“Real Estate”_, etc.
- Priorities: _“3 Mittel”_, _“5 Kritisch”_, etc.
- Types, Services (if used)

### Sie müssen manuell bestätigen:

✅ Jede Queue in Ihrer `config.yml` existiert  
✅ Jede Priority, die Ihr ML‑Modell vorhersagt, existiert  
✅ Wenn Sie „note“-Aktionen verwenden → Agent hat Berechtigung  
✅ Ticket‑Typen, die in der Automatisierung referenziert werden, existieren  

Wenn der Name falsch ist, schlägt das WebService‑Update fehl.

---

## 4. Erstellen Sie den WebService “OpenTicketAI”

Gehen Sie zu:

**Admin → Web Services**

![](/assets/webservice_overview.png)

### Schritt 1: Klicken Sie auf “Add Web Service”

![](/assets/otobo_webservice_import.png)

Dann wählen Sie **Import Web Service** aus.

### Schritt 2: Webservice importieren

Verwenden Sie die mit Open Ticket AI gelieferte Vorlage:

[Open Ticket Ai yaml](https://raw.githubusercontent.com/Softoft-Orga/open-ticket-ai/refs/heads/dev/deployment/znuny_demo/OpenTicketAI.yml)

Laden Sie die Datei über die Schaltfläche **Import web service** hoch.

Dies erstellt:

- `/ticket-get`
- `/ticket-update`
- `/ticket-search`
- `/ticket-create`

Alle eingeschränkt, sodass **nur der Benutzer `open_ticket_ai` sie verwenden kann**.

---

## 5. Warum der WebService eingeschränkt ist

Das YAML, das Sie importieren, enthält:

```yaml
ValueMap:
  UserLogin:
    ValueMapRegEx:
      .*: open_ticket_ai
```

Dies zwingt jede eingehende Anfrage, sich als `open_ticket_ai` zu authentifizieren – selbst wenn ein Angreifer beliebige Benutzernamen sendet.

Dies verhindert:

- Passwort‑Brute‑Force‑Angriffe
- API‑Missbrauch
- Unautorisierte Ticket‑Manipulation

Mit einem **16‑Zeichen‑Zufallspasswort** ist Brute‑Force selbst bei extremer Last unmöglich.

---

## 6. Verifizieren Sie, dass der WebService aktiv ist

Nach dem Import sollte Ihre Liste anzeigen:

![](/assets/webservice_overview.png)

Achten Sie auf:

✅ Name: **OpenTicketAI**  
✅ Provider Transport: **HTTP::REST**  
✅ Validity: **valid**  
✅ Restricted to user `open_ticket_ai`

Falls nicht gültig, bearbeiten → erneut speichern.