"""Service for fact-checking claims using evidence and Ollama LLM."""
from typing import List
from sqlalchemy.orm import Session
from app.services.llm.ollama_client import OllamaClient
from app.services.llm.prompts import FACT_CHECKING_PROMPT
from app.models.claim import Claim
from app.models.investigation import Investigation
from app.models.evidence import Evidence
from app.core.logging import logger


class FactChecker:
    """Fact-check claims using evidence and LLM analysis."""

    def __init__(self):
        self.ollama_client = OllamaClient()

    async def fact_check_claim(
        self,
        claim: Claim,
        evidence_list: List[Evidence],
        db: Session
    ) -> Investigation:
        """
        Fact-check a claim using provided evidence.

        Args:
            claim: Claim to fact-check
            evidence_list: List of Evidence records for this claim
            db: Database session (not used but kept for consistency)

        Returns:
            Investigation object (not yet committed to DB)
        """
        try:
            # Format evidence for prompt
            evidence_text = self._format_evidence(evidence_list)

            # Format prompt
            prompt = FACT_CHECKING_PROMPT.format(
                claim_text=claim.claim_text,
                evidence_list=evidence_text
            )

            # Call Ollama with retry logic
            result = await self._check_with_retry(prompt)

            if not result:
                logger.warning("no_verdict_returned", claim_id=str(claim.id))
                result = {
                    'verdict': 'unverifiable',
                    'confidence': 0.0,
                    'summary': 'Unable to determine verdict',
                    'reasoning': 'Fact-checking analysis returned no result'
                }

            # Calculate evidence metrics
            supporting_count = sum(1 for e in evidence_list if e.stance == 'supporting')
            refuting_count = sum(1 for e in evidence_list if e.stance == 'refuting')
            avg_reliability = (
                sum(e.source_reliability or 0.0 for e in evidence_list) / len(evidence_list)
                if evidence_list else 0.0
            )

            # Create Investigation
            investigation = Investigation(
                claim_id=claim.id,
                verdict=result.get('verdict', 'unverifiable'),
                confidence_score=result.get('confidence', 0.0),
                summary=result.get('summary', ''),
                reasoning=result.get('reasoning', ''),
                source_reliability_avg=avg_reliability,
                evidence_count=len(evidence_list),
                supporting_evidence_count=supporting_count,
                refuting_evidence_count=refuting_count,
                status='completed'
            )

            logger.info(
                "claim_fact_checked",
                claim_id=str(claim.id),
                verdict=investigation.verdict,
                confidence=investigation.confidence_score
            )

            return investigation

        except Exception as e:
            logger.error("fact_check_failed", claim_id=str(claim.id), error=str(e))
            raise

    def _format_evidence(self, evidence_list: List[Evidence]) -> str:
        """
        Format evidence list for prompt.

        Args:
            evidence_list: List of Evidence records

        Returns:
            Formatted string of evidence for LLM prompt
        """
        if not evidence_list:
            return "No evidence found."

        formatted = []
        for i, evidence in enumerate(evidence_list, 1):
            formatted.append(
                f"{i}. Source: {evidence.source_name or 'Unknown'}\n"
                f"   URL: {evidence.source_url}\n"
                f"   Stance: {evidence.stance}\n"
                f"   Snippet: {evidence.snippet}\n"
            )

        return "\n".join(formatted)

    async def _check_with_retry(self, prompt: str, max_retries: int = 3) -> dict:
        """
        Fact-check with retry logic for Ollama failures.

        Args:
            prompt: Formatted prompt for fact-checking
            max_retries: Maximum number of retry attempts

        Returns:
            Dictionary with verdict, confidence, summary, reasoning
        """
        for attempt in range(max_retries):
            try:
                result = await self.ollama_client.generate_json(prompt)

                # Validate required fields
                if isinstance(result, dict) and 'verdict' in result:
                    return result
                else:
                    logger.warning("invalid_verdict_format", result=result, attempt=attempt+1)
                    if attempt < max_retries - 1:
                        continue
                    return {}

            except Exception as e:
                logger.error("ollama_error", attempt=attempt+1, error=str(e))
                if attempt < max_retries - 1:
                    continue
                raise

        return {}
