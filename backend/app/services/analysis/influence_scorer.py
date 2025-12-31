"""Service for calculating U.S. politics influence scores for articles."""
from typing import Optional
from app.models.article import Article
from app.models.source import NewsSource


class InfluenceScorer:
    """Calculate political influence scores for articles."""

    POLITICAL_KEYWORDS = [
        'president', 'congress', 'senate', 'house', 'election',
        'vote', 'campaign', 'policy', 'legislation', 'government',
        'democrat', 'republican', 'political', 'white house',
        'supreme court', 'federal', 'state legislature', 'governor',
        'biden', 'trump', 'bill', 'law', 'capitol', 'washington',
    ]

    HIGH_INFLUENCE_SOURCES = [
        'nytimes.com', 'washingtonpost.com', 'wsj.com',
        'reuters.com', 'apnews.com', 'politico.com', 'thehill.com',
        'cnn.com', 'foxnews.com', 'nbcnews.com', 'abcnews.go.com',
    ]

    def calculate_influence_score(
        self,
        article: Article,
        source: Optional[NewsSource] = None
    ) -> float:
        """
        Calculate influence score (0.0 to 1.0) based on:
        - Source credibility/reach (0.0 - 0.4)
        - Political keyword density in content (0.0 - 0.4)
        - Title relevance (0.0 - 0.2)

        Args:
            article: Article to score
            source: NewsSource (optional, will use article.source if available)

        Returns:
            Float between 0.0 and 1.0 representing political influence
        """
        score = 0.0

        # Use provided source or article's source
        if not source and hasattr(article, 'source'):
            source = article.source

        # Source credibility (0.0 - 0.4)
        if source:
            if any(domain in source.url for domain in self.HIGH_INFLUENCE_SOURCES):
                score += 0.4
            else:
                score += 0.2

        # Political keyword density in content (0.0 - 0.4)
        if article.content:
            content_lower = article.content.lower()
            keyword_count = sum(1 for keyword in self.POLITICAL_KEYWORDS if keyword in content_lower)
            # Normalize by content length (per 1000 chars)
            density = (keyword_count / (len(article.content) / 1000)) if article.content else 0
            score += min(0.4, density * 0.1)

        # Title relevance (0.0 - 0.2)
        if article.title:
            title_lower = article.title.lower()
            title_keywords = sum(1 for keyword in self.POLITICAL_KEYWORDS if keyword in title_lower)
            score += min(0.2, title_keywords * 0.1)

        return min(1.0, score)
