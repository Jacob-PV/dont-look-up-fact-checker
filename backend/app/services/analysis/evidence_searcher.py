"""Service for searching evidence for claims."""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.article import Article
from app.models.claim import Claim
from app.core.logging import logger


class EvidenceSearcher:
    """Search for evidence supporting or refuting claims."""

    def search_evidence_for_claim(
        self,
        claim: Claim,
        db: Session,
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search articles for evidence related to claim.

        Args:
            claim: Claim object to find evidence for
            db: Database session
            max_results: Maximum number of evidence items to return

        Returns:
            List of dicts with:
            - article_id: UUID of source article
            - source_url: Article URL
            - source_name: Source name
            - snippet: Relevant excerpt
            - context: Surrounding text
            - relevance_score: 0.0-1.0 similarity score
        """
        try:
            # Extract keywords from claim
            keywords = self._extract_keywords(claim.claim_text)

            if not keywords:
                logger.warning("no_keywords_extracted", claim_id=str(claim.id))
                return []

            # Search articles containing keywords
            query = db.query(Article).filter(
                Article.status == 'processed'
            )

            # Filter by keyword matches in content or title
            keyword_filters = []
            for keyword in keywords[:5]:  # Top 5 keywords
                keyword_filters.append(Article.content.ilike(f'%{keyword}%'))
                keyword_filters.append(Article.title.ilike(f'%{keyword}%'))

            if keyword_filters:
                query = query.filter(or_(*keyword_filters))

            articles = query.limit(max_results * 2).all()  # Get more than needed for filtering

            # Extract snippets and calculate relevance
            evidence_data = []
            for article in articles:
                if not article.content:
                    continue

                snippet = self._extract_snippet(
                    article.content,
                    claim.claim_text,
                    keywords
                )

                if snippet:
                    relevance_score = self._calculate_relevance(
                        claim.claim_text,
                        snippet
                    )

                    # Only include if relevance is above threshold
                    if relevance_score > 0.1:
                        evidence_data.append({
                            'article_id': str(article.id),
                            'source_url': article.url or '',
                            'source_name': article.source.name if article.source else 'Unknown',
                            'snippet': snippet,
                            'context': self._get_context(article.content, snippet),
                            'relevance_score': relevance_score
                        })

            # Sort by relevance and return top results
            evidence_data.sort(key=lambda x: x['relevance_score'], reverse=True)
            final_evidence = evidence_data[:max_results]

            logger.info(
                "evidence_search_completed",
                claim_id=str(claim.id),
                evidence_found=len(final_evidence)
            )

            return final_evidence

        except Exception as e:
            logger.error("evidence_search_failed", claim_id=str(claim.id), error=str(e))
            return []

    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract important keywords from claim text.

        Args:
            text: Claim text to extract keywords from

        Returns:
            List of keywords sorted by importance
        """
        # Common stop words to exclude
        stop_words = {
            'the', 'a', 'an', 'is', 'was', 'are', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'to', 'of', 'in', 'for', 'on', 'at',
            'by', 'with', 'from', 'as', 'that', 'this', 'these', 'those', 'it',
            'its', 'or', 'and', 'but', 'if', 'so', 'than', 'then', 'not', 'no'
        }

        # Clean and split text
        words = text.lower().replace(',', ' ').replace('.', ' ').split()

        # Filter and get meaningful keywords
        keywords = [
            w.strip() for w in words
            if w.strip() not in stop_words and len(w.strip()) > 3
        ]

        # Return unique keywords preserving order
        seen = set()
        unique_keywords = []
        for kw in keywords:
            if kw not in seen:
                seen.add(kw)
                unique_keywords.append(kw)

        return unique_keywords

    def _extract_snippet(
        self,
        content: str,
        claim: str,
        keywords: List[str],
        snippet_length: int = 200
    ) -> str:
        """
        Extract relevant snippet from article content.

        Args:
            content: Article content
            claim: Claim text
            keywords: Keywords to search for
            snippet_length: Length of snippet to extract

        Returns:
            Relevant snippet from content
        """
        if not content:
            return ""

        content_lower = content.lower()

        # Find position of best keyword match
        best_pos = -1
        best_keyword = None

        for keyword in keywords[:3]:  # Check top 3 keywords
            pos = content_lower.find(keyword.lower())
            if pos != -1:
                best_pos = pos
                best_keyword = keyword
                break

        if best_pos == -1:
            # No keyword found, return beginning
            return content[:snippet_length].strip()

        # Extract snippet around keyword
        start = max(0, best_pos - snippet_length // 2)
        end = min(len(content), best_pos + snippet_length // 2)

        # Try to start at sentence boundary
        if start > 0:
            # Look for period before start
            period_pos = content.rfind('.', max(0, start - 50), start)
            if period_pos != -1:
                start = period_pos + 1

        # Try to end at sentence boundary
        if end < len(content):
            # Look for period after end
            period_pos = content.find('.', end, min(len(content), end + 50))
            if period_pos != -1:
                end = period_pos + 1

        snippet = content[start:end].strip()

        # Add ellipsis if truncated
        if start > 0:
            snippet = '...' + snippet
        if end < len(content):
            snippet = snippet + '...'

        return snippet

    def _get_context(
        self,
        content: str,
        snippet: str,
        context_length: int = 300
    ) -> str:
        """
        Get surrounding context for snippet.

        Args:
            content: Full article content
            snippet: Snippet to find context for
            context_length: Length of context to extract

        Returns:
            Surrounding context
        """
        if not content or not snippet:
            return ""

        # Remove ellipsis from snippet for finding
        snippet_clean = snippet.replace('...', '').strip()

        pos = content.find(snippet_clean)
        if pos == -1:
            # Try case-insensitive search
            pos = content.lower().find(snippet_clean.lower())

        if pos == -1:
            return snippet

        # Get context around snippet
        start = max(0, pos - context_length)
        end = min(len(content), pos + len(snippet_clean) + context_length)

        context = content[start:end].strip()

        # Add ellipsis if truncated
        if start > 0:
            context = '...' + context
        if end < len(content):
            context = context + '...'

        return context

    def _calculate_relevance(
        self,
        claim: str,
        snippet: str
    ) -> float:
        """
        Calculate relevance score (0.0-1.0) between claim and snippet.

        Uses Jaccard similarity coefficient.

        Args:
            claim: Claim text
            snippet: Evidence snippet

        Returns:
            Relevance score from 0.0 (no match) to 1.0 (perfect match)
        """
        # Clean and tokenize
        claim_words = set(claim.lower().replace(',', ' ').replace('.', ' ').split())
        snippet_words = set(snippet.lower().replace(',', ' ').replace('.', ' ').split())

        # Remove very common words for better matching
        stop_words = {'the', 'a', 'an', 'is', 'was', 'are', 'were', 'be', 'to', 'of', 'in', 'for', 'on', 'at'}
        claim_words = claim_words - stop_words
        snippet_words = snippet_words - stop_words

        if not claim_words or not snippet_words:
            return 0.0

        # Jaccard similarity: intersection / union
        intersection = claim_words.intersection(snippet_words)
        union = claim_words.union(snippet_words)

        if not union:
            return 0.0

        return len(intersection) / len(union)
