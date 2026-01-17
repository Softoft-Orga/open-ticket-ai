---
title: 'Wie Sie ein KI-Modell mit Ihren eigenen Ticketdaten feinabstimmen: Vollständiger Trainingsleitfaden'
description: 'Erfahren Sie, wie Sie Transformer-Modelle mit benutzerdefinierten Ticketdaten mithilfe von Hugging Face und Open Ticket AI feinabstimmen. Schritt-für-Schritt-Anleitung für domänenspezifische Klassifizierung mit Python.'
lang: en
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

# Wie Sie ein KI-Modell mit Ihren eigenen Ticketdaten feinabstimmen

Die Feinabstimmung eines KI-Modells mit Ihren eigenen Ticketdaten ist ein leistungsstarker Weg, die Ticketklassifizierung für Ihr Unternehmen anzupassen. Durch das Training eines Modells mit gekennzeichneten Support‑Tickets vermitteln Sie ihm Ihre domänenspezifische Sprache und Kategorien. Dieser Prozess umfasst in der Regel das Vorbereiten eines Datensatzes (oft eine CSV‑ oder JSON‑Datei mit Tickets und Labels), das Auswählen oder Erstellen von Labels (wie Abteilungen oder Prioritätsstufen) und anschließend das Trainieren eines Modells wie eines Transformer‑basierten Klassifikators mit diesen Daten. Sie können Werkzeuge wie die Hugging Face‑Transformer‑Bibliothek nutzen, um Modelle lokal zu trainieren, oder eine dedizierte Lösung wie **Open Ticket AI (ATC)**, die eine On‑Premise‑REST‑API für die Ticketklassifizierung bereitstellt. In beiden Fällen profitieren Sie vom Transfer‑Learning: ein vortrainiertes Modell (z. B. BERT, DistilBERT oder RoBERTa) wird an Ihre Ticketkategorien angepasst, was die Genauigkeit gegenüber einem generischen Modell erheblich steigert.

Moderne Textklassifizierungs‑Workflows folgen diesen übergeordneten Schritten:

- **Collect and Label Data:** Sammeln Sie historische Tickets und ordnen Sie ihnen die richtigen Kategorien (Queues) oder Prioritäten zu. Jeder Ticket sollte ein Textfeld und mindestens ein Label haben.
- **Format the Dataset:** Speichern Sie diese gekennzeichneten Daten in einem strukturierten Format (CSV oder JSON). Zum Beispiel könnte eine CSV die Spalten `"text","label"` enthalten.
- **Split into Train/Test:** Reservieren Sie einen Teil für Validierung/Test, um die Leistung zu bewerten.
- **Fine-Tune the Model:** Verwenden Sie eine Bibliothek wie Hugging Face Transformers oder unsere Open Ticket AI API, um ein Klassifizierungsmodell mit den Daten zu trainieren.
- **Evaluate and Deploy:** Prüfen Sie die Genauigkeit (oder F1) auf zurückgehaltenen Daten und verwenden Sie anschließend das trainierte Modell, um neue Tickets zu klassifizieren.

Technikaffine Leser können diesen Schritten im Detail folgen. Die nachstehenden Beispiele zeigen, wie Ticketdaten vorbereitet und ein Modell mit **Hugging Face Transformers** feinabgestimmt wird, sowie wie unsere Open Ticket AI‑Lösung diesen Workflow über API‑Aufrufe unterstützt. Durchgehend gehen wir von gängigen Ticketkategorien (z. B. „Billing“, „Technical Support“) und Prioritäts‑Labels aus, aber Ihre Labels können alles sein, was für Ihr System relevant ist.

## Vorbereitung Ihrer Ticketdaten

Zunächst sammeln Sie einen repräsentativen Satz vergangener Tickets und kennzeichnen sie gemäß Ihrem Klassifizierungsschema. Labels können Abteilungen (wie **Technical Support**, **Customer Service**, **Billing** usw.) oder Prioritätsstufen (z. B. **Low**, **Medium**, **High**) sein. Zum Beispiel enthält der Softoft‑Ticket‑Datensatz Kategorien wie _Technical Support_, _Billing and Payments_, _IT Support_ und _General Inquiry_. Ein Beispielmodell von Hugging Face verwendet Labels wie _Billing Question_, _Feature Request_, _General Inquiry_ und _Technical Issue_. Definieren Sie die Kategorien, die für Ihren Workflow sinnvoll sind.

Organisieren Sie die Daten im CSV‑ oder JSON‑Format. Jeder Datensatz sollte den Tickettext und sein Label enthalten. Zum Beispiel könnte eine CSV wie folgt aussehen:

```
text,label
"My printer will not connect to WiFi",Hardware,  # Example ticket text and its category
"I need help accessing my account",Account
```

Wenn Sie Prioritäten oder mehrere Labels einbeziehen, können Sie weitere Spalten hinzufügen (z. B. `priority`). Die genaue Struktur ist flexibel, solange Sie jeden Tickettext eindeutig seinem/ihren Label(s) zuordnen. Es ist üblich, eine Spalte für den Ticketinhalt (z. B. `"text"` oder `"ticket_text"`) und eine Spalte für das Label zu haben.

Möglicherweise müssen Sie den Text leicht bereinigen und vorverarbeiten (z. B. Signaturen, HTML‑Tags entfernen oder Daten anonymisieren), aber in vielen Fällen funktioniert roher Tickettext gut als Eingabe für moderne NLP‑Modelle. Abschließend teilen Sie die gekennzeichneten Daten in einen Trainings‑ und einen Validierungs‑/Test‑Satz auf (z. B. 80 % train / 20 % test). Diese Aufteilung ermöglicht es Ihnen, zu messen, wie gut das feinabgestimmte Modell generalisiert.

## Kennzeichnung von Tickets

Konsistente, genaue Labels sind entscheidend. Stellen Sie sicher, dass jedes Ticket korrekt einer Ihrer gewählten Kategorien zugewiesen wird. Dies kann manuell durch Support‑Mitarbeiter erfolgen oder mithilfe vorhandener Ticket‑Metadaten, falls verfügbar. Oft kennzeichnen Organisationen Tickets nach _queue_ oder Abteilung und manchmal auch nach _priority_. Zum Beispiel kategorisiert der Softoft‑E‑Mail‑Ticket‑Datensatz Tickets sowohl nach Abteilung (queue) als auch nach Priorität. Priorität kann nützlich sein, wenn Sie ein Modell trainieren möchten, das Dringlichkeit vorhersagt: z. B. `Low`, `Medium`, `Critical`. In vielen Setups könnten Sie ein Modell für die Abteilungsklassifizierung und ein weiteres für die Prioritätsklassifizierung trainieren.

Unabhängig von Ihrem Schema stellen Sie sicher, dass Sie eine endliche Menge von Label‑Werten haben. In einer CSV könnte das so aussehen:

```
text,label,priority
"System crash when saving file","Technical Support","High"
"Request to change billing address","Billing","Low"
```

Dieses Beispiel hat zwei Label‑Spalten: eine für die Kategorie und eine für die Priorität. Der Einfachheit halber gehen wir in den folgenden Beispielen von einer Single‑Label‑Klassifizierungsaufgabe aus (eine Label‑Spalte).

**Wichtige Tipps zur Kennzeichnung:**
- Definieren Sie Ihre Label‑Namen eindeutig. Zum Beispiel _Technical Support_ vs _IT Support_ vs _Hardware Issue_ – vermeiden Sie mehrdeutige Überschneidungen.
- Wenn Tickets häufig zu mehreren Kategorien gehören, könnten Sie eine Multi‑Label‑Klassifizierung (mehrere Labels zuweisen) in Betracht ziehen oder sie in separate Modelle aufteilen.
- Verwenden Sie eine konsistente Formatierung (gleiche Schreibweise, Groß‑/Kleinschreibung) für die Labels in Ihrem Datensatz.

Am Ende dieses Schrittes sollten Sie eine gekennzeichnete Datensatzdatei (CSV oder JSON) mit Tickettexten und deren Labels besitzen, die bereit für das Modell ist.

## Feinabstimmung mit Hugging Face Transformers

Eine der flexibelsten Methoden, einen Textklassifikator fein abzustimmen, ist die Verwendung der [Hugging Face Transformers](https://huggingface.co/transformers/)-Bibliothek. Damit können Sie von einem vortrainierten Sprachmodell (wie BERT oder RoBERTa) ausgehen und es weiter auf Ihrem spezifischen Ticket‑Datensatz trainieren. Die Kernschritte sind: Tokenisieren des Textes, Einrichten eines `Trainer` und Aufruf von `train()`.

1. **Load the Dataset:** Verwenden Sie `datasets` oder `pandas`, um Ihre CSV/JSON zu laden. Zum Beispiel kann die Hugging Face‑`datasets`‑Bibliothek eine CSV direkt einlesen:

   ```python
   from datasets import load_dataset
   dataset = load_dataset("csv", data_files={
       "train": "tickets_train.csv",
       "validation": "tickets_val.csv"
   })
   # Assuming 'text' is the column with ticket content, and 'label' is the category column.
   ```

2. **Tokenize the Text:** Vortrainierte Transformer benötigen tokenisierten Input. Laden Sie einen Tokenizer (z. B. DistilBERT) und wenden Sie ihn auf Ihren Text an:

   ```python
   from transformers import AutoTokenizer
   tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

   def preprocess_function(examples):
       # Tokenize the texts (this will produce input_ids, attention_mask, etc.)
       return tokenizer(examples["text"], truncation=True, padding="max_length")

   tokenized_datasets = dataset.map(preprocess_function, batched=True)
   ```

   This follows the Hugging Face example: first load the DistilBERT tokenizer, then use`Dataset.map` to tokenize all texts in batches. The result (`tokenized_datasets`) contains input IDs and attention masks, ready for the model.

3. **Load the Model:** Wählen Sie ein vortrainiertes Modell und geben Sie die Anzahl der Labels an. Zum Beispiel, um DistilBERT für die Klassifizierung fein abzustimmen:

   ```python
   from transformers import AutoModelForSequenceClassification
   num_labels = 4  # set this to the number of your categories
   model = AutoModelForSequenceClassification.from_pretrained(
       "distilbert-base-uncased", num_labels=num_labels
   )
   ```

   This matches Hugging Face’s sequence classification example, where the model is loaded with `num_labels` equal to the classes in your dataset.

4. **Set Training Arguments and Trainer:** Definieren Sie Hyperparameter mit `TrainingArguments` und erstellen Sie anschließend einen `Trainer` mit Ihrem Modell und den tokenisierten Daten:

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

   This reflects the Hugging Face guide: after setting up `TrainingArguments` (for output directory, epochs, batch size, etc.), we instantiate `Trainer` with the model, datasets, tokenizer, and training arguments.

5. **Train the Model:** Rufen Sie `trainer.train()` auf, um die Feinabstimmung zu starten. Dies läuft über die angegebene Anzahl von Epochen und evaluiert bei Vorhandensein periodisch den Validierungs‑Datensatz.

   ```python
   trainer.train()
   ```

   As per the docs, this single command begins fine-tuning. Training may take minutes to hours depending on data size and hardware (GPU recommended for large datasets).

6. **Evaluate and Save:** Nach dem Training evaluieren Sie das Modell auf Ihrem Test‑Set, um Genauigkeit oder andere Metriken zu prüfen. Anschließend speichern Sie das feinabgestimmte Modell und den Tokenizer:

   ```python
   trainer.evaluate()
   model.save_pretrained("fine_tuned_ticket_model")
   tokenizer.save_pretrained("fine_tuned_ticket_model")
   ```

   You can later reload this model with
   `AutoModelForSequenceClassification.from_pretrained("fine_tuned_ticket_model")`.

Nach dem Training können Sie das Modell für Inferenz verwenden. Zum Beispiel macht die pipeline‑API von Hugging Face das einfach:

```python
from transformers import pipeline

classifier = pipeline("text-classification", model="fine_tuned_ticket_model")
results = classifier("Please reset my password and clear my cache.")
print(results)
```

This will output the predicted label and confidence for the new ticket text. As demonstrated by Hugging Face examples, the `pipeline("text-classification")` abstraction lets you quickly classify new ticket texts with the fine-tuned model.

## Verwendung von Open Ticket AI (Softoft’s ATC) für Training und Inferenz

Unser **Open Ticket AI**‑System (auch bekannt als ATC – AI Ticket Classification) bietet eine On‑Premise‑Docker‑Lösung mit einer REST‑API, die Ihre gekennzeichneten Ticketdaten aufnehmen und Modelle automatisch trainieren kann. Das bedeutet, Sie können alle Daten lokal behalten und dennoch leistungsstarke ML nutzen. Die ATC‑API verfügt über Endpunkte zum Hochladen von Daten, zum Auslösen des Trainings und zur Klassifizierung von Tickets.

- **Upload Training Data:** Senden Sie Ihre gekennzeichnete Tickets‑CSV an den Endpunkt `/api/v1/train-data`. Die API erwartet eine CSV‑Payload (`Content-Type: text/csv`) mit Ihren Trainingsdaten. Zum Beispiel mit Python `requests`:

  ```python
  import requests
  url = "http://localhost:8080/api/v1/train-data"
  headers = {"Content-Type": "text/csv"}
  with open("tickets_labeled.csv", "rb") as f:
      res = requests.post(url, headers=headers, data=f)
  print(res.status_code, res.text)
  ```

  This corresponds to the “Train Data” API in the ATC docs. A successful response means the data is received.

- **Start Model Training:** Nach dem Hochladen der Daten starten Sie das Training, indem Sie `/api/v1/train` aufrufen (kein Body erforderlich). In der Praxis:

  ```bash
  curl -X POST http://localhost:8080/api/v1/train
  ```

  Or in Python:

  ```python
  train_res = requests.post("http://localhost:8080/api/v1/train")
  print(train_res.status_code, train_res.text)
  ```

  This matches the developer documentation example, which shows that a simple POST initiates training. The service will train the model on the uploaded data (it uses its own training pipeline under the hood, possibly based on similar Transformer models). Training runs on your server, and the model is saved locally when done.

- **Classify New Tickets:** Sobald das Training abgeschlossen ist, verwenden Sie den Endpunkt `/api/v1/classify`, um Vorhersagen für neue Tickettexte zu erhalten. Senden Sie eine JSON‑Payload mit dem Feld `"ticket_data"` , das den Tickettext enthält. Zum Beispiel:

  ```python
  ticket_text = "My laptop overheats when I launch the app"
  res = requests.post(
      "http://localhost:8080/api/v1/classify",
      json={"ticket_data": ticket_text}
  )
  print(res.json())  # e.g. {"predicted_label": "Hardware Issue", "confidence": 0.95}
  ```

  The ATC docs show a similar `curl` example for classification. The response will typically include the predicted category (and possibly confidence).

Die Verwendung der REST‑API von Open Ticket AI integriert den Trainingsablauf in Ihre eigenen Systeme. Sie können Uploads und Trainingsläufe automatisieren (z. B. nächtliches Training oder Training mit neuen Daten) und anschließend den Klassifizierungs‑Endpunkt in Ihrem Ticket‑Workflow nutzen. Da alles On‑Premise läuft, verlässt sensibler Ticketinhalt niemals Ihre Server.

## Beispiel-Python-Code

Im Folgenden ein zusammengefasstes Beispiel, das beide Workflows illustriert:

```python
# Example: Fine-tuning with Hugging Face
from transformers import AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
from datasets import load_dataset

# Load and split your CSV dataset
dataset = load_dataset("csv", data_files={"train": "train.csv", "validation": "val.csv"})
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")


# Tokenize
def preprocess(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length")


tokenized = dataset.map(preprocess, batched=True)

# Load model
num_labels = 5  # e.g., number of ticket categories
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=num_labels
    )

# Set up Trainer
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

# Use the model for classification
from transformers import pipeline

classifier = pipeline("text-classification", model="fine_tuned_ticket_model")
print(classifier("Example: The app crashes when I try to open it"))

# Example: Using Open Ticket AI API
import requests

# Upload data (CSV)
with open("tickets_labeled.csv", "rb") as data_file:
    res = requests.post(
        "http://localhost:8080/api/v1/train-data",
        headers={"Content-Type": "text/csv"},
        data=data_file
        )
    print("Upload status:", res.status_code)
# Trigger training
train_res = requests.post("http://localhost:8080/api/v1/train")
print("Training status:", train_res.status_code)
# Classify new ticket
res = requests.post(
    "http://localhost:8080/api/v1/classify",
    json={"ticket_data": "Cannot log into account"}
    )
print("Prediction:", res.json())
```

Dieses Skript demonstriert beide Methoden: die Hugging Face‑Feinabstimmungspipeline und die Open Ticket AI‑REST‑Aufrufe. Es lädt und tokenisiert einen CSV‑Datensatz, feinabgestimmte einen DistilBERT‑Klassifikator und verwendet ihn anschließend über eine pipeline. Es zeigt außerdem, wie dieselben Daten per POST an die ATC‑API gesendet, das Training ausgelöst und die Klassifizierung durchgeführt wird.

## Fazit

Die Feinabstimmung eines KI‑Modells mit Ihren eigenen Ticketdaten ermöglicht hochgenaue, maßgeschneiderte Ticketklassifizierung. Durch das Kennzeichnen vergangener Tickets und das Trainieren eines Modells wie eines Transformers nutzen Sie Transfer‑Learning und Domänenwissen. Unabhängig davon, ob Sie die Python‑APIs von Hugging Face oder eine schlüsselfertige Lösung wie Open Ticket AI (Softoft’s On‑Prem‑Klassifizierungsservice) verwenden, ist der Workflow ähnlich: gekennzeichnete Daten vorbereiten, darauf trainieren und anschließend das trainierte Modell für Vorhersagen einsetzen.

Wir haben gezeigt, wie Sie Ihren CSV/JSON‑Datensatz strukturieren, die `Trainer`‑API von Hugging Face zur Feinabstimmung nutzen und die Open Ticket AI‑REST‑API für On‑Prem‑Training und Inferenz einsetzen. Die Dokumentation von Hugging Face bietet detaillierte Anleitungen zur Verwendung von Tokenizern und dem `Trainer`, und Beispiel‑Model‑Cards veranschaulichen, wie Klassifizierungsmodelle für die Ticket‑Weiterleitung eingesetzt werden. Mit diesen Werkzeugen können Sie schnell iterieren: verschiedene vortrainierte Modelle ausprobieren (z. B. BERT, RoBERTa oder sogar domänenspezifische Modelle), mit Hyperparametern experimentieren und die Leistung auf Ihrem Test‑Set messen.

Wenn Sie diese Schritte befolgen, kann Ihr Support‑System Tickets automatisch an das richtige Team weiterleiten, dringende Probleme kennzeichnen und Ihrem Personal unzählige Stunden manueller Sortierung ersparen. Diese tiefe Integration von NLP in Ihren Ticket‑Workflow ist jetzt mit modernen Bibliotheken und APIs zugänglich – Sie müssen lediglich Ihre Daten und Labels bereitstellen.