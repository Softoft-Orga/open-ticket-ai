---
description: Fine-tune an AI model on your ticket data for accurate, automated classification.
  This guide shows how to prepare datasets and train with Hugging Face or a REST API.
---
# How to Fine-Tune an AI Model with Your Own Ticket Data

Fine-tuning an AI model on your own ticket data is a powerful way to customize ticket classification
for your organization. By training a model on labeled support tickets, you teach it your
domain-specific language and categories. This process generally involves preparing a dataset (often
a CSV or JSON file of tickets and labels), choosing or creating labels (such as departments or
priority levels), and then training a model like a Transformer-based classifier on that data. You
can use tools like Hugging Face’s Transformer library to train models locally, or use a dedicated
solution like **Open Ticket AI (ATC)**, which provides an on-premise REST API for ticket
classification. In either case, you benefit from transfer learning: a pre-trained model (e.g. BERT,
DistilBERT or RoBERTa) is adapted to your ticket categories, greatly improving accuracy over a
generic model.

Modern text classification workflows follow these high-level steps:

* **Collect and Label Data:** Gather historical tickets and assign them the correct categories (
  queues) or priorities. Each ticket should have a text field and at least one label.
* **Format the Dataset:** Save this labeled data in a structured format (CSV or JSON). For example,
  a CSV might have columns `"text","label"`.
* **Split into Train/Test:** Reserve a portion for validation/testing to evaluate performance.
* **Fine-Tune the Model:** Use a library like Hugging Face Transformers, or our Open Ticket AI API,
  to train a classification model on the data.
* **Evaluate and Deploy:** Check accuracy (or F1) on held-out data, then use the trained model to
  classify new tickets.

Tech-savvy readers can follow these steps in detail. The examples below illustrate how to prepare
ticket data and fine-tune a model using **Hugging Face Transformers**, as well as how our Open
Ticket AI solution supports this workflow via API calls. Throughout, we assume common ticket
categories (e.g. “Billing”, “Technical Support”) and priority labels, but your labels can be
anything relevant to your system.

## Preparing Your Ticket Data

First, gather a representative set of past tickets and label them according to your classification
scheme. Labels could be departments (like **Technical Support**, **Customer Service**, **Billing**,
etc.) or priority levels (e.g. **Low**, **Medium**, **High**). For example, the Softoft ticket
dataset includes categories such as *Technical Support*, *Billing and Payments*, *IT Support*, and
*General Inquiry*. A Hugging Face example model uses labels like *Billing Question*, *Feature
Request*, *General Inquiry*, and *Technical Issue*. Define whatever categories make sense for your
workflow.

Organize the data in CSV or JSON format. Each record should contain the ticket text and its label.
For instance, a CSV might look like:

```
text,label
"My printer will not connect to WiFi",Hardware,  # Example ticket text and its category
"I need help accessing my account",Account
```

If you include priorities or multiple labels, you could add more columns (e.g. `priority`). The
exact structure is flexible, as long as you clearly map each ticket text to its label(s). It’s
common to have one column for the ticket content (e.g. `"text"` or `"ticket_text"`) and one column
for the label.

You may need to clean and preprocess the text slightly (e.g. remove signatures, HTML tags, or
anonymize data), but in many cases raw ticket text works fine as input to modern NLP models.
Finally, split the labeled data into a training set and a validation/test set (for example, 80%
train / 20% test). This split lets you measure how well the fine-tuned model generalizes.

## Labeling Tickets

Consistent, accurate labels are crucial. Make sure each ticket is correctly assigned to one of your
chosen categories. This might be done manually by support staff or by using existing ticket metadata
if available. Often, organizations label tickets by *queue* or department, and sometimes also by
*priority*. For example, the Softoft email ticket dataset categorizes tickets by both department (
queue) and priority. Priority can be useful if you want to train a model to predict urgency: e.g.,
`Low`, `Medium`, `Critical`. In many setups, you might train one model for department classification
and another for priority classification.

Whatever your scheme, ensure you have a finite set of label values. In a CSV, you might have:

```
text,label,priority
"System crash when saving file","Technical Support","High"
"Request to change billing address","Billing","Low"
```

This example has two label columns: one for category and one for priority. For simplicity, in the
following examples we assume a single-label classification task (one label column).

**Key tips for labeling:**

* Define your label names clearly. For instance, *Technical Support* vs *IT Support* vs *Hardware
  Issue* – avoid ambiguous overlap.
* If tickets often belong to multiple categories, you might consider multi-label classification (
  assigning multiple labels) or break it into separate models.
* Use consistent formatting (same spelling, casing) for labels in your dataset.

By the end of this step, you should have a labeled dataset file (CSV or JSON) with ticket texts and
their labels, ready for the model.

## Fine-Tuning with Hugging Face Transformers

One of the most flexible ways to fine-tune a text classifier is using
the [Hugging Face Transformers](https://huggingface.co/transformers/) library. This lets you start
from a pre-trained language model (like BERT or RoBERTa) and train it further on your specific
ticket dataset. The core steps are: tokenize the text, set up a `Trainer`, and call `train()`.

1. **Load the Dataset:** Use `datasets` or `pandas` to load your CSV/JSON. For example, Hugging
   Face’s `datasets` library can read a CSV directly:

   ```python
   from datasets import load_dataset
   dataset = load_dataset("csv", data_files={
       "train": "tickets_train.csv",
       "validation": "tickets_val.csv"
   })
   # Assuming 'text' is the column with ticket content, and 'label' is the category column.
   ```

2. **Tokenize the Text:** Pre-trained transformers require tokenized input. Load a tokenizer (e.g.
   DistilBERT) and apply it to your text:

   ```python
   from transformers import AutoTokenizer
   tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

   def preprocess_function(examples):
       # Tokenize the texts (this will produce input_ids, attention_mask, etc.)
       return tokenizer(examples["text"], truncation=True, padding="max_length")

   tokenized_datasets = dataset.map(preprocess_function, batched=True)
   ```

   This follows the Hugging Face example: first load the DistilBERT tokenizer, then use`Dataset.map`
   to tokenize all texts in batches. The result (`tokenized_datasets`) contains input IDs and
   attention masks, ready for the model.

3. **Load the Model:** Choose a pre-trained model and specify the number of labels. For instance, to
   fine-tune DistilBERT for classification:

   ```python
   from transformers import AutoModelForSequenceClassification
   num_labels = 4  # set this to the number of your categories
   model = AutoModelForSequenceClassification.from_pretrained(
       "distilbert-base-uncased", num_labels=num_labels
   )
   ```

   This matches Hugging Face’s sequence classification example, where the model is loaded with
   `num_labels` equal to the classes in your dataset.

4. **Set Training Arguments and Trainer:** Define hyperparameters with `TrainingArguments`, then
   create a `Trainer` with your model and tokenized data:

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

   This reflects the Hugging Face guide: after setting up `TrainingArguments` (for output directory,
   epochs, batch size, etc.), we instantiate `Trainer` with the model, datasets, tokenizer, and
   training arguments.

5. **Train the Model:** Call `trainer.train()` to start fine-tuning. This will run for the specified
   number of epochs, periodically evaluating on the validation set if provided.

   ```python
   trainer.train()
   ```

   As per the docs, this single command begins fine-tuning. Training may take minutes to hours
   depending on data size and hardware (GPU recommended for large datasets).

6. **Evaluate and Save:** After training, evaluate the model on your test set to check accuracy or
   other metrics. Then save the fine-tuned model and tokenizer:

   ```python
   trainer.evaluate()
   model.save_pretrained("fine_tuned_ticket_model")
   tokenizer.save_pretrained("fine_tuned_ticket_model")
   ```

   You can later reload this model with
   `AutoModelForSequenceClassification.from_pretrained("fine_tuned_ticket_model")`.

Once trained, you can use the model for inference. For example, Hugging Face’s pipeline API makes it
easy:

```python
from transformers import pipeline

classifier = pipeline("text-classification", model="fine_tuned_ticket_model")
results = classifier("Please reset my password and clear my cache.")
print(results)
```

This will output the predicted label and confidence for the new ticket text. As demonstrated by
Hugging Face examples, the `pipeline("text-classification")` abstraction lets you quickly classify
new ticket texts with the fine-tuned model.

## Using Open Ticket AI (Softoft’s ATC) for Training and Inference

Our **Open Ticket AI** system (also known as ATC – AI Ticket Classification) provides an on-premise,
Dockerized solution with a REST API that can ingest your labeled ticket data and train models
automatically. This means you can keep all data local and still leverage powerful ML. The ATC API
has endpoints to upload data, trigger training, and classify tickets.

* **Upload Training Data:** Send your labeled tickets CSV to the `/api/v1/train-data` endpoint. The
  API expects a CSV payload (`Content-Type: text/csv`) containing your training data. For example,
  using Python `requests`:

  ```python
  import requests
  url = "http://localhost:8080/api/v1/train-data"
  headers = {"Content-Type": "text/csv"}
  with open("tickets_labeled.csv", "rb") as f:
      res = requests.post(url, headers=headers, data=f)
  print(res.status_code, res.text)
  ```

  This corresponds to the “Train Data” API in the ATC docs. A successful response means the data is
  received.

* **Start Model Training:** After uploading the data, trigger training by calling `/api/v1/train` (
  no body needed). In practice:

  ```bash
  curl -X POST http://localhost:8080/api/v1/train
  ```

  Or in Python:

  ```python
  train_res = requests.post("http://localhost:8080/api/v1/train")
  print(train_res.status_code, train_res.text)
  ```

  This matches the developer documentation example, which shows that a simple POST initiates
  training. The service will train the model on the uploaded data (it uses its own training pipeline
  under the hood, possibly based on similar Transformer models). Training runs on your server, and
  the model is saved locally when done.

* **Classify New Tickets:** Once training is complete, use the `/api/v1/classify` endpoint to get
  predictions for new ticket texts. Send a JSON payload with the field `"ticket_data"` containing
  the ticket text. For example:

  ```python
  ticket_text = "My laptop overheats when I launch the app"
  res = requests.post(
      "http://localhost:8080/api/v1/classify",
      json={"ticket_data": ticket_text}
  )
  print(res.json())  # e.g. {"predicted_label": "Hardware Issue", "confidence": 0.95}
  ```

  The ATC docs show a similar `curl` example for classification. The response will typically include
  the predicted category (and possibly confidence).

Using the REST API of Open Ticket AI integrates the training flow into your own systems. You can
automate uploads and training runs (e.g. nightly training or training on new data), and then use the
classification endpoint in your ticketing workflow. Since everything runs on-premise, sensitive
ticket content never leaves your servers.

## Example Python Code

Below is a consolidated example illustrating both workflows:

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

This script demonstrates both methods: the Hugging Face fine-tuning pipeline and the Open Ticket AI
REST calls. It loads and tokenizes a CSV dataset, fine-tunes a DistilBERT classifier, and then uses
it via a pipeline. It also shows how to POST the same data to the ATC API and trigger
training/classification.

## Conclusion

Fine-tuning an AI model on your own ticket data enables highly accurate, customized ticket
classification. By labeling past tickets and training a model like a Transformer, you leverage
transfer learning and domain knowledge. Whether you use Hugging Face’s Python APIs or a turnkey
solution like Open Ticket AI (Softoft’s on-prem classification service), the workflow is similar:
prepare labeled data, train on it, and then use the trained model for predictions.

We’ve shown how to structure your CSV/JSON dataset, use Hugging Face’s `Trainer` API to fine-tune,
and use the Open Ticket AI REST API for on-prem training and inference. Hugging Face’s documentation
provides detailed guidance on using tokenizers and the `Trainer`, and example model cards illustrate
how classification models are applied to ticket routing. With these tools, you can iterate quickly:
try different pre-trained models (e.g. BERT, RoBERTa, or even domain-specific models), experiment
with hyperparameters, and measure performance on your test set.

By following these steps, your support system can automatically route tickets to the right team,
flag urgent issues, and save your staff countless hours of manual sorting. This deep integration of
NLP into your ticket workflow is now accessible with modern libraries and APIs – you just need to
supply your data and labels.

