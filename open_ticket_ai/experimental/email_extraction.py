# FILE_PATH: open_ticket_ai\experimental\email_extraction.py
"""This module provides text cleaning and email signature removal utilities for German text.

It includes functions to:
- Clean German text by removing stop words and converting to lowercase
- Remove signature blocks from email bodies using pattern matching and NLP techniques

Dependencies:
    spacy: For German NLP processing
    nltk: For stopword removal and tokenization
"""

import re

import spacy

nlp = spacy.load('de_core_news_sm')

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')


def clean_text(text):
    """Cleans German text by converting to lowercase and removing stop words.

    This function processes input text through the following steps:
    1. Converts all text to lowercase
    2. Tokenizes the text into individual words
    3. Removes German stop words using NLTK's predefined list
    4. Rejoins the remaining words into a cleaned string

    Args:
        text (str): The input text to be cleaned

    Returns:
        str: The cleaned text with stop words removed and in lowercase

    Note:
        Requires NLTK German stopwords to be downloaded (handled automatically)
    """
    text = text.lower()
    stop_words = set(stopwords.words('german'))
    word_tokens = word_tokenize(text, language="german")
    filtered_text = [word for word in word_tokens if word not in stop_words]
    return ' '.join(filtered_text)


def remove_signature(email):
    """Removes signature blocks from email bodies using pattern matching and NLP.

    Processes email content by:
    1. Splitting at common signature separators (e.g., '---', '***')
    2. Removing signature elements through:
        - Common German/English closing phrases
        - Contact information patterns (phone, email, etc.)
        - Company/organization details
        - Named entity recognition for persons and organizations
    3. Reconstructing the email body with cleaned content

    Args:
        email (str): The full email content including potential signature

    Returns:
        str: The processed email body with signature elements removed

    Note:
        Uses spaCy's German NLP model (de_core_news_sm) for entity recognition.
        Designed primarily for German emails but handles common English closings.
    """
    parts = re.split(r'-{2,}|\*{2,}', email)
    main_body = parts[0]

    if len(parts) > 1:
        signature_candidate = parts[-1]
        signature_candidate = re.sub(
            r'(?i)(mit freundlichen grüßen|beste grüße|herzliche grüße|viele grüße|cheers|thank you|thanks)[^\n]*',
            '', signature_candidate)
        signature_candidate = re.sub(r'(?i)\b(Tel|Telephone|Phone|Fax|E-Mail|Email|Web|Website|URL):.*', '',
                                     signature_candidate)
        signature_candidate = re.sub(
            r'(?i)\b(Address|Adresse|Location|Standort|Company|Firma|Position|Titel|Geschäftsführung):.*', '',
            signature_candidate)
        signature_candidate = re.sub(r'[\n\r]+', ' ',
                                     signature_candidate)

        doc = nlp(signature_candidate)
        for ent in doc.ents:
            if ent.label_ in ['PER', 'ORG']:
                signature_candidate = signature_candidate.replace(ent.text, '')

        main_body += ' ' + signature_candidate.strip()

    return main_body.strip()


if __name__ == '__main__':
    email_text = """
    Hallo Herr Müller,

hier ist der Bericht über die Ergebnisse der letzten Woche. Bitte lassen Sie mich wissen, ob Sie Fragen haben.

Mit freundlichen Grüßen
John Doe
John Doe
Position: Chefredakteur
Company: Beispiel GmbH
Tel: +49 123 456789
E-Mail: john.doe@beispiel.de
Web: www.beispiel.de
    """

    print(clean_text(remove_signature(email_text)))
