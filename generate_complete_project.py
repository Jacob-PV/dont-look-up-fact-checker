#!/usr/bin/env python3
"""
Complete project generation script for Don't Look Up Fact-Checker.
This script generates all remaining files for a production-ready MVP.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# File contents dictionary - all files to be created
FILES = {
    # ============================================================
    # BACKEND SCHEMAS
    # ============================================================
    "backend/app/schemas/common.py": '''"""Common Pydantic schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""
    items: list
    total: int
    limit: int
    offset: int


class MessageResponse(BaseModel):
    """Simple message response."""
    message: str
    detail: Optional[str] = None
''',

    "backend/app/schemas/source.py": '''"""News source Pydantic schemas."""
from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
from uuid import UUID


class NewsSourceBase(BaseModel):
    """Base news source schema."""
    name: str
    source_type: str  # 'rss', 'api'
    url: str
    reliability_score: float = 0.5
    political_bias: Optional[str] = None
    fetch_frequency_minutes: int = 60


class NewsSourceCreate(NewsSourceBase):
    """Schema for creating a news source."""
    pass


class NewsSourceUpdate(BaseModel):
    """Schema for updating a news source."""
    name: Optional[str] = None
    is_active: Optional[bool] = None
    reliability_score: Optional[float] = None
    fetch_frequency_minutes: Optional[int] = None


class NewsSourceResponse(NewsSourceBase):
    """Schema for news source response."""
    id: UUID
    is_active: bool
    last_fetched_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
''',

    "backend/app/schemas/article.py": '''"""Article Pydantic schemas."""
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class ArticleBase(BaseModel):
    """Base article schema."""
    title: str
    url: str
    author: Optional[str] = None
    published_at: Optional[datetime] = None


class ArticleCreate(ArticleBase):
    """Schema for creating an article."""
    source_id: UUID
    content: Optional[str] = None


class ArticleResponse(ArticleBase):
    """Schema for article response."""
    id: UUID
    source_id: UUID
    source_name: Optional[str] = None
    status: str
    claim_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ArticleDetailResponse(ArticleResponse):
    """Schema for detailed article response."""
    content: Optional[str] = None
    claims: List = []
''',

    "backend/app/schemas/claim.py": '''"""Claim Pydantic schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class ClaimBase(BaseModel):
    """Base claim schema."""
    claim_text: str
    claim_type: Optional[str] = None
    context: Optional[str] = None
    is_checkable: bool = True


class ClaimCreate(ClaimBase):
    """Schema for creating a claim."""
    article_id: UUID
    extraction_confidence: Optional[float] = None


class ClaimResponse(ClaimBase):
    """Schema for claim response."""
    id: UUID
    article_id: UUID
    extraction_confidence: Optional[float]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ClaimDetailResponse(ClaimResponse):
    """Schema for detailed claim response."""
    article_title: Optional[str] = None
    investigation: Optional[dict] = None
''',

    "backend/app/schemas/investigation.py": '''"""Investigation Pydantic schemas."""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class InvestigationBase(BaseModel):
    """Base investigation schema."""
    verdict: str
    confidence_score: float
    summary: str


class InvestigationCreate(InvestigationBase):
    """Schema for creating an investigation."""
    claim_id: UUID
    reasoning: Optional[str] = None


class InvestigationResponse(InvestigationBase):
    """Schema for investigation response."""
    id: UUID
    claim_id: UUID
    claim_text: Optional[str] = None
    evidence_count: int = 0
    supporting_evidence_count: int = 0
    refuting_evidence_count: int = 0
    propaganda_signals: dict = {}
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InvestigationDetailResponse(InvestigationResponse):
    """Schema for detailed investigation response."""
    reasoning: Optional[str]
    evidence: List = []
''',

    "backend/app/schemas/evidence.py": '''"""Evidence Pydantic schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class EvidenceBase(BaseModel):
    """Base evidence schema."""
    source_url: str
    source_name: Optional[str]
    snippet: str
    stance: str  # 'supporting', 'refuting', 'neutral'


class EvidenceCreate(EvidenceBase):
    """Schema for creating evidence."""
    investigation_id: UUID
    source_reliability: Optional[float] = None
    relevance_score: Optional[float] = None


class EvidenceResponse(EvidenceBase):
    """Schema for evidence response."""
    id: UUID
    source_reliability: Optional[float]
    relevance_score: Optional[float]
    published_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True
''',

    # ============================================================
    # BACKEND CORE SERVICES
    # ============================================================
    "backend/app/core/__init__.py": '''"""Core services package."""
''',

    "backend/app/core/logging.py": '''"""Structured logging setup."""
import structlog
import logging
from app.config import settings


def setup_logging():
    """Configure structured logging."""
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, settings.LOG_LEVEL),
    )

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


logger = structlog.get_logger()
''',

    "backend/app/core/security.py": '''"""Security utilities."""
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_api_key(api_key: str) -> str:
    """Hash API key for storage."""
    return hashlib.sha256(
        (api_key + settings.API_KEY_SALT).encode()
    ).hexdigest()


def generate_api_key() -> str:
    """Generate a random API key."""
    return secrets.token_urlsafe(32)


def verify_api_key(plain_key: str, hashed_key: str) -> bool:
    """Verify API key against hash."""
    return hash_api_key(plain_key) == hashed_key
''',

    # ============================================================
    # LLM SERVICES
    # ============================================================
    "backend/app/services/__init__.py": '''"""Services package."""
''',

    "backend/app/services/llm/__init__.py": '''"""LLM services package."""
''',

    "backend/app/services/llm/ollama_client.py": '''"""Ollama API client for LLM inference."""
import httpx
import json
from typing import Optional, Dict, Any
from app.config import settings
from app.core.logging import logger


class OllamaClient:
    """Client for Ollama API."""

    def __init__(self):
        self.base_url = settings.OLLAMA_API_URL
        self.model = settings.OLLAMA_MODEL
        self.timeout = 60.0

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """Generate completion from Ollama."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "system": system_prompt,
                        "stream": False,
                        "options": {
                            "temperature": temperature,
                            "num_predict": max_tokens
                        }
                    }
                )
                response.raise_for_status()
                result = response.json()
                return result.get("response", "")
        except Exception as e:
            logger.error("ollama_generation_failed", error=str(e))
            raise

    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate JSON response from Ollama."""
        response_text = await self.generate(prompt, system_prompt)

        # Try to extract JSON from response
        try:
            # Remove markdown code blocks if present
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]

            return json.loads(response_text.strip())
        except json.JSONDecodeError as e:
            logger.error("json_parse_failed", response=response_text, error=str(e))
            return {}
''',

    "backend/app/services/llm/prompts.py": '''"""LLM prompt templates."""

CLAIM_EXTRACTION_PROMPT = """You are a fact-checking assistant. Extract all verifiable factual claims from the following article.

A factual claim is a statement that can be objectively verified as true or false using evidence.

EXCLUDE:
- Opinions and subjective statements
- Predictions about the future
- Questions
- Purely descriptive statements without assertions

For each claim, provide:
1. claim_text: The exact claim from the article
2. claim_type: "factual", "statistic", or "quote"
3. context: 1-2 surrounding sentences for context
4. checkability: Score from 0.0 to 1.0 indicating how verifiable this claim is

Article:
{article_text}

Output your response as a JSON array:
[
  {{
    "claim_text": "exact claim from article",
    "claim_type": "factual|statistic|quote",
    "context": "surrounding context",
    "checkability": 0.9
  }}
]

Only output the JSON array, no other text.
"""

FACT_CHECKING_PROMPT = """You are an expert fact-checker. Analyze the following claim using the provided evidence.

Claim: {claim_text}

Evidence:
{evidence_list}

Tasks:
1. Determine the verdict: "true", "mostly_true", "mixed", "mostly_false", "false", or "unverifiable"
2. Provide a confidence score from 0.0 to 1.0
3. Write a summary of your findings (2-3 sentences)
4. Explain your reasoning process

Verdict meanings:
- true: Claim is accurate and supported by all evidence
- mostly_true: Claim is largely accurate with minor inaccuracies
- mixed: Claim has both accurate and inaccurate elements
- mostly_false: Claim is largely inaccurate with some accurate elements
- false: Claim is completely inaccurate
- unverifiable: Not enough evidence to determine truth

Output your response as JSON:
{{
  "verdict": "true|mostly_true|mixed|mostly_false|false|unverifiable",
  "confidence": 0.85,
  "summary": "Brief summary of findings",
  "reasoning": "Detailed reasoning process"
}}

Only output the JSON object, no other text.
"""

PROPAGANDA_DETECTION_PROMPT = """You are an expert in detecting propaganda and manipulation techniques.

Analyze the following text for propaganda techniques:

Text: {text}

Common propaganda techniques to look for:
- Appeal to fear: Using fear to influence decisions
- Loaded language: Emotionally charged words
- Bandwagon: "Everyone else believes this"
- Appeal to authority: Misusing authority figures
- False dilemma: Presenting only two options
- Straw man: Misrepresenting opposing views
- Ad hominem: Attacking the person not the argument

For each technique detected, provide:
1. technique: Name of the propaganda technique
2. confidence: Score from 0.0 to 1.0
3. evidence: Quote from text showing this technique

Calculate an overall propaganda score from 0.0 to 1.0.

Output as JSON:
{{
  "techniques_detected": [
    {{
      "technique": "appeal_to_fear",
      "confidence": 0.85,
      "evidence": "quote from text"
    }}
  ],
  "overall_propaganda_score": 0.65
}}

Only output the JSON object, no other text.
"""
''',

    # Continue with more files in next batch...
    "backend/app/services/privacy/__init__.py": '''"""Privacy services package."""
''',

    "backend/app/services/privacy/pii_detector.py": '''"""PII detection using spaCy and Presidio."""
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
''',

}  # End of FILES dictionary

def create_files():
    """Create all files in the project."""
    for file_path, content in FILES.items():
        full_path = BASE_DIR / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"Creating: {file_path}")
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"\\n✅ Created {len(FILES)} files successfully!")


if __name__ == "__main__":
    create_files()
