"""PII detection using spaCy and Presidio."""
import spacy
from typing import List, Dict
from app.config import settings
from app.core.logging import logger

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.warning("spacy_model_not_found", message="Run: python -m spacy download en_core_web_sm")
    nlp = None


class PIIDetector:
    """Detect PII in text using NLP."""

    def __init__(self):
        self.nlp = nlp
        self.enabled = settings.PII_DETECTION_ENABLED

    def detect(self, text: str) -> List[Dict]:
        """Detect PII entities in text."""
        if not self.enabled or not self.nlp:
            return []

        doc = self.nlp(text)
        pii_entities = []

        for ent in doc.ents:
            if ent.label_ in ["PERSON", "GPE", "ORG", "EMAIL", "PHONE"]:
                pii_entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "confidence": 0.8  # spaCy doesn't provide confidence, use default
                })

        return pii_entities


class PIIRedactor:
    """Redact PII from text."""

    def __init__(self):
        self.detector = PIIDetector()

    def redact(self, text: str) -> tuple[str, int]:
        """Redact PII and return redacted text + count."""
        entities = self.detector.detect(text)

        if not entities:
            return text, 0

        # Sort entities by position (reverse order to maintain positions)
        entities_sorted = sorted(entities, key=lambda x: x["start"], reverse=True)

        redacted_text = text
        for entity in entities_sorted:
            placeholder = f"[{entity['label']}]"
            redacted_text = (
                redacted_text[:entity["start"]] +
                placeholder +
                redacted_text[entity["end"]:]
            )

        return redacted_text, len(entities)
