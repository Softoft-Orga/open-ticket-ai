---
title: 'How to Fine-Tune an AI Model with Your Own Ticket Data: Complete Training Guide'
description: 'Lernen Sie, Transformer-Modelle mit eigenen Ticketdaten mithilfe von Hugging Face und Open Ticket AI zu fine-tunen. Schritt-für-Schritt-Anleitung für domänenspezifische Klassifikation mit Python.'
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

# Wie Sie ein KI-Modell mit Ihren eigenen Ticketdaten fine-tunen

Das Fine-Tuning eines KI-Modells mit Ihren eigenen Ticketdaten ist eine leistungsstarke Methode, um die Ticketklassifikation für Ihre Organisation anzupassen. Indem Sie ein Modell auf gelabelten Support-Tickets trainieren, bringen Sie ihm Ihre domänenspezifische Sprache und Kategorien bei. Dieser Prozess umfasst im Allgemeinen die Vorbereitung eines Datensatzes (oft eine CSV- oder JSON-Datei mit Tickets und Labels), die Auswahl oder Erstellung von Labels (wie Abteilungen oder Prioritätsstufen) und anschließend das Training eines Modells wie eines Transformer-basierten Klassifikators auf diesen Daten. Sie können Tools wie Hugging Faces Transformer-Bibliothek verwenden, um Modelle lokal zu trainieren, oder eine dedizierte Lösung wie **Open Ticket AI (ATC)** nutzen, die eine On-Premise-REST-API für die Ticketklassifikation bereitstellt. In beiden Fällen profitieren Sie von Transfer Learning: Ein vortrainiertes Modell (z. B. BERT, DistilBERT oder RoBERTa) wird an Ihre Ticketkategorien angepasst, was die Genauigkeit gegenüber einem generischen Modell erheblich verbessert.

Moderne Textklassifikations-Workflows folgen diesen groben Schritten:

- **Daten sammeln und labeln:** Sammeln Sie historische Tickets und weisen Sie ihnen die korrekten Kategorien (Queues) oder Prioritäten zu. Jedes Ticket sollte ein Textfeld und mindestens ein Label haben.
- **Datensatz formatieren:** Speichern Sie diese gelabelten Daten in einem strukturierten Format (CSV oder JSON). Eine CSV-Datei könnte beispielsweise die Spalten `"text"` und `"label"` haben.
- **In Trainings-/Testdaten aufteilen:** Reservieren Sie einen Teil für die Validierung/Testung, um die Leistung zu bewerten.
- **Modell fine-tunen:** Verwenden Sie eine Bibliothek wie Hugging Face Transformers oder unsere Open Ticket AI API, um ein Klassifikationsmodell auf den Daten zu trainieren.
- **Evaluieren und bereitstellen:** Überprüfen Sie die Genauigkeit (oder den F1-Score) anhand der zurückgehaltenen Daten und verwenden Sie dann das trainierte Modell, um neue Tickets zu klassifizieren.

Technisch versierte Leser können diese Schritte im Detail nachvollziehen. Die folgenden Beispiele veranschaulichen, wie Sie Ticketdaten vorbereiten und ein Modell mit **Hugging Face Transformers** fine-tunen, sowie wie unsere Open Ticket AI-Lösung diesen Workflow über API-Aufrufe unterstützt. Wir gehen dabei von gängigen Ticketkategorien (z. B. "Billing", "Technical Support") und Prioritätslabels aus, aber Ihre Labels können alles sein, was für Ihr System relevant ist.

## Vorbereitung Ihrer Ticketdaten

Sammeln Sie zunächst einen repräsentativen Satz vergangener Tickets und labeln Sie sie gemäß Ihrem Klassifikationsschema. Labels könnten Abteilungen (wie **Technical Support**, **Customer Service**, **Billing** usw.) oder Prioritätsstufen (z. B. **Low**, **Medium**, **High**) sein. Der Softoft-Ticketdatensatz enthält beispielsweise Kategorien wie _Technical Support_, _Billing and Payments_, _IT Support_ und _General Inquiry_. Ein Hugging Face-Beispielmodell verwendet Labels wie _Billing Question_, _Feature Request_, _General Inquiry_ und _Technical Issue_. Definieren Sie die Kategorien, die für Ihren Workflow sinnvoll sind.

Organisieren Sie die Daten im CSV- oder JSON-Format. Jeder Datensatz sollte den Tickettext und sein Label enthalten. Eine CSV-Datei könnte beispielsweise so aussehen:

```
text,label
"My printer will not connect to WiFi",Hardware,  # Beispiel-Tickettext und seine Kategorie
"I need help accessing my account",Account
```

Wenn Sie Prioritäten oder mehrere Labels einbeziehen, könnten Sie weitere Spalten hinzufügen (z. B. `priority`). Die genaue Struktur ist flexibel, solange Sie jeden Tickettext klar seinen Label(s) zuordnen. Üblich ist eine Spalte für den Ticketinhalt (z. B. `"text"` oder `"ticket_text"`) und eine Spalte für das Label.

Möglicherweise müssen Sie den Text leicht bereinigen und vorverarbeiten (z. B. Signaturen, HTML-Tags entfernen oder Daten anonymisieren), aber in vielen Fällen funktioniert roher Tickettext gut als Eingabe für moderne NLP-Modelle. Teilen Sie schließlich die gelabelten Daten in einen Trainingssatz und einen Validierungs-/Testsatz auf (z. B. 80 % Training / 20 % Test). Diese Aufteilung ermöglicht es Ihnen zu messen, wie gut das fine-getunte Modell generalisiert.

## Labeln von Tickets

Konsistente, genaue Labels sind entscheidend. Stellen Sie sicher, dass jedes Ticket korrekt einer Ihrer gewählten Kategorien zugewiesen ist. Dies kann manuell durch Support-Mitarbeiter oder mithilfe vorhandener Ticket-Metadaten erfolgen. Oft werden Tickets von Organisationen nach _Queue_ oder Abteilung gelabelt und manchmal auch nach _Priorität_. Der Softoft-E-Mail-Ticketdatensatz kategorisiert Tickets beispielsweise sowohl nach Abteilung (Queue) als auch nach Priorität. Die Priorität kann nützlich sein, wenn Sie ein Modell trainieren möchten, um Dringlichkeit vorherzusagen: z. B. `Low`, `Medium`, `Critical`. In vielen Setups könnten Sie ein Modell für die Abteilungsklassifikation und ein weiteres für die Prioritätsklassifikation trainieren.

Welches Schema Sie auch wählen, stellen Sie sicher, dass Sie einen endlichen Satz von Labelwerten haben. In einer CSV-Datei könnten Sie haben:

```
text,label,priority
"System crash when saving file","Technical Support","High"
"Request to change billing address","Billing","Low"
```

Dieses Beispiel hat zwei Label-Spalten: eine für die Kategorie und eine für die Priorität. Der Einfachheit halber gehen wir in den folgenden Beispielen von einer Single-Label-Klassifikationsaufgabe aus (eine Label-Spalte).

**Wichtige Tipps für das Labeln:**

- Definieren Sie Ihre Labelnamen klar. Zum Beispiel _Technical Support_ vs. _IT Support_ vs. _Hardware Issue_ – vermeiden Sie mehrdeutige Überschneidungen.
- Wenn Tickets oft mehreren Kategorien angehören, sollten Sie eine Multi-Label-Klassifikation (Zuweisung mehrerer Labels) in Betracht ziehen oder sie in separate Modelle aufteilen.
- Verwenden Sie konsistente Formatierung (gleiche Schreibweise, Groß-/Kleinschreibung) für Labels in Ihrem Datensatz.

Am Ende dieses Schritts sollten Sie eine gelabelte Datensatzdatei (CSV oder JSON) mit Tickettexten und ihren Labels haben, die bereit für das Modell ist.

## Fine-Tuning mit Hugging Face Transformers

Eine der flexibelsten Möglichkeiten, einen Textklassifikator zu fine-tunen, ist die Verwendung der [Hugging Face Transformers](https://huggingface.co/transformers/)-Bibliothek. Dies ermöglicht es Ihnen, mit einem vortrainierten Sprachmodell (wie BERT oder RoBERTa) zu beginnen und es weiter auf Ihrem spezifischen Ticketdatensatz zu trainieren. Die Kernschritte sind: Text tokenisieren, einen `Trainer` einrichten und `train()` aufrufen.

1. **Datensatz laden:** Verwenden Sie `datasets` oder `pandas`, um Ihre CSV/JSON zu laden. Die `datasets`-Bibliothek von Hugging Face kann beispielsweise eine CSV-Datei direkt lesen:

   ```python
   from datasets import load_dataset
   dataset = load_dataset("csv", data_files={
       "train": "tickets_train.csv",
       "validation": "tickets_val.csv"
   })
   # Angenommen, 'text' ist die Spalte mit dem Ticketinhalt und 'label' ist die Kategorie-Spalte.
   ```

2. **Text tokenisieren:** Vortrainierte Transformer benötigen tokenisierte Eingaben. Laden Sie einen Tokenizer (z. B. DistilBERT) und wenden Sie ihn auf Ihren Text an:

   ```python
   from transformers import AutoTokenizer
   tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

   def preprocess_function(examples):
       # Tokenisiere die Texte (dies erzeugt input_ids, attention_mask, etc.)
       return tokenizer(examples["text"], truncation=True, padding="max_length")

   tokenized_datasets = dataset.map(preprocess_function, batched=True)
   ```

   Dies folgt dem Hugging Face-Beispiel: Laden Sie zuerst den DistilBERT-Tokenizer und verwenden Sie dann `Dataset.map`, um alle Texte in Batches zu tokenisieren. Das Ergebnis (`tokenized_datasets`) enthält Input-IDs und Attention-Masks und ist bereit für das Modell.

3. **Modell laden:** Wählen Sie ein vortrainiertes Modell und geben Sie die Anzahl der Labels an. Um beispielsweise DistilBERT für die Klassifikation zu fine-tunen:

   ```python
   from transformers import AutoModelForSequenceClassification
   num_labels = 4  # Setzen Sie dies auf die Anzahl Ihrer Kategorien
   model = AutoModelForSequenceClassification.from_pretrained(
       "distilbert-base-uncased", num_labels=num_labels
   )
   ```

   Dies entspricht dem Hugging Face-Beispiel für Sequenzklassifikation, bei dem das Modell mit `num_labels` entsprechend den Klassen in Ihrem Datensatz geladen wird.

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

   Dies spiegelt die Hugging Face-Anleitung wider: Nachdem `TrainingArguments` (für Ausgabeverzeichnis, Epochen, Batch-Größe usw.) eingerichtet wurden, instanziieren wir `Trainer` mit dem Modell, den Datensätzen, dem Tokenizer und den Trainingsargumenten.

5. **Modell trainieren:** Rufen Sie `trainer.train()` auf, um mit dem Fine-Tuning zu beginnen. Dies läuft für die angegebene Anzahl von Epochen und evaluiert periodisch auf dem Validierungssatz, falls vorhanden.

   ```python
   trainer.train()
   ```

   Gemäß der Dokumentation beginnt mit diesem einzelnen Befehl das Fine-Tuning. Das Training kann je nach Datenmenge und Hardware (GPU wird für große Datensätze empfohlen) Minuten bis Stunden dauern.

6. **Evaluieren und speichern:** Evaluieren Sie nach dem Training das Modell auf Ihrem Testset, um die Genauigkeit oder andere Metriken zu überprüfen. Speichern Sie dann das fine-getunte Modell und den Tokenizer:

   ```python
   trainer.evaluate()
   model.save_pretrained("fine_tuned_ticket_model")
   tokenizer.save_pretrained("fine_tuned_ticket_model")
   ```

   Sie können dieses Modell später mit `AutoModelForSequenceClassification.from_pretrained("fine_tuned_ticket_model")` wieder laden.

Nach dem Training können Sie das Modell für Inferenz verwenden. Die Pipeline-API von Hugging Face macht dies beispielsweise einfach:

```python
from transformers import pipeline

classifier = pipeline("text-classification", model="fine_tuned_ticket_model")
results = classifier("Please reset my password and clear my cache.")
print(results)
```

Dies gibt das vorhergesagte Label und die Konfidenz für den neuen Tickettext aus. Wie von Hugging Face-Beispielen gezeigt, ermöglicht die Abstraktion `pipeline("text-classification")`, neue Tickettexte schnell mit dem fine-getunten Modell zu klassifizieren.

## Verwendung von Open Ticket AI (Softofts ATC) für Training und Inferenz

Unser **Open Ticket AI**-System (auch bekannt als ATC – AI Ticket Classification) bietet eine On-Premise-, Dockerisierte Lösung mit einer REST-API, die Ihre gelabelten Ticketdaten aufnehmen und Modelle automatisch trainieren kann. Das bedeutet, Sie können alle Daten lokal halten und dennoch leistungsstarkes ML nutzen. Die ATC-API verfügt über Endpunkte zum Hochladen von Daten, Auslösen des Trainings und Klassifizieren von Tickets.

- **Trainingsdaten hochladen:** Senden Sie Ihre gelabelte Ticket-CSV an den Endpunkt `/api/v1/train-data`. Die API erwartet eine CSV-Payload (`Content-Type: text/csv`), die Ihre Trainingsdaten enthält. Beispiel mit Python `requests`:

  ```python
  import requests
  url = "http://localhost:8080/api/v1/train-data"
  headers = {"Content-Type": "text/csv"}
  with open("tickets_labeled.csv", "rb") as f:
      res = requests.post(url, headers=headers, data=f)
  print(res.status_code, res.text)
  ```

  Dies entspricht der "Train Data"-API in der ATC-Dokumentation. Eine erfolgreiche Antwort bedeutet, dass die Daten empfangen wurden.

- **Modelltraining starten:** Nach dem Hochladen der Daten lösen Sie das Training durch Aufruf von `/api/v1/train` aus (kein Body benötigt). In der Praxis:

  ```bash
  curl -X POST http://localhost:8080/api/v1/train
  ```

  Oder in Python:

  ```python
  train_res = requests.post("http://localhost:8080/api/v1/train")
  print(train_res.status_code, train_res.text)
  ```

  Dies entspricht dem Beispiel aus der Entwicklerdokumentation, das zeigt, dass ein einfacher POST das Training initiiert. Der Service trainiert das Modell auf den hochgeladenen Daten (er verwendet unter der Haube seine eigene Trainingspipeline, möglicherweise basierend auf ähnlichen Transformer-Modellen). Das Training läuft auf Ihrem Server, und das Modell wird nach Abschluss lokal gespeichert.

- **Neue Tickets klassifizieren:** Sobald das Training abgeschlossen ist, verwenden Sie den Endpunkt `/api/v1/classify`, um Vorhersagen für neue Tickettexte zu erhalten. Senden Sie eine JSON-Payload mit dem Feld `"ticket_data"`, das den Tickettext enthält. Beispiel:

  ```python
  ticket_text = "My laptop overheats when I launch the app"
  res = requests.post(
      "http://localhost:8080/api/v1/classify",
      json={"ticket_data": ticket_text}
  )
  print(res.json())  # z. B. {"predicted_label": "Hardware Issue", "confidence": 0.95}
  ```

  Die ATC-Dokumentation zeigt ein ähnliches `curl`-Beispiel für die Klassifikation. Die Antwort enthält typischerweise die vorhergesagte Kategorie (und möglicherweise die Konfidenz).

Die Verwendung der REST-API von Open Ticket AI integriert den Trainingsfluss in Ihre eigenen Systeme. Sie können Uploads und Trainingsläufe automatisieren (z. B. nächtliches Training oder Training auf neuen Daten) und dann den Klassifikationsendpunkt in Ihrem Ticket-Workflow verwenden. Da alles On-Premise läuft, verlassen sensible Ticketinhalte niemals Ihre Server.

## Beispiel-Python-Code

Nachfolgend ein konsolidiertes Beispiel, das beide Workflows veranschaulicht:

```python
# Beispiel: Fine-Tuning mit Hugging Face
from transformers import AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
from datasets import load_dataset

# Laden und Aufteilen Ihres CSV-Datensatzes
dataset = load_dataset("csv", data_files={"train": "train.csv", "validation": "val.csv"})
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")


# Tokenisieren
def preprocess(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length")


tokenized = dataset.map(preprocess, batched=True)

# Modell laden
num_labels = 5  # z. B. Anzahl der Ticketkategorien
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=num_labels
    )

# Trainer einrichten
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

# Modell für Klassifikation verwenden
from transformers import pipeline

classifier = pipeline("text-classification", model="fine_tuned_ticket_model")
print(classifier("Example: The app crashes when I try to open it"))

# Beispiel: Verwendung der Open Ticket AI API
import requests

# Daten hochladen (CSV)
with open("tickets_labeled.csv", "rb") as data_file:
    res = requests.post(
        "http://localhost:8080/api/v1/train-data",
        headers={"Content-Type": "text/csv"},
        data=data_file
        )
    print("Upload status:", res.status_code)
# Training auslösen
train_res = requests.post("http://localhost:8080/api/v1/train")
print("Training status:", train_res.status_code)
# Neues Ticket klassifizieren
res = requests.post(
    "http://localhost:8080/api/v1/classify",
    json={"ticket_data": "Cannot log into account"}
    )
print("Prediction:", res.json())
```

Dieses Skript demonstriert beide Methoden: die Hugging Face Fine-Tuning-Pipeline und die Open Ticket AI REST-Aufrufe. Es lädt und tokenisiert einen CSV-Datensatz, fine-tunt einen DistilBERT-Klassifikator und verwendet ihn dann über eine Pipeline. Es zeigt auch, wie dieselben Daten an die ATC-API gepostet und Training/Klassifikation ausgelöst werden.

## Fazit

Das Fine-Tuning eines KI-Modells mit Ihren eigenen Ticketdaten ermöglicht eine hochgenaue, maßgeschneiderte Ticketklassifikation. Indem Sie vergangene Tickets labeln und ein Modell wie einen Transformer trainieren, nutzen Sie Transfer Learning und Domänenwissen. Ob Sie Hugging Faces Python-APIs oder eine Komplettlösung wie Open Ticket AI (Softofts On-Premise-Klassifikationsservice) verwenden, der Workflow ist ähnlich: Gelabelte Daten vorbereiten, darauf trainieren und dann das trainierte Modell für Vorhersagen verwenden.

Wir haben gezeigt, wie Sie Ihren CSV/JSON-Datensatz strukturieren, Hugging Faces `Trainer`-API für das Fine-Tuning verwenden und die Open Ticket AI REST-API für On-Premise-Training und Inferenz nutzen. Die Dokumentation von Hugging Face bietet detaillierte Anleitungen zur Verwendung von Tokenizern und dem `Trainer`, und Beispiel-Model-Cards veranschaulichen, wie Klassifikationsmodelle für Ticket-Routing angewendet werden. Mit diesen Tools können Sie schnell iterieren: Probieren Sie verschiedene vortrainierte Modelle aus (z. B. BERT, RoBERTa oder sogar domänenspezifische Modelle), experimentieren Sie mit Hyperparametern und messen Sie die Leistung auf Ihrem Testset.

Indem Sie diese Schritte befolgen, kann Ihr Support-System Tickets automatisch an das richtige Team weiterleiten, dringende Probleme kennzeichnen und Ihrem Personal unzählige Stunden manueller Sortierung ersparen. Diese tiefe Integration von NLP in Ihren Ticket-Workflow ist nun mit modernen Bibliotheken und APIs zugänglich – Sie müssen lediglich Ihre Daten und Labels bereitstellen.