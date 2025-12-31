"""Service for extracting claims from articles using Ollama LLM."""
import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.services.llm.ollama_client import OllamaClient
from app.services.llm.prompts import CLAIM_EXTRACTION_PROMPT
from app.models.article import Article
from app.models.claim import Claim
from app.core.logging import logger


class ClaimExtractor:
    """Extract verifiable claims from articles using LLM."""

    def __init__(self):
        self.ollama_client = OllamaClient()

    async def extract_claims(self, article: Article, db: Session) -> List[Claim]:
        """
        Extract claims from an article.

        Args:
            article: Article to extract claims from
            db: Database session (not used in extraction but kept for consistency)

        Returns:
            List of Claim objects (not yet committed to DB)
        """
        if not article.content:
            logger.warning("article_missing_content", article_id=str(article.id))
            return []

        try:
            # Format prompt with article content
            prompt = CLAIM_EXTRACTION_PROMPT.format(article_text=article.content)

            # Call Ollama with retry logic
            claims_data = await self._extract_with_retry(prompt)

            if not claims_data:
                logger.warning("no_claims_extracted", article_id=str(article.id))
                return []

            # Create Claim objects
            claims = []
            for claim_dict in claims_data:
                claim = Claim(
                    article_id=article.id,
                    claim_text=claim_dict.get('claim_text', ''),
                    claim_type=claim_dict.get('claim_type', 'factual'),
                    context=claim_dict.get('context', ''),
                    is_checkable=claim_dict.get('checkability', 0.0) > 0.5,
                    extraction_confidence=claim_dict.get('checkability', 0.0),
                    status='pending'
                )
                claims.append(claim)

            logger.info("claims_extracted", article_id=str(article.id), count=len(claims))
            return claims

        except Exception as e:
            logger.error("claim_extraction_failed", article_id=str(article.id), error=str(e))
            raise

    async def _extract_with_retry(self, prompt: str, max_retries: int = 3) -> List[Dict[str, Any]]:
        """
        Extract claims with retry logic for Ollama failures.

        Args:
            prompt: Formatted prompt for claim extraction
            max_retries: Maximum number of retry attempts

        Returns:
            List of claim dictionaries
        """
        for attempt in range(max_retries):
            try:
                result = await self.ollama_client.generate_json(prompt)

                # Handle case where result is a dict with 'claims' key
                if isinstance(result, dict) and 'claims' in result:
                    return result['claims']
                # Handle case where result is directly a list
                elif isinstance(result, list):
                    return result
                # Handle empty/invalid response
                else:
                    logger.warning("invalid_claims_format", result=result, attempt=attempt+1)
                    if attempt < max_retries - 1:
                        continue
                    return []

            except json.JSONDecodeError as e:
                logger.warning("json_parse_error", attempt=attempt+1, error=str(e))
                if attempt < max_retries - 1:
                    continue
                return []
            except Exception as e:
                logger.error("ollama_error", attempt=attempt+1, error=str(e))
                if attempt < max_retries - 1:
                    continue
                raise

        return []
