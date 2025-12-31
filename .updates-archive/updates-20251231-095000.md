# Future Updates

## Bugs


## Improvements
- Implement claim extraction Celery task that processes pending articles and extracts verifiable claims using Ollama LLM
- Implement fact-checking Celery task that verifies extracted claims by finding evidence and using Ollama to analyze
- Add U.S. politics influence ranking system to articles (score 0.0-1.0) that determines evaluation priority
- Create priority queue system where articles with higher political influence are evaluated first
- Add periodic Celery tasks for claim extraction (every 5 minutes) and fact-checking (continuous processing)
- Implement claim extraction service that uses Ollama client with claim extraction prompts
- Implement fact-checking service that uses Ollama client with fact-checking prompts
- Add influence_score field to Article model and create migration
- Update article status workflow: pending -> processing -> processed -> verified

## General Notes
- Prioritize politically influential articles for faster fact-checking of important news
- Ensure claim extraction handles JSON parsing errors gracefully
- Add retry logic for Ollama API failures
