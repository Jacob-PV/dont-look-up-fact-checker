"""Service for detecting propaganda in text."""
from typing import Dict, Any
from app.services.llm.ollama_client import OllamaClient
from app.services.llm.prompts import PROPAGANDA_DETECTION_PROMPT
from app.core.logging import logger


class PropagandaDetector:
    """Detect propaganda techniques in text using LLM."""

    def __init__(self):
        self.ollama_client = OllamaClient()

    async def detect_propaganda(self, text: str) -> Dict[str, Any]:
        """
        Detect propaganda in text.

        Args:
            text: Text to analyze for propaganda

        Returns:
            Dictionary with:
            - techniques_detected: list of {technique, confidence, evidence}
            - overall_propaganda_score: float (0.0-1.0)
        """
        try:
            # Format prompt with text
            prompt = PROPAGANDA_DETECTION_PROMPT.format(text=text)

            # Call Ollama with retry logic
            result = await self._detect_with_retry(prompt)

            if not result:
                logger.warning("no_propaganda_result", text_length=len(text))
                return {
                    'techniques_detected': [],
                    'overall_propaganda_score': 0.0
                }

            # Ensure result has required fields
            if 'techniques_detected' not in result:
                result['techniques_detected'] = []

            if 'overall_propaganda_score' not in result:
                result['overall_propaganda_score'] = 0.0

            logger.info(
                "propaganda_detected",
                score=result.get('overall_propaganda_score', 0.0),
                techniques_count=len(result.get('techniques_detected', []))
            )

            return result

        except Exception as e:
            logger.error("propaganda_detection_failed", error=str(e))
            return {
                'techniques_detected': [],
                'overall_propaganda_score': 0.0
            }

    async def _detect_with_retry(
        self,
        prompt: str,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Detect propaganda with retry logic for Ollama failures.

        Args:
            prompt: Formatted propaganda detection prompt
            max_retries: Maximum number of retry attempts

        Returns:
            Dictionary with propaganda detection results
        """
        for attempt in range(max_retries):
            try:
                result = await self.ollama_client.generate_json(prompt)

                # Validate result format
                if isinstance(result, dict) and 'overall_propaganda_score' in result:
                    # Ensure propaganda_score is a float between 0.0 and 1.0
                    score = result.get('overall_propaganda_score', 0.0)
                    if isinstance(score, (int, float)):
                        result['overall_propaganda_score'] = max(0.0, min(1.0, float(score)))
                    else:
                        result['overall_propaganda_score'] = 0.0

                    # Ensure techniques_detected is a list
                    if 'techniques_detected' not in result or not isinstance(result['techniques_detected'], list):
                        result['techniques_detected'] = []

                    return result
                else:
                    logger.warning(
                        "invalid_propaganda_format",
                        result=result,
                        attempt=attempt + 1
                    )

                    if attempt < max_retries - 1:
                        continue

                    # Return empty result if all retries fail
                    return {
                        'techniques_detected': [],
                        'overall_propaganda_score': 0.0
                    }

            except Exception as e:
                logger.error(
                    "ollama_propaganda_error",
                    attempt=attempt + 1,
                    error=str(e)
                )

                if attempt < max_retries - 1:
                    continue

                # Re-raise on final attempt
                raise

        # Fallback if loop completes without returning
        return {
            'techniques_detected': [],
            'overall_propaganda_score': 0.0
        }
