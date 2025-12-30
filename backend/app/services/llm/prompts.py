"""LLM prompt templates."""

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
