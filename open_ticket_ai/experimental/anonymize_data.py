# FILE_PATH: open_ticket_ai\experimental\anonymize_data.py
# Installationen und Modelldownload (falls noch nicht geschehen)
"""Module for anonymizing personally identifiable information (PII) in text.

This module provides functionality to detect and replace various types of sensitive
information in German text using named entity recognition, regular expressions, and
the Faker library for generating replacement data.

Example:
    To anonymize a text string:

    ```python
    anonymized = anonymize_text("Original text with PII")
    ```

Note:
    Uses German locale for generating fake data and models optimized for German text.
"""
import re

import phonenumbers
from faker import Faker

try:
    import spacy

    nlp = spacy.load("de_core_news_sm")
except Exception:  # pragma: no cover - optional dependency
    nlp = None

fake = Faker("de_DE")


def anonymize_text(text):
    """Anonymizes sensitive information (PII) in the input text by replacing it with fake data.

    This function identifies and replaces the following types of personally identifiable information (PII):
      - Person names (PER), organization names (ORG), and locations (LOC) using spaCy's named entity recognition
      - Email addresses using regular expressions
      - Phone numbers (valid German numbers) using the `phonenumbers` library
      - IBANs using regular expressions
      - Street addresses (German format) using regular expressions

    The replacements are done in the following order:
      1. Named entities (processed from last to first to avoid index shifting)
      2. Email addresses
      3. Phone numbers
      4. IBANs
      5. Street addresses

    Args:
        text (str): The input text containing sensitive information to be anonymized.

    Returns:
        str: The anonymized text with all detected PII replaced by fake data.

    Note:
        Uses Faker with German localization for generating replacement data.
    """
    if nlp is None:
        return text

    doc = nlp(text)
    new_text = text
    # Ersetzungen für erkannte Named Entities (von hinten nach vorn, um Indexprobleme zu vermeiden)
    for ent in sorted(doc.ents, key=lambda e: e.start_char, reverse=True):
        start, end = ent.start_char, ent.end_char
        if ent.label_ == "PER":  # Personenname
            fake_name = fake.first_name() + " " + fake.last_name()
            new_text = new_text[:start] + fake_name + new_text[end:]
        elif ent.label_ == "ORG":  # Organisation/Firma
            fake_org = fake.company()
            new_text = new_text[:start] + fake_org + new_text[end:]
        elif ent.label_ == "LOC":  # Ort (Stadt, Land, etc.)
            fake_city = fake.city_name()
            new_text = new_text[:start] + fake_city + new_text[end:]
    # E-Mail-Adressen maskieren (Regex)
    new_text = re.sub(r'\b[\w.+-]+@[\w-]+\.\w+\b', lambda m: fake.ascii_email(), new_text)
    # Telefonnummern erkennen und ersetzen
    def replace_phone(match):
        """Replaces a matched phone number with a fake German phone number if valid.

        Args:
            match (re.Match): A regex match object containing the phone number string.

        Returns:
            str: Fake phone number if input is valid, original string otherwise.
        """
        num_str = match.group(0)
        try:
            num = phonenumbers.parse(num_str, "DE")
            if phonenumbers.is_valid_number(num):
                return fake.phone_number()
        except phonenumbers.NumberParseException:
            pass
        return num_str
    new_text = re.sub(r'\+?\d[\d\s\-\(\)]{7,}\d', replace_phone, new_text)
    # IBAN erkennen und ersetzen
    new_text = re.sub(
        r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b",
        lambda m: fake.iban(),
        new_text,
    )
    # (Optional) Einfache Erkennung von Adressen mit Straßenname und Nummer
    new_text = re.sub(
        r'\b[A-ZÄÖÜ][a-zäöüß]+(?:straße|Str\.|Weg|Platz)\s*\d+[a-zA-Z]?\b',
        lambda m: fake.street_address(),
        new_text
    )
    return new_text

# Beispieltext mit PII
text = (
    "Herr Dr. Max Mustermann wohnt in der Musterstraße 5 in 55122 Mainz. "
    "Er arbeitet bei der Musterfirma GmbH. Kontakt: max@mustermann.de, +49 170 1234567."
)
if __name__ == '__main__':

    print("Original:", text)
    print("Anonymisiert:", anonymize_text(text))
