---
title: 'Wie man ein KI-Modell mit eigenen Ticket-Daten feinabstimmt: Vollständige Trainingsanleitung'
description: 'Lernen Sie, Transformer-Modelle auf benutzerdefinierten Ticket-Daten mit Hugging Face und Open Ticket AI feinabzustimmen. Schritt-für-Schritt-Anleitung für domänenspezifische Klassifizierung mit Python.'
lang: de
date: 2025-08-18
tags:
  - ai-fine-tuning
  - model-training
  - transformer-models
  - huggingface
  - bert-training
  - custom-ai-models
  - ticket-classification
category: Tutorial
draft: false
image: ../../../assets/images/ai-brain-connected-statistics-dark-blue.png
---

# Wie man ein KI-Modell mit eigenen Ticket-Daten feinabstimmt

Das Feinabstimmen eines KI-Modells auf Ihre eigenen Ticket-Daten ist eine leistungsstarke Methode, um die Ticket-Klassifizierung für Ihr Unternehmen anzupassen. Indem Sie ein Modell auf gelabelten Support-Tickets trainieren, bringen Sie ihm Ihre domänenspezifische Sprache und Kategorien bei. Dieser Prozess umfasst im Allgemeinen die Vorbereitung eines Datensatzes (oft eine CSV- oder JSON-Datei mit Tickets und Labels), die Auswahl oder Erstellung von Labels (wie Abteilungen oder Prioritätsstufen) und anschließend das Training eines Modells wie eines Transformer-basierten Klassifikators auf diesen Daten. Sie können Tools wie Hugging Faces Transformer-Bibliothek verwenden, um Modelle lokal zu trainieren, oder eine dedizierte Lösung wie **Open Ticket AI (ATC)** nutzen, die eine On-Premise-REST-API für die Ticket-Klassifizierung bereitstellt. In beiden Fällen profitieren Sie von Transfer Learning: Ein vortrainiertes Modell (z.B. BERT, DistilBERT oder RoBERTa) wird an Ihre Ticket-Kategorien angepasst, was die Genauigkeit gegenüber einem generischen Modell erheblich verbessert.

Moderne Textklassifizierungs-Workflows folgen diesen übergeordneten Schritten:

- **Daten sammeln und labeln:** Sammeln Sie historische Tickets und weisen Sie ihnen die richtigen Kategorien (Queues) oder Prioritäten zu. Jedes Ticket sollte ein Textfeld und mindestens ein Label haben.
- **Datensatz formatieren:** Speichern Sie diese gelabelten Daten in einem strukturierten Format (CSV oder JSON). Beispielsweise könnte eine CSV-Datei die Spalten `"text"`, `"label"` haben.
- **In Trainings-/Testdaten aufteilen:** Legen Sie einen Teil für Validierung/Test zurück, um die Leistung zu bewerten.
- **Modell feinabstimmen:** Verwenden Sie eine Bibliothek wie Hugging Face Transformers oder unsere Open Ticket AI API, um ein Klassifizierungsmodell auf den Daten zu trainieren.
- **Evaluieren und bereitstellen:** Überprüfen Sie die Genauigkeit (oder den F1-Score) auf den zurückgehaltenen Daten und verwenden Sie dann das trainierte Modell, um neue Tickets zu klassifizieren.

Technisch versierte Leser können diese Schritte im Detail verfolgen. Die folgenden Beispiele veranschaulichen, wie man Ticket-Daten vorbereitet und ein Modell mit **Hugging Face Transformers** feinabstimmt, sowie wie unsere Open Ticket AI-Lösung diesen Workflow über API-Aufrufe unterstützt. Dabei gehen wir von gängigen Ticket-Kategorien (z.B. "Billing", "Technical Support") und Prioritäts-Labels aus, aber Ihre Labels können alles sein, was für Ihr System relevant ist.

## Vorbereitung Ihrer Ticket-Daten

Sammeln Sie zunächst einen repräsentativen Satz vergangener Tickets und labeln Sie sie gemäß Ihrem Klassifizierungsschema. Labels könnten Abteilungen (wie **Technical Support**, **Customer Service**, **Billing** usw.) oder Prioritätsstufen (z.B. **Low**, **Medium**, **High**) sein. Beispielsweise enthält der Softoft-Ticket-Datensatz Kategorien wie _Technical Support_, _Billing and Payments_, _IT Support_ und _General Inquiry_. Ein Hugging Face-Beispielmodell verwendet Labels wie _Billing Question_, _Feature Request_, _General Inquiry_ und _Technical Issue_. Definieren Sie beliebige Kategorien, die für Ihren Workflow sinnvoll sind.

Organisieren Sie die Daten im CSV- oder JSON-Format. Jeder Datensatz sollte den Ticket-Text und sein Label enthalten. Beispielsweise könnte eine CSV-Datei so aussehen:

```
text,label
"My printer will not connect to WiFi",Hardware,  # Beispiel-Tickettext und seine Kategorie
"I need help accessing my account",Account
```

Wenn Sie Prioritäten oder mehrere Labels einbeziehen, könnten Sie weitere Spalten hinzufügen (z.B. `priority`). Die genaue Struktur ist flexibel, solange Sie jeden Ticket-Text klar seinen Label(s) zuordnen. Es ist üblich, eine Spalte für den Ticket-Inhalt (z.B. `"text"` oder `"ticket_text"`) und eine Spalte für das Label zu haben.

Möglicherweise müssen Sie den Text leicht bereinigen und vorverarbeiten (z.B. Signaturen, HTML-Tags entfernen oder Daten anonymisieren), aber in vielen Fällen funktioniert roher Ticket-Text gut als Eingabe für moderne NLP-Modelle. Teilen Sie schließlich die gelabelten Daten in einen Trainingssatz und einen Validierungs-/Testsatz auf (z.B. 80% Training / 20% Test). Diese Aufteilung ermöglicht es Ihnen, zu messen, wie gut das feinabgestimmte Modell generalisiert.

## Labeln von Tickets

Konsistente, genaue Labels sind entscheidend. Stellen Sie sicher, dass jedes Ticket korrekt einer Ihrer gewählten Kategorien zugewiesen ist. Dies kann manuell durch Support-Mitarbeiter oder unter Verwendung vorhandener Ticket-Metadaten erfolgen. Oft labeln Organisationen Tickets nach _Queue_ oder Abteilung und manchmal auch nach _Priorität_. Beispielsweise kategorisiert der Softoft-E-Mail-Ticket-Datensatz Tickets sowohl nach Abteilung (Queue) als auch nach Priorität. Priorität kann nützlich sein, wenn Sie ein Modell trainieren möchten, um Dringlichkeit vorherzusagen: z.B. `Low`, `Medium`, `Critical`. In vielen Setups könnten Sie ein Modell für die Abteilungsklassifizierung und ein weiteres für die Prioritätsklassifizierung trainieren.

Welches Schema Sie auch wählen, stellen Sie sicher, dass Sie einen endlichen Satz von Label-Werten haben. In einer CSV-Datei könnten Sie haben:

```
text,label,priority
"System crash when saving file","Technical Support","High"
"Request to change billing address","Billing","Low"
```

Dieses Beispiel hat zwei Label-Spalten: eine für die Kategorie und eine für die Priorität. Der Einfachheit halber gehen wir in den folgenden Beispielen von einer Single-Label-Klassifizierungsaufgabe aus (eine Label-Spalte).

**Wichtige Tipps für das Labeln:**

- Definieren Sie Ihre Label-Namen klar. Zum Beispiel _Technical Support_ vs _IT Support_ vs _Hardware Issue_ – vermeiden Sie mehrdeutige Überschneidungen.
- Wenn Tickets oft mehreren Kategorien angehören, sollten Sie Multi-Label-Klassifizierung (Zuweisung mehrerer Labels) in Betracht ziehen oder sie in separate Modelle aufteilen.
- Verwenden Sie konsistente Formatierung (gleiche Schreibweise, Groß-/Kleinschreibung) für Labels in Ihrem Datensatz.

Am Ende dieses Schritts sollten Sie eine gelabelte Datensatzdatei (CSV oder JSON) mit Ticket-Texten und ihren Labels haben, die für das Modell bereit ist.

## Feinabstimmung mit Hugging Face Transformers

Eine der flexibelsten Möglichkeiten, einen Textklassifikator feinabzustimmen, ist die Verwendung der [Hugging Face Transformers](https://huggingface.co/transformers/)-Bibliothek. Dies ermöglicht es Ihnen, mit einem vortrainierten Sprachmodell (wie BERT oder RoBERTa) zu beginnen und es weiter auf Ihrem spezifischen Ticket-Datensatz zu trainieren. Die Kernschritte sind: Text tokenisieren, einen `Trainer` einrichten und `train()` aufrufen.

1. **Datensatz laden:** Verwenden Sie `datasets` oder `pandas`, um Ihre CSV/JSON zu laden. Beispielsweise kann Hugging Faces `datasets`-Bibliothek eine CSV-Datei direkt lesen:

   ```python
   from datasets import load_dataset
   dataset = load_dataset("csv", data_files={
       "train": "tickets_train.csv",
       "validation": "tickets_val.csv"
   })
   # Angenommen, 'text' ist die Spalte mit dem Ticket-Inhalt und 'label' ist die Kategorie-Spalte.
   ```

2. **Text tokenisieren:** Vortrainierte Transformer benötigen tokenisierte Eingaben. Laden Sie einen Tokenizer (z.B. DistilBERT) und wenden Sie ihn auf Ihren Text an:

   ```python
   from transformers import AutoTokenizer
   tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

   def preprocess_function(examples):
       # Tokenisiere die Texte (dies erzeugt input_ids, attention_mask usw.)
       return tokenizer(examples["text"], truncation=True, padding="max_length")

   tokenized_datasets = dataset.map(preprocess_function, batched=True)
   ```

   Dies folgt dem Hugging Face-Beispiel: Zuerst wird der DistilBERT-Tokenizer geladen, dann wird `Dataset.map` verwendet, um alle Texte in Batches zu tokenisieren. Das Ergebnis (`tokenized_datasets`) enthält Input-IDs und Attention-Masks und ist bereit für das Modell.

3. **Modell laden:** Wählen Sie ein vortrainiertes Modell und geben Sie die Anzahl der Labels an. Um beispielsweise DistilBERT für die Klassifizierung feinabzustimmen:

   ```python
   from transformers import AutoModelForSequenceClassification
   num_labels = 4  # Setzen Sie dies auf die Anzahl Ihrer Kategorien
   model = AutoModelForSequenceClassification.from_pretrained(
       "distilbert-base-uncased", num_labels=num_labels
   )
   ```

   Dies entspricht Hugging Faces Sequenzklassifizierungsbeispiel, bei dem das Modell mit `num_labels` gleich den Klassen in Ihrem Datensatz geladen wird.

4. **Trainingsargumente und Trainer einrichten:** Definieren Sie Hyperparameter mit `TrainingArguments` und erstellen Sie dann einen `Trainer` mit Ihrem Modell und den tokenisierten Daten:

   ```python
   from transformers import TrainingArguments, Trainer
   training_args = TrainingArguments(
       output_dir="./ticket_model",
       num_train_epochs=3,
       per_device_train_batch_size=8,
       per_device_eval_batch_size=8,
       learning_rate=2e-5,
       evaluation_strategy="epoch"
   )
   trainer = Trainer(
       model=model,
       args=training_args,
       train_dataset=tokenized_datasets["train"],
       eval_dataset=tokenized_datasets["validation"],
       tokenizer=tokenizer
   )
   ```

   Dies spiegelt die Hugging Face-Anleitung wider: Nach dem Einrichten von `TrainingArguments` (für Ausgabeverzeichnis, Epochen, Batch-Größe usw.) instanziieren wir `Trainer` mit dem Modell, den Datensätzen, dem Tokenizer und den Trainingsargumenten.

5. **Modell trainieren:** Rufen Sie `trainer.train()` auf, um mit der Feinabstimmung zu beginnen. Dies wird für die angegebene Anzahl von Epochen laufen und periodisch auf dem Validierungssatz evaluieren, falls bereitgestellt.

   ```python
   trainer.train()
   ```

   Gemäß der Dokumentation beginnt mit diesem einzelnen Befehl die Feinabstimmung. Das Training kann je nach Datenmenge und Hardware (GPU wird für große Datensätze empfohlen) Minuten bis Stunden dauern.

6. **Evaluieren und speichern:** Nach dem Training evaluieren Sie das Modell auf Ihrem Testset, um die Genauigkeit oder andere Metriken zu überprüfen. Speichern Sie dann das feinabgestimmte Modell und den Tokenizer:

   ```python
   trainer.evaluate()
   model.save_pretrained("fine_tuned_ticket_model")
   tokenizer.save_pretrained("fine_tuned_ticket_model")
   ```

   Sie können dieses Modell später mit `AutoModelForSequenceClassification.from_pretrained("fine_tuned_ticket_model")` wieder laden.

Einmal trainiert, können Sie das Modell für Inferenz verwenden. Beispielsweise macht Hugging Faces Pipeline-API es einfach:

```python
from transformers import pipeline

classifier = pipeline("text-classification", model="fine_tuned_ticket_model")
results = classifier("Please reset my password and clear my cache.")
print(results)
```

Dies gibt das vorhergesagte Label und die Konfidenz für den neuen Ticket-Text aus. Wie von Hugging Face-Beispielen gezeigt, ermöglicht die Abstraktion `pipeline("text-classification")`, neue Ticket-Texte schnell mit dem feinabgestimmten Modell zu klassifizieren.

## Verwendung von Open Ticket AI (Softofts ATC) für Training und Inferenz

Unser **Open Ticket AI**-System (auch bekannt als ATC – AI Ticket Classification) bietet eine On-Premise, dockerisierte Lösung mit einer REST-API, die Ihre gelabelten Ticket-Daten aufnehmen und Modelle automatisch trainieren kann. Das bedeutet, Sie können alle Daten lokal behalten und dennoch leistungsstarkes ML nutzen. Die ATC-API hat Endpunkte zum Hochladen von Daten, Auslösen des Trainings und Klassifizieren von Tickets.

- **Trainingsdaten hochladen:** Senden Sie Ihre gelabelte Tickets-CSV an den Endpunkt `/api/v1/train-data`. Die API erwartet eine CSV-Nutzlast (`Content-Type: text/csv`), die Ihre Trainingsdaten enthält. Beispielsweise mit Python `requests`:

  ```python
  import requests
  url = "http://localhost:8080/api/v1/train-data"
  headers = {"Content-Type": "text/csv"}
  with open("tickets_labeled.csv", "rb") as f:
      res = requests.post(url, headers=headers, data=f)
  print(res.status_code, res.text)
  ```

  Dies entspricht der "Train Data" API in der ATC-Dokumentation. Eine erfolgreiche Antwort bedeutet, dass die Daten empfangen wurden.

- **Modelltraining starten:** Nach dem Hochladen der Daten lösen Sie das Training durch Aufruf von `/api/v1/train` aus (kein Body benötigt). In der Praxis:

  ```bash
  curl -X POST http://localhost:8080/api/v1/train
  ```

  Oder in Python:

  ```python
  train_res = requests.post("http://localhost:8080/api/v1/train")
  print(train_res.status_code, train_res.text)
  ```

  Dies stimmt mit dem Entwicklerdokumentationsbeispiel überein, das zeigt, dass ein einfacher POST das Training initiiert. Der Dienst trainiert das Modell auf den hochgeladenen Daten (er verwendet unter der Haube seine eigene Trainingspipeline, möglicherweise basierend auf ähnlichen Transformer-Modellen). Das Training läuft auf Ihrem Server, und das Modell wird nach Abschluss lokal gespeichert.

- **Neue Tickets klassifizieren:** Sobald das Training abgeschlossen ist, verwenden Sie den Endpunkt `/api/v1/classify`, um Vorhersagen für neue Ticket-Texte zu erhalten. Senden Sie eine JSON-Nutzlast mit dem Feld `"ticket_data"`, das den Ticket-Text enthält. Beispiel:

  ```python
  ticket_text = "My laptop overheats when I launch the app"
  res = requests.post(
      "http://localhost:8080/api/v1/classify",
      json={"ticket_data": ticket_text}
  )
  print(res.json())  # z.B. {"predicted_label": "Hardware Issue", "confidence": 0.95}
  ```

  Die ATC-Dokumentation zeigt ein ähnliches `curl`-Beispiel für die Klassifizierung. Die Antwort enthält typischerweise die vorhergesagte Kategorie (und möglicherweise die Konfidenz).

Die Verwendung der REST-API von Open Ticket AI integriert den Trainingsfluss in Ihre eigenen Systeme. Sie können Uploads und Trainingsläufe automatisieren (z.B. nächtliches Training oder Training auf neuen Daten) und dann den Klassifizierungsendpunkt in Ihrem Ticket-Workflow verwenden. Da alles On-Premise läuft, verlassen sensible Ticket-Inhalte niemals Ihre Server.

## Beispiel-Python-Code

Nachfolgend ein konsolidiertes Beispiel, das beide Workflows veranschaulicht:

```python
# Beispiel: Feinabstimmung mit Hugging Face
from transformers import AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
from datasets import load_dataset

# Lade und teile Ihren CSV-Datensatz
dataset = load_dataset("csv", data_files={"train": "train.csv", "validation": "val.csv"})
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")


# Tokenisiere
def preprocess(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length")


tokenized = dataset.map(preprocess, batched=True)

# Lade Modell
num_labels = 5  # z.B. Anzahl der Ticket-Kategorien
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=num_labels
    )

# Richte Trainer ein
training_args = TrainingArguments(
    output_dir="./model_out", num_train_epochs=3, per_device_train_batch_size=8
)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["validation"],
    tokenizer=tokenizer
)
trainer.train()
trainer.evaluate()
model.save_pretrained("fine_tuned_ticket_model")
tokenizer.save_pretrained("fine_tuned_ticket_model")

# Verwende das Modell zur Klassifizierung
from transformers import pipeline

classifier = pipeline("text-classification", model="fine_tuned_ticket_model")
print(classifier("Example: The app crashes when I try to open it"))

# Beispiel: Verwendung der Open Ticket AI API
import requests

# Lade Daten hoch (CSV)
with open("tickets_labeled.csv", "rb") as data_file:
    res = requests.post(
        "http://localhost:8080/api/v1/train-data",
        headers={"Content-Type": "text/csv"},
        data=data_file
        )
    print("Upload status:", res.status_code)
# Trigger Training
train_res = requests.post("http://localhost:8080/api/v1/train")
print("Training status:", train_res.status_code)
# Klassifiziere neues Ticket
res = requests.post(
    "http://localhost:8080/api/v1/classify",
    json={"ticket_data": "Cannot log into account"}
    )
print("Prediction:", res.json())
```

Dieses Skript demonstriert beide Methoden: die Hugging Face-Feinabstimmungs-Pipeline und die Open Ticket AI-REST-Aufrufe. Es lädt und tokenisiert einen CSV-Datensatz, stimmt einen DistilBERT-Klassifikator fein ab und verwendet ihn dann über eine Pipeline. Es zeigt auch, wie dieselben Daten an die ATC-API gepostet und Training/Klassifizierung ausgelöst werden.

## Fazit

Das Feinabstimmen eines KI-Modells auf Ihre eigenen Ticket-Daten ermöglicht eine hochgenaue, maßgeschneiderte Ticket-Klassifizierung. Indem Sie vergangene Tickets labeln und ein Modell wie einen Transformer trainieren, nutzen Sie Transfer Learning und Domänenwissen. Ob Sie Hugging Faces Python-APIs oder eine Komplettlösung wie Open Ticket AI (Softofts On-Prem-Klassifizierungsdienst) verwenden, der Workflow ist ähnlich: Bereiten Sie gelabelte Daten vor, trainieren Sie darauf und verwenden Sie dann das trainierte Modell für Vorhersagen.

Wir haben gezeigt, wie Sie Ihren CSV/JSON-Datensatz strukturieren, Hugging Faces `Trainer`-API zur Feinabstimmung verwenden und die Open Ticket AI-REST-API für On-Prem-Training und -Inferenz nutzen. Hugging Faces Dokumentation bietet detaillierte Anleitungen zur Verwendung von Tokenizern und dem `Trainer`, und Beispiel-Model-Cards veranschaulichen, wie Klassifizierungsmodelle auf Ticket-Routing angewendet werden. Mit diesen Tools können Sie schnell iterieren: Probieren Sie verschiedene vortrainierte Modelle aus (z.B. BERT, RoBERTa oder sogar domänenspezifische Modelle), experimentieren Sie mit Hyperparametern und messen Sie die Leistung auf Ihrem Testset.

Indem Sie diese Schritte befolgen, kann Ihr Support-System Tickets automatisch an das richtige Team weiterleiten, dringende Probleme kennzeichnen und Ihren Mitarbeitern unzählige Stunden manuellen Sortierens ersparen. Diese tiefe Integration von NLP in Ihren Ticket-Workflow ist mit modernen Bibliotheken und APIs nun zugänglich – Sie müssen nur Ihre Daten und Labels bereitstellen.
