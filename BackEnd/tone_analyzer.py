# tone_analyzer.py
from enum import Enum
from pydantic import BaseModel

class ToneCategory(str, Enum):
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    FORMAL = "formal"
    CASUAL = "casual"
    URGENT = "urgent"
    SALES = "sales"

class StyleTemplate(BaseModel):
    greeting_format: str
    sign_off: str
    paragraph_count: int
    avg_sentence_length: int
    keywords: list[str]

# Style templates dictionary
STYLE_TEMPLATES = {
    ToneCategory.PROFESSIONAL: StyleTemplate(
        greeting_format="Dear {recipient},",
        sign_off="Best regards,",
        paragraph_count=3,
        avg_sentence_length=15,
        keywords=["opportunity", "collaboration", "professional", "looking forward"]
    ),
    ToneCategory.FRIENDLY: StyleTemplate(
        greeting_format="Hi {recipient},",
        sign_off="Cheers,",
        paragraph_count=2,
        avg_sentence_length=12,
        keywords=["thanks", "appreciate", "chat", "catch up"]
    ),
    # Add more templates for other tone categories
}

def get_style_prompt(tone: ToneCategory, context: str) -> str:
    """Generate a style-specific prompt addition based on tone."""
    template = STYLE_TEMPLATES.get(tone, STYLE_TEMPLATES[ToneCategory.PROFESSIONAL])
    
    style_prompt = f"""
    Use a {tone} tone with these characteristics:
    - Start with: "{template.greeting_format}"
    - End with: "{template.sign_off}"
    - Write approximately {template.paragraph_count} paragraphs
    - Keep sentences around {template.avg_sentence_length} words on average
    - Include some of these tone-appropriate phrases if relevant: {', '.join(template.keywords)}
    """
    
    return style_prompt
def analyze_tone(email_content):
    # Basic tone analysis
    word_count = len(email_content.split())
    sentence_count = email_content.count('.') + email_content.count('!') + email_content.count('?')
    
    # Check for tone indicators
    tone_indicators = {
        "professional": ["opportunity", "regards", "sincerely", "collaboration"],
        "friendly": ["hi", "thanks", "appreciate", "chat"],
        "formal": ["formally", "request", "accordance", "hereby"],
        "casual": ["hey", "just", "anyway", "btw"]
    }
    
    detected_tone = "neutral"
    max_count = 0
    
    for tone, keywords in tone_indicators.items():
        count = sum(1 for word in keywords if word.lower() in email_content.lower())
        if count > max_count:
            max_count = count
            detected_tone = tone
    
    return {
        "detected_tone": detected_tone,
        "word_count": word_count,
        "avg_words_per_sentence": word_count / max(1, sentence_count),
        "formality_score": 0.8 if detected_tone in ["professional", "formal"] else 0.4
    }